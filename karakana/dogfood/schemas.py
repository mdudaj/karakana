"""Schemas for Karakana dogfood runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

COMMAND_STATUSES = {"planned", "skipped", "passed", "warning", "failed", "error"}
FINDING_TYPES = {"broken_command", "ux_friction", "missing_eval", "missing_doc", "weak_doc", "safety_gap", "routing_gap", "trace_gap", "artifact_gap", "overlap_or_duplicate", "slow_or_noisy_command", "manual_review"}
SEVERITIES = {"low", "medium", "high", "critical"}
BACKLOG_TYPES = {"bug", "ux_improvement", "doc_update", "eval_update", "safety_update", "skill_update", "prompt_update", "test_update", "release_blocker", "manual_review"}
PRIORITIES = {"p0", "p1", "p2", "p3"}
DOGFOOD_STATUSES = {"draft", "running", "completed", "completed_with_warnings", "failed", "blocked", "error"}


@dataclass
class DogfoodCommandResult:
    command_id: str
    command: str
    status: str
    exit_code: int | None = None
    artifact_paths: list[str] = field(default_factory=list)
    stdout_excerpt: str | None = None
    stderr_excerpt: str | None = None
    duration_seconds: float | None = None
    noise_score: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in COMMAND_STATUSES:
            raise ValueError(f"Invalid command status: {self.status}")
        self.stdout_excerpt = redact_value(self.stdout_excerpt)
        self.stderr_excerpt = redact_value(self.stderr_excerpt)
        self.warnings = redact_value(self.warnings)
        self.errors = redact_value(self.errors)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DogfoodCommandResult":
        return cls(**data)


@dataclass
class DogfoodFinding:
    finding_id: str
    finding_type: str
    title: str
    summary: str
    severity: str
    affected_command: str | None = None
    affected_area: str | None = None
    evidence: list[str] = field(default_factory=list)
    recommended_action: str | None = None
    suggested_target: str | None = None
    suggested_skill: str | None = None
    suggested_eval: str | None = None
    risk_level: str = "low"
    requires_human_review: bool = True

    def __post_init__(self) -> None:
        if self.finding_type not in FINDING_TYPES:
            raise ValueError(f"Invalid finding type: {self.finding_type}")
        if self.severity not in SEVERITIES:
            raise ValueError(f"Invalid severity: {self.severity}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DogfoodFinding":
        return cls(**data)


@dataclass
class DogfoodBacklogItem:
    item_id: str
    title: str
    item_type: str
    summary: str
    priority: str
    source_finding_ids: list[str] = field(default_factory=list)
    suggested_issue_title: str | None = None
    suggested_skills: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    recommended_model_route: dict[str, Any] = field(default_factory=dict)
    risk_level: str = "low"

    def __post_init__(self) -> None:
        if self.item_type not in BACKLOG_TYPES:
            raise ValueError(f"Invalid backlog item type: {self.item_type}")
        if self.priority not in PRIORITIES:
            raise ValueError(f"Invalid priority: {self.priority}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DogfoodBacklogItem":
        return cls(**data)


@dataclass
class DogfoodRun:
    dogfood_id: str
    project: str
    skillpack: str | None
    status: str
    created_at: str
    command_results: list[DogfoodCommandResult] = field(default_factory=list)
    findings: list[DogfoodFinding] = field(default_factory=list)
    backlog: list[DogfoodBacklogItem] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in DOGFOOD_STATUSES:
            raise ValueError(f"Invalid dogfood status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DogfoodRun":
        return cls(
            dogfood_id=data["dogfood_id"],
            project=data["project"],
            skillpack=data.get("skillpack"),
            status=data["status"],
            created_at=data["created_at"],
            command_results=[DogfoodCommandResult.from_dict(item) for item in data.get("command_results", [])],
            findings=[DogfoodFinding.from_dict(item) for item in data.get("findings", [])],
            backlog=[DogfoodBacklogItem.from_dict(item) for item in data.get("backlog", [])],
            warnings=list(data.get("warnings", [])),
            errors=list(data.get("errors", [])),
            next_actions=list(data.get("next_actions", [])),
        )
