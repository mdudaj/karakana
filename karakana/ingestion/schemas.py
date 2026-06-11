"""Schemas for reviewable ingestion artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

SOURCE_TYPES = {"file", "trace", "action", "patch_review", "proposal", "codex_task", "test_run", "github_event", "manual_note", "scan"}
CANDIDATE_TYPES = {"ubongo_memory", "skill_update", "eval_update", "prompt_update", "safety_update", "project_convention", "behavior_update", "manual_review"}
BUNDLE_STATUSES = {"draft", "ready_for_review", "accepted", "rejected", "partially_applied", "applied", "blocked", "error"}
CANDIDATE_STATUSES = {"draft", "ready_for_review", "accepted", "rejected", "applied", "superseded", "blocked"}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class IngestionSource:
    source_type: str
    source_id: str | None = None
    path: str | None = None
    project: str | None = None
    skillpack: str | None = None
    title: str | None = None
    content_hash: str | None = None
    collected_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.source_type not in SOURCE_TYPES:
            raise ValueError(f"Invalid source type: {self.source_type}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ClassificationResult:
    category: str
    confidence: float
    rationale: str
    suggested_targets: list[str] = field(default_factory=list)
    risk_level: str = "low"
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IngestionCandidate:
    candidate_id: str
    candidate_type: str
    title: str
    summary: str
    target_path: str | None = None
    proposed_content: str | None = None
    evidence: list[str] = field(default_factory=list)
    classification: ClassificationResult | None = None
    risk_level: str = "low"
    status: str = "draft"
    requires_human_review: bool = True
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.candidate_type not in CANDIDATE_TYPES:
            raise ValueError(f"Invalid candidate type: {self.candidate_type}")
        if self.status not in CANDIDATE_STATUSES:
            raise ValueError(f"Invalid candidate status: {self.status}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.classification:
            data["classification"] = self.classification.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IngestionCandidate":
        classification = data.get("classification")
        return cls(**{**data, "classification": ClassificationResult(**classification) if classification else None})


@dataclass
class IngestionBundle:
    ingest_id: str
    project: str | None
    skillpack: str | None
    status: str
    created_at: str
    sources: list[IngestionSource] = field(default_factory=list)
    candidates: list[IngestionCandidate] = field(default_factory=list)
    redaction_applied: bool = False
    warnings: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in BUNDLE_STATUSES:
            raise ValueError(f"Invalid bundle status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "ingest_id": self.ingest_id,
            "project": self.project,
            "skillpack": self.skillpack,
            "status": self.status,
            "created_at": self.created_at,
            "sources": [source.to_dict() for source in self.sources],
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "redaction_applied": self.redaction_applied,
            "warnings": self.warnings,
            "next_actions": self.next_actions,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IngestionBundle":
        return cls(
            ingest_id=data["ingest_id"],
            project=data.get("project"),
            skillpack=data.get("skillpack"),
            status=data["status"],
            created_at=data["created_at"],
            sources=[IngestionSource(**source) for source in data.get("sources", [])],
            candidates=[IngestionCandidate.from_dict(candidate) for candidate in data.get("candidates", [])],
            redaction_applied=bool(data.get("redaction_applied", False)),
            warnings=list(data.get("warnings", [])),
            next_actions=list(data.get("next_actions", [])),
        )
