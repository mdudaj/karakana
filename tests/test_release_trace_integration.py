from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_release_command_creates_trace():
    result = CliRunner().invoke(app, ["release", "check"])

    assert result.exit_code == 0
    trace = TraceStore(Path.cwd()).latest()
    assert trace is not None
    assert trace.command == "release check"
    assert "release_check_id" in trace.outputs

