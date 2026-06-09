"""Schemas for model response review."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

REVIEW_STATUSES = {"passed", "warning", "blocked", "error"}
REVIEW_SEVERITIES = {"info", "low", "medium", "high", "critical"}


@dataclass
class ResponseReviewFinding:
    finding_type: str
    severity: str
    message: str
    evidence: str | None = None

    def __post_init__(self) -> None:
        if self.severity not in REVIEW_SEVERITIES:
            raise ValueError(f"Invalid review severity: {self.severity}")


@dataclass
class ResponseReview:
    status: str
    findings: list[ResponseReviewFinding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blocked: bool = False
    requires_human_review: bool = True

    def __post_init__(self) -> None:
        if self.status not in REVIEW_STATUSES:
            raise ValueError(f"Invalid review status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ResponseReview":
        return cls(
            status=data["status"],
            findings=[ResponseReviewFinding(**finding) for finding in data.get("findings", [])],
            warnings=list(data.get("warnings", [])),
            blocked=bool(data.get("blocked", False)),
            requires_human_review=bool(data.get("requires_human_review", True)),
        )
