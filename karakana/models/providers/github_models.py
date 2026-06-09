"""GitHub Models provider adapter."""

from __future__ import annotations

import os

from karakana.models.base import ModelProvider
from karakana.models.errors import ModelProviderNotConfigured
from karakana.models.providers.http import chat_payload, parse_openai_compatible_response, post_json
from karakana.models.schemas import ModelRequest, ModelResponse


class GitHubModelsProvider(ModelProvider):
    name = "github"

    def __init__(self) -> None:
        self.token = os.environ.get("GITHUB_TOKEN")
        self.endpoint = os.environ.get("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com")

    def is_configured(self) -> bool:
        return bool(self.token)

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.validate_request(request)
        if not self.is_configured():
            raise ModelProviderNotConfigured("GITHUB_TOKEN is required for GitHub Models live calls")
        raw = post_json(
            self.endpoint.rstrip("/") + "/chat/completions",
            chat_payload(request),
            headers={"Authorization": f"Bearer {self.token}"},
        )
        content, usage, finish_reason = parse_openai_compatible_response(self.name, request.model, raw)
        return ModelResponse(provider=self.name, model=request.model, content=content, usage=usage, raw=raw, finish_reason=finish_reason)

    def redact_config(self) -> dict:
        return {"provider": self.name, "configured": self.is_configured(), "endpoint": self.endpoint}
