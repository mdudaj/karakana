"""Schemas and redaction helpers for Karakana run traces."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any

TRACE_STATUSES = {"started", "success", "failed", "cancelled", "partial"}
SAFETY_CHECK_STATUSES = {"passed", "warning", "failed", "skipped"}
SECRET_PATTERNS = (
    "token",
    "secret",
    "password",
    "api_key",
    "apikey",
    "authorization",
    "bearer",
    "private_key",
    "client_secret",
)


@dataclass
class TraceArtifact:
    path: str
    kind: str
    description: str | None = None


@dataclass
class SafetyCheck:
    name: str
    status: str
    message: str | None = None

    def __post_init__(self) -> None:
        if self.status not in SAFETY_CHECK_STATUSES:
            raise ValueError(f"Invalid safety check status: {self.status}")


@dataclass
class RunTrace:
    run_id: str
    command: str
    project: str | None
    skill: str | None
    task: str | None
    task_type: str | None
    selected_model: str | None
    status: str
    started_at: str
    finished_at: str | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    artifacts: list[TraceArtifact] = field(default_factory=list)
    safety_checks: list[SafetyCheck] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in TRACE_STATUSES:
            raise ValueError(f"Invalid trace status: {self.status}")
        self.inputs = redact_value(self.inputs)
        self.outputs = redact_value(self.outputs)

    def finish(self, status: str) -> None:
        if status not in TRACE_STATUSES:
            raise ValueError(f"Invalid trace status: {status}")
        self.status = status
        self.finished_at = now_utc()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["inputs"] = redact_value(data["inputs"])
        data["outputs"] = redact_value(data["outputs"])
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunTrace":
        artifacts = [TraceArtifact(**artifact) for artifact in data.get("artifacts", [])]
        safety_checks = [SafetyCheck(**check) for check in data.get("safety_checks", [])]
        return cls(
            run_id=data["run_id"],
            command=data["command"],
            project=data.get("project"),
            skill=data.get("skill"),
            task=data.get("task"),
            task_type=data.get("task_type"),
            selected_model=data.get("selected_model"),
            status=data["status"],
            started_at=data["started_at"],
            finished_at=data.get("finished_at"),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            artifacts=artifacts,
            safety_checks=safety_checks,
            warnings=data.get("warnings", []),
            errors=data.get("errors", []),
            next_actions=data.get("next_actions", []),
        )


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact_value(value: Any, key: str | None = None) -> Any:
    if key and _is_secret_key(key):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(item_key): redact_value(item_value, str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return [redact_value(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, str):
        return _redact_secret_like_string(value)
    return value


def _is_secret_key(key: str) -> bool:
    lowered = key.lower()
    if lowered in {"token_usage", "input_tokens", "output_tokens", "total_tokens"}:
        return False
    return any(pattern in lowered for pattern in SECRET_PATTERNS)


def _redact_secret_like_string(value: str) -> str:
    redacted = re.sub(
        r"\b(token|secret|password|api_key|apikey|authorization|private_key|client_secret|access_key|refresh_token)\s*[:=]\s*\S+",
        r"\1=[REDACTED]",
        value,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", redacted, flags=re.IGNORECASE)
    return redacted
