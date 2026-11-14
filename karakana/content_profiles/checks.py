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


def assess(narratives, context, md):
    findings, gaps, results = [], [], {}
    inventories = {}

    def add(doc, rule, message, *, line=1, section="", field=None, record_id=None, warning=False, unsupported=False):
        loc = {"path": doc.path, "line": line, "section": section}
        if field:
            loc["field"] = field
        if record_id and RECORD_ID.fullmatch(record_id):
            loc["record_id"] = record_id
        findings.append({"document": doc.key, "rule_id": rule, "severity": "warning" if warning else "error",
                         "category": "unsupported" if unsupported else "check", "location": loc, "message": message})

    def edge(doc, row, field, expected, extras=(), section=""):
        try:
            return references(row.values[field], expected, extras)
        except ContentError as exc:
            add(doc, exc.rule, str(exc), line=row.line, field=field, section=section, unsupported=exc.unsupported)
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
                else:
                    add(doc, "CP-COVERAGE-002", "Conditional content is absent; its applicability remains for review. Tailored omissions are not checked in M1.",
                        section=slot["heading"], warning=True)
            covered.append({"slot": slot["id"], "state": "checked" if present else "missing" if slot["required"] else "not_assessed"})
        reqs, criteria, questions = {}, {}, {}
        for spec in profile["tables"]:
            section = next(s["heading"] for s in profile["slots"] if s["id"] == spec["slot"])
            seen = set()
            for row in doc.tables.get(spec["id"], []):
                for field in spec["required_fields"]:
                    value = plain(md, row.values[field])
                    if not value.strip() or SUBSTITUTION.search(value):
                        add(doc, "CP-CONTENT-001", "Complete the required field with source content, not a blank or substitution prompt.",
                            line=row.line, section=section, field=field)
                # Edition has two explicitly supported header names.
                if spec["record_type"] == "standard" and not all(row.values.values()):
                    add(doc, "CP-CONTENT-001", "Complete reference, edition and application fields.", line=row.line, section=section)
                for field, value in row.values.items():
                    if SUBSTITUTION.search(plain(md, value)):
                        add(doc, "CP-CONTENT-001", "Replace the unresolved substitution field or move a literal example into code.",
                            line=row.line, section=section, field=field)
                rid = row.values.get(spec["identity"], "")
                if spec["identity"]:
                    if not rid or rid in seen:
                        add(doc, "CP-ID-001", "A table identity is missing or duplicated.", line=row.line, section=section)
                    seen.add(rid)
                kind = spec["record_type"]
                if kind in {"requirement", "criterion", "gap"}:
                    if not RECORD_ID.fullmatch(rid):
                        add(doc, "CP-ID-001", "M1 record IDs use a literal uppercase prefix and numeric suffix, without changing their identity.",
                            line=row.line, section=section, unsupported=True)
                        continue
                    identity = (kind, rid)
                    if identity in identities:
                        add(doc, "CP-ID-001", "A qualified record identity is duplicated in this namespace.", line=row.line,
                            section=section, record_id=rid)
                    identities[identity] = doc.key
                    if kind == "requirement":
                        reqs[rid] = (row, spec["id"])
                        statement = row.values.get("Requirement", row.values.get("Requirement / constraint", ""))
                        if WORDING.search(plain(md, statement)):
                            add(doc, "CP-WORDING-001", "This statement may be vague or describe authoring activity. Review its observable product behavior or measure.",
                                line=row.line, section=section, record_id=rid, warning=True)
                    elif kind == "criterion":
                        criteria[rid] = row
                    else:
                        questions[rid] = row
                        gaps.append({"document": doc.key, "record_id": rid, "kind": "declared_question",
                                     "location": {"path": doc.path, "line": row.line, "section": section},
                                     "affected_records": sorted(set(MENTION.findall(row.values["Effect on acceptance"]))),
                                     "resolution_detail": "not_assessed"})
                if kind == "verification" and row.values.get("Remaining gap", "").strip():
                    gaps.append({"document": doc.key, "record_id": None, "kind": "declared_design_gap",
                                 "location": {"path": doc.path, "line": row.line, "section": section},
                                 "affected_records": sorted(set(MENTION.findall(row.values["Requirement / risk"]))),
                                 "resolution_detail": "not_assessed"})
                if kind == "decision" and re.search(r"(?:^|;|\bStatus\s*:)\s*Accepted\s*[.]?\s*$", row.values["Decision"], re.I):
                    add(doc, "CP-CLAIM-001", "Accepted-decision evidence checking is not supported in M1. Use a later evidence-mapping check.",
                        line=row.line, section=section, unsupported=True)
        for line, value in doc.prose:
            if SUBSTITUTION.search(value):
                add(doc, "CP-CONTENT-001", "Replace the unresolved substitution prompt with actual source content.", line=line)
            if CLAIM.search(value):
                add(doc, "CP-CLAIM-REVIEW", "This prose may claim an observed result or accepted decision. M1 does not validate that evidence; review the source.",
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
                add(doc, "CP-REFERENCE-001", "M1 requirements documents define their records directly, without inherited baselines.", unsupported=True)
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
            for key in baselines:
                r, c, q = inventories[key]
                if target_reqs & r.keys() or target_criteria & c.keys():
                    add(doc, "CP-REFERENCE-001", "The selected requirement baselines contain ambiguous identities.")
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
