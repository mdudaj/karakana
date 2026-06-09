from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def seed_trace(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(command="plan", project="karakana", skill="missing", task_type="planning")
    trace.errors.append("Skill not found: skills/missing/SKILL.md")
    trace.finish("failed")
    store.save(trace)
    return trace


def test_improve_cli_propose_list_show_latest(tmp_path, monkeypatch):
    seed_trace(tmp_path)
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    propose = runner.invoke(app, ["improve", "propose", "--project", "karakana", "--since", "7 days"])
    assert propose.exit_code == 0
    assert "Improvement proposal written to:" in propose.output

    proposal_id = (tmp_path / ".karakana" / "proposals" / "latest").read_text(encoding="utf-8").strip()
    assert (tmp_path / ".karakana" / "proposals" / proposal_id / "proposal.json").exists()
    assert (tmp_path / ".karakana" / "proposals" / proposal_id / "proposal.md").exists()

    list_result = runner.invoke(app, ["improve", "list"])
    show_result = runner.invoke(app, ["improve", "show", proposal_id])
    latest_result = runner.invoke(app, ["improve", "latest"])

    assert proposal_id in list_result.output
    assert "# Karakana Self-Improvement Proposal" in show_result.output
    assert "# Karakana Self-Improvement Proposal" in latest_result.output

    latest_trace = TraceStore(tmp_path).latest()
    assert latest_trace.command == "improve propose"
    assert latest_trace.status == "success"
    assert latest_trace.outputs["proposal_id"] == proposal_id


def test_improve_cli_json_output(tmp_path, monkeypatch):
    seed_trace(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["improve", "propose", "--project", "karakana", "--json"])

    assert result.exit_code == 0
    assert '"proposal_id"' in result.output
