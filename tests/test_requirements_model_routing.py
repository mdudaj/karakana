from karakana.requirements.issues import generate_issues
from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.stories import generate_stories


def test_requirement_issue_contains_recommended_model_route():
    prd = generate_prd(RequirementSource(source_type="note"), "Plan a safe requirements decomposition.")
    issue = generate_issues(prd, generate_stories(prd))[0]

    assert issue.recommended_model_route["provider"] == "github"
    assert issue.recommended_model_route["model"] == "gpt-5-mini"
