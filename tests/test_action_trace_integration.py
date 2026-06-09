import json

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore
from tests.test_action_extractor import write_response


def test_action_extract_creates_trace_and_redacts(tmp_path, monkeypatch):
    response = write_response(tmp_path, "TODO: Update documentation with token=abc.\n", {"status": "passed", "blocked": False})
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["action", "extract", "--from-response", str(response)])
    trace = TraceStore(tmp_path).latest()

    assert result.exit_code == 0
    assert trace.command == "action extract"
    assert trace.outputs["actions_count"] == 1
    assert "abc" not in json.dumps(trace.to_dict())
