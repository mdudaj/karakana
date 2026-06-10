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
    "code_implementation": "gpt-5.4-mini",
    "routine_code_implementation": "gpt-5.4-mini",
    "test_generation": "gpt-5.4-mini",
    "refactoring": "gpt-5.4",
    "ci_repair": "gpt-5.4",
    "deep_pr_review": "gpt-5.4",
    "migration_review": "gpt-5.5",
    "high_risk_code_review": "gpt-5.5",
    "security_or_auth_change": "gpt-5.5",
    "payment_or_billing_logic": "gpt-5.5",
    "database_or_index_migration": "gpt-5.5",
    "viewflow_process_state_change": "gpt-5.5",
}


def select_model(task_type: str) -> str:
    """Return the configured model name for a task type."""
    return DEFAULT_MODEL_ROUTING.get(task_type, "gpt-5-mini")
