from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_workspace_status_creates_trace():
    result = CliRunner().invoke(app, ["workspace", "status", "--workspace", "default"])

    assert result.exit_code == 0
    trace = TraceStore(Path.cwd()).latest()
    assert trace.command == "workspace status"
    assert trace.outputs["status_collected"] is True
