from typer.testing import CliRunner

from karakana.cli import app
from tests.test_eval_runner import write_eval, write_memory_tree, write_skill


def test_eval_cli_list_show_run_latest_and_report(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    write_eval(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    list_result = runner.invoke(app, ["eval", "list"])
    show_result = runner.invoke(app, ["eval", "show", "demo"])
    run_result = runner.invoke(app, ["eval", "run", "--suite", "safety"])
    latest_result = runner.invoke(app, ["eval", "latest"])

    assert list_result.exit_code == 0
    assert "demo" in list_result.output
    assert show_result.exit_code == 0
    assert '"id": "demo"' in show_result.output
    assert run_result.exit_code == 0
    assert "Status: passed" in run_result.output
    assert latest_result.exit_code == 0
    assert "# Karakana Evaluation Report" in latest_result.output

    eval_run_id = next((tmp_path / ".karakana" / "eval-runs").glob("*eval-*")).name
    report_result = runner.invoke(app, ["eval", "report", eval_run_id])
    assert report_result.exit_code == 0
    assert "Demo" in report_result.output
