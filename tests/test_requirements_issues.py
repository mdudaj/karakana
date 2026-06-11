from karakana.requirements.issues import generate_issues
from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.stories import generate_stories


def test_issue_drafts_include_model_route_and_vertical_scope():
    prd = generate_prd(RequirementSource(source_type="note"), "Add issue drafts as vertical slices.")
    stories = generate_stories(prd)

    issues = generate_issues(prd, stories)

    assert issues
    assert issues[0].recommended_model_route["provider"] == "github"
    assert issues[0].scope
    assert "requirements" in issues[0].labels


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
