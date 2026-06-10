"""Cost-effective provider/model routing map."""

from __future__ import annotations

MODEL_TIERS = {
    "claude-haiku-4.5": {"cost_tier": "low", "capability_tier": "lightweight_language"},
    "gpt-5-mini": {"cost_tier": "low_to_medium", "capability_tier": "planning_reasoning"},
    "gpt-5.4-mini": {"cost_tier": "low_to_medium", "capability_tier": "routine_coding"},
    "gpt-5.4": {"cost_tier": "medium", "capability_tier": "serious_coding"},
    "gpt-5.5": {"cost_tier": "high", "capability_tier": "principal_engineer"},
    "mock-model": {"cost_tier": "none", "capability_tier": "mock"},
}

DEFAULT_MODEL_ROUTING = {
    "issue_triage": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast, low-cost issue summarization and classification."},
    "documentation": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast documentation and cleanup."},
    "changelog": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast release notes and changelog generation."},
    "simple_summary": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast summary work."},
    "planning": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "General planning and reasoning."},
    "architecture_review": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Architecture reasoning before code execution."},
    "reflection": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Trace review and improvement reasoning."},
    "skill_design": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Skill and prompt design."},
    "action_extraction_review": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Review extracted actions and preserve developer control."},
    "routine_code_implementation": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Cost-effective first pass for simple code edits."},
    "test_generation": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Cost-effective first pass for routine tests."},
    "codex_task_drafting": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Draft implementation prompts and simple coding tasks."},
    "code_implementation": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Cost-effective first pass for routine implementation."},
    "ci_repair": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "CI repair often requires repository reasoning and test iteration."},
    "refactoring": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Serious day-to-day coding and multi-file edits."},
    "deep_pr_review": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Strong code review without defaulting to the most expensive model."},
    "pr_review": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Strong PR review without defaulting to principal-level escalation."},
    "ci_failure_analysis": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "CI failures usually require repository-aware reasoning."},
    "framework_code_implementation": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Invenio, Viewflow, Django, and GePG framework-level work."},
    "high_risk_code_review": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Principal-level review for high-risk changes."},
    "security_or_auth_change": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Authentication, authorization, SSO, OAuth, and secrets require highest scrutiny."},
    "payment_or_billing_logic": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Payment, billing, idempotency, and reconciliation are high-risk."},
    "database_or_index_migration": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Data migrations, OpenSearch index changes, and schema changes are high-risk."},
    "viewflow_process_state_change": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Active workflow/process-state changes can break running business processes."},
    "cross_project_architecture": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Multi-project architectural decisions require highest reasoning depth."},
}


def route_model(task_type: str, provider: str | None = None, model: str | None = None) -> dict:
    route = DEFAULT_MODEL_ROUTING.get(
        task_type,
        {"provider": "mock", "model": "mock-model", "mode": "mock", "rationale": "Unknown task type; use mock dry-run routing."},
    ).copy()
    manual_override = bool(provider or model)
    if provider:
        route["provider"] = provider
    if model:
        route["model"] = model
    route["task_type"] = task_type
    route["manual_override"] = manual_override
    route.update(MODEL_TIERS.get(route["model"], {"cost_tier": "unknown", "capability_tier": "unknown"}))
    return route


def available_task_types() -> list[str]:
    return sorted(DEFAULT_MODEL_ROUTING)
