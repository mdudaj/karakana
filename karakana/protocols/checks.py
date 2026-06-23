"""Protocol artifact gate checks for run traces."""

from __future__ import annotations

import secrets
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from karakana.traces.schemas import RunTrace, redact_value
from karakana.traces.store import TraceStore

CHECK_STATUSES = {"passed", "failed", "warning", "error"}

ARTIFACT_ALIASES = {
    "acceptance_criteria": {"acceptance_criteria", "requirements_prd", "requirements_prd_markdown", "requirements_readiness"},
    "accessibility_checklist": {"accessibility_checklist", "ux_accessibility_checklist"},
    "adr": {"adr", "architecture_decision", "decision_record"},
    "approval_record": {"approval_record", "human_approval", "review_approval"},
    "change_summary": {"change_summary", "patch_summary", "patch_lifecycle_summary", "codex_patch_summary"},
    "definition_of_done": {"definition_of_done", "requirements_readiness", "requirements_prd"},
    "handoff": {"handoff", "session_handoff", "workspace_handoff"},
    "migration_plan": {"migration_plan", "database_migration_plan"},
    "requirements_note": {"requirements_note", "requirements_prd", "requirements_prd_markdown"},
    "rollback_plan": {"rollback_plan"},
    "safety_review": {"safety_review", "patch_review", "model_response_review", "ingestion_review"},
    "schema_contract": {"schema_contract", "schema", "api_contract", "data_contract"},
    "screenshot_or_render_evidence": {"screenshot", "render_evidence", "playwright_screenshot", "template_render_evidence"},
    "task_classification": {"task_classification", "protocol_classification"},
    "test_or_eval_rationale": {"test_or_eval_rationale", "test_result", "eval_report_json", "eval_report_markdown"},
    "threat_or_abuse_case_note": {"threat_or_abuse_case_note", "threat_model", "abuse_case_note"},
    "trace": {"trace", "run_trace"},
    "user_story": {"user_story", "requirements_stories", "requirements_stories_markdown"},
    "ux_description": {"ux_description", "frontend_review", "design_review"},
    "verification_summary": {"verification_summary", "test_result", "eval_report_json", "eval_report_markdown", "patch_gate", "requirements_readiness"},
}


@dataclass
class ProtocolArtifactCheck:
    artifact_kind: str
    status: str
    evidence: list[str] = field(default_factory=list)
    message: str | None = None

    def __post_init__(self) -> None:
        if self.status not in CHECK_STATUSES:
            raise ValueError(f"Invalid protocol artifact check status: {self.status}")
        self.evidence = redact_value(self.evidence)
        self.message = redact_value(self.message)


@dataclass
class ProtocolCheckResult:
    check_id: str
    trace_id: str
    status: str
    protocol_id: str | None
    work_category: str | None
    risk_level: str | None
    required_artifacts: list[str] = field(default_factory=list)
    checks: list[ProtocolArtifactCheck] = field(default_factory=list)
    missing_artifacts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommended_next_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in CHECK_STATUSES:
            raise ValueError(f"Invalid protocol check status: {self.status}")
        self.metadata = redact_value(self.metadata)

    @property
    def ok(self) -> bool:
        return self.status == "passed"

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


def run_protocol_check(repo_root: Path, trace_id: str) -> tuple[ProtocolCheckResult, Path]:
    trace = TraceStore(repo_root).load(trace_id)
    result = check_trace_protocol_artifacts(repo_root, trace)
    store = ProtocolCheckStore(repo_root)
    path = store.save(result)
    return result, path


def check_trace_protocol_artifacts(repo_root: Path, trace: RunTrace) -> ProtocolCheckResult:
    required = list(dict.fromkeys(trace.required_artifacts))
    warnings: list[str] = []
    if not trace.protocol_id:
        warnings.append("Trace has no protocol_id.")
    if not required:
        warnings.append("Trace has no required_artifacts.")

    checks = [_check_artifact(repo_root, trace, artifact_kind) for artifact_kind in required]
    missing = [check.artifact_kind for check in checks if check.status == "failed"]
    next_actions = [f"Produce or link required artifact: {artifact_kind}." for artifact_kind in missing]
    status = "failed" if missing else ("warning" if warnings else "passed")
    return ProtocolCheckResult(
        check_id=generate_protocol_check_id(),
        trace_id=trace.run_id,
        status=status,
        protocol_id=trace.protocol_id,
        work_category=trace.work_category,
        risk_level=trace.risk_level,
        required_artifacts=required,
        checks=checks,
        missing_artifacts=missing,
        warnings=warnings,
        recommended_next_actions=next_actions,
        metadata={"command": trace.command, "project": trace.project, "task_type": trace.task_type},
    )


def _check_artifact(repo_root: Path, trace: RunTrace, artifact_kind: str) -> ProtocolArtifactCheck:
    evidence = _artifact_evidence(repo_root, trace, artifact_kind)
    if evidence:
        return ProtocolArtifactCheck(artifact_kind=artifact_kind, status="passed", evidence=evidence)
    return ProtocolArtifactCheck(
        artifact_kind=artifact_kind,
        status="failed",
        message=f"Required artifact not found: {artifact_kind}",
    )


def _artifact_evidence(repo_root: Path, trace: RunTrace, artifact_kind: str) -> list[str]:
    aliases = ARTIFACT_ALIASES.get(artifact_kind, {artifact_kind})
    evidence: list[str] = []
    if artifact_kind == "trace":
        trace_path = repo_root / ".karakana" / "runs" / trace.run_id / "trace.json"
        if trace_path.exists():
            evidence.append(str(trace_path))
    for artifact in trace.artifacts:
        if artifact.kind in aliases or artifact.kind == artifact_kind:
            path = Path(artifact.path)
            resolved = path if path.is_absolute() else repo_root / path
            if resolved.exists():
                evidence.append(str(resolved))
            else:
                evidence.append(f"{artifact.path} ({artifact.kind}, path missing)")
    for key, value in trace.outputs.items():
        if key in aliases or key == artifact_kind:
            evidence.append(f"trace.outputs.{key}={value}")
    if artifact_kind == "task_classification" and trace.protocol_id and trace.work_category and trace.risk_level:
        evidence.append("trace.protocol_id/work_category/risk_level")
    if artifact_kind == "handoff" and trace.outputs.get("session_handoff"):
        evidence.append(f"trace.outputs.session_handoff={trace.outputs['session_handoff']}")
    return sorted(set(evidence))


class ProtocolCheckStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / ".karakana" / "protocol-checks"

    def save(self, result: ProtocolCheckResult) -> Path:
        import json

        check_dir = self.root / result.check_id
        check_dir.mkdir(parents=True, exist_ok=True)
        path = check_dir / "check.json"
        path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (check_dir / "check.md").write_text(render_protocol_check(result), encoding="utf-8")
        self._write_latest(result.check_id)
        return path

    def load(self, check_id: str) -> ProtocolCheckResult:
        import json

        path = self.root / check_id / "check.json"
        if not path.exists():
            raise FileNotFoundError(f"Protocol check not found: {check_id}")
        data = json.loads(path.read_text(encoding="utf-8"))
        data["checks"] = [ProtocolArtifactCheck(**item) for item in data.get("checks", [])]
        return ProtocolCheckResult(**data)

    def _write_latest(self, check_id: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "latest").write_text(check_id + "\n", encoding="utf-8")


def render_protocol_check(result: ProtocolCheckResult) -> str:
    return f"""# Karakana Protocol Check

## Summary

- Check ID: {result.check_id}
- Trace ID: {result.trace_id}
- Status: {result.status}
- Protocol: {result.protocol_id or ""}
- Category: {result.work_category or ""}
- Risk: {result.risk_level or ""}

## Required Artifacts

{_bullets(result.required_artifacts)}

## Checks

{_check_lines(result.checks)}

## Missing Artifacts

{_bullets(result.missing_artifacts)}

## Warnings

{_bullets(result.warnings)}

## Recommended Next Actions

{_bullets(result.recommended_next_actions)}
"""


def generate_protocol_check_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-protocol-check-{secrets.token_hex(3)}"


def _check_lines(checks: list[ProtocolArtifactCheck]) -> str:
    if not checks:
        return "- None"
    lines = []
    for check in checks:
        detail = f" ({'; '.join(check.evidence)})" if check.evidence else (f" - {check.message}" if check.message else "")
        lines.append(f"- {check.artifact_kind}: {check.status}{detail}")
    return "\n".join(lines)


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
