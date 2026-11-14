"""Current-run reports with separate byte manifests and semantic assessment."""

from datetime import datetime, timezone
from importlib.metadata import version, PackageNotFoundError
from importlib.resources import files
import json

from . import CHECKER_VERSION
from .loader import sha
from .schemas import ContentReport


CODE = ("__init__.py", "schemas.py", "loader.py", "reader.py", "checks.py", "report.py")


def json_bytes(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def checker_fingerprint():
    package = files("karakana.content_profiles")
    entries = [{"component": "content_profiles/" + name, "sha256": sha(package.joinpath(name).read_bytes())} for name in CODE]
    tools = files("karakana.tools")
    for name in ("engineering_content.py", "engineering_artifacts.py"):
        entries.append({"component": "tools/" + name, "sha256": sha(tools.joinpath(name).read_bytes())})
    return {"version": CHECKER_VERSION, "components": entries, "sha256": sha(json_bytes(entries))}


def parser_version():
    try:
        return version("markdown-it-py")
    except PackageNotFoundError:
        return "unavailable"


def failure(exc, *, path="context"):
    return {"document": None, "rule_id": exc.rule, "severity": "error",
            "category": "unsupported" if exc.unsupported else "check",
            "location": exc.location or {"path": path, "line": 1}, "message": str(exc)}


def build_report(namespace, documents, findings, gaps, inputs, profiles, *, manifest=None):
    documents = sorted(documents, key=lambda d: d["key"])
    findings = sorted(findings, key=lambda f: (f["location"].get("path", ""), f["location"].get("line", 0),
                                               f["rule_id"], f["location"].get("record_id", ""), f["message"]))
    gaps = sorted(gaps, key=lambda g: (g["document"], g["location"]["line"], g["record_id"] or ""))
    errors = [f for f in findings if f["severity"] == "error"]
    status = "unsupported" if any(f["category"] == "unsupported" for f in errors) else "incomplete" if errors else "complete"
    coverage = {
        "scope": "M1 standard narrative packs only",
        "supported": ["default_profile_coverage", "record_integrity", "selected_requirement_links", "current_run_manifest"],
        "advanced_context": "unsupported", "saved_report_verification": "unsupported",
        "unassessed": ["semantic_correctness", "evidence_authenticity", "omission_applicability",
                       "open_item_resolution_details", "unmapped_prose_claims", "product_readiness", "acceptance"],
    }
    assessment = {"namespace": namespace, "documents": documents, "findings": findings,
                  "open_acceptance_items": gaps, "coverage": coverage, "completeness": status}
    if manifest is None:
        manifest = {"sources": inputs.manifest(), "profiles": sorted(profiles, key=lambda x: x["id"]),
                    "checker": checker_fingerprint(), "parser_version": parser_version()}
    data = {"report_version": "0.1", **assessment,
            "review_required": True, "readiness": "unresolved" if gaps else "not_assessed",
            "acceptance": "not_assessed", "generated_utc": datetime.now(timezone.utc).isoformat(),
            "manifest": manifest,
            "assessment_digest": sha(json_bytes(assessment))}
    return ContentReport(data)


def render_text(report):
    data = report.to_dict()
    if report.ok:
        first = (f"Content checks passed for the selected M1 profiles. Review is required; "
                 f"{len(data['open_acceptance_items'])} source gap entries remain unresolved.")
    else:
        first = "Content check is " + data["completeness"] + ". Correct the reported errors or select supported content."
    lines = [first, "Saved-report verification is not supported in M1. Run check again for current inputs."]
    for finding in data["findings"]:
        loc = finding["location"]
        lines.append(f"{finding['rule_id']} {finding['severity']} {loc.get('path', 'input')}:{loc.get('line', 1)}: {finding['message']}")
    return "\n".join(lines) + "\n"
