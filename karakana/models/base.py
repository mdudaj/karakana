"""Base model provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from karakana.models.errors import ModelProviderRequestError
from karakana.models.schemas import ModelMessage, ModelRequest, ModelResponse


class ModelProvider(ABC):
    name: str

    @abstractmethod
    def is_configured(self) -> bool:
        ...

    def build_request(self, prompt: str, model: str, **kwargs) -> ModelRequest:
        return ModelRequest(
            provider=self.name,
            model=model,
            messages=[ModelMessage(role="user", content=prompt)],
            task_type=kwargs.get("task_type"),
            project=kwargs.get("project"),
            skill=kwargs.get("skill"),
            temperature=kwargs.get("temperature"),
            max_output_tokens=kwargs.get("max_output_tokens"),
            metadata=kwargs.get("metadata") or {},
        )

    @abstractmethod
    def complete(self, request: ModelRequest) -> ModelResponse:
        ...

    def validate_request(self, request: ModelRequest) -> None:
        errors = request.validate()
        if errors:
            raise ModelProviderRequestError("; ".join(errors))

    def redact_config(self) -> dict:
        return {"provider": self.name, "configured": self.is_configured()}
