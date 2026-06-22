"""Classify cross-project patterns into proposal targets."""

from __future__ import annotations

from karakana.crosslinks.schemas import CrosslinkPattern


def classify_pattern(pattern: CrosslinkPattern) -> dict:
    if pattern.pattern_type == "conflicting_memory":
        return {"scope": "conflicting", "proposal_type": "manual_review", "target": None}
    if pattern.pattern_type in {"shared_skill_need", "shared_workflow"}:
        skill = _skill_target(pattern)
        return {"scope": "global/shared", "proposal_type": "shared_skill_update", "target": f"skills/{skill}/SKILL.md"}
    if pattern.pattern_type == "shared_eval_need":
        return {"scope": "global/shared", "proposal_type": "shared_eval_update", "target": "evals/shared/regression-case.yml"}
    if pattern.pattern_type in {"shared_risk", "shared_safety_rule"}:
        return {"scope": "global/shared", "proposal_type": "global_ubongo_update", "target": "ubongo/global/engineering-standards.md"}
    if pattern.pattern_type == "candidate_skillpack_update":
        return {"scope": "project-specific", "proposal_type": "skillpack_update", "target": "skillpacks/<project>.yml"}
    return {"scope": "manual-review", "proposal_type": "manual_review", "target": None}


def _skill_target(pattern: CrosslinkPattern) -> str:
    text = (pattern.title + " " + pattern.summary).lower()
    if "viewflow" in text or "process" in text or "workflow" in text:
        return "viewflow-framework"
    if "payment" in text or "billing" in text or "gepg" in text:
        return "gepg-billing"
    if "invenio" in text or "opensearch" in text:
        return "invenio-framework"
    return "karakana-self-improvement"
