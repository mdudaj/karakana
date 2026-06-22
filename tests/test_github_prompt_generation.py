from pathlib import Path

from karakana.tools.github import GitHubPromptGenerator, reduce_ci_log


def test_issue_triage_prompt_generation(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-issue-event.json"))
    monkeypatch.setenv("GITHUB_EVENT_NAME", "issues")
    monkeypatch.setenv("GITHUB_REPOSITORY", "mdudaj/karakana")

    prompt = GitHubPromptGenerator(root).build_issue_triage_prompt(
        project="karakana",
        skill="karakana-self-improvement",
    )

    assert "# Karakana GitHub Task" in prompt
    assert "issue_triage" in prompt
    assert "Improve memory validation output" in prompt
    assert "karakana-self-improvement" in prompt
    assert "Do not post GitHub comments automatically" in prompt


def test_pr_review_prompt_generation(monkeypatch):
    root = Path.cwd()
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(root / "tests" / "fixtures" / "github-pr-event.json"))
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request")

    prompt = GitHubPromptGenerator(root).build_pr_review_prompt(
        project="karakana",
        skill="github-pr-review",
    )

    assert "pr_review" in prompt
    assert "Add skill validator tests" in prompt
    assert "github-pr-review" in prompt
    assert "blocking issues" in prompt


def test_ci_failure_prompt_generation(monkeypatch):
    root = Path.cwd()
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)

    prompt = GitHubPromptGenerator(root).build_ci_failure_prompt(
        project="karakana",
        skill="ci-failure-analysis",
        log_file=root / "tests" / "fixtures" / "sample-ci-failure.log",
    )

    assert "ci_failure_analysis" in prompt
    assert "Traceback" in prompt
    assert "AssertionError" in prompt
    assert "ci-failure-analysis" in prompt


def test_reduce_ci_log_keeps_failure_lines():
    reduced = reduce_ci_log("ok\nFAILED test\nTraceback here\nall done")

    assert "FAILED test" in reduced
    assert "Traceback here" in reduced
