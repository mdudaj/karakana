from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_ingest_command_creates_trace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("architecture decision command\n", encoding="utf-8")

    result = CliRunner().invoke(app, ["ingest", "file", "README.md", "--project", "karakana", "--classify"])

    assert result.exit_code == 0
    trace = TraceStore(tmp_path).latest()
    assert trace.command == "ingest file"
    assert trace.outputs["candidate_count"] == 1
