from pathlib import Path

from karakana.improvement.schemas import ImprovementProposal, ProposedChange
from karakana.improvement.store import ProposalStore
from typer.testing import CliRunner

from karakana.cli import app


def seed_proposal(tmp_path, target="ubongo/projects/karakana/open-issues.md", risk="low", content="new content"):
    proposal = ImprovementProposal(
        proposal_id="20260101-000000-improve-apply1",
        project="karakana",
        status="ready_for_review",
        created_at="2026-01-01T00:00:00+00:00",
        source_run_ids=["run"],
        summary="Apply test",
        changes=[
            ProposedChange(
                target_path=target,
                change_type="memory_update",
                title="Apply",
                rationale="Because",
                proposed_content=content,
                risk_level=risk,
            )
        ],
    )
    ProposalStore(tmp_path).save(proposal)
    return proposal.proposal_id


def test_apply_dry_run(tmp_path, monkeypatch):
    proposal_id = seed_proposal(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "apply", proposal_id])

    assert result.exit_code == 0
    assert "Dry run: no files modified." in result.output
    assert not (tmp_path / "ubongo" / "projects" / "karakana" / "open-issues.md").exists()


def test_apply_write_allowed_path(tmp_path, monkeypatch):
    target = tmp_path / "ubongo" / "projects" / "karakana" / "open-issues.md"
    target.parent.mkdir(parents=True)
    target.write_text("old", encoding="utf-8")
    proposal_id = seed_proposal(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "apply", proposal_id, "--write"])

    assert result.exit_code == 0
    assert target.read_text(encoding="utf-8") == "new content"
    assert (tmp_path / ".karakana" / "proposals" / proposal_id / "backups" / "ubongo__projects__karakana__open-issues.md.bak").exists()


def test_apply_refuses_env(tmp_path, monkeypatch):
    proposal_id = seed_proposal(tmp_path, target=".env")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "apply", proposal_id, "--write"])

    assert result.exit_code == 1
    assert "Refusing to modify env file" in result.output


def test_apply_refuses_workflow(tmp_path, monkeypatch):
    proposal_id = seed_proposal(tmp_path, target=".github/workflows/test.yml")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "apply", proposal_id, "--write"])

    assert result.exit_code == 1
    assert "Refusing to modify blocked path" in result.output


def test_apply_skips_high_risk(tmp_path, monkeypatch):
    proposal_id = seed_proposal(tmp_path, risk="high")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "apply", proposal_id, "--write"])

    assert result.exit_code == 0
    assert "Applied 0 file(s)." in result.output
