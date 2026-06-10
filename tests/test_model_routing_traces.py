from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_model_route_records_trace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "route", "--task-type", "planning", "--provider", "mock", "--model", "mock-model"])
    trace = TraceStore(tmp_path).latest()

    assert result.exit_code == 0
    assert trace.outputs["selected_provider"] == "mock"
    assert trace.outputs["selected_model"] == "mock-model"
    assert trace.outputs["manual_override"] is True
    assert trace.outputs["cost_tier"] == "none"
