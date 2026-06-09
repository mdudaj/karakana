from typer.testing import CliRunner

from karakana.cli import app
from tests.test_action_extractor import write_response


def test_action_cli_extract_list_show_latest(tmp_path, monkeypatch):
    response = write_response(tmp_path, "## Next Actions\n- Codex task: Implement a safe parser.\n", {"status": "passed", "blocked": False})
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    extract = runner.invoke(app, ["action", "extract", "--from-response", str(response)])
    listed = runner.invoke(app, ["action", "list"])
    latest = runner.invoke(app, ["action", "latest"])
    action_run_id = next((tmp_path / ".karakana" / "actions").glob("*actions-*")).name
    shown = runner.invoke(app, ["action", "show", action_run_id])

    assert extract.exit_code == 0
    assert "Actions: 1" in extract.output
    assert listed.exit_code == 0
    assert action_run_id in listed.output
    assert "# Karakana Action Bundle" in latest.output
    assert "# Karakana Action Bundle" in shown.output
