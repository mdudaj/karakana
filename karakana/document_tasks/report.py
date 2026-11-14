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
    result["diagnostics"].append({"code": error.code, "severity": "error", "location": error.location,
                                  "message": str(error), "next_action": "Correct the declared input or choose a permitted fresh output, then prepare again."})


def validate_prepare_result(result):
    fields = {"result_version", "operation", "outcome", "task", "selection", "content_report",
              "freshness", "diagnostics", "manifest", "run"}
    if (set(result) != fields or result["result_version"] != "0.1" or result["operation"] != "prepare"
            or result["content_report"] is not None
            or result["outcome"] not in {"prepared", "blocked", "unsupported", "failed"}
            or result["freshness"]["saved_bundle"] != "not_assessed"):
        raise TaskError("Preparation result violates its supported contract.", code="DT-RESULT-001", outcome="failed")


def literal_output(value):
    """Escape terminal controls, including source-provided bidi/format controls."""
    return "".join(c if c.isprintable() else json.dumps(c, ensure_ascii=True)[1:-1] for c in str(value))


def render_text(result):
    task = result["task"] or {}
    scope = literal_output(task.get("scope", "selected task"))
    lines = [f"{scope} — {result['outcome']}."]
    if result["outcome"] == "prepared":
        lines.append("Task prepared. Content was not checked.")
    else:
        lines.append("Task was not prepared. Content was not checked.")
    lines.append("Completeness, readiness, acceptance and saved verification: not assessed. Review is required.")
    selection = result["selection"]
    lines.append("Resources: " + selection["state"] + ".")
    for item in selection["effective"]:
        lines.append(f"{literal_output(item['role'])}: {literal_output(item['path'])} "
                     f"({literal_output(item['revision'])}; {item['origin']}; {item['revision_basis']}).")
    for item in selection["overrides"]:
        lines.append("Override: " + literal_output(item["previous"]["path"]) + " -> " + literal_output(item["effective"]["path"]) + ".")
    if selection["context"]:
        lines.append("Check context selected (not assessed): " + literal_output(selection["context"]["path"]) + ".")
    if selection["state"] == "not_selected":
        for item in selection["recommendations"]:
            lines.append("Unselected recommendation: " + literal_output(item["artifact_type"]) + " guide/template; choose explicitly if relevant.")
    for diagnostic in result["diagnostics"]:
        location = diagnostic["location"]
        label = location.get("path", location.get("input", "request")) + location.get("pointer", "")
        lines.append(f"{diagnostic['code']} {literal_output(label)}: {literal_output(diagnostic['message'])} "
                     + literal_output(diagnostic["next_action"]))
    if result["outcome"] == "prepared":
        lines.append("Prompt: " + literal_output(result["run"]["bundle"]) + "/prompt.md")
    return "\n".join(lines) + "\n"
