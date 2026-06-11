"""Schemas for requirements decomposition artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

SOURCE_TYPES = {"action", "ingest", "patch_review", "proposal", "handoff", "file", "note"}
REQUIREMENT_STATUSES = {"draft", "ready_for_review", "approved", "superseded", "published", "blocked", "error"}
READINESS_STATUSES = {"ready", "not_ready", "warning", "blocked", "error"}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class RequirementSource:
    source_type: str
    source_id: str | None = None
    path: str | None = None
    project: str | None = None
    skillpack: str | None = None
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.source_type not in SOURCE_TYPES:
            raise ValueError(f"Invalid requirement source type: {self.source_type}")
        self.metadata = redact_value(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class HarnessSubsystemImpact:
    instructions: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    environment: list[str] = field(default_factory=list)
    state: list[str] = field(default_factory=list)
    feedback: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class StandardsSpecContext:
    standards: list[str] = field(default_factory=list)
    spec: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class RequirementPRD:
    req_id: str
    title: str
    project: str | None
    skillpack: str | None
    status: str
    source: RequirementSource
    context: str
    problem: str
    goal: str
    non_goals: list[str] = field(default_factory=list)
    users_or_actors: list[str] = field(default_factory=list)
    functional_requirements: list[str] = field(default_factory=list)
    non_functional_requirements: list[str] = field(default_factory=list)
    harness_impact: HarnessSubsystemImpact = field(default_factory=HarnessSubsystemImpact)
    standards_spec: StandardsSpecContext = field(default_factory=StandardsSpecContext)
    risks: list[str] = field(default_factory=list)
    safety_constraints: list[str] = field(default_factory=list)
    suggested_skills: list[str] = field(default_factory=list)
    suggested_skillpack: str | None = None
    model_route: dict[str, Any] = field(default_factory=dict)
    test_and_eval_plan: list[str] = field(default_factory=list)
    rollout_or_review_plan: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in REQUIREMENT_STATUSES:
            raise ValueError(f"Invalid requirement status: {self.status}")
        self.context = redact_value(self.context)
        self.problem = redact_value(self.problem)
        self.goal = redact_value(self.goal)
        self.metadata = redact_value(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RequirementPRD":
        payload = dict(data)
        payload["source"] = RequirementSource(**payload["source"])
        payload["harness_impact"] = HarnessSubsystemImpact(**payload.get("harness_impact", {}))
        payload["standards_spec"] = StandardsSpecContext(**payload.get("standards_spec", {}))
        return cls(**payload)


@dataclass
class UserStory:
    story_id: str
    req_id: str
    title: str
    actor: str
    want: str
    outcome: str
    acceptance_criteria: list[str] = field(default_factory=list)
    standards: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    required_skills: list[str] = field(default_factory=list)
    required_tests_or_evals: list[str] = field(default_factory=list)
    definition_of_ready: list[str] = field(default_factory=list)
    definition_of_done: list[str] = field(default_factory=list)
    risk_level: str = "low"

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserStory":
        return cls(**data)


@dataclass
class IssueDraft:
    issue_id: str
    req_id: str
    story_id: str | None
    title: str
    summary: str
    scope: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    implementation_notes: list[str] = field(default_factory=list)
    suggested_skills: list[str] = field(default_factory=list)
    suggested_skillpack: str | None = None
    recommended_model_route: dict[str, Any] = field(default_factory=dict)
    safety_constraints: list[str] = field(default_factory=list)
    tests_or_evals: list[str] = field(default_factory=list)
    definition_of_done: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    risk_level: str = "low"

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IssueDraft":
        return cls(**data)


@dataclass
class ReadinessCheck:
    req_id: str
    status: str
    ready: bool
    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommended_next_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in READINESS_STATUSES:
            raise ValueError(f"Invalid readiness status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReadinessCheck":
        return cls(**data)
