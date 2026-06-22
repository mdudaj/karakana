from pathlib import Path


def test_github_pr_review_includes_standards_vs_spec_mode():
    text = Path("skills/github-pr-review/SKILL.md").read_text(encoding="utf-8")

    assert "Standards-vs-Spec Review Mode" in text
    assert "## Standards Review" in text
    assert "## Spec Review" in text
    assert "### Acceptance Criteria Check" in text
