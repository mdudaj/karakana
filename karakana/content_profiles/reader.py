"""Bounded source maps and lossless raw-table reading for selected narrative views."""

from dataclasses import dataclass, field
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
    children = md.parseInline(value)[0].children or []
    return ANCHOR.sub("", "".join(t.content for t in children if t.type in {"text", "softbreak", "hardbreak"}))


@dataclass
class Table:
    headers: list
    rows: list
    line: int
    end: int


@dataclass
class Source:
    key: str
    path: str
    sections: list
    tables: list
    anchors: dict
    prose: list
    lines: int

    def bounds(self, locator):
        if "anchor" in locator:
            bounds = self.anchors.get(locator["anchor"])
            if bounds is None:
                raise ContentError("The explicit anchor is absent. Locate current source content.", rule="CP-LOCATOR-001",
                                   location={"path": self.path, "line": 1})
            return bounds
        matches = [s for s in self.sections if s.path == tuple(locator["heading"])]
        if len(matches) != 1:
            raise ContentError("The heading path is absent or ambiguous. Use a unique full path or explicit anchor.",
                               rule="CP-LOCATOR-001", location={"path": self.path, "line": 1})
        return matches[0].line, matches[0].end


def read_source(raw, key, path, md):
    try:
        body = raw.decode("utf-8").replace("\r\n", "\n")
    except UnicodeError as exc:
        raise ContentError("Use a UTF-8 narrative source.") from exc
    location = {"path": path, "line": 1}
    if body.startswith("\ufeff") or "\r" in body:
        raise ContentError("Use supported LF or CRLF input without a BOM or standalone CR.", unsupported=True)
    if body.startswith("---\n"):
        raise ContentError("Frontmatter/P02 sources are outside narrative-0.1. Use the separate structural validator.", unsupported=True)
    if CONTROL.search(body):
        raise ContentError("Remove unsupported control characters from the source.")
    lines, tokens = body.splitlines(), md.parse(body)
    ignored, table_spans, headings, prose, title = set(), [], [], [], []
    heading_lines, stack = set(), []
    for i, token in enumerate(tokens):
        if token.type in {"fence", "code_block", "blockquote_open"} and token.map:
            ignored.update(range(*token.map))
        if token.type == "heading_open" and token.level == 0 and token.map:
            heading_lines.update(range(*token.map))
            value = tokens[i + 1].content.strip()
            level = int(token.tag[1:])
            if level == 1:
                title.append(value)
            else:
                value = re.sub(r"^\d{2}\s+", "", value).strip()
                while stack and stack[-1][0] >= level: stack.pop()
                stack.append((level, value))
                headings.append((tuple(v for _, v in stack), level, token.map[0]))
        if token.type == "table_open" and token.level == 0 and token.map:
            table_spans.append(tuple(token.map))
    if len(title) != 1 or not plain(md, title[0]).strip() or SUBSTITUTION.search(plain(md, title[0])):
        raise ContentError("Supply one completed document title.", rule="CP-METADATA-001", location=location)
    sections = [Section("", 1, headings[0][2] if headings else len(lines))]
    for index, (path_parts, level, start) in enumerate(headings):
        end = next((h[2] for h in headings[index+1:] if h[1] <= level), len(lines))
        sections.append(Section(path_parts[-1], start+1, end, path=path_parts))
    for token in tokens:
        if (token.type != "inline" or not token.map or token.map[0] in ignored
                or token.map[0] in heading_lines or any(a <= token.map[0] < b for a,b in table_spans)):
            continue
        value = plain(md, token.content)
        if value.strip(): prose.append((token.map[0]+1, token.content))
    for s in sections:
        s.prose = [(line, value) for line,value in prose if s.line <= line <= s.end]
    tables, consumed = [], set()
    for begin,end in table_spans:
        consumed.update(range(begin,end))
        raw_rows=[]
        for i in range(begin,end):
            line=lines[i]
            if not line.startswith("| ") or not line.endswith(" |"):
                raise ContentError("Use complete contiguous | cell | table boundaries.", rule="CP-TABLE-001", location={**location,"line":i+1})
            raw_rows.append([v.strip().replace("&#124;","|").replace("<br>","\n") for v in line[1:-1].split("|")])
        headers=raw_rows[0]
        if len(raw_rows)<2 or len(headers)!=len(set(headers)) or not all(headers) or len(raw_rows[1])!=len(headers) or any(v!='---' for v in raw_rows[1]):
            raise ContentError("Use unique headers and a complete supported separator row.", rule="CP-TABLE-001", location={**location,"line":begin+1})
        rows=[]
        for offset,cells in enumerate(raw_rows[2:],2):
            if len(cells)!=len(headers):
                raise ContentError("Table row width differs from its header. No cells were discarded.", rule="CP-TABLE-001", location={**location,"line":begin+offset+1})
            if any(cells): rows.append(Row({h:ANCHOR.sub('',v).strip() for h,v in zip(headers,cells)},begin+offset+1,path))
        tables.append(Table(headers,rows,begin+1,end))
    for i,line in enumerate(lines):
        if i not in ignored and i not in consumed and (line.strip().startswith('|') or line.strip().endswith('|')):
            raise ContentError("A table row was not consumed completely. Correct its raw boundaries and separator.", rule="CP-TABLE-001", location={**location,"line":i+1})
    anchors={}
    anchor_lines=[]
    for i,line in enumerate(lines):
        if i in ignored:continue
        children=md.parseInline(line)[0].children or []
        for child in children:
            if child.type!='text':continue
            for match in ANCHOR.finditer(child.content):
                if match[1] in anchors:
                    raise ContentError("Duplicate explicit anchor. Retain unique source locations.", rule="CP-HEADING-001", location={**location,"line":i+1})
                anchors[match[1]]=(i+1,i+1)
                anchor_lines.append((match[1],i+1,bool(ANCHOR.fullmatch(line.strip()))))
    for name,line,standalone in anchor_lines:
        if not standalone:continue
        next_nonempty=next((j for j in range(line,len(lines)) if lines[j].strip()),len(lines))
        following=next((s for s in sections if s.line==next_nonempty+1),None)
        if following:anchors[name]=(following.line,following.end)
        else:
            end=min([s.line-1 for s in sections if s.line>line]+[other-1 for _,other,_ in anchor_lines if other>line]+[len(lines)])
            anchors[name]=(line+1,end)
    return Source(key,path,sections,tables,anchors,prose,len(lines))


def read_narrative(raw, key, path, profile, md, mapped_slots=()):
    source=read_source(raw,key,path,md)
    for table in source.tables:
        if not any(table.headers in spec['headers'] for spec in profile['tables']):
            raise ContentError("An unregistered table cannot be silently ignored. Select supported registered columns.",
                               rule="CP-TABLE-001", unsupported=True, location={"path":path,"line":table.line})
    sections,tables={},{}
    native_tables=set()
    for slot in profile['slots']:
        wanted=() if not slot['heading'] else (slot['heading'],)
        matches=[s for s in source.sections if s.path==wanted]
        if len(matches)>1:
            if slot['id'] in mapped_slots: continue
            raise ContentError("A default heading is ambiguous. Use a unique heading path or explicit source anchor.",rule="CP-HEADING-001",location={"path":path,"line":matches[1].line})
        if not matches:continue
        section=matches[0];sections[slot['heading']]=section
        spec=next((t for t in profile['tables'] if t['slot']==slot['id']),None)
        candidates=[t for t in source.tables if section.line<=t.line<=section.end]
        if candidates and (not spec or len(candidates)!=1 or candidates[0].headers not in spec['headers']):
            raise ContentError("Select one supported registered table per profile slot.",rule="CP-TABLE-001",location={"path":path,"line":section.line})
        if candidates:
            tables[spec['id']]=candidates[0].rows
            native_tables.add(candidates[0].line)
    for section in source.sections:
        if section.path and section.path != (section.heading,):
            sections.setdefault(" / ".join(section.path), section)
        elif section.heading not in sections:
            sections[section.heading] = section
    meta={}
    for row in tables.get('metadata',[]):
        name=row.values['Document information']
        if name in meta:raise ContentError("Duplicate document-information field.",rule="CP-METADATA-001",location={"path":path,"line":row.line})
        meta[name]=row.values['Value']
    return Narrative(key,path,profile,sections,tables,meta,source.prose,source=source,native_tables=native_tables)
