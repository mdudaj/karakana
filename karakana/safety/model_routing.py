"""Warnings for cost-aware and risk-aware model routing."""

from __future__ import annotations

LOW_RISK_TASKS = {"documentation", "changelog", "simple_summary", "issue_triage"}
ROUTINE_CODE_TASKS = {"routine_code_implementation", "test_generation", "codex_task_drafting", "code_implementation"}
DEEP_PLANNING_TASKS = {"implementation_planning", "architecture_review", "framework_design", "protocol_workflow_planning", "system_assessment", "skill_design"}
HIGH_RISK_TASKS = {
    "high_risk_planning",
    "model_routing_planning",
    "safety_policy_planning",
    "cross_project_architecture",
    "security_or_auth_change",
    "payment_or_billing_logic",
    "database_or_index_migration",
    "viewflow_process_state_change",
    "high_risk_code_review",
}


def validate_model_route(task_type: str, provider: str, model: str, risk_level: str | None = None) -> list[str]:
    warnings: list[str] = []
    if task_type in LOW_RISK_TASKS and model == "gpt-5.5":
        warnings.append("Low-risk language work should not route to GPT-5.5 by default.")
    if task_type in ROUTINE_CODE_TASKS and model == "gpt-5.5":
        warnings.append("Routine coding should start with GPT-5.4-mini, not GPT-5.5.")
    if task_type in DEEP_PLANNING_TASKS and model in {"claude-haiku-4.5", "gpt-5-mini", "gpt-5.4-mini"}:
        warnings.append("Consequential planning should route to GPT-5.4 by default.")
    if task_type in HIGH_RISK_TASKS and provider == "openai_codex" and model not in {"gpt-5.4", "gpt-5.5"}:
        warnings.append("High-risk auth/payment/migration/process-state tasks should not route below GPT-5.4 without explicit override.")
    if task_type in {"high_risk_planning", "model_routing_planning", "safety_policy_planning", "cross_project_architecture"} and model != "gpt-5.5":
        warnings.append("High-risk planning should route to GPT-5.5 by default.")
    if model == "gpt-5.5" and risk_level not in {"high", "critical"} and task_type not in HIGH_RISK_TASKS:
        warnings.append("GPT-5.5 selection should include a high-risk or stuck-work rationale.")
    return warnings
