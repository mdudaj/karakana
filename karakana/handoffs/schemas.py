"""Schemas for durable session handoff artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.handoffs.redaction import redact_handoff_text
from karakana.traces.schemas import redact_value


@dataclass
class HandoffArtifact:
    handoff_id: str
    created_at: str
    updated_at: str
    workspace: str | None
    project: str
    skillpack: str
    current_milestone: str
    purpose: str
    source_artifacts: list[str] = field(default_factory=list)
    state_summary: str = ""
    decisions: list[str] = field(default_factory=list)
    open_findings: list[str] = field(default_factory=list)
    inspect_first: list[str] = field(default_factory=list)
    do_not_reread: list[str] = field(default_factory=list)
    reference_artifacts: list[str] = field(default_factory=list)
    suggested_skills: list[str] = field(default_factory=list)
    exact_next_action: str = ""
    safety_constraints: list[str] = field(default_factory=list)
    return_handoff_expected: bool = True
    staleness_notes: list[str] = field(default_factory=list)
    notes_for_fresh_agent: list[str] = field(default_factory=list)
    recovered: bool = False
    previous_handoff_id: str | None = None
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.current_milestone = redact_handoff_text(self.current_milestone)
        self.purpose = redact_handoff_text(self.purpose)
        self.state_summary = redact_handoff_text(self.state_summary)
        self.exact_next_action = redact_handoff_text(self.exact_next_action)
        for name in (
            "source_artifacts", "decisions", "open_findings", "inspect_first", "do_not_reread",
            "reference_artifacts", "suggested_skills", "safety_constraints", "staleness_notes",
            "notes_for_fresh_agent", "warnings",
        ):
            setattr(self, name, [redact_handoff_text(item) for item in getattr(self, name)])

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HandoffArtifact":
        return cls(**data)


@dataclass(frozen=True)
class HandoffDoctorReport:
    project: str
    handoff_id: str | None
    status: str
    checks: dict[str, bool]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))
