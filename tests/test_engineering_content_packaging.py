"""Qualify actual wheel resources/CLI outside the editable source checkout."""

import email
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def invoke(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=120)
    assert result.returncode == 0, result.stdout[-2500:] + result.stderr[-2500:]
    return result


def test_built_wheel_resources_cli_and_optional_parser(isolated_repo, tmp_path):
    wheels, site, working = (tmp_path / n for n in ('wheels', 'site', 'outside'))
    working.mkdir()
    invoke([sys.executable, '-m', 'pip', 'wheel', '--no-deps', '--no-build-isolation', '--no-index',
            '--wheel-dir', str(wheels), str(isolated_repo)], working)
    wheel = next(wheels.glob('karakana-*.whl'))
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert 'karakana/content_profiles/requirements-0.1.json' in names
        assert 'karakana/content_profiles/system-design-0.1.json' in names
        metadata = email.message_from_bytes(archive.read(next(n for n in names if n.endswith('.dist-info/METADATA'))))
        deps = metadata.get_all('Requires-Dist')
        parser_deps = [d for d in deps if d.startswith('markdown-it-py')]
        assert len(parser_deps) == 2 and all('extra ==' in d for d in parser_deps)
        assert any('"content"' in d for d in parser_deps) and any('"dev"' in d for d in parser_deps)
        assert not any('"workbooks"' in d for d in parser_deps)
    invoke([sys.executable, '-m', 'pip', 'install', '--no-deps', '--no-index', '--target', str(site), str(wheel)], working)
    for key, source in [('req', 'skills/engineering-requirements/assets/requirements-example.md'),
                        ('design', 'skills/engineering-design-records/assets/system-design-example.md')]:
        shutil.copyfile(ROOT / source, working / f'{key}.md')
    context = {'context_version': '0.1', 'namespace': 'example', 'documents': [
        {'key': 'req', 'path': 'req.md', 'format': 'narrative-0.1', 'profile': {'id': 'requirements', 'version': '0.1'}},
        {'key': 'design', 'path': 'design.md', 'format': 'narrative-0.1', 'profile': {'id': 'system-design', 'version': '0.1'}, 'requirements': ['req']}]}
    (working / 'context.json').write_text(json.dumps(context))
    shutil.copytree(ROOT / 'tests/fixtures/engineering_content', working / 'tests/fixtures/engineering_content')
    contexts = working / 'docs/skills/engineering-artifact-catalogue/content-checks'
    contexts.mkdir(parents=True)
    for name in ('tailored', 'evidence'):
        shutil.copyfile(ROOT / f'docs/skills/engineering-artifact-catalogue/content-checks/{name}.json', contexts / f'{name}.json')
    code = '''
import sys, json
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from importlib.resources import files
from karakana.tools import engineering_content
assert Path(engineering_content.__file__).is_relative_to(Path(sys.argv[1]))
for name in ('requirements', 'system-design'):
    assert json.loads(files('karakana.content_profiles').joinpath(name+'-0.1.json').read_bytes())['profile_id'] == name
assert engineering_content.main(['--root', '.', 'check', '--context', 'context.json', '--format', 'json']) == 0
import contextlib, io
for name in ('tailored', 'evidence'):
    context = Path('docs/skills/engineering-artifact-catalogue/content-checks') / (name + '.json')
    result = engineering_content.check_content(Path.cwd(), context)
    assert result.ok, result.to_dict()['findings']
    report = Path(name + '-report.json')
    report.write_text(json.dumps(result.to_dict()))
    assert engineering_content.verify_report(Path.cwd(), context, report).to_dict()['verification'] == 'current'
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        assert engineering_content.main(['--root', '.', 'verify', '--context', str(context), '--report', str(report), '--format', 'json']) == 0
    assert json.loads(capture.getvalue())['verification'] == 'current'
'''
    result = invoke([sys.executable, '-I', '-c', code, str(site)], working)
    report = json.loads(result.stdout)
    assert report['completeness'] == 'complete'
    assert len(report['manifest']['profiles']) == 2
    # Exercise an actually blocked import in a new subprocess, not a string check.
    blocked = '''
import sys, json, importlib.abc
from pathlib import Path
sys.path.insert(0, sys.argv[1])
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'markdown_it' or fullname.startswith('markdown_it.') or fullname == 'openpyxl':
            raise ModuleNotFoundError('blocked optional module')
sys.meta_path.insert(0, Block())
from karakana.tools.engineering_content import check_content
from karakana.tools.engineering_artifacts import parse_document
text = '\\n'.join(['---','contract_version: "0.1"','namespace: "example"','document_id: "D-1"','document_type: "document"','content_version: "0.1"','status: "draft"','owner: "unconfirmed"','requested_action: "review"','source_authority: "authored Markdown"','---','# Narrative','No structured records.'])
Path('p02.md').write_text(text)
assert not parse_document(Path.cwd(),Path('p02.md'),'example')['tables']
result=check_content(Path.cwd(),Path('context.json')).to_dict()
assert result['completeness']=='unsupported'
assert any(f['rule_id']=='CP-DEPENDENCY-001' for f in result['findings'])
print('installed wheel: optional import refused; P02 Markdown still works')
'''
    assert 'P02 Markdown still works' in invoke([sys.executable, '-I', '-c', blocked, str(site)], working).stdout
