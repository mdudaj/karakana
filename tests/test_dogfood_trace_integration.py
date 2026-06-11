from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_dogfood_run_creates_trace():
    result = CliRunner().invoke(app, ["dogfood", "run", "--project", "karakana", "--skillpack", "karakana"])

    assert result.exit_code == 0
    trace = TraceStore(Path.cwd()).latest()
    assert trace is not None
    assert trace.command == "dogfood run"
    assert "dogfood_id" in trace.outputs
    artifact_paths = trace.outputs.get("artifacts") or []
    assert any("model-response.md" in path for path in artifact_paths)
    assert any(artifact.kind == "dogfood_nested_artifact" for artifact in trace.artifacts)
