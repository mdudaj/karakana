"""OpenAI provider adapter."""

from __future__ import annotations

import os

from karakana.models.base import ModelProvider
from karakana.models.errors import ModelProviderNotConfigured
from karakana.models.providers.http import chat_payload, parse_openai_compatible_response, post_json
from karakana.models.schemas import ModelRequest, ModelResponse


class OpenAIProvider(ModelProvider):
    name = "openai"

    def __init__(self, name: str | None = None) -> None:
        if name:
            self.name = name
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.endpoint = os.environ.get("OPENAI_ENDPOINT", "https://api.openai.com/v1/chat/completions")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.validate_request(request)
        if not self.is_configured():
            raise ModelProviderNotConfigured("OPENAI_API_KEY is required for OpenAI live calls")
        raw = post_json(
            self.endpoint,
            chat_payload(request),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        content, usage, finish_reason = parse_openai_compatible_response(self.name, request.model, raw)
        return ModelResponse(provider=self.name, model=request.model, content=content, usage=usage, raw=raw, finish_reason=finish_reason)

    def redact_config(self) -> dict:
        return {"provider": self.name, "configured": self.is_configured(), "endpoint": self.endpoint}
