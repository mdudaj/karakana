from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app


def test_github_issue_triage_cli(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-issue-event.json"))

    result = CliRunner().invoke(
        app,
        ["github", "issue-triage", "--project", "karakana", "--skill", "karakana-self-improvement"],
    )

    output = root / ".karakana" / "issue-triage.md"
    assert result.exit_code == 0
    assert f"Issue triage prompt written to: {output}" in result.output
    assert "Improve memory validation output" in output.read_text(encoding="utf-8")


def test_github_pr_review_cli(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-pr-event.json"))

    result = CliRunner().invoke(
        app,
        ["github", "pr-review", "--project", "karakana", "--skill", "github-pr-review"],
    )

    output = root / ".karakana" / "pr-review.md"
    assert result.exit_code == 0
    assert f"PR review prompt written to: {output}" in result.output
    assert "Add skill validator tests" in output.read_text(encoding="utf-8")


def test_github_ci_failure_cli():
    root = Path.cwd()

    result = CliRunner().invoke(
        app,
        [
            "github",
            "ci-failure",
            "--project",
            "karakana",
            "--skill",
            "ci-failure-analysis",
            "--log-file",
            "tests/fixtures/sample-ci-failure.log",
        ],
    )

    output = root / ".karakana" / "ci-failure-analysis.md"
    assert result.exit_code == 0
    assert f"CI failure analysis prompt written to: {output}" in result.output
    assert "AssertionError" in output.read_text(encoding="utf-8")


def test_github_ci_failure_requires_log_file():
    result = CliRunner().invoke(
        app,
        ["github", "ci-failure", "--project", "karakana", "--skill", "ci-failure-analysis"],
    )

    assert result.exit_code == 1
    assert "--log-file is required" in result.output


def test_workflow_files_exist():
    root = Path.cwd()

    assert (root / ".github" / "workflows" / "issue-triage.yml").exists()
    assert (root / ".github" / "workflows" / "pr-review.yml").exists()
    assert (root / ".github" / "workflows" / "skill-eval.yml").exists()
    assert (root / ".github" / "workflows" / "ci-failure-analysis.yml").exists()
