"""Distinguish source fields from deterministic PRD fallback text."""

from __future__ import annotations

from karakana.requirements.schemas import RequirementPRD


GENERIC_PROBLEM = "Needs review: source describes intent, but problem statement should be confirmed."
GENERIC_GOAL_PREFIX = "Convert the source intent into reviewable requirements: "
GENERIC_FUNCTIONAL_REQUIREMENTS = (
    "Generate a PRD with context, problem, goal, requirements, risks, safety constraints, and review plan.",
    "Generate user stories and issue drafts as separate reviewable artifacts.",
    "Run Definition of Ready checks before handoff.",
    "Preserve Codex handoff boundaries and do not execute Codex.",
    "Create issue drafts only; do not publish GitHub issues by default.",
    "Preserve ingestion evidence and avoid direct memory or skill writes.",
)
GENERIC_ACCEPTANCE_CRITERIA = (
    "PRD includes all required sections.",
    "Stories include acceptance criteria.",
    "Issues are independently grabbable vertical slices.",
    "Readiness check reports missing information.",
)


def source_field_is_specific(prd: RequirementPRD, field: str) -> bool:
    if field == "problem":
        value = prd.problem.strip()
        has_content = bool(value and not value.casefold().startswith("needs review:"))
        legacy_specific = value != GENERIC_PROBLEM
    elif field == "goal":
        value = prd.goal.strip()
        is_fallback = value.casefold().startswith(GENERIC_GOAL_PREFIX.casefold())
        has_content = bool(value and not value.casefold().startswith("needs review:") and not is_fallback)
        legacy_specific = not is_fallback
    elif field == "functional_requirements":
        has_content = bool(prd.functional_requirements)
        legacy_specific = any(item not in GENERIC_FUNCTIONAL_REQUIREMENTS for item in prd.functional_requirements)
    elif field == "acceptance_criteria":
        has_content = bool(prd.standards_spec.acceptance_criteria)
        legacy_specific = any(item not in GENERIC_ACCEPTANCE_CRITERIA for item in prd.standards_spec.acceptance_criteria)
    else:
        raise ValueError(f"Unsupported source field: {field}")

    if not has_content:
        return False
    grounding = prd.metadata.get("source_grounding")
    if isinstance(grounding, dict) and field in grounding:
        return grounding[field] is True
    return legacy_specific
