"""Schemas for deterministic Karakana work protocols."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

WORK_CATEGORIES = {
    "requirements",
    "research",
    "architecture",
    "implementation",
    "test_eval",
    "documentation",
    "assessment",
    "memory",
    "skill",
    "model_routing",
    "safety",
    "migration",
    "release",
    "github_ci",
    "frontend",
}

WORK_ROLES = {
    "requester",
    "planner",
    "researcher",
    "implementer",
    "reviewer",
    "tester",
    "safety_reviewer",
    "release_operator",
    "memory_curator",
}

ACTION_KINDS = {
    "inspect",
    "classify",
    "plan",
    "modify",
    "verify",
    "review",
    "publish",
    "handoff",
}

RISK_LEVELS = {"low", "medium", "high", "critical"}

ARTIFACT_KINDS = {
    "acceptance_criteria",
    "accessibility_checklist",
    "adr",
    "approval_record",
    "change_summary",
    "definition_of_done",
    "migration_plan",
    "requirements_note",
    "rollback_plan",
    "schema_contract",
    "screenshot_or_render_evidence",
    "safety_review",
    "task_classification",
    "test_or_eval_rationale",
    "threat_or_abuse_case_note",
    "trace",
    "user_story",
    "ux_description",
    "verification_summary",
    "handoff",
}

CONDITION_KEYS = {
    "behavior_change",
    "ux_change",
    "architecture_change",
    "data_or_migration_change",
    "safety_or_permission_change",
    "risk_at_least",
}


@dataclass
class ProtocolArtifactRule:
    kind: str
    description: str = ""
    condition: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in ARTIFACT_KINDS:
            raise ValueError(f"Invalid protocol artifact kind: {self.kind}")
        for key in self.condition:
            if key not in CONDITION_KEYS:
                raise ValueError(f"Invalid protocol artifact condition: {key}")
        risk = self.condition.get("risk_at_least")
        if risk and risk not in RISK_LEVELS:
            raise ValueError(f"Invalid protocol artifact risk condition: {risk}")


@dataclass
class ProtocolStep:
    step_id: str
    action: str
    instruction: str
    required: bool = True

    def __post_init__(self) -> None:
        if self.action not in ACTION_KINDS:
            raise ValueError(f"Invalid protocol action: {self.action}")


@dataclass
class WorkProtocol:
    protocol_id: str
    name: str
    version: str
    category: str
    roles: list[str]
    risk_floor: str
    summary: str
    standards: list[str] = field(default_factory=list)
    required_inputs: list[str] = field(default_factory=list)
    steps: list[ProtocolStep] = field(default_factory=list)
    artifacts: list[ProtocolArtifactRule] = field(default_factory=list)
    approval_gates: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    blocked_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    path: str | None = None

    def __post_init__(self) -> None:
        if self.category not in WORK_CATEGORIES:
            raise ValueError(f"Invalid protocol category: {self.category}")
        if self.risk_floor not in RISK_LEVELS:
            raise ValueError(f"Invalid protocol risk floor: {self.risk_floor}")
        invalid_roles = [role for role in self.roles if role not in WORK_ROLES]
        if invalid_roles:
            raise ValueError(f"Invalid protocol roles: {', '.join(invalid_roles)}")

    def required_artifacts_for(self, conditions: dict[str, Any] | None = None) -> list[ProtocolArtifactRule]:
        conditions = conditions or {}
        required = []
        seen = set()
        for artifact in self.artifacts:
            if artifact.kind in seen or not artifact_required(artifact, conditions):
                continue
            required.append(artifact)
            seen.add(artifact.kind)
        return required

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProtocolValidationResult:
    protocol_id: str
    path: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def artifact_required(artifact: ProtocolArtifactRule, conditions: dict[str, Any]) -> bool:
    if not artifact.condition:
        return True
    for key, expected in artifact.condition.items():
        if key == "risk_at_least":
            if _risk_rank(str(conditions.get("risk_level", "low"))) < _risk_rank(str(expected)):
                return False
            continue
        if bool(conditions.get(key)) != bool(expected):
            return False
    return True


def _risk_rank(risk: str) -> int:
    order = ["low", "medium", "high", "critical"]
    if risk not in order:
        raise ValueError(f"Invalid risk level: {risk}")
    return order.index(risk)
