"""Recompute both raw M2 assessments and every deterministic wrapper field."""

from copy import deepcopy
from pathlib import Path

from .inputs import CapturedInputs, json_bytes
from .schemas import TaskError, contract, decode, literal
from .assessment import begin, capture, producer_data, validate_report, timestamp, apply_report, recheck, validate_scope
from .report import add_failure, validate_assessment_result
from .bundles import save_assessment


def semantic(result):
    """Only documented run and M2 generation metadata are volatile."""
    value = deepcopy(result)
    del value["run"]
    if value["content_report"] is not None:
        value["content_report"].pop("generated_utc", None)
    return json_bytes(value)


def saved_bundle(root, project, bundle):
    saved = CapturedInputs(root)
    saved.project = project
    path = saved.path(str(bundle))
    relative = path.relative_to(saved.root)
    if len(relative.parts) < 2 or relative.parts[0] != ".karakana" or not path.is_dir():
        raise TaskError("Select an existing assessment bundle under .karakana/.", code="DT-BUNDLE-001", outcome="unsupported")
    result = decode(saved.read((relative / "result.json").as_posix(), "saved_result"))
    report_path = (relative / "content-report.json").as_posix()
    report = decode(saved.read(report_path, "saved_report"))
    contract(result, ("result_version", "operation", "outcome", "task", "selection", "content_report", "freshness", "diagnostics", "manifest", "run"))
    if (result["result_version"] != "0.1" or result["operation"] not in ("check", "verify")
            or (result["operation"] == "verify" and result["outcome"] != "verified")):
        raise TaskError("Select a supported check or successful verification bundle, not preparation or incomplete output.",
                        code="DT-BUNDLE-001", outcome="unsupported")
    contract(result["run"], ("id", "generated_utc", "bundle"))
    literal(result["run"]["id"])
    timestamp(result["run"]["generated_utc"])
    recorded = saved.path(result["run"]["bundle"]).relative_to(saved.root)
    if len(recorded.parts) < 2 or recorded.parts[0] != ".karakana":
        raise TaskError("Saved output metadata is outside the supported runtime root.", code="DT-BUNDLE-001", outcome="unsupported")
    if not isinstance(result["task"], dict) or result["task"].get("project") != project:
        raise TaskError("Select an assessment bundle for this project.", code="DT-PROJECT-001", outcome="unsupported")
    if json_bytes(report) != json_bytes(result["content_report"]):
        raise TaskError("The bare and nested reports differ. Run check into a new bundle.", code="DT-BUNDLE-001", outcome="stale_or_mismatched")
    validate_report(report, verification=result["operation"] == "verify")
    return saved, result, report_path


def verify_task(root, request_path, bundle, output=None):
    result = begin("verify")
    try:
        inputs, request = capture(root, request_path, result)
        saved_inputs, old, report_path = saved_bundle(inputs.root, request["project"], bundle)
        from karakana.tools.engineering_content import verify_report

        raw = producer_data(verify_report(inputs.root, request["context"], report_path), verification=True)
        validate_scope(inputs, result, raw)
        apply_report(result, raw)
        result["freshness"]["saved_bundle"] = "current"
        result["outcome"] = "verified" if raw["completeness"] == "complete" else result["outcome"]
        # A saved check is compared to a recomputed check result, not a verify envelope.
        expected = deepcopy(result)
        if old["operation"] == "check":
            expected["operation"] = "check"
            expected["freshness"]["saved_bundle"] = "not_assessed"
            apply_report(expected, {k: v for k, v in raw.items() if k != "verification"})
        if raw["verification"] != "current" or semantic(old) != semantic(expected):
            error = TaskError("Saved task inputs or result fields differ from recomputation. Run check into a new bundle.",
                              code="DT-VERIFY-001", outcome="stale_or_mismatched")
            add_failure(result, error)
            result["freshness"] = {"inputs": "current", "saved_bundle": "stale_or_mismatched"}

        def current():
            saved_inputs.recheck()
            recheck(inputs, result)

        save_assessment(inputs, result, output, current)
    except TaskError as exc:
        add_failure(result, exc)
        result["freshness"]["saved_bundle"] = "stale_or_mismatched"
    except (OSError, UnicodeError) as exc:
        add_failure(result, TaskError("A saved or current local input is unavailable. Select a complete guarded bundle and current request.",
                                      code="DT-READ-001", outcome="failed"))
        result["freshness"]["saved_bundle"] = "stale_or_mismatched"
    validate_assessment_result(result)
    return result
