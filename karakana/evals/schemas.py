"""Schemas for deterministic Karakana evaluation cases and reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

CASE_RESULT_STATUSES = {"passed", "failed", "warning", "skipped", "error"}
RUN_STATUSES = {"passed", "failed", "partial", "error"}


@dataclass
class EvalInput:
    task: str
    project: str | None = None
    skill: str | None = None
    task_type: str | None = None
    prompt_file: str | None = None
    context_files: list[str] = field(default_factory=list)


@dataclass
class EvalExpectation:
    must_include: list[str] = field(default_factory=list)
    must_not_include: list[str] = field(default_factory=list)
    required_sections: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)
    max_length: int | None = None
    min_length: int | None = None
    expected_model: str | None = None
    expected_provider: str | None = None
    safety_flags: list[str] = field(default_factory=list)


@dataclass
class EvalCase:
    id: str
    name: str
    description: str
    suite: str
    input: EvalInput
    expectations: EvalExpectation
    tags: list[str] = field(default_factory=list)
    risk_level: str = "low"
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class EvalCaseResult:
    case_id: str
    status: str
    score: float
    passed_checks: list[str] = field(default_factory=list)
    failed_checks: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    output_excerpt: str | None = None
    artifacts: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in CASE_RESULT_STATUSES:
            raise ValueError(f"Invalid eval case status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class EvalRunReport:
    eval_run_id: str
    status: str
    started_at: str
    finished_at: str | None
    total_cases: int
    passed: int
    failed: int
    warnings: int
    results: list[EvalCaseResult]

    def __post_init__(self) -> None:
        if self.status not in RUN_STATUSES:
            raise ValueError(f"Invalid eval run status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvalRunReport":
        return cls(
            eval_run_id=data["eval_run_id"],
            status=data["status"],
            started_at=data["started_at"],
            finished_at=data.get("finished_at"),
            total_cases=data["total_cases"],
            passed=data["passed"],
            failed=data["failed"],
            warnings=data["warnings"],
            results=[EvalCaseResult(**result) for result in data.get("results", [])],
        )
