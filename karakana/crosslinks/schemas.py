"""Schemas for cross-project knowledge links."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

BUNDLE_STATUSES = {"draft", "ready_for_review", "reviewed", "partially_applied", "applied", "blocked", "error"}
PATTERN_TYPES = {"shared_workflow", "shared_risk", "shared_skill_need", "shared_eval_need", "shared_prompt_need", "shared_safety_rule", "shared_project_convention", "duplicated_memory", "conflicting_memory", "candidate_skillpack_update", "manual_review"}
PROPOSAL_TYPES = {"global_ubongo_update", "shared_skill_update", "shared_eval_update", "shared_prompt_update", "skillpack_update", "cross_project_issue_draft", "project_specific_follow_up", "manual_review"}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class CrosslinkProjectRef:
    project_id: str
    workspace: str | None = None
    path: str | None = None
    skillpack: str | None = None
    memory_path: str | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _redact_crosslink_text(redact_value(asdict(self)))


@dataclass
class CrosslinkEvidence:
    project_id: str
    source_type: str
    source_id: str | None = None
    path: str | None = None
    summary: str | None = None
    risk_level: str = "low"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")
        self.summary = _redact_crosslink_text(redact_value(self.summary))
        self.metadata = redact_value(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class CrosslinkPattern:
    pattern_id: str
    pattern_type: str
    title: str
    summary: str
    projects: list[str] = field(default_factory=list)
    evidence: list[CrosslinkEvidence] = field(default_factory=list)
    suggested_targets: list[str] = field(default_factory=list)
    risk_level: str = "low"
    confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.pattern_type not in PATTERN_TYPES:
            raise ValueError(f"Invalid pattern type: {self.pattern_type}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrosslinkPattern":
        payload = dict(data)
        payload["evidence"] = [CrosslinkEvidence(**item) for item in payload.get("evidence", [])]
        return cls(**payload)


@dataclass
class CrosslinkProposal:
    proposal_id: str
    proposal_type: str
    title: str
    summary: str
    target_path: str | None = None
    proposed_content: str | None = None
    affected_projects: list[str] = field(default_factory=list)
    source_patterns: list[str] = field(default_factory=list)
    risk_level: str = "low"
    requires_human_review: bool = True
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.proposal_type not in PROPOSAL_TYPES:
            raise ValueError(f"Invalid proposal type: {self.proposal_type}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")
        self.proposed_content = _redact_crosslink_text(redact_value(self.proposed_content))

    def to_dict(self) -> dict[str, Any]:
        return _redact_crosslink_text(redact_value(asdict(self)))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrosslinkProposal":
        return cls(**data)


@dataclass
class CrosslinkBundle:
    crosslink_id: str
    workspace: str
    status: str
    created_at: str
    projects: list[CrosslinkProjectRef] = field(default_factory=list)
    patterns: list[CrosslinkPattern] = field(default_factory=list)
    proposals: list[CrosslinkProposal] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in BUNDLE_STATUSES:
            raise ValueError(f"Invalid crosslink status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrosslinkBundle":
        return cls(
            crosslink_id=data["crosslink_id"],
            workspace=data["workspace"],
            status=data["status"],
            created_at=data["created_at"],
            projects=[CrosslinkProjectRef(**item) for item in data.get("projects", [])],
            patterns=[CrosslinkPattern.from_dict(item) for item in data.get("patterns", [])],
            proposals=[CrosslinkProposal.from_dict(item) for item in data.get("proposals", [])],
            warnings=list(data.get("warnings", [])),
            next_actions=list(data.get("next_actions", [])),
        )


def _redact_crosslink_text(value: Any) -> Any:
    """Redact secret environment names as well as secret values in crosslink artifacts."""
    if isinstance(value, dict):
        return {key: _redact_crosslink_text(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_crosslink_text(item) for item in value]
    if isinstance(value, str):
        return re.sub(r"\b(GITHUB_TOKEN|GH_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY)\b", "[REDACTED_SECRET_NAME]", value)
    return value
