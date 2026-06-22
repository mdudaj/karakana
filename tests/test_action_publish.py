from typer.testing import CliRunner

from karakana.cli import app
from tests.test_action_extractor import write_response


def test_action_publish_dry_run(tmp_path, monkeypatch):
    response = write_response(tmp_path, "Create issue: Track safe follow-up.\n", {"status": "passed", "blocked": False})
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(app, ["action", "extract", "--from-response", str(response)])
    action_run_id = next((tmp_path / ".karakana" / "actions").glob("*actions-*")).name

    result = runner.invoke(app, ["action", "publish", action_run_id])

    assert result.exit_code == 0
    assert "Dry run: no actions published." in result.output
    assert "Would create issues: 1" in result.output


def test_action_publish_create_codex_tasks(tmp_path, monkeypatch):
    response = write_response(tmp_path, "Codex task: Implement safe follow-up.\n", {"status": "passed", "blocked": False})
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(app, ["action", "extract", "--from-response", str(response)])
    action_run_id = next((tmp_path / ".karakana" / "actions").glob("*actions-*")).name

    result = runner.invoke(app, ["action", "publish", action_run_id, "--create-codex-tasks"])

    assert result.exit_code == 0
    assert (tmp_path / ".karakana" / "codex-tasks" / action_run_id).exists()
