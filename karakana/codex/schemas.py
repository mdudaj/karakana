"""Schemas for Codex handoff and patch review artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

REVIEW_STATUSES = {"passed", "warning", "blocked", "error"}
SEVERITIES = {"info", "low", "medium", "high", "critical"}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class CodexHandoffTask:
    task_id: str
    source_action_run_id: str | None
    source_action_id: str | None
    title: str
    description: str
    project: str | None = None
    skill: str | None = None
    suggested_skills: list[str] = field(default_factory=list)
    recommended_provider: str = "openai_codex"
    recommended_model: str = "gpt-5.4-mini"
    escalation_model: str | None = "gpt-5.4"
    risk_level: str = "low"
    rationale: str | None = None
    context: str | None = None
    safety_rules: list[str] = field(default_factory=list)
    tests_to_run: list[str] = field(default_factory=list)
    approval_requirements: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")
        self.description = redact_value(self.description)
        self.context = redact_value(self.context)
        self.metadata = redact_value(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CodexHandoffTask":
        return cls(**data)


@dataclass
class PatchArtifact:
    patch_run_id: str
    source_task_id: str | None
    created_at: str
    git_branch: str | None
    git_status: str | None
    diff_path: str | None
    summary_path: str | None
    tests_path: str | None
    files_changed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    project: str | None = None
    skillpack: str | None = None
    repository_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatchArtifact":
        return cls(**data)


@dataclass
class PatchReviewFinding:
    finding_type: str
    severity: str
    message: str
    file_path: str | None = None
    evidence: str | None = None

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"Invalid severity: {self.severity}")
        self.message = redact_value(self.message)
        self.evidence = redact_value(self.evidence)


@dataclass
class PatchReview:
    patch_run_id: str
    status: str
    risk_level: str
    findings: list[PatchReviewFinding] = field(default_factory=list)
    blocked: bool = False
    requires_human_review: bool = True
    recommended_next_actions: list[str] = field(default_factory=list)
    project: str | None = None
    skillpack: str | None = None
    repository_path: str | None = None

    def __post_init__(self) -> None:
        if self.status not in REVIEW_STATUSES:
            raise ValueError(f"Invalid patch review status: {self.status}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatchReview":
        findings = [PatchReviewFinding(**finding) for finding in data.get("findings", [])]
        return cls(
            patch_run_id=data["patch_run_id"],
            status=data["status"],
            risk_level=data["risk_level"],
            findings=findings,
            blocked=bool(data.get("blocked", False)),
            requires_human_review=bool(data.get("requires_human_review", True)),
            recommended_next_actions=list(data.get("recommended_next_actions", [])),
            project=data.get("project"),
            skillpack=data.get("skillpack"),
            repository_path=data.get("repository_path"),
        )
