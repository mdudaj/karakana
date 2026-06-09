"""Deterministic model routing for Karakana planning outputs."""

from __future__ import annotations

DEFAULT_MODEL_ROUTING = {
    "planning": "gpt-5-mini",
    "architecture_review": "gpt-5-mini",
    "reflection": "gpt-5-mini",
    "skill_design": "gpt-5-mini",
    "issue_triage": "claude-haiku-4.5",
    "documentation": "claude-haiku-4.5",
    "changelog": "claude-haiku-4.5",
    "simple_summary": "claude-haiku-4.5",
    "code_implementation": "codex-gpt-5.5",
    "refactoring": "codex-gpt-5.5",
    "ci_repair": "codex-gpt-5.5",
    "deep_pr_review": "codex-gpt-5.5",
    "migration_review": "codex-gpt-5.5",
}


def select_model(task_type: str) -> str:
    """Return the configured model name for a task type."""
    return DEFAULT_MODEL_ROUTING.get(task_type, "gpt-5-mini")
