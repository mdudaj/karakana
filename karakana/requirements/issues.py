"""Generate reviewable issue drafts from stories."""

from __future__ import annotations

from karakana.requirements.schemas import IssueDraft, RequirementPRD, UserStory
from karakana.requirements.msc_platform import MSC_PLATFORM_SLICES, is_msc_platform


def generate_issues(prd: RequirementPRD, stories: list[UserStory]) -> list[IssueDraft]:
    if is_msc_platform(prd.project):
        return _generate_msc_platform_issues(prd, stories)

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


def _generate_msc_platform_issues(prd: RequirementPRD, stories: list[UserStory]) -> list[IssueDraft]:
    story_by_title = {story.title: story for story in stories}
    issues: list[IssueDraft] = []
    for index, item in enumerate(MSC_PLATFORM_SLICES, start=1):
        story = story_by_title.get(item.title)
        safety = list(dict.fromkeys([*item.safety_constraints, *prd.safety_constraints]))
        issues.append(
            IssueDraft(
                issue_id=f"{prd.req_id}-issue-{index}",
                req_id=prd.req_id,
                story_id=story.story_id if story else None,
                title=item.title,
                summary=f"Implement the stemgen-platform vertical slice for {item.workflow}: {item.evidence_artifact}.",
                scope=[
                    f"Research objective supported: {item.research_objective}",
                    f"Research question supported: {item.research_question}",
                    f"Platform capability: {item.platform_capability}",
                    f"Workflow: {item.workflow}",
                    f"Evidence artifact produced: {item.evidence_artifact}",
                    f"Schema artifact: {item.schema_artifact}",
                    "Keep this issue narrow; do not combine it with another slice.",
                ],
                out_of_scope=list(item.out_of_scope),
                acceptance_criteria=list(item.acceptance_criteria),
                implementation_notes=[
                    *[f"Target file: {path}" for path in item.target_files],
                    "Use schema-backed evidence artifacts before implementation behavior depends on them.",
                    "Preserve official TIE sources as Tier 1 curriculum facts.",
                ],
                suggested_skills=list(prd.suggested_skills),
                suggested_skillpack=prd.suggested_skillpack,
                recommended_model_route=dict(prd.model_route),
                safety_constraints=safety,
                tests_or_evals=[item.verification_command],
                definition_of_done=list(item.definition_of_done),
                labels=["requirements", "msc-platform", "vertical-slice", item.suffix, f"risk:{item.risk_level}"],
                risk_level=item.risk_level,
                metadata={
                    "project_context": "stemgen-platform",
                    "research_objective": item.research_objective,
                    "research_question": item.research_question,
                    "platform_capability": item.platform_capability,
                    "workflow": item.workflow,
                    "evidence_artifact": item.evidence_artifact,
                    "schema_artifact": item.schema_artifact,
                    "target_files": list(item.target_files),
                    "verification_command": item.verification_command,
                    "slice": item.suffix,
                },
            )
        )
    return issues
