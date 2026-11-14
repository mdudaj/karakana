"""Lazy, explicit M2 delegation and independent task-input provenance."""

from datetime import datetime, timezone
from uuid import uuid4

from karakana.content_profiles.schemas import ContentError, ContentReport, shape
from .inputs import CapturedInputs, MAX_CONFIG_BYTES, fingerprint, json_bytes
from .schemas import TaskError, decode, validate_request, literal
from .selection import resolve_selection
from .prepare import _context
from .report import new_result, add_failure, validate_assessment_result
from .bundles import save_assessment


def timestamp(value):
    try:
        date = datetime.fromisoformat(value)
        if date.tzinfo is None or date.utcoffset() is None:
            raise ValueError()
    except (TypeError, ValueError) as exc:
        raise TaskError("Select a result with a timezone-aware generation time.", code="DT-RESULT-001", outcome="unsupported") from exc


def _location(value):
    if not isinstance(value, dict) or not {"path", "line"} <= value.keys():
        raise ValueError()
    literal(value["path"])
    if type(value["line"]) is not int or value["line"] < 1:
        raise ValueError()


def validate_report(data, *, verification=False):
    """Validate the supported producer contract, never a process code or .ok flag.

    M2 owns source/schema semantics. This boundary checks required JSON shapes,
    producer identity and authority/completeness invariants before consuming it.
    Saved assessment correctness is subsequently established by M2 recomputation.
    """
    try:
        fields = ("report_version", "namespace", "documents", "findings", "open_acceptance_items", "coverage",
                  "completeness", "review_required", "readiness", "acceptance", "generated_utc", "manifest", "assessment_digest")
        shape(data, fields, ("verification",) if verification else ())
        if data["report_version"] != "0.2":
            raise ValueError()
        timestamp(data["generated_utc"])
        # Round-trip rejects non-JSON objects, NaN and invalid UTF-8.
        decode(json_bytes(data))
        if data["namespace"] is not None:
            literal(data["namespace"])
        for key in ("documents", "findings", "open_acceptance_items"):
            if not isinstance(data[key], list):
                raise ValueError()
        shape(data["coverage"], ("scope", "supported", "advanced_context", "saved_report_verification", "claims", "unassessed"))
        coverage = data["coverage"]
        literal(coverage["scope"])
        if (coverage["advanced_context"] != "supported" or coverage["saved_report_verification"] != "supported"
                or not isinstance(coverage["claims"], list)):
            raise ValueError()
        for key in ("supported", "unassessed"):
            if not isinstance(coverage[key], list) or any(not isinstance(s, str) for s in coverage[key]):
                raise ValueError()
        for claim in coverage["claims"]:
            shape(claim, ("source", "kind", "fields", "evidence_status"))
            _location(claim["source"])
            if (claim["kind"] not in {"decision", "test_result"}
                    or claim["evidence_status"] not in {"external_not_checked", "local_hashed_not_authenticated"}):
                raise ValueError()
            fields = ("revision", "actor", "result", "time", "evidence") + (("environment",) if claim["kind"] == "test_result" else ())
            shape(claim["fields"], fields)
            for location in claim["fields"].values():
                _location(location)
        if not {"acceptance", "product_readiness", "evidence_authenticity", "semantic_correctness"} <= set(coverage["unassessed"]):
            raise ValueError()
        shape(data["manifest"], ("sources", "profiles", "checker", "parser_version"))
        manifest = data["manifest"]
        if not isinstance(manifest["sources"], list) or not isinstance(manifest["profiles"], list):
            raise ValueError()
        for source in manifest["sources"]:
            shape(source, ("path", "requested", "sha256", "roles"))
            for key in ("path", "requested", "sha256"):
                literal(source[key])
            if not isinstance(source["roles"], list) or any(not isinstance(s, str) for s in source["roles"]):
                raise ValueError()
        for profile in manifest["profiles"]:
            shape(profile, ("id", "version", "sha256"))
            for v in profile.values():
                literal(v)
        shape(manifest["checker"], ("version", "components", "sha256"))
        if manifest["checker"]["version"] != "0.2.0" or not isinstance(manifest["checker"]["components"], list):
            raise ValueError()
        literal(manifest["checker"]["sha256"])
        for component in manifest["checker"]["components"]:
            shape(component, ("component", "sha256"))
            literal(component["component"]); literal(component["sha256"])
        literal(manifest["parser_version"]); literal(data["assessment_digest"])
        errors = []
        for finding in data["findings"]:
            shape(finding, ("document", "rule_id", "severity", "category", "location", "message"))
            if finding["document"] is not None:
                literal(finding["document"])
            for key in ("rule_id", "category", "message"):
                literal(finding[key], limit=32768, multiline=True)
            if finding["severity"] not in {"error", "warning"} or not isinstance(finding["location"], dict):
                raise ValueError()
            _location(finding["location"])
            if finding["category"] not in {"check", "unsupported", "review"}:
                raise ValueError()
            if finding["severity"] == "error":
                errors.append(finding)
        expected = "unsupported" if any(f["category"] == "unsupported" for f in errors) else "incomplete" if errors else "complete"
        if (data["completeness"] != expected or data["review_required"] is not True
                or data["acceptance"] != "not_assessed"
                or data["readiness"] != ("unresolved" if data["open_acceptance_items"] else "not_assessed")):
            raise ValueError()
        keys = set()
        for doc in data["documents"]:
            shape(doc, ("key", "path", "document_id", "content_version", "profile", "requirements", "criteria",
                        "coverage", "unassessed_section_count", "completeness", "readiness", "acceptance", "review_required"))
            literal(doc["key"]); literal(doc["path"])
            if doc["key"] in keys:
                raise ValueError()
            keys.add(doc["key"])
            shape(doc["profile"], ("id", "version"))
            for value in doc["profile"].values():
                literal(value)
            for key in ("document_id", "content_version"):
                if doc[key] is not None:
                    literal(doc[key])
            if any(not isinstance(doc[k], list) for k in ("requirements", "criteria", "coverage")):
                raise ValueError()
            for key in ("requirements", "criteria"):
                for value in doc[key]:
                    literal(value)
            for entry in doc["coverage"]:
                shape(entry, ("slot", "state"))
                literal(entry["slot"])
                if entry["state"] not in {"checked", "omitted_with_rationale", "missing", "not_assessed"}:
                    raise ValueError()
            if (doc["completeness"] not in {"complete", "incomplete", "unsupported"}
                    or doc["readiness"] not in {"unresolved", "not_assessed"}
                    or doc["review_required"] is not True or doc["acceptance"] != "not_assessed"
                    or (doc["unassessed_section_count"] is not None and type(doc["unassessed_section_count"]) is not int)):
                raise ValueError()
            own_errors = [f for f in errors if f["document"] == doc["key"]]
            own_status = "unsupported" if any(f["category"] == "unsupported" for f in own_errors) else "incomplete" if own_errors else "complete"
            if doc["completeness"] != own_status:
                raise ValueError()
        for gap in data["open_acceptance_items"]:
            shape(gap, ("document", "record_id", "kind", "location", "affected_records", "resolution_detail"),
                  ("affected_scopes", "effect", "resolver", "next_action"))
            literal(gap["document"]); _location(gap["location"])
            if gap["record_id"] is not None:
                literal(gap["record_id"])
            if (gap["kind"] not in {"declared_question", "declared_design_gap", "mapped_open_item"}
                    or gap["resolution_detail"] not in {"declared", "not_assessed"}
                    or not isinstance(gap["affected_records"], list)):
                raise ValueError()
            for value in gap["affected_records"]:
                literal(value)
            if gap["resolution_detail"] == "declared":
                for field in ("effect", "resolver", "next_action"):
                    _location(gap[field])
                if not isinstance(gap["affected_scopes"], list) or not gap["affected_scopes"]:
                    raise ValueError()
                for scope in gap["affected_scopes"]:
                    _location(scope); literal(scope["document"])
        for doc in data["documents"]:
            affected = any(any(s["document"] == doc["key"] for s in gap.get("affected_scopes", []))
                           if gap.get("affected_scopes") else gap["document"] == doc["key"]
                           for gap in data["open_acceptance_items"])
            if doc["readiness"] != ("unresolved" if affected else "not_assessed"):
                raise ValueError()
        if verification and data.get("verification") not in {"current", "stale_or_mismatched"}:
            raise ValueError()
    except (ContentError, TaskError, ValueError, TypeError, KeyError, UnicodeError, OverflowError) as exc:
        error = TaskError("Content producer data is unsupported or inconsistent. Supply the supported M2 report0.2 contract.",
                          code="DT-PRODUCER-001", outcome="unsupported")
        if isinstance(data, dict):
            allowed = {"blocked", "not_ready", "failed", "unsupported", "ready", "accepted", "complete", "incomplete"}
            error.producer_state = {k: data[k] for k in ("outcome", "status", "state", "completeness", "readiness", "acceptance")
                                    if isinstance(data.get(k), str) and data[k] in allowed}
        raise error from exc
    return data


def producer_data(report, *, verification=False):
    if not isinstance(report, ContentReport):
        # Retain only known typed state labels, never arbitrary foreign payloads.
        validate_report(report, verification=verification)
        raise TaskError("Select the supported M2 report producer.", code="DT-PRODUCER-001", outcome="unsupported")
    return validate_report(report.to_dict(), verification=verification)


def begin(operation):
    now = datetime.now(timezone.utc)
    result = new_result(now.strftime("%Y%m%d-%H%M%S-") + uuid4().hex[:12], now.isoformat())
    result["operation"] = operation
    return result


def capture(root, request_path, result):
    inputs = CapturedInputs(root)
    result["manifest"].update(root=str(inputs.root), wrapper=fingerprint())
    request = validate_request(decode(inputs.read(str(request_path), "task_request", limit=MAX_CONFIG_BYTES)))
    inputs.project = request["project"]
    result["task"] = {"project": request["project"], "skill": request["skill"], **request["task"]}
    result["selection"].update(resolve_selection(request, inputs))
    if request["context"] is None:
        raise TaskError("Content was not checked. Select a check context for this document.", pointer="/context")
    result["selection"]["context"] = _context(inputs, request)
    # These fixed local instructions are optional for context-only installed use.
    # Checking does not render a planner prompt or require a checkout skill pack.
    for path, role in (("AGENTS.md", "repository_instructions"), ("KARAKANA.md", "project_contract")):
        inputs.read(path, role, optional=True)
    result["manifest"]["inputs"] = inputs.manifest()
    return inputs, request


def apply_report(result, data):
    result["content_report"] = data
    result["outcome"] = {"complete": "checked", "incomplete": "failed", "unsupported": "unsupported"}[data["completeness"]]
    result["freshness"]["inputs"] = "current"


def validate_scope(inputs, result, data):
    """A producer cannot silently omit declared documents or change their type."""
    context = result["selection"]["context"]
    declared = {d["key"]: d for d in context["documents"]}
    actual = {d["key"]: d for d in data["documents"]}
    mismatch = data["namespace"] != context["namespace"] or not actual.keys() <= declared.keys()
    if data["completeness"] == "complete" and actual.keys() != declared.keys():
        mismatch = True
    for key, doc in actual.items():
        spec = declared.get(key)
        if spec is None or doc["profile"] != spec["profile"] or doc["path"] != inputs.path(spec["path"]).relative_to(inputs.root).as_posix():
            mismatch = True
    if mismatch:
        raise TaskError("Content producer scope does not match the declared context. No documents may be silently filtered.",
                        code="DT-PRODUCER-001", outcome="unsupported")
    for source in data["manifest"]["sources"]:
        inputs.path(source["requested"])


def recheck(inputs, result):
    from karakana.tools.engineering_content import _recheck_before_output

    inputs.recheck()
    if fingerprint() != result["manifest"]["wrapper"]:
        raise TaskError("Task code changed. Run check again with stable inputs.", code="DT-DRIFT-001", outcome="failed")
    try:
        _recheck_before_output(inputs.root, ContentReport(result["content_report"]))
    except ContentError as exc:
        raise TaskError("Content inputs or checker changed before output. Run check again.", code="DT-DRIFT-001", outcome="failed") from exc


def check_task(root, request_path, output=None):
    result = begin("check")
    try:
        inputs, request = capture(root, request_path, result)
        from karakana.tools.engineering_content import check_content

        data = producer_data(check_content(inputs.root, request["context"]))
        validate_scope(inputs, result, data)
        apply_report(result, data)
        save_assessment(inputs, result, output, lambda: recheck(inputs, result))
    except TaskError as exc:
        add_failure(result, exc)
    except (OSError, UnicodeError) as exc:
        add_failure(result, TaskError("A required local resource is unavailable. Check the installation and declared inputs.",
                                      code="DT-READ-001", outcome="failed"))
    validate_assessment_result(result)
    return result
