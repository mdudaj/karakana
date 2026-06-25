"""Cost-aware model escalation policy."""

from __future__ import annotations

ESCALATION_RULES = [
    {
        "from_provider": "github",
        "from_model": "claude-haiku-4.5",
        "to_provider": "github",
        "to_model": "gpt-5-mini",
        "signals": {"issue_is_ambiguous", "architecture_reasoning_needed", "safety_or_security_relevance", "repeated_low_confidence"},
        "rationale": "Planning or safety-relevant ambiguity needs stronger reasoning than lightweight language work.",
    },
    {
        "from_provider": "github",
        "from_model": "gpt-5-mini",
        "to_provider": "openai_codex",
        "to_model": "gpt-5.4",
        "signals": {
            "multi_file_implementation_planning",
            "framework_design_needed",
            "protocol_or_workflow_change",
            "system_impact_assessment",
            "architecture_reasoning_needed",
        },
        "rationale": "Consequential planning should use stronger repository-aware reasoning before implementation starts.",
    },
    {
        "from_provider": "github",
        "from_model": "gpt-5-mini",
        "to_provider": "openai_codex",
        "to_model": "gpt-5.5",
        "signals": {
            "high_risk_planning",
            "model_routing_change",
            "safety_policy_change",
            "cross_project_architecture",
            "production_risk_planning",
        },
        "rationale": "High-risk planning should use principal-level reasoning before implementation starts.",
    },
    {
        "from_provider": "github",
        "from_model": "gpt-5-mini",
        "to_provider": "openai_codex",
        "to_model": "gpt-5.4-mini",
        "signals": {"code_files_need_editing", "tests_need_writing", "local_repo_inspection_needed", "patch_generation_needed"},
        "rationale": "Repository edits and tests should move from planning to a cost-effective Codex coding model.",
    },
    {
        "from_provider": "openai_codex",
        "from_model": "gpt-5.4-mini",
        "to_provider": "openai_codex",
        "to_model": "gpt-5.4",
        "signals": {
            "more_than_3_files_changed",
            "tests_fail_after_first_patch",
            "task_involves_refactor",
            "task_involves_ci_failure",
            "task_requires_framework_understanding",
            "generated_patch_is_structurally_incomplete",
        },
        "rationale": "Routine Codex work should escalate to gpt-5.4 when complexity, framework depth, or first-pass failures appear.",
    },
    {
        "from_provider": "openai_codex",
        "from_model": "gpt-5.4",
        "to_provider": "openai_codex",
        "to_model": "gpt-5.5",
        "signals": {
            "security_or_authentication_change",
            "billing_or_payment_logic",
            "database_migration",
            "opensearch_index_change",
            "viewflow_process_state_change",
            "invenio_custom_field_or_vocab_migration",
            "repeated_failure_after_two_attempts",
            "high_risk_pr_review",
            "production_deployment_risk",
        },
        "rationale": "High-risk or repeatedly stuck work requires principal-level review.",
    },
]


def recommend_escalation(current_provider: str, current_model: str, signals: list[str]) -> dict:
    signal_set = set(signals)
    for rule in ESCALATION_RULES:
        if rule["from_provider"] != current_provider or rule["from_model"] != current_model:
            continue
        matched = sorted(signal_set & rule["signals"])
        if matched:
            return {
                "should_escalate": True,
                "from_provider": current_provider,
                "from_model": current_model,
                "to_provider": rule["to_provider"],
                "to_model": rule["to_model"],
                "matched_signals": matched,
                "rationale": rule["rationale"],
            }
    return {
        "should_escalate": False,
        "from_provider": current_provider,
        "from_model": current_model,
        "to_provider": current_provider,
        "to_model": current_model,
        "matched_signals": [],
        "rationale": "No escalation signals matched the current route.",
    }
