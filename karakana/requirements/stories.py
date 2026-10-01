"""Generate vertical-slice user stories from PRDs."""

from __future__ import annotations

from karakana.requirements.grounding import source_field_is_specific
from karakana.requirements.schemas import RequirementPRD, UserStory
from karakana.requirements.msc_platform import is_msc_platform, slices_for_prd


LEGACY_TEMPLATE_SLICES = (
    ("schema and storage", "define and persist structured artifacts"),
    ("CLI command", "operate the workflow from the command line"),
    ("artifact generation", "review generated markdown and JSON outputs"),
    ("safety and readiness gate", "verify scope, safety, tests, and review before handoff"),
    ("evals and tests", "protect the behavior with deterministic checks"),
)


def has_legacy_template_wants(stories: list[UserStory]) -> bool:
    return tuple(story.want for story in stories) == tuple(want for _, want in LEGACY_TEMPLATE_SLICES)


def is_legacy_template_stories(prd: RequirementPRD, stories: list[UserStory]) -> bool:
    if not has_legacy_template_wants(stories):
        return False
    return all(
        story == UserStory(
            story_id=f"{prd.req_id}-story-{index}",
            req_id=prd.req_id,
            title=f"{prd.title}: {title}",
            actor="developer",
            want=want,
            outcome="the work can move forward without vague implementation tasks",
            acceptance_criteria=[
                f"Given the PRD, when {title} is implemented, then artifacts remain reviewable.",
                "Given missing information, when readiness runs, then gaps are reported.",
            ],
            standards=list(prd.standards_spec.standards),
            risks=list(prd.risks),
            required_skills=list(prd.suggested_skills),
            required_tests_or_evals=list(prd.test_and_eval_plan),
            definition_of_ready=["PRD exists.", "Acceptance criteria exist.", "Safety constraints are listed.", "Model route is recommended."],
            definition_of_done=["Tests and evals pass.", "Artifacts are generated under .karakana/requirements/.", "Human review remains required before publishing or execution."],
            risk_level="high" if any("High-risk" in item for item in prd.safety_constraints) else "medium",
        )
        for index, (story, (title, want)) in enumerate(zip(stories, LEGACY_TEMPLATE_SLICES), start=1)
    )


def generate_stories(prd: RequirementPRD) -> list[UserStory]:
    if is_msc_platform(prd.project):
        return _generate_msc_platform_stories(prd)

    if not source_field_is_specific(prd, "functional_requirements"):
        return [_story(
            prd, 1, "Needs review: define source-specific behavior",
            "Needs review: identify the user or role.",
            "Needs review: add source-specific functional requirements.",
            "Needs review: confirm the intended outcome.",
            ["Needs review: add source-specific acceptance criteria."],
        )]

    actors = prd.users_or_actors if prd.metadata.get("actors_grounded") is True else []
    actor = actors[0] if len(actors) == 1 else "Needs review: assign a source actor to this requirement."
    outcome = prd.goal if source_field_is_specific(prd, "goal") else "Needs review: confirm the intended outcome."
    criteria = prd.standards_spec.acceptance_criteria if source_field_is_specific(prd, "acceptance_criteria") else []
    if not criteria:
        mapped_criteria = ["Needs review: add source-specific acceptance criteria."]
    elif len(prd.functional_requirements) == 1:
        mapped_criteria = list(criteria)
    else:
        mapped_criteria = [f"Source criterion (mapping needs review): {item}" for item in criteria]

    return [
        _story(prd, index, f"Requirement {index}: {requirement}", actor, requirement, outcome, mapped_criteria)
        for index, requirement in enumerate(prd.functional_requirements, start=1)
    ]


def _story(prd: RequirementPRD, index: int, title: str, actor: str, want: str, outcome: str, criteria: list[str]) -> UserStory:
    return UserStory(
        story_id=f"{prd.req_id}-story-{index}",
        req_id=prd.req_id,
        title=title,
        actor=actor,
        want=want,
        outcome=outcome,
        acceptance_criteria=list(criteria),
        standards=list(prd.standards_spec.standards),
        risks=list(prd.risks),
        required_skills=list(prd.suggested_skills),
        required_tests_or_evals=list(prd.test_and_eval_plan),
        definition_of_ready=["Confirm the actor, outcome, and source criterion mapping before implementation."],
        definition_of_done=["Verify source acceptance criteria and record human review before publishing or execution."],
        risk_level="high" if any("High-risk" in item for item in prd.safety_constraints) else "medium",
    )


def _generate_msc_platform_stories(prd: RequirementPRD) -> list[UserStory]:
    stories: list[UserStory] = []
    for index, item in enumerate(slices_for_prd(prd.project, prd.title, prd.goal, prd.context), start=1):
        stories.append(
            UserStory(
                story_id=f"{prd.req_id}-story-{index}",
                req_id=prd.req_id,
                title=item.title,
                actor="research platform developer",
                want=f"{item.platform_capability} for {item.workflow}",
                outcome=f"{item.evidence_artifact} can be generated or validated as research evidence",
                acceptance_criteria=list(item.acceptance_criteria),
                standards=[
                    f"Research objective supported: {item.research_objective}",
                    f"Research question supported: {item.research_question}",
                    f"Evidence artifact produced: {item.evidence_artifact}",
                    f"Schema artifact: {item.schema_artifact}",
                ],
                risks=list(prd.risks),
                required_skills=list(prd.suggested_skills),
                required_tests_or_evals=[item.verification_command],
                definition_of_ready=[
                    "Research objective is referenced.",
                    "Evidence artifact is named.",
                    "Schema artifact is named.",
                    "Verification command is defined.",
                    "Out-of-scope boundary is explicit.",
                ],
                definition_of_done=list(item.definition_of_done),
                risk_level=item.risk_level,
            )
        )
    return stories
