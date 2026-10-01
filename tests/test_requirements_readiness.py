from karakana.requirements.prd import generate_prd
from karakana.requirements.readiness import check_readiness
from karakana.requirements.issues import generate_issues
from karakana.requirements.schemas import IssueDraft, RequirementSource
from karakana.requirements.stories import generate_stories
from karakana.requirements.summary import render_readiness


CONCRETE_SEED = """## Specification / PRD Seed

Create a reviewable PRD for Karakana backlog discovery.

Problem: Handoffs omit the active project development backlog.

Goal: Link active project backlog items from Karakana handoffs.

Functional requirements:
- Handoffs include only their own project's active backlog path.

Acceptance criteria:
- A handoff for a project with open items links its backlog; completed-only backlogs are omitted.
"""


def test_readiness_checks_report_ready():
    prd = generate_prd(RequirementSource(source_type="note"), CONCRETE_SEED)

    check = check_readiness(prd)

    assert check.ready
    assert "model route is recommended" in check.passed
    assert not check.failed


def test_readiness_rejects_generic_generated_sections():
    prd = generate_prd(RequirementSource(source_type="file", title="development-backlog.md"), "# Karakana development backlog reliability\n\n## Requirements and user stories\n\nHandoffs link active backlog items.")

    check = check_readiness(prd)

    assert not check.ready
    assert check.status == "not_ready"
    assert check.failed == [
        "problem describes the source task",
        "goal describes the source task",
        "functional requirements describe source behavior",
        "acceptance criteria verify source behavior",
    ]
    assert "Add task-specific Problem, Goal, Functional requirements, and Acceptance criteria" in check.recommended_next_actions[0]
    assert "## Failed Checks" in render_readiness(check)


def test_readiness_rejects_legacy_generic_prd_without_grounding_metadata():
    prd = generate_prd(RequirementSource(source_type="file"), "# Karakana backlog\n\nHandoffs link active items.")
    del prd.metadata["source_grounding"]

    check = check_readiness(prd)

    assert not check.ready
    assert len(check.failed) == 4


def test_readiness_accepts_explicit_requirement_text_that_matches_a_template():
    source = """## Specification / PRD Seed

Problem: The requirements command cannot produce reviewable PRDs for intake work.
Goal: Produce a concrete PRD for the intake workflow.
Functional requirements:
- Generate a PRD with context, problem, goal, requirements, risks, safety constraints, and review plan.
Acceptance criteria:
- PRD includes all required sections.
"""
    prd = generate_prd(RequirementSource(source_type="note"), source)

    check = check_readiness(prd)

    assert check.ready
    assert check.status in {"ready", "warning"}


def test_msc_platform_readiness_fails_generic_issue():
    prd = generate_prd(RequirementSource(source_type="note"), "Milestone 22.6 cleanup", project="msc-platform")
    generic_issue = IssueDraft(
        issue_id="issue-1",
        req_id=prd.req_id,
        story_id=None,
        title="Build curriculum pipeline",
        summary="Build a broad pipeline.",
        scope=["Implement everything."],
        out_of_scope=[],
        acceptance_criteria=["It works."],
        tests_or_evals=[],
    )

    check = check_readiness(prd, [generic_issue])

    assert not check.ready
    assert any("missing_research_objective" in item for item in check.failed)
    assert any("too_broad_for_vertical_slice" in item for item in check.failed)


def test_msc_platform_readiness_passes_vertical_issues():
    prd = generate_prd(RequirementSource(source_type="note"), CONCRETE_SEED, project="msc-platform")
    issues = generate_issues(prd, generate_stories(prd))

    check = check_readiness(prd, issues)

    assert check.ready
    assert "msc-platform issues are evidence-linked vertical slices" in check.passed
