"""Rule-based analysis of Karakana run traces."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from karakana.improvement.schemas import AnalysisFinding, AnalysisResult, EvidenceRef
from karakana.traces.schemas import RunTrace
from karakana.traces.store import TraceStore


class TraceAnalyzer:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.trace_store = TraceStore(repo_root)

    def analyze(self, project: str | None = None, since: str | None = None, limit: int = 20) -> AnalysisResult:
        traces = self._filter_traces(project=project, since=since, limit=limit)
        findings: list[AnalysisFinding] = []
        warnings: list[str] = []

        if not traces:
            warnings.append("No run traces found for the selected window.")
            return AnalysisResult(project=project, source_run_ids=[], findings=[], warnings=warnings)

        findings.extend(self._failed_or_partial_findings(traces, project))
        findings.extend(self._warning_findings(traces, project))
        findings.extend(self._missing_memory_findings(traces, project))
        findings.extend(self._missing_skill_findings(traces))
        findings.extend(self._missing_eval_findings(traces))
        findings.extend(self._prompt_without_followup_findings(traces, project))
        findings.extend(self._repeated_failure_findings(traces, project))

        return AnalysisResult(
            project=project,
            source_run_ids=[trace.run_id for trace in traces],
            findings=_dedupe_findings(findings),
            warnings=warnings,
        )

    def _filter_traces(self, project: str | None, since: str | None, limit: int) -> list[RunTrace]:
        cutoff = _parse_since(since)
        traces = []
        for trace in self.trace_store.list_runs(limit=limit):
            if project and trace.project not in (project, None):
                continue
            if cutoff and _parse_datetime(trace.started_at) < cutoff:
                continue
            traces.append(trace)
        return traces

    def _failed_or_partial_findings(self, traces: list[RunTrace], project: str | None) -> list[AnalysisFinding]:
        findings = []
        for trace in traces:
            if trace.status in {"failed", "partial"}:
                findings.append(
                    AnalysisFinding(
                        finding_type="repeated_failure",
                        title=f"Investigate {trace.command} {trace.status} run",
                        description=f"Run `{trace.run_id}` ended with status `{trace.status}`.",
                        evidence=[_evidence(trace)],
                        suggested_change_type="memory_update",
                        suggested_target_path=_known_issues_path(project or trace.project),
                        risk_level="medium",
                    )
                )
        return findings

    def _warning_findings(self, traces: list[RunTrace], project: str | None) -> list[AnalysisFinding]:
        return [
            AnalysisFinding(
                finding_type="documentation_gap",
                title=f"Document warning from {trace.command}",
                description="A run completed with warnings that may deserve durable documentation.",
                evidence=[_evidence(trace, "; ".join(trace.warnings))],
                suggested_change_type="doc_update",
                suggested_target_path="README.md",
                risk_level="low",
            )
            for trace in traces
            if trace.warnings
        ]

    def _missing_memory_findings(self, traces: list[RunTrace], project: str | None) -> list[AnalysisFinding]:
        findings = []
        for trace in traces:
            message = " ".join(trace.errors).lower()
            if "missing required memory files" in message:
                findings.append(
                    AnalysisFinding(
                        finding_type="missing_memory",
                        title="Add missing project memory notes",
                        description="A command failed because required ubongo project memory files were missing.",
                        evidence=[_evidence(trace)],
                        suggested_change_type="memory_update",
                        suggested_target_path=_open_issues_path(project or trace.project),
                        risk_level="low",
                    )
                )
        return findings

    def _missing_skill_findings(self, traces: list[RunTrace]) -> list[AnalysisFinding]:
        findings = []
        for trace in traces:
            message = " ".join(trace.errors)
            if "Skill not found" in message:
                findings.append(
                    AnalysisFinding(
                        finding_type="missing_skill",
                        title="Document or add missing skill",
                        description="A command referenced a skill that could not be loaded.",
                        evidence=[_evidence(trace, message)],
                        suggested_change_type="skill_update",
                        suggested_target_path="skills/",
                        risk_level="medium",
                    )
                )
        return findings

    def _missing_eval_findings(self, traces: list[RunTrace]) -> list[AnalysisFinding]:
        findings = []
        for trace in traces:
            if trace.status == "failed" and trace.skill:
                findings.append(
                    AnalysisFinding(
                        finding_type="missing_eval",
                        title=f"Add regression coverage for {trace.skill}",
                        description="A failed run should be considered for future regression coverage.",
                        evidence=[_evidence(trace)],
                        suggested_change_type="eval_update",
                        suggested_target_path=f"skills/{trace.skill}/evals/regression-case.yml",
                        risk_level="low",
                    )
                )
        return findings

    def _prompt_without_followup_findings(self, traces: list[RunTrace], project: str | None) -> list[AnalysisFinding]:
        findings = []
        for trace in traces:
            if trace.status == "success" and trace.artifacts and not trace.next_actions:
                if any("prompt" in artifact.kind for artifact in trace.artifacts):
                    findings.append(
                        AnalysisFinding(
                            finding_type="workflow_gap",
                            title=f"Define follow-up for {trace.command} prompt artifacts",
                            description="A prompt artifact was generated without recorded next actions.",
                            evidence=[_evidence(trace)],
                            suggested_change_type="doc_update",
                            suggested_target_path=_open_issues_path(project or trace.project),
                            risk_level="low",
                        )
                    )
        return findings

    def _repeated_failure_findings(self, traces: list[RunTrace], project: str | None) -> list[AnalysisFinding]:
        failed_commands = Counter(trace.command for trace in traces if trace.status == "failed")
        findings = []
        for command, count in failed_commands.items():
            if count >= 2:
                evidence = [_evidence(trace) for trace in traces if trace.command == command and trace.status == "failed"]
                findings.append(
                    AnalysisFinding(
                        finding_type="repeated_failure",
                        title=f"Repeated failures in {command}",
                        description=f"`{command}` failed {count} times in the selected trace window.",
                        evidence=evidence,
                        suggested_change_type="memory_update",
                        suggested_target_path=_known_issues_path(project),
                        risk_level="medium",
                    )
                )
        return findings


def _evidence(trace: RunTrace, summary: str | None = None) -> EvidenceRef:
    artifact_path = trace.artifacts[0].path if trace.artifacts else None
    return EvidenceRef(run_id=trace.run_id, artifact_path=artifact_path, summary=summary or f"{trace.command} ended as {trace.status}")


def _known_issues_path(project: str | None) -> str:
    return f"ubongo/projects/{project or 'karakana'}/known-issues.md"


def _open_issues_path(project: str | None) -> str:
    return f"ubongo/projects/{project or 'karakana'}/open-issues.md"


def _parse_since(since: str | None) -> datetime | None:
    if not since:
        return None
    parts = since.strip().split()
    if len(parts) != 2:
        return None
    try:
        amount = int(parts[0])
    except ValueError:
        return None
    unit = parts[1].lower()
    if unit.startswith("day"):
        return datetime.now(timezone.utc) - timedelta(days=amount)
    if unit.startswith("hour"):
        return datetime.now(timezone.utc) - timedelta(hours=amount)
    return None


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _dedupe_findings(findings: list[AnalysisFinding]) -> list[AnalysisFinding]:
    seen = set()
    unique = []
    for finding in findings:
        key = (finding.finding_type, finding.title, finding.suggested_target_path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)
    return unique
