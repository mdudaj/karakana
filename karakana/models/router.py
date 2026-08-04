"""Cost-effective provider/model routing map."""

from __future__ import annotations

FRONTIER_CODEX_MODEL = "gpt-5.6-sol"
CODEX_5_6_FAMILY = {"gpt-5.6": "family_alias", "gpt-5.6-sol": "default_frontier", "gpt-5.6-terra": "frontier_variant", "gpt-5.6-luna": "frontier_variant"}

MODEL_TIERS = {
    "claude-haiku-4.5": {"cost_tier": "low", "capability_tier": "lightweight_language"},
    "gpt-5-mini": {"cost_tier": "low_to_medium", "capability_tier": "planning_reasoning"},
    "gpt-5.4-mini": {"cost_tier": "low_to_medium", "capability_tier": "routine_coding"},
    "gpt-5.4": {"cost_tier": "medium", "capability_tier": "serious_coding"},
    "gpt-5.5": {"cost_tier": "high", "capability_tier": "principal_engineer"},
    "gpt-5.6": {"cost_tier": "frontier", "capability_tier": "frontier_principal_engineer", "family": "gpt-5.6", "variant": "alias"},
    "gpt-5.6-sol": {"cost_tier": "frontier", "capability_tier": "frontier_principal_engineer"},
    "gpt-5.6-terra": {"cost_tier": "frontier", "capability_tier": "frontier_principal_engineer", "family": "gpt-5.6", "variant": "terra"},
    "gpt-5.6-luna": {"cost_tier": "frontier", "capability_tier": "frontier_principal_engineer", "family": "gpt-5.6", "variant": "luna"},
    "mock-model": {"cost_tier": "none", "capability_tier": "mock"},
}


def infer_task_type(task: str, *, intent: str = "general") -> str:
    """Infer a routing task type from natural-language task text."""
    text = task.lower()
    if intent == "planning":
        if _contains_any(text, {"model routing", "model route", "provider routing"}):
            return "model_routing_planning"
        if _contains_any(text, {"safety policy", "approval policy", "permission policy"}):
            return "safety_policy_planning"
        if _contains_any(text, {"cross-project", "multi-project", "workspace architecture"}):
            return "cross_project_architecture"
        if _contains_any(text, {"authentication", "authorization", "payment", "billing", "migration", "opensearch", "production", "process state", "workflow state"}):
            return "high_risk_planning"
        if _contains_any(text, {"framework", "invenio", "viewflow", "django", "gepg", "custom field", "vocabulary"}):
            return "framework_design"
        if _contains_any(text, {"protocol", "workflow", "handoff lifecycle"}):
            return "protocol_workflow_planning"
        if _contains_any(text, {"architecture", "adr", "system design"}):
            return "architecture_review"
        if _contains_any(text, {"assessment", "assess", "analyse", "analyze", "recommendation", "recommendations"}):
            return "system_assessment"
        if _contains_any(text, {"multi-file", "multiple files", "refactor", "implementation plan"}):
            return "implementation_planning"
        if _contains_any(text, {"skill design", "prompt design", "skill update"}):
            return "skill_design"
        return "planning"

    if _contains_any(text, {"model routing", "model route", "provider routing"}):
        return "model_routing_planning"
    if _contains_any(text, {"safety policy", "approval policy", "permission policy"}):
        return "safety_policy_planning"
    if _contains_any(text, {"cross-project", "multi-project", "workspace architecture"}):
        return "cross_project_architecture"
    if _contains_any(text, {"production", "deploy", "deployment", "publish app", "app publish", "publish to production"}):
        return "high_risk_planning"
    if _contains_any(text, {"authentication", "authorization", "oauth", "sso", "permission", "permissions", "secret"}):
        return "security_or_auth_change"
    if _contains_any(text, {"payment", "billing", "invoice", "reconciliation", "idempotency"}):
        return "payment_or_billing_logic"
    if _contains_any(text, {"migration", "schema change", "database", "opensearch", "index change"}):
        return "database_or_index_migration"
    if _contains_any(text, {"viewflow", "process state", "workflow state"}):
        return "viewflow_process_state_change"
    if _contains_any(text, {"ci failure", "failing ci", "test failure", "failed workflow", "pipeline failure"}):
        return "ci_failure_analysis"
    if _contains_any(text, {"repair ci", "fix ci", "fix failing test", "fix failed workflow"}):
        return "ci_repair"
    if _contains_any(text, {"pr review", "pull request review", "review diff", "code review"}):
        return "pr_review"
    if _contains_any(text, {"deep review", "regression-risk", "regression risk"}):
        return "deep_pr_review"
    if _contains_any(text, {"changelog", "release notes", "release-note"}):
        return "changelog"
    if _contains_any(text, {"documentation", "docs", "readme"}):
        return "documentation"
    if _contains_any(text, {"triage", "classify issue"}):
        return "issue_triage"
    if _contains_any(text, {"summarize", "summary"}):
        return "simple_summary"
    if _contains_any(text, {"reflection", "reflect", "trace review"}):
        return "reflection"
    if _contains_any(text, {"evidence review", "source-grounded"}):
        return "evidence_review"
    if _contains_any(text, {"research", "investigate", "find prior art"}):
        return "research"
    if _contains_any(text, {"assessment", "assess", "analyse", "analyze", "recommendation", "recommendations"}):
        return "assessment_review"
    if _contains_any(text, {"skill design", "prompt design", "skill update"}):
        return "skill_design"
    if _contains_any(text, {"implementation plan", "plan ", "planning", "requirements"}):
        return "planning"
    if _contains_any(text, {"task draft", "draft task", "codex task", "handoff task"}):
        return "codex_task_drafting"
    if _contains_any(text, {"test", "tests", "regression coverage"}):
        return "test_generation"
    if _contains_any(text, {"refactor", "multi-file", "multiple files"}):
        return "refactoring"
    if _contains_any(text, {"framework", "invenio", "django", "gepg", "custom field", "vocabulary"}):
        return "framework_code_implementation"
    if _contains_any(text, {"architecture", "adr", "system design"}):
        return "architecture_review"
    if _contains_any(text, {"protocol", "workflow", "handoff lifecycle"}):
        return "protocol_workflow_planning"
    if _contains_any(text, {"implement", "implementation", "code", "edit", "fix", "add feature", "build"}):
        return "code_implementation"
    if _contains_any(text, {"plan", "planning", "requirements"}):
        return "planning"
    return "planning"


def _contains_any(value: str, terms: set[str]) -> bool:
    return any(term in value for term in terms)


ROLE_POLICIES = {
    "triage_summarizer": {
        "token_budget": "small",
        "token_policy": "Use Codex mini for concise classification, issue triage, and simple summaries; do not perform implementation reasoning.",
        "escalation_policy": "Escalate to planner only when the task needs sequencing, risk analysis, or requirements decisions.",
    },
    "documentation_writer": {
        "token_budget": "small",
        "token_policy": "Use Codex mini for documentation, changelog, release-note, and cleanup prose that does not require deep repository reasoning.",
        "escalation_policy": "Escalate to deep planner when documentation changes encode architecture, safety policy, public contracts, or repeated workflow guidance.",
    },
    "planner": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini for routine bounded planning, requirements decomposition, reflection, and review preparation.",
        "escalation_policy": "Escalate to deep planner when planning has multi-file, framework, protocol, workflow, or system impact.",
    },
    "deep_planner": {
        "token_budget": "large",
        "token_policy": "Use stronger Codex reasoning for consequential planning before code execution: multi-file implementation plans, framework design, protocol/workflow changes, and system-impact assessments.",
        "escalation_policy": "Escalate to principal planner when auth, billing, migrations, model routing, safety policy, production risk, or cross-project architecture is involved.",
    },
    "principal_planner": {
        "token_budget": "reserved",
        "token_policy": "Reserve frontier principal-level reasoning for high-risk planning before implementation starts: auth, billing, migrations, model routing, safety policy, workflow state, production risk, and cross-project architecture.",
        "escalation_policy": "Requires explicit high-risk rationale and should produce reviewable implementation boundaries before mutation.",
    },
    "assessment_reviewer": {
        "token_budget": "standard",
        "token_policy": "Use cost-aware planning models for non-mutating assessments and recommendations; keep findings grounded in current repository state.",
        "escalation_policy": "Escalate to deep planner when the assessment has architecture, workflow, model-routing, or system impact.",
    },
    "reflection_reviewer": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini to review traces, outcomes, and improvement opportunities without proposing silent mutation.",
        "escalation_policy": "Escalate to deep planner when reflection proposes workflow, skill, prompt, eval, or governance changes.",
    },
    "researcher": {
        "token_budget": "standard",
        "token_policy": "Use Codex mini for non-mutating repository/document research, evidence gathering, and source-grounded synthesis.",
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
        "token_policy": "Reserve the frontier route for auth, billing, migrations, workflow state, cross-project architecture, and stuck work.",
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
    "issue_triage": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only low-cost issue summarization and classification."},
    "documentation": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only fast documentation and cleanup."},
    "changelog": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only fast release notes and changelog generation."},
    "simple_summary": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only fast summary work."},
    "planning": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only routine bounded planning and requirements reasoning."},
    "assessment_review": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only cost-aware non-mutating assessment and recommendation review."},
    "implementation_planning": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Consequential multi-file implementation planning benefits from stronger repository reasoning before mutation."},
    "architecture_review": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Architecture and system-impact reasoning should use stronger planning before code execution."},
    "framework_design": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Framework design requires deeper repository and ecosystem reasoning."},
    "protocol_workflow_planning": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Protocol and workflow changes need stronger planning before implementation."},
    "system_assessment": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "System-impact assessment needs stronger repository-aware reasoning."},
    "high_risk_planning": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "High-risk planning should use frontier principal-level reasoning before implementation starts."},
    "model_routing_planning": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Model routing changes affect harness behavior and require frontier principal-level planning."},
    "safety_policy_planning": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Safety policy planning requires frontier principal-level review before implementation."},
    "reflection": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only trace review and improvement reasoning."},
    "research": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only non-mutating repository and documentation research."},
    "evidence_review": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only evidence review and source-grounded synthesis."},
    "skill_design": {"provider": "openai_codex", "model": "gpt-5.4", "mode": "codex", "rationale": "Skill and prompt design can affect repeated workflows and benefits from stronger planning."},
    "action_extraction_review": {"provider": "openai_codex", "model": "gpt-5.4-mini", "mode": "codex", "rationale": "Codex-only review of extracted actions while preserving developer control."},
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
    "high_risk_code_review": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Frontier principal-level review for high-risk changes."},
    "security_or_auth_change": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Authentication, authorization, SSO, OAuth, and secrets require frontier scrutiny."},
    "payment_or_billing_logic": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Payment, billing, idempotency, and reconciliation are high-risk and benefit from frontier scrutiny."},
    "database_or_index_migration": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Data migrations, OpenSearch index changes, and schema changes are high-risk and benefit from frontier scrutiny."},
    "viewflow_process_state_change": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Active workflow/process-state changes can break running business processes and benefit from frontier scrutiny."},
    "cross_project_architecture": {"provider": "openai_codex", "model": "gpt-5.6-sol", "mode": "codex", "rationale": "Multi-project architectural planning requires frontier reasoning depth before implementation."},
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
