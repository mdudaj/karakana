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
