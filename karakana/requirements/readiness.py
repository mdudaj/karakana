"""Definition of Ready checks for requirements."""

from __future__ import annotations

from karakana.requirements.schemas import ReadinessCheck, RequirementPRD


def check_readiness(prd: RequirementPRD) -> ReadinessCheck:
    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []

    _check(bool(prd.goal and "Needs review" not in prd.goal), "goal is clear", passed, failed)
    _check(bool(prd.problem), "problem is clear", passed, failed)
    _check(bool(prd.functional_requirements), "scope is defined", passed, failed)
    _check(bool(prd.non_goals), "non-goals are defined", passed, failed)
    _check(bool(prd.standards_spec.acceptance_criteria), "acceptance criteria exist", passed, failed)
    _check(bool(prd.suggested_skills), "suggested skills exist", passed, failed)
    if prd.suggested_skillpack:
        passed.append("suggested skillpack exists")
    else:
        warnings.append("suggested skillpack is intentionally absent or needs review")
    _check(bool(prd.risks), "risk level is known", passed, failed)
    _check(bool(prd.safety_constraints), "safety constraints are listed", passed, failed)
    impact = prd.harness_impact
    _check(all([impact.instructions, impact.tools, impact.environment, impact.state, impact.feedback]), "harness subsystem impact is mapped", passed, failed)
    _check(bool(prd.test_and_eval_plan), "test/eval plan exists", passed, failed)
    _check(bool(prd.model_route.get("provider") and prd.model_route.get("model")), "model route is recommended", passed, failed)
    _check(bool(prd.rollout_or_review_plan), "human review requirement is clear", passed, failed)

    ready = not failed
    status = "ready" if ready and not warnings else ("warning" if ready else "not_ready")
    return ReadinessCheck(
        req_id=prd.req_id,
        status=status,
        ready=ready,
        passed=passed,
        failed=failed,
        warnings=warnings,
        recommended_next_actions=["Review PRD with a human.", "Generate stories and issue drafts.", "Address failed readiness checks before Codex handoff."] if failed else ["Review generated stories and issues.", "Use action or Codex handoff only after approval."],
    )


def _check(condition: bool, label: str, passed: list[str], failed: list[str]) -> None:
    (passed if condition else failed).append(label)
