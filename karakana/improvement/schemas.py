"""Schemas for deterministic self-improvement proposals."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from karakana.traces.schemas import redact_value

PROPOSAL_STATUSES = {"draft", "ready_for_review", "rejected", "accepted", "superseded"}
CHANGE_TYPES = {
    "memory_update",
    "skill_update",
    "prompt_update",
    "eval_update",
    "doc_update",
    "config_update",
    "workflow_update",
}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass(frozen=True)
class EvidenceRef:
    run_id: str
    artifact_path: str | None = None
    summary: str | None = None


@dataclass
class ProposedChange:
    target_path: str
    change_type: str
    title: str
    rationale: str
    proposed_content: str | None = None
    evidence: list[EvidenceRef] = field(default_factory=list)
    risk_level: str = "low"
    requires_human_review: bool = True

    def __post_init__(self) -> None:
        if self.change_type not in CHANGE_TYPES:
            raise ValueError(f"Invalid change type: {self.change_type}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")
        self.proposed_content = redact_value(self.proposed_content)


@dataclass
class ImprovementProposal:
    proposal_id: str
    project: str | None
    status: str
    created_at: str
    source_run_ids: list[str]
    summary: str
    changes: list[ProposedChange] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in PROPOSAL_STATUSES:
            raise ValueError(f"Invalid proposal status: {self.status}")
        self.summary = redact_value(self.summary)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImprovementProposal":
        changes = []
        for change in data.get("changes", []):
            evidence = [EvidenceRef(**item) for item in change.get("evidence", [])]
            changes.append(
                ProposedChange(
                    target_path=change["target_path"],
                    change_type=change["change_type"],
                    title=change["title"],
                    rationale=change["rationale"],
                    proposed_content=change.get("proposed_content"),
                    evidence=evidence,
                    risk_level=change.get("risk_level", "low"),
                    requires_human_review=change.get("requires_human_review", True),
                )
            )
        return cls(
            proposal_id=data["proposal_id"],
            project=data.get("project"),
            status=data["status"],
            created_at=data["created_at"],
            source_run_ids=data.get("source_run_ids", []),
            summary=data["summary"],
            changes=changes,
            warnings=data.get("warnings", []),
            next_actions=data.get("next_actions", []),
        )


@dataclass(frozen=True)
class AnalysisFinding:
    finding_type: str
    title: str
    description: str
    evidence: list[EvidenceRef]
    suggested_change_type: str
    suggested_target_path: str | None = None
    risk_level: str = "low"


@dataclass(frozen=True)
class AnalysisResult:
    project: str | None
    source_run_ids: list[str]
    findings: list[AnalysisFinding]
    warnings: list[str] = field(default_factory=list)
