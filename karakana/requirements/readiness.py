"""Definition of Ready checks for requirements."""

from __future__ import annotations

from karakana.requirements.msc_platform import is_msc_platform
from karakana.requirements.schemas import IssueDraft, ReadinessCheck, RequirementPRD


GENERIC_TITLE_TERMS = {
    "build curriculum pipeline",
    "implement evaluation workflow",
    "create ai review engine",
    "add whatsapp integration",
    "schema and storage",
    "cli command",
    "artifact generation",
}


def check_readiness(prd: RequirementPRD, issues: list[IssueDraft] | None = None) -> ReadinessCheck:
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

    if is_msc_platform(prd.project):
        _check(bool(issues), "msc-platform issue drafts exist", passed, failed)
        for issue in issues or []:
            issue_failures = validate_vertical_slice_issue(issue, project=prd.project)
            for warning in issue_failures:
                label = f"{issue.title}: {warning}"
                if warning in {"missing_research_objective", "missing_evidence_artifact", "missing_schema_artifact"}:
                    failed.append(label)
                elif warning in {"missing_verification_command", "missing_out_of_scope", "too_broad_for_vertical_slice", "generic_project_context"}:
                    failed.append(label)
                else:
                    warnings.append(label)
        if issues and not failed:
            passed.append("msc-platform issues are evidence-linked vertical slices")

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


def validate_vertical_slice_issue(issue: IssueDraft, project: str | None = None) -> list[str]:
    problems: list[str] = []
    text = "\n".join(
        [
            issue.title,
            issue.summary,
            *issue.scope,
            *issue.out_of_scope,
            *issue.acceptance_criteria,
            *issue.implementation_notes,
            *issue.tests_or_evals,
            *issue.definition_of_done,
        ]
    ).lower()
    metadata = issue.metadata or {}

    if not _has_value(metadata, "research_objective") and "research objective" not in text:
        problems.append("missing_research_objective")
    if not _has_value(metadata, "evidence_artifact") and "evidence artifact" not in text:
        problems.append("missing_evidence_artifact")
    if project == "msc-platform" and not _has_value(metadata, "schema_artifact") and "schema" not in text:
        problems.append("missing_schema_artifact")
    if not (metadata.get("verification_command") or issue.tests_or_evals or "verification command" in text):
        problems.append("missing_verification_command")
    if not issue.out_of_scope:
        problems.append("missing_out_of_scope")
    if _too_broad(issue.title, text):
        problems.append("too_broad_for_vertical_slice")
    if project == "msc-platform" and "stemgen-platform" not in text and "msc-platform" not in text and metadata.get("project_context") != "stemgen-platform":
        problems.append("generic_project_context")
    return problems


def _has_value(metadata: dict, key: str) -> bool:
    value = metadata.get(key)
    return isinstance(value, str) and bool(value.strip())


def _too_broad(title: str, text: str) -> bool:
    lowered_title = title.lower()
    if any(term in lowered_title for term in GENERIC_TITLE_TERMS):
        return True
    broad_terms = ("pipeline", "workflow", "engine", "integration")
    has_slice_marker = "slice " in lowered_title or "slice-" in text or "schema artifact" in text
    return any(term in lowered_title for term in broad_terms) and not has_slice_marker
