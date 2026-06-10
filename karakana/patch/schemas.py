"""Schemas for patch lifecycle artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

GATE_STATUSES = {"passed", "warning", "blocked", "error"}
APPLY_STATUSES = {"dry_run_passed", "applied", "conflict", "blocked", "error"}
COMMIT_STATUSES = {"dry_run", "committed", "blocked", "error"}
RISK_LEVELS = {"low", "medium", "high", "critical"}


@dataclass
class PatchGateResult:
    patch_run_id: str
    status: str
    risk_level: str
    blocked: bool
    checks_passed: list[str] = field(default_factory=list)
    checks_failed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    required_actions: list[str] = field(default_factory=list)
    patch_review_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in GATE_STATUSES:
            raise ValueError(f"Invalid gate status: {self.status}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {self.risk_level}")
        self.metadata = redact_value(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatchGateResult":
        return cls(**data)


@dataclass
class PatchBranchPlan:
    patch_run_id: str
    current_branch: str | None
    proposed_branch: str
    base_branch: str
    can_create: bool
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class PatchApplyResult:
    patch_run_id: str
    status: str
    dry_run: bool
    applied: bool
    files_changed: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in APPLY_STATUSES:
            raise ValueError(f"Invalid apply status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class PatchCommitResult:
    patch_run_id: str
    status: str
    committed: bool
    commit_sha: str | None = None
    message: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in COMMIT_STATUSES:
            raise ValueError(f"Invalid commit status: {self.status}")
        self.message = redact_value(self.message)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))
