"""Controlled model execution service."""

from __future__ import annotations

import json
from pathlib import Path
import secrets
from datetime import datetime, timezone

from karakana.models.errors import ModelProviderError
from karakana.models.registry import default_registry
from karakana.models.review.report import write_review_artifacts
from karakana.models.review.reviewer import review_response
from karakana.models.schemas import ModelResponse
from karakana.safety.model_calls import failed_model_checks, validate_model_call
from karakana.traces.schemas import redact_value


class ModelExecutor:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def execute_prompt(
        self,
        prompt: str,
        provider: str,
        model: str,
        live: bool = False,
        task_type: str | None = None,
        project: str | None = None,
        skill: str | None = None,
        output_dir: Path | None = None,
        metadata: dict | None = None,
        expected: str = "generic",
        strict_review: bool = False,
    ) -> ModelResponse | None:
        artifacts_dir = self._resolve_output_dir(output_dir)
        registry = default_registry()
        try:
            provider_impl = registry.get(provider)
            provider_known = True
        except ModelProviderError:
            provider_impl = None
            provider_known = False
        provider_configured = bool(provider_impl and provider_impl.is_configured())
        checks = validate_model_call(live, provider_configured, provider_known, prompt, model, artifacts_dir, self.repo_root)
        failures = failed_model_checks(checks)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        (artifacts_dir / "prompt.md").write_text(redact_value(prompt), encoding="utf-8")
        if not live:
            return None
        if failures:
            raise ModelProviderError("; ".join(check.message for check in failures))
        request = provider_impl.build_request(
            prompt,
            model,
            task_type=task_type,
            project=project,
            skill=skill,
            metadata=metadata or {},
        )
        (artifacts_dir / "model-request.json").write_text(
            json.dumps(request.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        response = provider_impl.complete(request)
        (artifacts_dir / "model-response.md").write_text(redact_value(response.content) + "\n", encoding="utf-8")
        (artifacts_dir / "model-response.json").write_text(
            json.dumps(response.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        review = review_response(response.content, expected=expected, strict=strict_review)
        write_review_artifacts(review, artifacts_dir)
        return response

    def _resolve_output_dir(self, output_dir: Path | None) -> Path:
        if output_dir is not None:
            path = output_dir if output_dir.is_absolute() else self.repo_root / output_dir
        else:
            path = self.repo_root / ".karakana" / "model-runs" / generate_model_run_id()
        return path


def generate_model_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-model-{secrets.token_hex(3)}"
