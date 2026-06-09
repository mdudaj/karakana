"""Schemas for provider-neutral model requests and responses."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value

ALLOWED_MESSAGE_ROLES = {"system", "user", "assistant", "tool"}


@dataclass(frozen=True)
class ModelMessage:
    role: str
    content: str


@dataclass
class ModelRequest:
    provider: str
    model: str
    messages: list[ModelMessage]
    task_type: str | None = None
    project: str | None = None
    skill: str | None = None
    temperature: float | None = None
    max_output_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.provider.strip():
            errors.append("Provider must not be empty.")
        if not self.model.strip():
            errors.append("Model must not be empty.")
        if not self.messages:
            errors.append("At least one message is required.")
        for index, message in enumerate(self.messages):
            if message.role not in ALLOWED_MESSAGE_ROLES:
                errors.append(f"Message {index} has unsupported role: {message.role}")
            if not message.content.strip():
                errors.append(f"Message {index} content must not be empty.")
        if self.temperature is not None and not 0 <= self.temperature <= 2:
            errors.append("Temperature must be between 0 and 2.")
        if self.max_output_tokens is not None and self.max_output_tokens <= 0:
            errors.append("max_output_tokens must be positive.")
        return errors


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass
class ModelResponse:
    provider: str
    model: str
    content: str
    usage: TokenUsage | None = None
    raw: dict[str, Any] | None = None
    finish_reason: str | None = None
    cached: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))
