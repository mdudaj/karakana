"""Operation results and literal terminal output; no product-readiness decision."""

import json

from .schemas import TaskError


def new_result(run_id, generated):
    return {"result_version": "0.1", "operation": "prepare", "outcome": "blocked", "task": None,
            "selection": {"state": "not_selected", "effective": [], "overrides": [], "recommendations": [],
                          "context": None, "instruction_review_required": True},
            "content_report": None,
            "freshness": {"inputs": "unresolved", "saved_bundle": "not_assessed"},
            "diagnostics": [], "manifest": {"root": None, "inputs": [], "wrapper": None},
            "run": {"id": run_id, "generated_utc": generated, "bundle": None}}


def add_failure(result, error):
    result["outcome"] = error.outcome
    result["freshness"]["inputs"] = "unresolved"
    if not result["selection"]["effective"]:
        result["selection"]["state"] = "unsupported" if error.outcome == "unsupported" else "blocked"
    operation = "prepare" if result["operation"] == "prepare" else "check"
    diagnostic = {"code": error.code, "severity": "error", "location": error.location,
                  "message": str(error), "next_action": f"Correct the declared input or choose a permitted fresh output, then run {operation} again."}
    if getattr(error, "producer_state", None):
        diagnostic["producer_state"] = error.producer_state
    result["diagnostics"].append(diagnostic)


def validate_prepare_result(result):
    fields = {"result_version", "operation", "outcome", "task", "selection", "content_report",
              "freshness", "diagnostics", "manifest", "run"}
    if (set(result) != fields or result["result_version"] != "0.1" or result["operation"] != "prepare"
            or result["content_report"] is not None
            or result["outcome"] not in {"prepared", "blocked", "unsupported", "failed"}
            or result["freshness"]["saved_bundle"] != "not_assessed"):
        raise TaskError("Preparation result violates its supported contract.", code="DT-RESULT-001", outcome="failed")


def validate_assessment_result(result):
    """Executable envelope invariants; M2's assessment remains an exact copy."""
    fields = {"result_version", "operation", "outcome", "task", "selection", "content_report",
              "freshness", "diagnostics", "manifest", "run"}
    success = result["outcome"] in {"checked", "verified"}
    report = result["content_report"]
    if (set(result) != fields or result["result_version"] != "0.1"
            or result["operation"] not in {"check", "verify"}
            or result["outcome"] not in {"checked", "verified", "blocked", "unsupported", "failed", "stale_or_mismatched"}
            or (result["operation"] == "check" and result["freshness"]["saved_bundle"] != "not_assessed")
            or (result["outcome"] == "checked" and result["operation"] != "check")
            or (result["outcome"] == "verified" and (result["operation"] != "verify"
                 or result["freshness"]["saved_bundle"] != "current" or report is None or report.get("verification") != "current"))
            or (success and (report is None or report["completeness"] != "complete"
                             or report["acceptance"] != "not_assessed" or report["review_required"] is not True))):
        raise TaskError("Assessment result violates its supported contract.", code="DT-RESULT-001", outcome="failed")


def literal_output(value):
    """Escape terminal controls, including source-provided bidi/format controls."""
    return "".join(c if c.isprintable() else json.dumps(c, ensure_ascii=True)[1:-1] for c in str(value))


def render_text(result):
    task = result["task"] or {}
    scope = literal_output(task.get("scope", "selected task"))
    lines = [f"{scope} — {result['outcome']}."]
    report = result["content_report"]
    if report is not None:
        lines.append(f"Content {report['completeness']}; inputs {result['freshness']['inputs']}; "
                     f"saved bundle {result['freshness']['saved_bundle']}.")
        lines.append(f"Review required. Readiness {report['readiness']}; acceptance {report['acceptance']}.")
        lines.append(f"{len(report['open_acceptance_items'])} source gap entries remain; review their declared scopes and next actions.")
        if "verification" in report:
            lines.append("Raw content report verification: " + report["verification"] + ".")
    elif result["outcome"] == "prepared":
        lines.append("Task prepared. Content was not checked.")
    elif result["operation"] == "prepare":
        lines.append("Task was not prepared. Content was not checked.")
    else:
        lines.append("Content was not checked.")
    if report is None:
        lines.append("Completeness, readiness, acceptance and saved verification: not assessed. Review is required.")
    selection = result["selection"]
    lines.append("Resources: " + selection["state"] + ".")
    for item in selection["effective"]:
        lines.append(f"{literal_output(item['role'])}: {literal_output(item['path'])} "
                     f"({literal_output(item['revision'])}; {item['origin']}; {item['revision_basis']}).")
    for item in selection["overrides"]:
        lines.append("Override: " + literal_output(item["previous"]["path"]) + " -> " + literal_output(item["effective"]["path"]) + ".")
    if selection["context"]:
        label = "Check context: " if report else "Check context selected (not assessed): "
        lines.append(label + literal_output(selection["context"]["path"]) + ".")
    if selection["state"] == "not_selected":
        for item in selection["recommendations"]:
            lines.append("Unselected recommendation: " + literal_output(item["artifact_type"]) + " guide/template; choose explicitly if relevant.")
    for diagnostic in result["diagnostics"]:
        location = diagnostic["location"]
        label = location.get("path", location.get("input", "request")) + location.get("pointer", "")
        lines.append(f"{diagnostic['code']} {literal_output(label)}: {literal_output(diagnostic['message'])} "
                     + literal_output(diagnostic["next_action"]))
        if diagnostic.get("producer_state"):
            lines.append("Producer state: " + literal_output(json.dumps(diagnostic["producer_state"], sort_keys=True)))
    if report is not None:
        for document in report["documents"]:
            lines.append("Document: " + literal_output(document["key"]) + " / " + literal_output(document["path"]) +
                         f"; {document['completeness']}; readiness {document['readiness']}; acceptance {document['acceptance']}.")
        lines.append("Coverage and unassessed scope: " + literal_output(json.dumps(report["coverage"], ensure_ascii=False, sort_keys=True)))
        for finding in report["findings"]:
            lines.append(literal_output(finding["rule_id"]) + " " + literal_output(finding["severity"]) + " " +
                         literal_output(json.dumps(finding["location"], ensure_ascii=False, sort_keys=True)) + ": " +
                         literal_output(finding["message"]))
        for gap in report["open_acceptance_items"]:
            lines.append("Open item: " + literal_output(json.dumps(gap, ensure_ascii=False, sort_keys=True)))
        if result["outcome"] in {"failed", "unsupported", "stale_or_mismatched"}:
            lines.append("Correct reported inputs or select supported content, then run check into a fresh bundle. Manual review remains available.")
    if result["outcome"] == "prepared":
        lines.append("Prompt: " + literal_output(result["run"]["bundle"]) + "/prompt.md")
    return "\n".join(lines) + "\n"
