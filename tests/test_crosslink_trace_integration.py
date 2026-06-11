from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_crosslink_scan_creates_trace():
    runner = CliRunner()
    result = runner.invoke(app, ["crosslink", "scan", "--workspace", "default"])

    assert result.exit_code == 0
    trace = TraceStore(Path.cwd()).latest()
    assert trace is not None
    assert trace.command == "crosslink scan"
    assert "crosslink_id" in trace.outputs
