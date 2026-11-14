import json
from pathlib import Path
import subprocess
import sys

from typer.testing import CliRunner

from karakana.cli import app
from karakana.document_tasks.report import render_text
from tests.document_task_support import make_task, save_request


def test_cli_real_text_and_json_have_domain_states_and_no_markup(tmp_path):
    request = make_task(tmp_path)
    request["task"]["scope"] = "[red]Literal selected scope[/red]"; save_request(tmp_path, request)
    runner = CliRunner()
    text = runner.invoke(app, ["docs", "content", "prepare", "--root", str(tmp_path), "--request", "request.json"])
    assert text.exit_code == 0, text.output
    assert "[red]Literal selected scope[/red]" in text.stdout
    assert "\x1b" not in text.stdout and "not assessed" in text.stdout
    raw = runner.invoke(app, ["docs", "content", "prepare", "--root", str(tmp_path), "--request", "request.json", "--format", "json"])
    assert raw.exit_code == 0, raw.output
    result = json.loads(raw.stdout)
    assert result["outcome"] == "prepared" and result["content_report"] is None
    assert not raw.stderr and "\x1b" not in raw.stdout
    assert json.loads((tmp_path / result["run"]["bundle"] / "result.json").read_text()) == result


def test_cli_syntax_and_domain_failure_channels(tmp_path):
    make_task(tmp_path); runner = CliRunner()
    missing = runner.invoke(app, ["docs", "content", "prepare", "--format", "json"])
    assert missing.exit_code == 2 and missing.stdout == "" and missing.stderr
    malformed = tmp_path / "bad.json"; malformed.write_text('{"duplicated":1,"duplicated":2}')
    bad = runner.invoke(app, ["docs", "content", "prepare", "--root", str(tmp_path), "--request", "bad.json", "--format", "json"])
    assert bad.exit_code == 2
    result = json.loads(bad.stdout)
    assert result["outcome"] == "blocked" and result["task"] is None and result["diagnostics"]
    assert "Traceback" not in bad.output


def test_subprocess_outside_checkout_emits_one_json_object(tmp_path):
    make_task(tmp_path)
    result = subprocess.run([sys.executable, '-c', 'from karakana.cli import app; app()', 'docs', 'content', 'prepare',
                             '--request', 'request.json', '--format', 'json'], cwd=tmp_path,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["outcome"] == "prepared"
    assert not result.stderr


def test_s2_live_and_overwrite_options_are_not_advertised_or_accepted():
    runner = CliRunner()
    group = runner.invoke(app, ['docs', 'content', '--help'])
    assert group.exit_code == 0 and 'prepare' in group.output
    for name in ('check', 'verify'):
        assert runner.invoke(app, ['docs', 'content', name, '--help']).exit_code == 2
    for option in ('--live', '--force', '--overwrite'):
        assert runner.invoke(app, ['docs', 'content', 'prepare', option]).exit_code == 2


def test_error_text_escapes_terminal_control_sequences():
    from karakana.document_tasks.report import new_result, add_failure
    from karakana.document_tasks.schemas import TaskError
    result = new_result('test', '2026-11-14T00:00:00+00:00')
    add_failure(result, TaskError('Literal\x1b[31m error'))
    text = render_text(result)
    assert '\x1b' not in text and '\\u001b' in text
    assert 'not assessed' in text
