"""Rule-based self-improvement proposal generation."""

from __future__ import annotations

from pathlib import Path

from karakana.improvement.analyzer import TraceAnalyzer
from karakana.improvement.schemas import AnalysisFinding, ImprovementProposal, ProposedChange
from karakana.improvement.store import generate_proposal_id
from karakana.traces.schemas import now_utc, redact_value


class ImprovementProposer:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.analyzer = TraceAnalyzer(repo_root)

    def propose(self, project: str | None = None, since: str | None = None, limit: int = 20) -> ImprovementProposal:
        analysis = self.analyzer.analyze(project=project, since=since, limit=limit)
        changes = [_change_from_finding(finding, project) for finding in analysis.findings]
        summary = _summary(changes, analysis.warnings)
        return ImprovementProposal(
            proposal_id=generate_proposal_id(),
            project=project,
            status="ready_for_review",
            created_at=now_utc(),
            source_run_ids=analysis.source_run_ids,
            summary=summary,
            changes=changes,
            warnings=analysis.warnings,
            next_actions=[
                "Review this proposal.",
                "Convert accepted changes into a normal branch and pull request.",
                "Run tests before merging any proposed repository changes.",
            ],
        )


def _change_from_finding(finding: AnalysisFinding, project: str | None) -> ProposedChange:
    target = finding.suggested_target_path or _default_target(finding, project)
    risk = _risk_for_target(target, finding.risk_level)
    return ProposedChange(
        target_path=target,
        change_type=finding.suggested_change_type,
        title=finding.title,
        rationale=finding.description,
        proposed_content=redact_value(_proposed_content(finding)),
        evidence=finding.evidence,
        risk_level=risk,
        requires_human_review=True,
    )


def _default_target(finding: AnalysisFinding, project: str | None) -> str:
    if finding.finding_type == "missing_skill":
        return "skills/"
    if finding.finding_type == "missing_eval":
        return "evals/regression-cases/"
    if finding.finding_type == "workflow_gap":
        return ".github/workflows/"
    return f"ubongo/projects/{project or 'karakana'}/open-issues.md"


def _proposed_content(finding: AnalysisFinding) -> str:
    evidence = ", ".join(evidence.run_id for evidence in finding.evidence)
    return (
        f"Proposed note: {finding.title}\n\n"
        f"Rationale: {finding.description}\n\n"
        f"Evidence runs: {evidence}\n"
    )


def _risk_for_target(target: str, fallback: str) -> str:
    lowered = target.lower()
    high_terms = ("auth", "permission", "billing", "migration", "deploy", ".github/workflows")
    if any(term in lowered for term in high_terms):
        return "high"
    return fallback


def _summary(changes: list[ProposedChange], warnings: list[str]) -> str:
    if not changes:
        return "No concrete self-improvement changes were proposed for the selected trace window."
    return f"Generated {len(changes)} evidence-based proposed change(s)." + (f" Warnings: {len(warnings)}." if warnings else "")
