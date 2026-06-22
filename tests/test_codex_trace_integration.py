from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_capture_diff_creates_trace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["codex", "capture-diff"])
    trace = TraceStore(tmp_path).latest()

    assert result.exit_code == 0
    assert trace.command == "codex capture-diff"
    assert "patch_run_id" in trace.outputs
