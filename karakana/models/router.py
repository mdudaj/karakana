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
        "token_policy": "Use GitHub inference for concise classification, issue triage, and simple summaries; do not perform implementation reasoning.",
        "escalation_policy": "Escalate to planner only when the task needs sequencing, risk analysis, or requirements decisions.",
    },
    "documentation_writer": {
        "token_budget": "small",
        "token_policy": "Use lightweight GitHub inference for documentation, changelog, release-note, and cleanup prose that does not require deep repository reasoning.",
        "escalation_policy": "Escalate to deep planner when documentation changes encode architecture, safety policy, public contracts, or repeated workflow guidance.",
    },
    "planner": {
        "token_budget": "standard",
        "token_policy": "Use GitHub inference for routine bounded planning, requirements decomposition, reflection, and review preparation.",
        "escalation_policy": "Escalate to deep planner when planning has multi-file, framework, protocol, workflow, or system impact.",
    },
    "deep_planner": {
        "token_budget": "large",
        "token_policy": "Use stronger Codex reasoning for consequential planning before code execution: multi-file implementation plans, framework design, protocol/workflow changes, and system-impact assessments.",
        "escalation_policy": "Escalate to principal planner when auth, billing, migrations, model routing, safety policy, production risk, or cross-project architecture is involved.",
    },
    "principal_planner": {
        "token_budget": "reserved",
        "token_policy": "Reserve principal-level reasoning for high-risk planning before implementation starts: auth, billing, migrations, model routing, safety policy, workflow state, production risk, and cross-project architecture.",
        "escalation_policy": "Requires explicit high-risk rationale and should produce reviewable implementation boundaries before mutation.",
    },
    "assessment_reviewer": {
        "token_budget": "standard",
        "token_policy": "Use cost-aware planning models for non-mutating assessments and recommendations; keep findings grounded in current repository state.",
        "escalation_policy": "Escalate to deep planner when the assessment has architecture, workflow, model-routing, or system impact.",
    },
    "reflection_reviewer": {
        "token_budget": "standard",
        "token_policy": "Use GitHub inference to review traces, outcomes, and improvement opportunities without proposing silent mutation.",
        "escalation_policy": "Escalate to deep planner when reflection proposes workflow, skill, prompt, eval, or governance changes.",
    },
    "researcher": {
        "token_budget": "standard",
        "token_policy": "Use GitHub inference for non-mutating repository/document research, evidence gathering, and source-grounded synthesis.",
        "escalation_policy": "Escalate to deep planner when research changes architecture, workflow, safety, model routing, or implementation direction.",
    },
    "task_author": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini to draft bounded implementation prompts and handoff tasks after requirements, skill, and safety context exist.",
        "escalation_policy": "Escalate to deep planner when task drafting reveals architecture, framework, workflow, or multi-file ambiguity.",
    },
    "test_designer": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini for routine test generation and regression coverage plans grounded in existing test patterns.",
        "escalation_policy": "Escalate to serious implementer for flaky CI, complex fixtures, integration tests, or framework-heavy testing.",
    },
    "routine_implementer": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini for bounded implementation and test drafting after requirements and design context are available.",
        "escalation_policy": "Escalate to serious implementer after failed tests, broad multi-file coupling, or framework-level complexity.",
    },
    "serious_implementer": {
        "token_budget": "large",
        "token_policy": "Use stronger Codex routing for refactors, framework work, and non-routine repository edits.",
        "escalation_policy": "Escalate to principal reviewer only for high-risk domains, production blast radius, or repeated failure.",
    },
    "code_reviewer": {
        "token_budget": "large",
        "token_policy": "Use stronger Codex routing for repository-aware PR review, diff reasoning, regression-risk analysis, and review follow-up planning.",
        "escalation_policy": "Escalate to principal reviewer for auth, billing, migrations, workflow state, production-risk review, or high-risk findings.",
    },
    "ci_analyst": {
        "token_budget": "large",
        "token_policy": "Use stronger Codex routing for CI failure analysis, log triage, test isolation, and repair recommendations.",
        "escalation_policy": "Escalate to serious implementer when a repair patch is needed, or principal reviewer when CI failures affect high-risk domains.",
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
    "documentation": "documentation_writer",
    "changelog": "documentation_writer",
    "simple_summary": "triage_summarizer",
    "planning": "planner",
    "architecture_review": "deep_planner",
    "implementation_planning": "deep_planner",
    "framework_design": "deep_planner",
    "protocol_workflow_planning": "deep_planner",
    "system_assessment": "deep_planner",
    "assessment_review": "assessment_reviewer",
    "high_risk_planning": "principal_planner",
    "model_routing_planning": "principal_planner",
    "safety_policy_planning": "principal_planner",
    "reflection": "reflection_reviewer",
    "research": "researcher",
    "evidence_review": "researcher",
    "skill_design": "deep_planner",
    "action_extraction_review": "planner",
    "routine_code_implementation": "routine_implementer",
    "test_generation": "test_designer",
    "codex_task_drafting": "task_author",
    "code_implementation": "routine_implementer",
    "ci_repair": "ci_analyst",
    "refactoring": "serious_implementer",
    "deep_pr_review": "code_reviewer",
    "pr_review": "code_reviewer",
    "ci_failure_analysis": "ci_analyst",
    "framework_code_implementation": "serious_implementer",
    "high_risk_code_review": "principal_reviewer",
    "security_or_auth_change": "principal_reviewer",
    "payment_or_billing_logic": "principal_reviewer",
    "database_or_index_migration": "principal_reviewer",
    "viewflow_process_state_change": "principal_reviewer",
    "cross_project_architecture": "principal_planner",
}

DEFAULT_MODEL_ROUTING = {
    "issue_triage": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast, low-cost issue summarization and classification."},
    "documentation": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast documentation and cleanup."},
    "changelog": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast release notes and changelog generation."},
    "simple_summary": {"provider": "github", "model": "claude-haiku-4.5", "mode": "chat", "rationale": "Fast summary work."},
    "planning": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Routine bounded planning and requirements reasoning."},
    "assessment_review": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Cost-aware non-mutating assessment and recommendation review."},
    "implementation_planning": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Consequential multi-file implementation planning benefits from stronger repository reasoning before mutation."},
    "architecture_review": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Architecture and system-impact reasoning should use stronger planning before code execution."},
    "framework_design": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Framework design requires deeper repository and ecosystem reasoning."},
    "protocol_workflow_planning": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Protocol and workflow changes need stronger planning before implementation."},
    "system_assessment": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "System-impact assessment needs stronger repository-aware reasoning."},
    "high_risk_planning": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "High-risk planning should use principal-level reasoning before implementation starts."},
    "model_routing_planning": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Model routing changes affect harness behavior and require principal-level planning."},
    "safety_policy_planning": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Safety policy planning requires principal-level review before implementation."},
    "reflection": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Trace review and improvement reasoning."},
    "research": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Non-mutating repository and documentation research."},
    "evidence_review": {"provider": "github", "model": "gpt-5-mini", "mode": "chat", "rationale": "Evidence review and source-grounded synthesis."},
    "skill_design": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Skill and prompt design can affect repeated workflows and benefits from stronger planning."},
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
    "cross_project_architecture": {"provider": "openai_codex", "model": "gpt-5.5", "mode": "codex", "rationale": "Multi-project architectural planning requires highest reasoning depth before implementation."},
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
