import json
from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore
from tests.test_action_extractor import write_response


def test_action_extract_creates_trace_and_redacts(tmp_path, monkeypatch):
    secret = "fixture-action-trace-secret"
    response = write_response(tmp_path, f"TODO: Update documentation with token={secret}.\n", {"status": "passed", "blocked": False})
    # The old short sentinel also occurred in valid random artifact IDs in CI.
    action_run_id = "20261020-075528-actions-abc220"
    monkeypatch.setattr("karakana.actions.extractor.generate_action_run_id", lambda: action_run_id)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["action", "extract", "--from-response", str(response)])
    trace = TraceStore(tmp_path).latest()

    assert result.exit_code == 0
    assert trace.command == "action extract"
    assert trace.outputs["actions_count"] == 1
    assert "handoff_markdown" in trace.outputs
    assert trace.outputs["action_run_id"] == action_run_id
    assert secret not in json.dumps(trace.to_dict())
    persisted_actions = Path(trace.outputs["actions_json"]).read_text(encoding="utf-8")
    assert secret not in persisted_actions
    assert "token=[REDACTED]" in persisted_actions
