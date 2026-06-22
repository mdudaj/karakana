from karakana.actions.extractor import ActionExtractor
from tests.test_action_extractor import write_response


def test_suggested_skills_from_explicit_section(tmp_path):
    response = write_response(
        tmp_path,
        """## Suggested Skills
- viewflow-framework
- github-pr-review

## Next Actions
- Codex task: Implement Viewflow workflow review checks.
""",
        {"status": "passed", "blocked": False},
    )

    bundle = ActionExtractor().extract_from_response(response)

    assert bundle.suggested_skills == ["github-pr-review", "viewflow-framework"]
    assert bundle.actions[0].suggested_skills == ["viewflow-framework"]


def test_suggested_skills_from_keywords(tmp_path):
    response = write_response(tmp_path, "TODO: Review GePG payment callback reconciliation.", {"status": "passed", "blocked": False})

    bundle = ActionExtractor().extract_from_response(response)

    assert "gepg-billing" in bundle.suggested_skills
    assert "gepg-billing" in bundle.actions[0].suggested_skills


def test_generic_workflow_text_does_not_imply_viewflow(tmp_path):
    response = write_response(tmp_path, "TODO: Update the dogfood workflow documentation.", {"status": "passed", "blocked": False})

    bundle = ActionExtractor().extract_from_response(response, project="karakana", skill="karakana")

    assert "viewflow-framework" not in bundle.suggested_skills
    assert "viewflow-framework" not in bundle.actions[0].suggested_skills
