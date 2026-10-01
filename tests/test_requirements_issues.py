from karakana.requirements.issues import generate_issues
from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.stories import generate_stories
from karakana.requirements.summary import render_issues


def test_issue_drafts_include_model_route_and_vertical_scope():
    source = """## Specification / PRD Seed
Goal: Let maintainers find active backlog items from handoffs.
Functional requirements:
- Handoffs link their own project's active backlog.
Acceptance criteria:
- A handoff with open items links the correct backlog.
"""
    prd = generate_prd(RequirementSource(source_type="note"), source)
    stories = generate_stories(prd)

    issues = generate_issues(prd, stories)

    assert issues
    assert issues[0].recommended_model_route["provider"] == "openai_codex"
    assert issues[0].recommended_model_route["model"] == "gpt-6-sol"
    assert issues[0].scope
    assert "requirements" in issues[0].labels


def test_concrete_issue_drafts_preserve_source_requirements_and_criteria():
    source = """## Specification / PRD Seed
Problem: Handoffs omit active project backlog items.
Goal: Show maintainers active backlog items from handoffs.
Functional requirements:
- Handoffs link only their own project's active backlog.
- Completed-only backlogs are omitted from handoffs.
Acceptance criteria:
- A handoff with open items links its project's backlog.
"""
    prd = generate_prd(RequirementSource(source_type="note"), source)

    issues = generate_issues(prd, generate_stories(prd))

    assert len(issues) == 2
    assert [issue.scope for issue in issues] == [[item] for item in prd.functional_requirements]
    assert all(issue.acceptance_criteria == ["Source criterion (mapping needs review): A handoff with open items links its project's backlog."] for issue in issues)
    assert all(issue.implementation_notes == [f"Source requirement: {issue.scope[0]}"] for issue in issues)
    assert "Completed-only backlogs are omitted from handoffs." in render_issues(issues)
    assert "Generate reviewable artifacts." not in render_issues(issues)


def test_generic_source_issue_is_visibly_provisional_without_invented_scope():
    prd = generate_prd(RequirementSource(source_type="note"), "Add issue drafts as vertical slices.")

    issues = generate_issues(prd, generate_stories(prd))

    assert len(issues) == 1
    assert issues[0].title.startswith("Needs review:")
    assert not issues[0].scope
    assert "needs-review" in issues[0].labels
    assert "Generate a PRD with context" not in render_issues(issues)


def test_msc_platform_issues_include_research_evidence_fields():
    prd = generate_prd(RequirementSource(source_type="note"), "Milestone 22.6 cleanup", project="msc-platform")
    stories = generate_stories(prd)

    issues = generate_issues(prd, stories)

    first = issues[0]
    assert first.title == "Slice 1A: Curriculum source registry schema"
    assert first.metadata["project_context"] == "stemgen-platform"
    assert first.metadata["evidence_artifact"] == "source_registry.json"
    assert first.metadata["schema_artifact"] == "schemas/curriculum/source_registry.schema.json"
    assert first.tests_or_evals == ["python3 scripts/validate_json.py"]
    assert first.out_of_scope
