from karakana.requirements.prd import generate_prd
from karakana.requirements.readiness import check_readiness
from karakana.requirements.issues import generate_issues
from karakana.requirements.schemas import IssueDraft, RequirementSource
from karakana.requirements.stories import generate_stories


def test_readiness_checks_report_ready():
    prd = generate_prd(RequirementSource(source_type="note"), "Add readiness checks for safety constraints and model route.")

    check = check_readiness(prd)

    assert check.ready
    assert "model route is recommended" in check.passed
    assert not check.failed


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
    prd = generate_prd(RequirementSource(source_type="note"), "Milestone 22.6 cleanup", project="msc-platform")
    issues = generate_issues(prd, generate_stories(prd))

    check = check_readiness(prd, issues)

    assert check.ready
    assert "msc-platform issues are evidence-linked vertical slices" in check.passed
