"""Generate vertical-slice user stories from PRDs."""

from __future__ import annotations

from karakana.requirements.schemas import RequirementPRD, UserStory
from karakana.requirements.msc_platform import MSC_PLATFORM_SLICES, is_msc_platform


SLICES = [
    ("schema and storage", "define and persist structured artifacts"),
    ("CLI command", "operate the workflow from the command line"),
    ("artifact generation", "review generated markdown and JSON outputs"),
    ("safety and readiness gate", "verify scope, safety, tests, and review before handoff"),
    ("evals and tests", "protect the behavior with deterministic checks"),
]


def generate_stories(prd: RequirementPRD) -> list[UserStory]:
    if is_msc_platform(prd.project):
        return _generate_msc_platform_stories(prd)

    stories: list[UserStory] = []
    for index, (title, want) in enumerate(SLICES, start=1):
        stories.append(
            UserStory(
                story_id=f"{prd.req_id}-story-{index}",
                req_id=prd.req_id,
                title=f"{prd.title}: {title}",
                actor="developer",
                want=want,
                outcome="the work can move forward without vague implementation tasks",
                acceptance_criteria=[f"Given the PRD, when {title} is implemented, then artifacts remain reviewable.", "Given missing information, when readiness runs, then gaps are reported."],
                standards=list(prd.standards_spec.standards),
                risks=list(prd.risks),
                required_skills=list(prd.suggested_skills),
                required_tests_or_evals=list(prd.test_and_eval_plan),
                definition_of_ready=["PRD exists.", "Acceptance criteria exist.", "Safety constraints are listed.", "Model route is recommended."],
                definition_of_done=["Tests and evals pass.", "Artifacts are generated under .karakana/requirements/.", "Human review remains required before publishing or execution."],
                risk_level="high" if any("High-risk" in item for item in prd.safety_constraints) else "medium",
            )
        )
    return stories


def _generate_msc_platform_stories(prd: RequirementPRD) -> list[UserStory]:
    stories: list[UserStory] = []
    for index, item in enumerate(MSC_PLATFORM_SLICES, start=1):
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
