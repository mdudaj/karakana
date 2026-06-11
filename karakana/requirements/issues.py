"""Generate reviewable issue drafts from stories."""

from __future__ import annotations

from karakana.requirements.schemas import IssueDraft, RequirementPRD, UserStory


def generate_issues(prd: RequirementPRD, stories: list[UserStory]) -> list[IssueDraft]:
    issues: list[IssueDraft] = []
    for index, story in enumerate(stories, start=1):
        issues.append(
            IssueDraft(
                issue_id=f"{prd.req_id}-issue-{index}",
                req_id=prd.req_id,
                story_id=story.story_id,
                title=story.title,
                summary=f"Implement the vertical slice for {story.want}.",
                scope=[story.want, "Generate reviewable artifacts.", "Preserve Standards-vs-Spec and safety constraints."],
                out_of_scope=list(prd.non_goals),
                acceptance_criteria=list(story.acceptance_criteria),
                implementation_notes=list(prd.functional_requirements),
                suggested_skills=list(story.required_skills),
                suggested_skillpack=prd.suggested_skillpack,
                recommended_model_route=dict(prd.model_route),
                safety_constraints=list(prd.safety_constraints),
                tests_or_evals=list(story.required_tests_or_evals),
                definition_of_done=list(story.definition_of_done),
                labels=["requirements", "reviewable", f"risk:{story.risk_level}"],
                risk_level=story.risk_level,
            )
        )
    return issues
