"""Provider/model routing map."""

from __future__ import annotations

DEFAULT_MODEL_ROUTING = {
    "planning": {"provider": "github", "model": "gpt-5-mini"},
    "architecture_review": {"provider": "github", "model": "gpt-5-mini"},
    "reflection": {"provider": "github", "model": "gpt-5-mini"},
    "skill_design": {"provider": "github", "model": "gpt-5-mini"},
    "documentation": {"provider": "github", "model": "claude-haiku-4.5"},
    "changelog": {"provider": "github", "model": "claude-haiku-4.5"},
    "simple_summary": {"provider": "github", "model": "claude-haiku-4.5"},
    "issue_triage": {"provider": "github", "model": "gpt-5-mini"},
    "pr_review": {"provider": "openai", "model": "gpt-5.5-codex"},
    "ci_failure_analysis": {"provider": "openai", "model": "gpt-5.5-codex"},
    "code_implementation": {"provider": "openai", "model": "gpt-5.5-codex"},
    "refactoring": {"provider": "openai", "model": "gpt-5.5-codex"},
    "ci_repair": {"provider": "openai", "model": "gpt-5.5-codex"},
    "deep_pr_review": {"provider": "openai", "model": "gpt-5.5-codex"},
}


def route_model(task_type: str, provider: str | None = None, model: str | None = None) -> dict:
    route = DEFAULT_MODEL_ROUTING.get(task_type, {"provider": "mock", "model": "mock-model"}).copy()
    if provider:
        route["provider"] = provider
    if model:
        route["model"] = model
    return route
