"""Default-pack checks; uncertain wording and source gaps never grant acceptance."""

from datetime import date
import re

from .reader import plain, SUBSTITUTION
from .schemas import ContentError


RECORD_ID = re.compile(r"[A-Z][A-Z0-9_]*-\d{1,12}\Z")
RANGE = re.compile(r"\b([A-Z][A-Z0-9_]*-)(\d+)\s*[–-]\s*(?:\1)?(\d+)\b")
MENTION = re.compile(r"\b[A-Z][A-Z0-9_]*-[A-Za-z0-9_]+\b")
META = ("Document ID", "Revision", "Date", "Product / release applicability", "Canonical source / baseline")
WORDING = re.compile(r"\b(?:fast|secure|user-friendly|easy|we will|arrange a meeting|draft for review)\b", re.I)
CLAIM = re.compile(r"\b(?:all tests (?:passed|failed)|test results?:?\s*pass|decision (?:is|was) accepted)\b", re.I)


def references(value, expected, extras=()):
    """Resolve supported literal IDs/ranges only against the declared inventory."""
    allowed = set(expected) | set(extras)
    found = set()
    def expand(match):
        prefix, low, high = match.groups()
        if len(low) > 12 or len(high) > 12:
            raise ContentError("A reference range exceeds the supported ID syntax.", unsupported=True)
        start, end = int(low), int(high)
        subset = {item for item in allowed if re.fullmatch(re.escape(prefix) + r"\d+", item)
                  and start <= int(item[len(prefix):]) <= end}
        numbers = {int(item[len(prefix):]) for item in subset}
        if (end < start or prefix + low not in allowed or prefix + high not in allowed
                or end - start + 1 != len(subset) or len(numbers) != len(subset)):
            raise ContentError("A reference range has missing or ambiguous declared endpoints/records.", rule="CP-REFERENCE-001")
        found.update(subset)
        return " " * len(match.group(0))
    rest = RANGE.sub(expand, value)
    for item in MENTION.findall(rest):
        if item not in allowed:
            raise ContentError("A declared reference does not resolve in its selected baseline.", rule="CP-REFERENCE-001")
        found.add(item)
    result = found & set(expected)
    if not result:
        raise ContentError("This reference does not use supported declared IDs. Correct it or use a later tailored context.",
                           rule="CP-REFERENCE-001", unsupported=True)
    return result


def assess(narratives, context, md, resolved=None):
    findings, gaps, results = [], [], {}
    inventories = {}

    def add(doc, rule, message, *, line=1, section="", field=None, record_id=None, warning=False, unsupported=False, path=None):
        loc = {"path": path or doc.origins.get(section, {}).get("path", doc.path), "line": line, "section": section}
        if field:
            loc["field"] = field
        if record_id and RECORD_ID.fullmatch(record_id):
            loc["record_id"] = record_id
        findings.append({"document": doc.key, "rule_id": rule, "severity": "warning" if warning else "error",
                         "category": "unsupported" if unsupported else "check", "location": loc, "message": message})

    def edge(doc, row, field, expected, extras=(), section=""):
        try:
            mapped = resolved.links.get((row.path, row.line, field)) if resolved else None
            if mapped is None:
                return references(row.values[field], expected, extras)
            try:
                canonical = references(row.values[field], expected, extras)
            except ContentError as exc:
                # A custom prose cell may be declared explicitly; malformed or dangling
                # canonical IDs/ranges must still fail even beside a valid mapping.
                mentions = set(MENTION.findall(row.values[field]))
                if not exc.unsupported or RANGE.search(row.values[field]) or not mentions <= set(extras):
                    raise
                canonical = None
            if canonical is not None and canonical != mapped:
                raise ContentError("Explicit targets conflict with the canonical reference set. Reconcile both declarations.", rule="CP-REFERENCE-001")
            if not mapped <= set(expected):
                raise ContentError("An explicit target is outside this cell's selected baseline.", rule="CP-REFERENCE-001")
            return mapped
        except ContentError as exc:
            add(doc, exc.rule, str(exc), line=row.line, path=row.path, field=field, section=section, unsupported=exc.unsupported)
            return set()

    identities, document_ids = {}, {}
    for doc in narratives:
        profile, meta = doc.profile, doc.metadata
        document_id = meta.get("Document ID", "")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", document_id):
            add(doc, "CP-METADATA-001", "Supply a stable document ID in the document-information table.")
            document_id = None
        elif document_id in document_ids:
            add(doc, "CP-ID-001", "A document identity is duplicated in this namespace.")
        else:
            document_ids[document_id] = doc.key
        for name in META:
            if not meta.get(name) or SUBSTITUTION.search(plain(md, meta[name])):
                add(doc, "CP-METADATA-001", "Complete the required document-information field.", field=name)
        if meta.get("Date"):
            try:
                date.fromisoformat(meta["Date"])
            except ValueError:
                add(doc, "CP-METADATA-001", "Use an actual ISO calendar date; do not invent a date for this check.", field="Date")
        covered = []
        for slot in profile["slots"]:
            section = doc.sections.get(slot["heading"])
            table_spec = next((t for t in profile["tables"] if t["slot"] == slot["id"]), None)
            rows = doc.tables.get(slot["id"])
            present = section is not None
            if section and slot["kind"] in {"prose", "mixed"} and not any(v.strip() for _, v in section.prose):
                present = False
            if table_spec and (rows is None or len(rows) < table_spec["min_rows"]):
                present = False
            if not present:
                if slot["required"]:
                    add(doc, "CP-COVERAGE-001", "Required standard-pack content is missing or empty. Complete the selected section/table.",
                        line=section.line if section else 1, section=slot["heading"])
                elif slot["id"] not in doc.omissions:
                    add(doc, "CP-COVERAGE-002", "Conditional content is absent; review its applicability or locate an omission rationale.",
                        section=slot["heading"], warning=True)
            item = {"slot": slot["id"], "state": "checked" if present else "omitted_with_rationale" if slot["id"] in doc.omissions else "missing" if slot["required"] else "not_assessed"}
            if slot["id"] in doc.selections: item["source"] = doc.selections[slot["id"]]
            if slot["id"] in doc.omissions: item["rationale"] = doc.omissions[slot["id"]]
            covered.append(item)
        reqs, criteria, questions = {}, {}, {}
        for spec in profile["tables"]:
            section = next(s["heading"] for s in profile["slots"] if s["id"] == spec["slot"])
            seen = set()
            for row in doc.tables.get(spec["id"], []):
                for field in spec["required_fields"]:
                    value = plain(md, row.values[field])
                    if not value.strip() or SUBSTITUTION.search(value):
                        add(doc, "CP-CONTENT-001", "Complete the required field with source content, not a blank or substitution prompt.",
                            line=row.line, path=row.path, section=section, field=field)
                # Edition has two explicitly supported header names.
                if spec["record_type"] == "standard" and not all(row.values.values()):
                    add(doc, "CP-CONTENT-001", "Complete reference, edition and application fields.", line=row.line, path=row.path, section=section)
                for field, value in row.values.items():
                    if SUBSTITUTION.search(plain(md, value)):
                        add(doc, "CP-CONTENT-001", "Replace the unresolved substitution field or move a literal example into code.",
                            line=row.line, path=row.path, section=section, field=field)
                rid = row.values.get(spec["identity"], "")
                if spec["identity"]:
                    if not rid or rid in seen:
                        add(doc, "CP-ID-001", "A table identity is missing or duplicated.", line=row.line, path=row.path, section=section)
                    seen.add(rid)
                kind = spec["record_type"]
                if kind in {"requirement", "criterion", "gap"}:
                    if not RECORD_ID.fullmatch(rid):
                        add(doc, "CP-ID-001", "Record IDs use a literal uppercase prefix and numeric suffix, without changing their identity.",
                            line=row.line, path=row.path, section=section, unsupported=True)
                        continue
                    identity = (kind, rid)
                    physical = (row.path, row.line)
                    if identity in identities and identities[identity] != physical:
                        add(doc, "CP-ID-001", "A qualified record identity is duplicated in this namespace.", line=row.line, path=row.path,
                            section=section, record_id=rid)
                    identities[identity] = physical
                    if kind == "requirement":
                        reqs[rid] = (row, spec["id"])
                        statement = row.values.get("Requirement", row.values.get("Requirement / constraint", ""))
                        if WORDING.search(plain(md, statement)):
                            add(doc, "CP-WORDING-001", "This statement may be vague or describe authoring activity. Review its observable product behavior or measure.",
                                line=row.line, path=row.path, section=section, record_id=rid, warning=True)
                    elif kind == "criterion":
                        criteria[rid] = row
                    else:
                        questions[rid] = row
                        gaps.append({"document": doc.key, "record_id": rid, "kind": "declared_question",
                                     "location": {"path": row.path, "line": row.line, "section": section},
                                     "affected_records": sorted(set(MENTION.findall(row.values["Effect on acceptance"]))),
                                     "resolution_detail": "not_assessed"})
                if kind == "verification" and row.values.get("Remaining gap", "").strip():
                    gaps.append({"document": doc.key, "record_id": None, "kind": "declared_design_gap",
                                 "location": {"path": row.path, "line": row.line, "section": section},
                                 "affected_records": sorted(set(MENTION.findall(row.values["Requirement / risk"]))),
                                 "resolution_detail": "not_assessed"})
                if kind == "decision" and re.search(r"(?:^|;|\bStatus\s*:)\s*Accepted\s*[.]?\s*$", row.values["Decision"], re.I):
                    if not resolved or not resolved.claim_covers(row.path, row.line):
                        add(doc, "CP-CLAIM-001", "Locate the actual accepted decision and its revision, actor, time and evidence fields.",
                            line=row.line, path=row.path, section=section)
        for line, value in doc.prose:
            value = plain(md, value)
            if SUBSTITUTION.search(value):
                add(doc, "CP-CONTENT-001", "Replace the unresolved substitution prompt with actual source content.", line=line)
            if CLAIM.search(value):
                add(doc, "CP-CLAIM-REVIEW", "This prose may claim an observed result or accepted decision. Unmapped prose claims are not validated; review their source and evidence.",
                    line=line, warning=True)
        known_headings = {s["heading"] for s in profile["slots"]}
        unassessed = sorted(h for h in doc.sections if h not in known_headings)
        inventories[doc.key] = (reqs, criteria, questions)
        results[doc.key] = {"key": doc.key, "path": doc.path, "document_id": document_id,
                            "content_version": meta.get("Revision"),
                            "profile": {"id": profile["profile_id"], "version": profile["profile_version"]},
                            "requirements": sorted(reqs), "criteria": sorted(criteria),
                            "coverage": covered, "unassessed_section_count": len(unassessed)}

    specifications = {d["key"]: d for d in context["documents"]}
    by_key = {d.key: d for d in narratives}
    for doc in narratives:
        reqs, criteria, questions = inventories[doc.key]
        if doc.profile["profile_id"] == "requirements":
            if specifications[doc.key].get("requirements"):
                add(doc, "CP-REFERENCE-001", "Requirements documents define their records directly, without inherited baselines.", unsupported=True)
            forward, backward = set(), set()
            for rid, (row, table) in reqs.items():
                field = "Acceptance criteria" if table == "functional" else "Verification reference"
                for cid in edge(doc, row, field, criteria, questions, table):
                    forward.add((rid, cid))
            for cid, row in criteria.items():
                for rid in edge(doc, row, "Requirement ID", reqs, questions, "Acceptance and verification"):
                    backward.add((rid, cid))
            if forward != backward:
                add(doc, "CP-REFERENCE-001", "Requirement and criterion links do not agree in both directions. Reconcile the declared coverage.")
        else:
            baselines = specifications[doc.key].get("requirements", [])
            if (not baselines or any(key not in by_key or by_key[key].profile["profile_id"] != "requirements" for key in baselines)):
                add(doc, "CP-REFERENCE-001", "Declare the supported requirements documents used by this design.")
                continue
            target_reqs, target_criteria, target_questions = set(), set(), set()
            physical_records = {}
            for key in baselines:
                r, c, q = inventories[key]
                for kind, records in (("requirement", r), ("criterion", c)):
                    for rid, value in records.items():
                        row = value[0] if kind == "requirement" else value
                        identity = (kind, rid)
                        physical = (row.path, row.line)
                        if identity in physical_records and physical_records[identity] != physical:
                            add(doc, "CP-REFERENCE-001", "The selected requirement baselines contain ambiguous identities.")
                        physical_records[identity] = physical
                target_reqs.update(r); target_criteria.update(c); target_questions.update(q)
            coverage = set()
            for row in doc.tables.get("quality", []):
                coverage |= edge(doc, row, "Requirement / concern", target_reqs, target_questions, "Security and quality")
                edge(doc, row, "Verification reference / unresolved measure", target_criteria, target_questions, "Security and quality")
            verification = set()
            for row in doc.tables.get("verification", []):
                verification |= edge(doc, row, "Requirement / risk", target_reqs, target_questions, "Verification and unresolved matters")
                edge(doc, row, "Planned check / evidence", target_criteria, target_questions, "Verification and unresolved matters")
            if coverage != target_reqs or verification != target_reqs:
                add(doc, "CP-REFERENCE-001", "The selected requirement baseline lacks complete design response/verification coverage. Reconcile affected records.")
    for key, result in results.items():
        errors = [f for f in findings if f["document"] == key and f["severity"] == "error"]
        result["completeness"] = "unsupported" if any(f["category"] == "unsupported" for f in errors) else "incomplete" if errors else "complete"
    return list(results.values()), findings, gaps
