from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_requirements_commands_create_trace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["requirements", "prd", "--from-note", "Add requirements trace coverage", "--no-current-skillpack"])

    assert result.exit_code == 0
    trace = TraceStore(tmp_path).latest()
    assert trace.command == "requirements prd"
    assert trace.outputs["req_id"]
