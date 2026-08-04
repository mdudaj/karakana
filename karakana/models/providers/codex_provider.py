"""Codex CLI provider adapter."""

from __future__ import annotations

import os
import shutil

from karakana.models.base import ModelProvider
from karakana.models.errors import ModelProviderError
from karakana.models.router import CODEX_5_6_FAMILY, FRONTIER_CODEX_MODEL
from karakana.models.schemas import ModelRequest, ModelResponse


class CodexProvider(ModelProvider):
    name = "openai_codex"

    def __init__(self) -> None:
        self.executable = os.environ.get("CODEX_BIN") or shutil.which("codex")
        self.model = os.environ.get("OPENAI_CODEX_MODEL", "gpt-5.4-mini")

    def is_configured(self) -> bool:
        return bool(self.executable)

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.validate_request(request)
        raise ModelProviderError("openai_codex is a Codex CLI provider; use `karakana codex start` for live Codex execution.")

    def redact_config(self) -> dict:
        return {
            "provider": self.name,
            "configured": self.is_configured(),
            "executable": self.executable,
            "model": self.model,
            "frontier_default": FRONTIER_CODEX_MODEL,
            "available_frontier_models": sorted(CODEX_5_6_FAMILY),
        }
