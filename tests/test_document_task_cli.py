import json
from pathlib import Path
import subprocess
import sys
import pytest

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


def test_explicit_s2_commands_exist_without_live_or_overwrite_options():
    runner = CliRunner()
    group = runner.invoke(app, ['docs', 'content', '--help'])
    assert group.exit_code == 0 and 'prepare' in group.output
    for name in ('check', 'verify'):
        assert runner.invoke(app, ['docs', 'content', name, '--help']).exit_code == 0
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


@pytest.mark.parametrize('case,expected', [('check_complete',0),('check_incomplete',2),('check_unsupported',2),('check_missing',2),
                                         ('verify_current',0),('verify_stale',2),('verify_incomplete',2),('verify_foreign',2)])
def test_actual_subprocess_assessment_json_and_text_state_matrix(tmp_path,case,expected):
    from tests.document_task_support import make_assessment
    from karakana.document_tasks import check_task
    request,_=make_assessment(tmp_path)
    request['task']['scope']='[red]Literal scoped review[/red]';save_request(tmp_path,request)
    if case.endswith('incomplete'):
        p=tmp_path/'req.md';p.write_text(p.read_text().replace('## Purpose and scope','## Missing purpose'))
    if case=='check_unsupported':(tmp_path/'req.md').write_text('---\ntitle: native source\n---\n# Native\n')
    if case=='check_missing':request['context']=None;save_request(tmp_path,request)
    command='verify' if case.startswith('verify') else 'check'
    arguments=['docs','content',command,'--request','request.json']
    if command=='verify':
        old=check_task(tmp_path,'request.json');arguments+=['--bundle',old['run']['bundle']]
        if case=='verify_stale':(tmp_path/'docs/guide.md').write_text('Changed selected guide')
        elif case=='verify_foreign':
            p=tmp_path/old['run']['bundle']/'result.json';r=json.loads(p.read_text());r['task']['project']='foreign';p.write_text(json.dumps(r))
    for format in ['json','text']:
        r=subprocess.run([sys.executable,'-c','from karakana.cli import app; app()',*arguments,'--format',format],
                         cwd=tmp_path,text=True,capture_output=True,timeout=30)
        assert r.returncode==expected,(r.stdout,r.stderr)
        assert not r.stderr and '\x1b' not in r.stdout
        if format=='json':
            result=json.loads(r.stdout)
            assert result['operation']==command
            if result['content_report']:
                assert result['content_report']['acceptance']=='not_assessed'
                assert result['content_report']['review_required'] is True
            if case=='verify_stale':
                assert result['content_report']['verification']=='current'
                assert result['freshness']['saved_bundle']=='stale_or_mismatched'
        else:
            assert r.stdout.startswith('[red]Literal scoped review[/red]')
            assert 'Review' in r.stdout and 'acceptance' in r.stdout


@pytest.mark.parametrize('command',['check','verify'])
def test_s2_syntax_errors_are_stderr_only_and_no_force_or_live_options(command):
    runner=CliRunner()
    for flags in [[],['--format','invalid'],['--live'],['--overwrite'],['--force']]:
        result=runner.invoke(app,['docs','content',command,*flags])
        assert result.exit_code==2 and result.stdout=='' and result.stderr
