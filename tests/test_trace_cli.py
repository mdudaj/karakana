from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def create_trace(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(command="plan", project="karakana", skill="karakana-self-improvement")
    trace.finish("success")
    store.save(trace)
    return trace


def test_trace_list_latest_show_summary(tmp_path, monkeypatch):
    trace = create_trace(tmp_path)
    monkeypatch.chdir(tmp_path)

    runner = CliRunner()
    list_result = runner.invoke(app, ["trace", "list"])
    latest_result = runner.invoke(app, ["trace", "latest"])
    show_result = runner.invoke(app, ["trace", "show", trace.run_id])
    summary_result = runner.invoke(app, ["trace", "summary", trace.run_id])

    assert list_result.exit_code == 0
    assert trace.run_id in list_result.output
    assert latest_result.exit_code == 0
    assert f'"run_id": "{trace.run_id}"' in latest_result.output
    assert show_result.exit_code == 0
    assert '"command": "plan"' in show_result.output
    assert summary_result.exit_code == 0
    assert "# Karakana Run Summary" in summary_result.output
