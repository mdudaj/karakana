"""Schemas for extracted review-to-action artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

BUNDLE_STATUSES = {"draft", "ready_for_review", "blocked", "published", "partial", "error"}
ACTION_TYPES = {
    "github_issue_draft",
    "codex_task",
    "improvement_proposal",
    "documentation_update",
    "eval_case",
    "implementation_checklist",
    "follow_up_plan",
    "memory_update",
    "skill_update",
    "prompt_update",
    "handoff",
    "manual_review",
}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class ActionSource:
    source_type: str
    path: str | None = None
    run_id: str | None = None
    review_status: str | None = None
    review_path: str | None = None


@dataclass
class StandardsSpecContext:
    standards_summary: str | None = None
    spec_summary: str | None = None
    acceptance_criteria: list[str] = field(default_factory=list)
    standards_risks: list[str] = field(default_factory=list)
    spec_gaps: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.standards_summary = redact_value(self.standards_summary)
        self.spec_summary = redact_value(self.spec_summary)
        self.acceptance_criteria = redact_value(self.acceptance_criteria)
        self.standards_risks = redact_value(self.standards_risks)
        self.spec_gaps = redact_value(self.spec_gaps)


@dataclass
class ExtractedAction:
    action_id: str
    action_type: str
    title: str
    description: str
    target_path: str | None = None
    project: str | None = None
    skill: str | None = None
    suggested_skills: list[str] = field(default_factory=list)
    risk_level: str = "low"
    requires_human_review: bool = True
    requires_explicit_opt_in: bool = True
    suggested_command: str | None = None
    proposed_content: str | None = None
    evidence: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    standards_spec_context: StandardsSpecContext | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.action_type not in ACTION_TYPES:
            raise ValueError(f"Invalid action type: {self.action_type}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")
        self.description = redact_value(self.description)
        self.suggested_skills = redact_value(self.suggested_skills)
        self.proposed_content = redact_value(self.proposed_content)
        self.evidence = redact_value(self.evidence)
        self.metadata = redact_value(self.metadata)


@dataclass
class ActionBundle:
    action_run_id: str
    status: str
    created_at: str
    source: ActionSource
    summary: str
    suggested_skills: list[str] = field(default_factory=list)
    standards_spec_context: StandardsSpecContext | None = None
    actions: list[ExtractedAction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in BUNDLE_STATUSES:
            raise ValueError(f"Invalid action bundle status: {self.status}")
        self.summary = redact_value(self.summary)
        self.suggested_skills = redact_value(self.suggested_skills)
        self.warnings = redact_value(self.warnings)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActionBundle":
        actions = []
        for action in data.get("actions", []):
            action_data = dict(action)
            if action_data.get("standards_spec_context"):
                action_data["standards_spec_context"] = StandardsSpecContext(**action_data["standards_spec_context"])
            actions.append(ExtractedAction(**action_data))
        return cls(
            action_run_id=data["action_run_id"],
            status=data["status"],
            created_at=data["created_at"],
            source=ActionSource(**data["source"]),
            summary=data["summary"],
            suggested_skills=list(data.get("suggested_skills", [])),
            standards_spec_context=(
                StandardsSpecContext(**data["standards_spec_context"])
                if data.get("standards_spec_context")
                else None
            ),
            actions=actions,
            warnings=list(data.get("warnings", [])),
            next_steps=list(data.get("next_steps", [])),
        )
