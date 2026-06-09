from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app


def test_issue_triage_without_post_comment(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-issue-event.json"))
    result = CliRunner().invoke(app, ["github", "issue-triage", "--project", "karakana", "--skill", "karakana-self-improvement"])

    assert result.exit_code == 0
    assert "Issue triage prompt written to:" in result.output
    assert "Posted issue comment" not in result.output


def test_issue_triage_with_post_comment(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-issue-event.json"))
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setattr("karakana.tools.github_api.GitHubApiClient.post_issue_comment", lambda self, issue_number, body: {"html_url": f"https://example/{issue_number}"})

    result = CliRunner().invoke(app, ["github", "issue-triage", "--project", "karakana", "--skill", "karakana-self-improvement", "--post-comment"])

    assert result.exit_code == 0
    assert "Posted issue comment: https://example/1" in result.output


def test_pr_review_with_post_comment(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-pr-event.json"))
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setattr("karakana.tools.github_api.GitHubApiClient.post_issue_comment", lambda self, issue_number, body: {"html_url": f"https://example/pr/{issue_number}"})

    result = CliRunner().invoke(app, ["github", "pr-review", "--project", "karakana", "--skill", "github-pr-review", "--post-comment"])

    assert result.exit_code == 0
    assert "Posted PR comment: https://example/pr/7" in result.output
