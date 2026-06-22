from pathlib import Path


def test_docs_mention_viewflow_skill_usage():
    for path in ["README.md", "AGENTS.md", "docs/skill-vs-tool-policy.md"]:
        text = Path(path).read_text(encoding="utf-8")
        assert "viewflow-framework" in text
        assert "django-debugging" in text
        assert "gepg-billing" in text
        assert "invenio-framework" in text
