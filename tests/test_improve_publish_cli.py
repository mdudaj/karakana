from karakana.improvement.schemas import ImprovementProposal, ProposedChange
from karakana.improvement.store import ProposalStore
from karakana.traces.store import TraceStore
from typer.testing import CliRunner

from karakana.cli import app


def seed_proposal(tmp_path, risk="low"):
    proposal = ImprovementProposal(
        proposal_id="20260101-000000-improve-test01",
        project="karakana",
        status="ready_for_review",
        created_at="2026-01-01T00:00:00+00:00",
        source_run_ids=["run"],
        summary="Improve docs",
        changes=[
            ProposedChange(
                target_path="ubongo/projects/karakana/open-issues.md",
                change_type="memory_update",
                title="Improve docs",
                rationale="Because",
                proposed_content="content",
                risk_level=risk,
            )
        ],
    )
    ProposalStore(tmp_path).save(proposal)
    return proposal.proposal_id


def test_publish_dry_run(tmp_path, monkeypatch):
    proposal_id = seed_proposal(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "publish", proposal_id])

    assert result.exit_code == 0
    assert "Dry run: no GitHub write performed." in result.output


def test_publish_create_issue(monkeypatch, tmp_path):
    proposal_id = seed_proposal(tmp_path, risk="high")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    captured = {}

    def fake_create_issue(self, title, body, labels=None):
        captured["labels"] = labels
        return {"html_url": "https://example/issue"}

    monkeypatch.setattr("karakana.tools.github_api.GitHubApiClient.create_issue", fake_create_issue)

    result = CliRunner().invoke(app, ["improve", "publish", proposal_id, "--create-issue"])

    assert result.exit_code == 0
    assert "Created GitHub issue: https://example/issue" in result.output
    assert "risk:high" in captured["labels"]


def test_publish_create_pr_safety_rejects_main(monkeypatch, tmp_path):
    proposal_id = seed_proposal(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")

    result = CliRunner().invoke(app, ["improve", "publish", proposal_id, "--create-pr", "--head", "main"])

    assert result.exit_code == 1
    assert "GitHub PR safety checks failed." in result.output


def test_publish_write_trace_created(tmp_path, monkeypatch):
    proposal_id = seed_proposal(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "publish", proposal_id])

    latest = TraceStore(tmp_path).latest()
    assert result.exit_code == 0
    assert latest.command == "improve publish"
    assert latest.outputs["dry_run"] is True
