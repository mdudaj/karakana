"""Actual installed-wheel preparation outside the checkout, with optional imports blocked."""

import json
from pathlib import Path
import subprocess
import sys
import zipfile

from tests.document_task_support import make_task


def invoke(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=120)
    assert result.returncode == 0, result.stdout[-2000:] + result.stderr[-2000:]
    return result


def test_wheel_prepares_without_parser_and_does_not_invent_checkout_assets(isolated_repo, tmp_path):
    wheels, site, working = (tmp_path / name for name in ('wheels', 'site', 'outside'))
    working.mkdir(); make_task(working)
    invoke([sys.executable, '-m', 'pip', 'wheel', '--no-deps', '--no-build-isolation', '--no-index',
            '--wheel-dir', str(wheels), str(isolated_repo)], working)
    wheel = next(wheels.glob('karakana-*.whl'))
    with zipfile.ZipFile(wheel) as archive:
        assert 'karakana/document_tasks/prepare.py' in archive.namelist()
        assert not any(name.startswith('skills/') for name in archive.namelist())
    invoke([sys.executable, '-m', 'pip', 'install', '--no-deps', '--no-index', '--target', str(site), str(wheel)], working)
    code = r'''
import sys, json, importlib.abc
from pathlib import Path
sys.path.insert(0, sys.argv[1])
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in {'markdown_it', 'openpyxl'} or fullname.startswith(('markdown_it.', 'openpyxl.')):
            raise AssertionError('Preparation attempted optional import: ' + fullname)
sys.meta_path.insert(0, Block())
from karakana.document_tasks import prepare_task
import karakana.document_tasks.prepare as module
assert Path(module.__file__).is_relative_to(Path(sys.argv[1]))
result=prepare_task(Path.cwd(), 'request.json')
assert result['outcome']=='prepared', result['diagnostics']
assert result['content_report'] is None
assert json.loads((Path(result['run']['bundle'])/'result.json').read_text())==result
from typer.testing import CliRunner
from karakana.cli import app
cli=CliRunner().invoke(app,['docs','content','prepare','--request','request.json','--format','json'])
assert cli.exit_code==0, cli.output
assert json.loads(cli.stdout)['outcome']=='prepared'
assert 'markdown_it' not in sys.modules and 'karakana.tools.engineering_content' not in sys.modules
request=json.loads(Path('request.json').read_text())
request['resources'][0]={'artifact_type':'requirements','role':'guide',
 'path':'skills/engineering-requirements/references/requirements-template-guide.md','revision':'0.1'}
Path('request.json').write_text(json.dumps(request))
missing=prepare_task(Path.cwd(),'request.json')
assert missing['outcome']=='blocked' and missing['content_report'] is None
print('Installed wheel: real API/CLI prepare; parser absent; missing checkout asset refused.')
'''
    assert 'missing checkout asset refused' in invoke([sys.executable, '-I', '-c', code, str(site)], working).stdout
