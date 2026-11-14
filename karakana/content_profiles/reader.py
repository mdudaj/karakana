"""Read the supported narrative packs without trusting normalized table widths."""

from importlib.metadata import version, PackageNotFoundError
import re

from . import PARSER_VERSION
from .schemas import ContentError, Narrative, Row, Section, CONTROL


ANCHOR = re.compile(r'<a id="([a-z0-9][a-z0-9-]*)"></a>')
SUBSTITUTION = re.compile(r"\{\{[a-z_][a-z0-9_]*\}\}")


def parser():
    try:
        from markdown_it import MarkdownIt
        actual = version("markdown-it-py")
    except (ImportError, PackageNotFoundError) as exc:
        raise ContentError("Install Karakana with the content extra to check narrative packs.",
                           rule="CP-DEPENDENCY-001", unsupported=True) from exc
    if actual != PARSER_VERSION:
        raise ContentError("Install the content extra's pinned parser version before checking these profiles.",
                           rule="CP-DEPENDENCY-001", unsupported=True)
    return MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")


def plain(md, value):
    """Ignore literal code examples when checking placeholder-bearing prose."""
    children = md.parseInline(value)[0].children or []
    return "".join(t.content for t in children if t.type in {"text", "softbreak", "hardbreak"})


def read_narrative(raw, key, path, profile, md):
    try:
        body = raw.decode("utf-8").replace("\r\n", "\n")
    except UnicodeError as exc:
        raise ContentError("Use a UTF-8 narrative source.") from exc
    if body.startswith("\ufeff") or "\r" in body:
        raise ContentError("Use supported LF or CRLF input without a BOM or standalone CR.", unsupported=True)
    if body.startswith("---\n"):
        raise ContentError("Frontmatter/P02 sources are outside narrative-0.1. Use the separate structural validator.", unsupported=True)
    if CONTROL.search(body):
        raise ContentError("Remove unsupported control characters from the source.")
    lines, tokens = body.splitlines(), md.parse(body)
    ignored, table_spans, headings, prose = set(), [], [], []
    heading_lines = set()
    title = []
    for i, token in enumerate(tokens):
        if token.type in {"fence", "code_block", "blockquote_open"} and token.map:
            ignored.update(range(*token.map))
        if token.type == "heading_open" and token.level == 0 and token.map:
            heading_lines.update(range(*token.map))
            value = tokens[i + 1].content.strip()
            if token.tag == "h1":
                title.append(value)
            elif token.tag == "h2":
                headings.append((re.sub(r"^\d{2}\s+", "", value).strip(), token.map[0]))
        if token.type == "table_open" and token.level == 0 and token.map:
            table_spans.append(tuple(token.map))
    location = {"path": path, "line": 1}
    if len(title) != 1 or not plain(md, title[0]).strip() or SUBSTITUTION.search(plain(md, title[0])):
        raise ContentError("Supply one completed document title.", rule="CP-METADATA-001", location=location)
    sections = {"": Section("", 1, headings[0][1] if headings else len(lines))}
    for index, (heading, start) in enumerate(headings):
        if heading in sections:
            raise ContentError("A heading is duplicated or ambiguous. Use the supported unique pack headings.",
                               rule="CP-HEADING-001", location={"path": path, "line": start + 1})
        sections[heading] = Section(heading, start + 1,
                                    headings[index + 1][1] if index + 1 < len(headings) else len(lines))
    anchors = set()
    for i, line in enumerate(lines):
        if i in ignored:
            continue
        match = ANCHOR.fullmatch(line.strip())
        if match:
            if match[1] in anchors:
                raise ContentError("Duplicate explicit anchor. Retain unique source locations.", rule="CP-HEADING-001",
                                   location={"path": path, "line": i + 1})
            anchors.add(match[1])
    for token in tokens:
        if (token.type != "inline" or not token.map or token.map[0] in ignored
                or token.map[0] in heading_lines
                or any(a <= token.map[0] < b for a, b in table_spans)):
            continue
        value = plain(md, token.content)
        if value.strip() and not ANCHOR.fullmatch(value.strip()):
            prose.append((token.map[0] + 1, value))
    for section in sections.values():
        section.prose = [(line, value) for line, value in prose if section.line <= line <= section.end]
    tables = {}
    used_spans = set()
    registered = {t["slot"]: t for t in profile["tables"]}
    for slot in profile["slots"]:
        section = sections.get(slot["heading"])
        if section is None:
            continue
        candidates = [i for i in range(section.line - 1, section.end)
                      if i not in ignored and (lines[i].strip(" \t").startswith("|") or lines[i].strip(" \t").endswith("|"))]
        spans = [span for span in table_spans if section.line - 1 <= span[0] < section.end]
        spec = registered.get(slot["id"])
        if candidates or spans:
            loc = {"path": path, "section": slot["heading"], "line": (candidates[0] + 1) if candidates else section.line}
            if spec is None or len(spans) != 1:
                raise ContentError("This table shape is outside the standard-pack profile. Use supported content or wait for tailored checking.",
                                   rule="CP-TABLE-001", unsupported=True, location=loc)
            begin, end = spans[0]
            # A token reader may pad, truncate or stop before malformed neighbors.
            # Every row in its span AND every raw boundary candidate must agree.
            if candidates != list(range(begin, end)) or end - begin < 2:
                raise ContentError("A table row was not consumed completely. Use contiguous supported boundary-pipe rows.",
                                   rule="CP-TABLE-001", location=loc)
            raw_rows = []
            for i in candidates:
                line = lines[i]
                if not line.startswith("| ") or not line.endswith(" |"):
                    raise ContentError("A table row has unsupported boundaries. Use the complete | cell | convention.",
                                       rule="CP-TABLE-001", location={**loc, "line": i + 1})
                raw_rows.append([v.strip().replace("&#124;", "|").replace("<br>", "\n") for v in line[1:-1].split("|")])
            headers = raw_rows[0]
            if (headers not in spec["headers"] or len(raw_rows[1]) != len(headers)
                    or any(cell != "---" for cell in raw_rows[1])):
                raise ContentError("Table headers or separator differ from the supported profile.", rule="CP-TABLE-001", location=loc)
            rows = []
            for offset, cells in enumerate(raw_rows[2:], 2):
                if len(cells) != len(headers):
                    raise ContentError("Table row width differs from its header. No cells were discarded.",
                                       rule="CP-TABLE-001", location={**loc, "line": begin + offset + 1})
                if any(cells):
                    rows.append(Row(dict(zip(headers, cells)), begin + offset + 1))
            tables[spec["id"]] = rows
            used_spans.add((begin, end))
    if set(table_spans) - used_spans:
        raise ContentError("An unregistered table is outside M1 coverage; it cannot be silently ignored.",
                           rule="CP-TABLE-001", unsupported=True, location=location)
    meta = {}
    for row in tables.get("metadata", []):
        field = row.values["Document information"]
        if field in meta:
            raise ContentError("Duplicate document-information field.", rule="CP-METADATA-001", location={"path": path, "line": row.line})
        meta[field] = row.values["Value"]
    return Narrative(key, path, profile, sections, tables, meta, prose)
