"""Safety checks for live model calls."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

MAX_PROMPT_SIZE = 200000
SECRET_TERMS = (
    "token",
    "secret",
    "password",
    "api_key",
    "apikey",
    "authorization",
    "bearer",
    "private_key",
    "client_secret",
    "access_key",
    "refresh_token",
)


@dataclass(frozen=True)
class ModelCallCheck:
    name: str
    passed: bool
    message: str


def validate_model_call(
    explicit_live: bool,
    provider_configured: bool,
    provider_known: bool,
    prompt: str,
    model: str,
    output_dir: Path | None = None,
    repo_root: Path | None = None,
) -> list[ModelCallCheck]:
    lowered = prompt.lower()
    checks = [
        ModelCallCheck("explicit_live_flag_present", explicit_live, "Live model calls require --live."),
        ModelCallCheck("provider_known", provider_known, "Provider is unknown."),
        ModelCallCheck("provider_configured", provider_configured, "Provider is not configured."),
        ModelCallCheck("model_not_empty", bool(model.strip()), "Model must not be empty."),
        ModelCallCheck("prompt_not_empty", bool(prompt.strip()), "Prompt must not be empty."),
        ModelCallCheck("prompt_size_reasonable", len(prompt) <= MAX_PROMPT_SIZE, "Prompt is too large."),
        ModelCallCheck("prompt_redacted", not _has_secret_like_value(prompt), "Prompt appears to contain secret-like content."),
        ModelCallCheck(
            "no_raw_secret_patterns",
            "github_token=" not in lowered and "gh_token=" not in lowered and "openai_api_key=" not in lowered and "bearer " not in lowered,
            "Prompt appears to contain raw credential content.",
        ),
    ]
    if output_dir is not None and repo_root is not None:
        checks.append(ModelCallCheck("output_dir_safe", _output_dir_safe(output_dir, repo_root), "Output directory must be under .karakana/."))
    return checks


def failed_model_checks(checks: list[ModelCallCheck]) -> list[ModelCallCheck]:
    return [check for check in checks if not check.passed]


def _has_secret_like_value(prompt: str) -> bool:
    for term in SECRET_TERMS:
        if re.search(rf"{re.escape(term)}\s*[:=]\s*\S+", prompt, flags=re.IGNORECASE):
            return True
    return False


def _output_dir_safe(output_dir: Path, repo_root: Path) -> bool:
    try:
        resolved = output_dir.resolve()
        karakana_root = (repo_root / ".karakana").resolve()
        return resolved == karakana_root or resolved.is_relative_to(karakana_root)
    except OSError:
        return False
