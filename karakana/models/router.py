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

ROLE_POLICIES = {
    "triage_summarizer": {
        "token_budget": "small",
        "token_policy": "Use GitHub inference for concise classification, summaries, and handoff notes; do not perform implementation reasoning.",
        "escalation_policy": "Escalate to planner only when the task needs sequencing, risk analysis, or requirements decisions.",
    },
    "planner": {
        "token_budget": "standard",
        "token_policy": "Use GitHub inference for planning, requirements, architecture, reflection, and review preparation before code execution.",
        "escalation_policy": "Escalate to Codex implementation routes only after the plan identifies concrete repository edits.",
    },
    "routine_implementer": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini for bounded implementation and test drafting after requirements and design context are available.",
        "escalation_policy": "Escalate to serious implementer after failed tests, broad multi-file coupling, or framework-level complexity.",
    },
    "serious_implementer": {
        "token_budget": "large",
        "token_policy": "Use stronger Codex routing for refactors, CI repair, framework work, and repository-aware review.",
        "escalation_policy": "Escalate to principal reviewer only for high-risk domains, production blast radius, or repeated failure.",
    },
    "principal_reviewer": {
        "token_budget": "reserved",
        "token_policy": "Reserve the highest-cost route for auth, billing, migrations, workflow state, cross-project architecture, and stuck work.",
        "escalation_policy": "Requires explicit high-risk rationale; do not use for routine docs, triage, or first-pass implementation.",
    },
    "dry_run": {
        "token_budget": "none",
        "token_policy": "Use mock routing for unknown or dry-run tasks until a concrete task type is selected.",
        "escalation_policy": "Select a known task type before making live model calls.",
    },
}

TASK_ROLE_POLICIES = {
    "issue_triage": "triage_summarizer",
    "documentation": "triage_summarizer",
    "changelog": "triage_summarizer",
    "simple_summary": "triage_summarizer",
    "planning": "planner",
    "architecture_review": "planner",
    "reflection": "planner",
    "skill_design": "planner",
    "action_extraction_review": "planner",
    "routine_code_implementation": "routine_implementer",
    "test_generation": "routine_implementer",
    "codex_task_drafting": "routine_implementer",
    "code_implementation": "routine_implementer",
    "ci_repair": "serious_implementer",
    "refactoring": "serious_implementer",
    "deep_pr_review": "serious_implementer",
    "pr_review": "serious_implementer",
    "ci_failure_analysis": "serious_implementer",
    "framework_code_implementation": "serious_implementer",
    "high_risk_code_review": "principal_reviewer",
    "security_or_auth_change": "principal_reviewer",
    "payment_or_billing_logic": "principal_reviewer",
    "database_or_index_migration": "principal_reviewer",
    "viewflow_process_state_change": "principal_reviewer",
    "cross_project_architecture": "principal_reviewer",
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


def _apply_role_policy(route: dict, task_type: str) -> None:
    role = route.get("role") or TASK_ROLE_POLICIES.get(task_type, "dry_run")
    route["role"] = role
    for key, value in ROLE_POLICIES[role].items():
        route.setdefault(key, value)


def route_model(task_type: str, provider: str | None = None, model: str | None = None, skillpack_routes: dict | None = None) -> dict:
    route = DEFAULT_MODEL_ROUTING.get(
        task_type,
        {"provider": "mock", "model": "mock-model", "mode": "mock", "rationale": "Unknown task type; use mock dry-run routing."},
    ).copy()
    route["route_source"] = "global"
    if skillpack_routes and task_type in skillpack_routes:
        skillpack_route = skillpack_routes[task_type]
        route.update(
            {
                "provider": skillpack_route.get("provider", route["provider"]),
                "model": skillpack_route.get("model", route["model"]),
                "rationale": skillpack_route.get("rationale") or route.get("rationale"),
                "route_source": "skillpack",
            }
        )
    manual_override = bool(provider or model)
    if provider:
        route["provider"] = provider
    if model:
        route["model"] = model
    if manual_override:
        route["route_source"] = "manual_override"
    route["task_type"] = task_type
    route["manual_override"] = manual_override
    _apply_role_policy(route, task_type)
    route.update(MODEL_TIERS.get(route["model"], {"cost_tier": "unknown", "capability_tier": "unknown"}))
    return route


def available_task_types() -> list[str]:
    return sorted(DEFAULT_MODEL_ROUTING)
