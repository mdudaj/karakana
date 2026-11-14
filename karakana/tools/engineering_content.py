"""Opt-in standard narrative-pack checking; no automatic gates or source edits."""

import argparse
from pathlib import Path
from datetime import datetime

from karakana.content_profiles.checks import assess
from karakana.content_profiles.context import Context
from karakana.content_profiles.loader import Inputs, MAX_CONFIG_BYTES, load_profile, local_path, sha
from karakana.content_profiles.reader import parser, read_narrative
from karakana.content_profiles.report import build_report, failure, json_bytes, render_text, checker_fingerprint, parser_version
from karakana.content_profiles.schemas import ContentError, ContentReport, strict_json, validate_context
from karakana.tools.engineering_artifacts import write_new, ArtifactError


def check_content(root: Path, context_path: Path) -> ContentReport:
    """Recompute a scoped current-run report; never mutate sources or accept them."""
    try:
        inputs = Inputs(root)
    except ContentError as exc:
        return build_report(None, [], [failure(exc)], [], Inputs(Path.cwd()), [])
    namespace, documents, findings, gaps, profiles = None, [], [], [], []
    details = {}
    context_location = "context"
    try:
        starting_checker, starting_parser = checker_fingerprint(), parser_version()
        raw, context_location = inputs.read(str(context_path), "context", MAX_CONFIG_BYTES)
        context = validate_context(strict_json(raw))
        namespace = context["namespace"]
        md = parser()
        narratives, failed_documents, paths = [], [], set()
        for spec in sorted(context["documents"], key=lambda d: d["key"]):
            profile, identity = load_profile(spec["profile"]["id"], spec["profile"]["version"])
            if identity not in profiles:
                profiles.append(identity)
            raw, relative = inputs.read(spec["path"], "document:" + spec["key"])
            resolved = local_path(inputs.root, spec["path"])
            if resolved in paths:
                raise ContentError("The same physical source was declared more than once.", rule="CP-ID-001")
            paths.add(resolved)
            try:
                narratives.append(read_narrative(raw, spec["key"], relative, profile, md, tuple(c["slot"] for c in context.get("coverage", []) if c["document"] == spec["key"])))
            except ContentError as exc:
                if not exc.location:
                    exc.location = {"path": relative, "line": 1}
                finding = failure(exc)
                finding["document"] = spec["key"]
                findings.append(finding)
                failed_documents.append({"key": spec["key"], "path": relative, "document_id": None,
                                         "content_version": None, "profile": dict(spec["profile"]),
                                         "requirements": [], "criteria": [], "coverage": [],
                                         "unassessed_section_count": None,
                                         "completeness": "unsupported" if exc.unsupported else "incomplete"})
        resolved = None
        try:
            candidate = Context(inputs, narratives, context, md)
            candidate.prepare()
            resolved = candidate
        except ContentError as exc:
            # Keep visible source checks/gaps on otherwise readable documents.
            findings.append(failure(exc, path=context_location))
        documents, checks, gaps = assess(narratives, context, md, resolved)
        if resolved:
            for item in resolved.mapped_items:
                existing = next((g for g in gaps if g["location"]["path"] == item["location"]["path"]
                                 and g["location"]["line"] == item["location"]["line"]), None)
                if existing:
                    existing.update({k:v for k,v in item.items() if k not in {"kind", "record_id", "document"}})
                else:
                    gaps.append(item)
            details["claims"] = resolved.claims
            findings.extend(resolved.findings)
        documents.extend(failed_documents)
        findings.extend(checks)
        inputs.recheck()
        if checker_fingerprint() != starting_checker or parser_version() != starting_parser:
            raise ContentError("The checker changed during assessment. Run the check again.", rule="CP-DRIFT-001")
        for identity in profiles:
            _, current = load_profile(identity["id"], identity["version"])
            if current != identity:
                raise ContentError("A content profile changed during the check. Run the check again.", rule="CP-DRIFT-001")
    except ContentError as exc:
        findings.append(failure(exc, path=context_location))
    except (OSError, UnicodeError) as exc:
        error = ContentError("A required local resource is unavailable. Check the installation and declared inputs.", rule="CP-READ-001")
        findings.append(failure(error, path=context_location))
    return build_report(namespace, documents, findings, gaps, inputs, profiles, details=details)


def _recheck_before_output(root, report):
    """A safety recheck for this run, not a saved-report verification interface."""
    data = report.to_dict()
    current = Inputs(root)
    for source in data["manifest"]["sources"]:
        raw, relative = current.read(source["requested"], "output_recheck")
        if sha(raw) != source["sha256"] or relative != source["path"]:
            raise ContentError("A source changed before report output. Run the check again.", rule="CP-DRIFT-001")
    for identity in data["manifest"]["profiles"]:
        _, profile = load_profile(identity["id"], identity["version"])
        if profile != identity:
            raise ContentError("A profile changed before report output. Run the check again.", rule="CP-DRIFT-001")
    if (checker_fingerprint() != data["manifest"]["checker"]
            or parser_version() != data["manifest"]["parser_version"]):
        raise ContentError("The checker changed before report output. Run the check again.", rule="CP-DRIFT-001")



def verify_report(root: Path, context_path: Path, report_path: Path) -> ContentReport:
    """Recompute current checks and compare every persisted assessment/manifest field."""
    current = check_content(root, context_path)
    data = current.to_dict()
    try:
        saved_inputs = Inputs(root)
        raw, relative = saved_inputs.read(str(report_path), "saved_report")
        saved = strict_json(raw)
        if not isinstance(saved, dict) or saved.get("report_version") != "0.2":
            raise ContentError("Select a supported version 0.2 JSON report; regenerate incompatible reports with check.", rule="CP-REPORT-001", unsupported=True)
        generated = saved.get("generated_utc")
        try:
            timestamp = datetime.fromisoformat(generated)
            if timestamp.tzinfo is None or timestamp.utcoffset() is None: raise ValueError()
        except (TypeError, ValueError) as exc:
            raise ContentError("The saved report has an invalid generation time. Run check again.", rule="CP-REPORT-001") from exc
        expected = {k:v for k,v in data.items() if k != "generated_utc"}
        actual = {k:v for k,v in saved.items() if k not in {"generated_utc", "verification"}}
        if (saved.get("verification", "current") != "current" or json_bytes(actual) != json_bytes(expected)):
            raise ContentError("Saved inputs or assessment differ from recomputed checks. Run check again; a saved digest or pass cannot establish freshness.", rule="CP-VERIFY-001", location={"path":relative,"line":1})
        saved_inputs.recheck()
        _recheck_before_output(root, current)
        data["verification"] = "current"
        return ContentReport(data)
    except (ContentError, OSError) as exc:
        error = exc if isinstance(exc, ContentError) else ContentError("The saved report is unreadable. Select a guarded local JSON report.", rule="CP-REPORT-001")
        refused = build_report(data["namespace"], data["documents"], data["findings"]+[failure(error)],
                               data["open_acceptance_items"], Inputs(Path.cwd()), data["manifest"]["profiles"],
                               manifest=data["manifest"], details=data["coverage"])
        result = refused.to_dict(); result["verification"] = "stale_or_mismatched"
        return ContentReport(result)

def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=Path.cwd(), help="Declared local source/output root")
    commands = cli.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Check explicitly selected narrative profiles and source mappings")
    check.add_argument("--context", type=Path, required=True)
    check.add_argument("--format", choices=("text", "json"), default="text")
    check.add_argument("--output", type=Path, help="Optional new report path relative to root; existing files are preserved")
    verify = commands.add_parser("verify", help="Recompute current inputs and compare a saved JSON report")
    verify.add_argument("--context", type=Path, required=True)
    verify.add_argument("--report", type=Path, required=True)
    verify.add_argument("--format", choices=("text", "json"), default="text")
    args = cli.parse_args(argv)
    if args.command == "verify":
        report = verify_report(args.root, args.context, args.report)
    else:
        report = check_content(args.root, args.context)
        if args.output:
            try:
                output = local_path(Inputs(args.root).root, str(args.output))
                _recheck_before_output(args.root, report)
                value = json_bytes(report.to_dict()) if args.format == "json" else render_text(report).encode()
                write_new(Inputs(args.root).root, {output: value})
            except (ContentError, ArtifactError, FileExistsError, OSError) as exc:
                data = report.to_dict()
                error = exc if isinstance(exc, ContentError) else ContentError("Report output was refused. Choose a permitted new path; existing files were preserved.", rule="CP-OUTPUT-001")
                report = build_report(data["namespace"], data["documents"], data["findings"] + [failure(error)],
                                      data["open_acceptance_items"], Inputs(Path.cwd()), data["manifest"]["profiles"],
                                      manifest=data["manifest"], details=data["coverage"])
    if args.format == "json":
        print(json_bytes(report.to_dict()).decode(), end="")
    else:
        print(render_text(report), end="")
    return 0 if report.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
