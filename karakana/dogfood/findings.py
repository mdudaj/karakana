"""Dogfood finding classification."""

from __future__ import annotations

import secrets
from pathlib import Path

from karakana.dogfood.schemas import DogfoodFinding
from karakana.dogfood.summary import DogfoodStore


def analyze_dogfood(repo_root: Path, dogfood_id: str) -> tuple[list[DogfoodFinding], Path]:
    store = DogfoodStore(repo_root)
    run = store.load(dogfood_id)
    findings: list[DogfoodFinding] = []
    for result in run.command_results:
        if result.status in {"failed", "error"}:
            findings.append(_finding("broken_command", "high", f"Command failed: {result.command}", "A dogfood command failed and should be fixed or documented.", result.command, result.errors or [result.stderr_excerpt or "No stderr excerpt."]))
        elif result.status == "warning":
            findings.append(_finding("ux_friction", "medium", f"Command produced warnings: {result.command}", "A dogfood command completed with warnings that may need clearer UX or docs.", result.command, result.warnings or [result.stdout_excerpt or "Warning output not captured."]))
        elif result.status == "planned":
            findings.append(_finding("manual_review", "low", f"Command planned but not executed: {result.command}", "Dry-run dogfood planned this command. Execute it manually or run with explicit non-dry-run mode if needed.", result.command, ["planned"]))
    docs_required = ["docs/installation.md", "docs/configuration.md", "docs/daily-workflow.md", "docs/safety.md", "docs/release.md", "docs/troubleshooting.md", "docs/command-reference.md"]
    for relative in docs_required:
        if not (repo_root / relative).exists():
            findings.append(_finding("missing_doc", "medium", f"Missing doc: {relative}", "A required stable-harness documentation file is missing.", None, [relative], target=relative))
    if not (repo_root / "evals" / "dogfood").exists():
        findings.append(_finding("missing_eval", "medium", "Dogfood eval suite missing", "Dogfood workflows need deterministic eval coverage.", None, ["evals/dogfood"], target="evals/dogfood"))
    run.findings = findings
    if any(finding.severity in {"high", "critical"} for finding in findings):
        run.status = "completed_with_warnings"
    store.save(run)
    return findings, store.run_dir(dogfood_id) / "findings.md"


def _finding(ftype: str, severity: str, title: str, summary: str, command: str | None, evidence: list[str], target: str | None = None) -> DogfoodFinding:
    return DogfoodFinding(
        finding_id=f"finding-{secrets.token_hex(3)}",
        finding_type=ftype,
        title=title,
        summary=summary,
        severity=severity,
        affected_command=command,
        affected_area=target,
        evidence=evidence,
        recommended_action="Review and convert to a focused v1 hardening item.",
        suggested_target=target,
        suggested_skill="karakana-self-improvement",
        suggested_eval="evals/dogfood/" if ftype in {"missing_eval", "broken_command", "safety_gap"} else None,
        risk_level="high" if severity in {"high", "critical"} else "low",
    )
