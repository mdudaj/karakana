"""Actual producer-to-consumer state, scope and source-boundary checks."""

from copy import deepcopy
import json
import shutil

import pytest

from karakana.document_tasks import check_task
from karakana.document_tasks.report import render_text
from karakana.content_profiles.schemas import ContentReport, ContentError
from karakana.tools import engineering_content as m2
from tests.document_task_support import make_assessment, save_request, save_context
from tests.test_engineering_content_context import observations, claim, loc


@pytest.mark.parametrize('version', ['0.1', '0.2'])
@pytest.mark.parametrize('both', [False, True])
def test_actual_profiles_and_context_versions_preserve_raw_report_and_sources(tmp_path, version, both):
    make_assessment(tmp_path, version=version, both=both)
    before = {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    result = check_task(tmp_path, 'request.json')
    assert result['outcome'] == 'checked', result['diagnostics']
    report = result['content_report']
    assert report['completeness'] == 'complete' and report['readiness'] == 'unresolved'
    assert report['review_required'] and report['acceptance'] == 'not_assessed'
    assert len(report['documents']) == (2 if both else 1)
    assert report['open_acceptance_items']
    bundle = tmp_path / result['run']['bundle']
    assert json.loads((bundle / 'result.json').read_text()) == result
    assert json.loads((bundle / 'content-report.json').read_text()) == report
    assert m2.verify_report(tmp_path, 'context.json', (bundle / 'content-report.json').relative_to(tmp_path)).to_dict()['verification'] == 'current'
    assert result['freshness'] == {'inputs': 'current', 'saved_bundle': 'not_assessed'}
    assert all(p.read_bytes() == raw for p, raw in before.items())


@pytest.mark.parametrize('fault,expected', [('none','blocked'),('missing','blocked'),('format','unsupported'),
                                          ('profile','unsupported'),('version','unsupported'),('links01','blocked'),
                                          ('scope','blocked'),('source','failed'),('frontmatter','unsupported')])
def test_missing_unsupported_and_scope_inputs_do_not_succeed(tmp_path, fault, expected):
    request, context = make_assessment(tmp_path)
    if fault == 'none': request['context'] = None
    elif fault == 'missing': request['context'] = 'missing.json'
    elif fault == 'format': context['documents'][0]['format'] = 'frontmatter'
    elif fault == 'profile': context['documents'][0]['profile']['id'] = 'adr'
    elif fault == 'version': context['documents'][0]['profile']['version'] = '99'
    elif fault == 'links01': context.update(context_version='0.1', links=[])
    elif fault == 'scope': request['task']['artifact_types'] = ['requirements']
    elif fault == 'source': (tmp_path / 'req.md').unlink()
    elif fault == 'frontmatter': (tmp_path / 'req.md').write_text('---\ntitle: native\n---\n# Source\n')
    save_request(tmp_path, request); save_context(tmp_path, context)
    result = check_task(tmp_path, 'request.json')
    assert result['outcome'] == expected, result
    assert result['content_report'] is not None if fault in {'source', 'frontmatter'} else result['content_report'] is None
    assert result['outcome'] not in {'checked', 'verified'}


def test_context_only_use_does_not_require_or_read_planning_assets(tmp_path, monkeypatch):
    from karakana.document_tasks.inputs import CapturedInputs
    request, _ = make_assessment(tmp_path, both=False)
    request['resources'] = []; save_request(tmp_path, request)
    shutil.rmtree(tmp_path / 'skills'); shutil.rmtree(tmp_path / 'ubongo')
    original = CapturedInputs.read; reads = []
    def read(self, path, *a, **kw):
        reads.append(path)
        return original(self, path, *a, **kw)
    monkeypatch.setattr(CapturedInputs, 'read', read)
    assert check_task(tmp_path, 'request.json')['outcome'] == 'checked'
    assert not any(p.startswith(('skills/', 'ubongo/', 'prompts/')) for p in reads)
    assert 'docs/guide.md' not in reads and 'docs/unselected.md' not in reads


def test_optional_parser_absence_is_an_unsupported_assessment(tmp_path, monkeypatch):
    make_assessment(tmp_path)
    def missing(): raise ContentError('Select the installed content extra for narrative checking.', unsupported=True, rule='CP-DEPENDENCY-001')
    monkeypatch.setattr(m2, 'parser', missing)
    result = check_task(tmp_path, 'request.json')
    assert result['outcome'] == 'unsupported'
    assert result['content_report']['completeness'] == 'unsupported'
    assert result['content_report']['findings'][0]['rule_id'] == 'CP-DEPENDENCY-001'


@pytest.mark.parametrize('field,value', [('report_version','9'),('readiness','ready'),('acceptance','accepted'),
    ('review_required',False),('completeness','incomplete'),('manifest',{}),('coverage',{}),('documents',None),
    ('documents',[]),('namespace','other'),('generated_utc','2026-11-14'),('findings',[{}]),
    ('open_acceptance_items',[{}]),('assessment_digest',None)])
def test_invalid_or_conflicting_producer_fields_never_become_success(tmp_path, monkeypatch, field, value):
    make_assessment(tmp_path)
    data = m2.check_content(tmp_path, 'context.json').to_dict(); data[field] = value
    monkeypatch.setattr(m2, 'check_content', lambda *a: ContentReport(data))
    result = check_task(tmp_path, 'request.json')
    assert result['outcome'] == 'unsupported' and result['content_report'] is None
    assert result['diagnostics'][0]['code'] == 'DT-PRODUCER-001'


@pytest.mark.parametrize('state', ['blocked','not_ready'])
def test_process_success_foreign_payload_retains_only_known_typed_state(tmp_path, monkeypatch, state):
    make_assessment(tmp_path)
    monkeypatch.setattr(m2, 'check_content', lambda *a: {'exit_code':0,'status':state,'private':'not printed'})
    result = check_task(tmp_path, 'request.json')
    assert result['outcome'] == 'unsupported' and result['content_report'] is None
    assert result['diagnostics'][0]['producer_state'] == {'status': state}
    assert state in render_text(result)
    assert 'not printed' not in json.dumps(result)


def test_missing_field_and_false_ok_cannot_control_domain_state(tmp_path, monkeypatch):
    make_assessment(tmp_path)
    data = m2.check_content(tmp_path, 'context.json').to_dict()
    class FalseOK(ContentReport):
        @property
        def ok(self): return False
    monkeypatch.setattr(m2, 'check_content', lambda *a: FalseOK(data))
    assert check_task(tmp_path, 'request.json')['outcome'] == 'checked'
    del data['acceptance']
    assert check_task(tmp_path, 'request.json')['outcome'] == 'unsupported'


def test_mapped_scopes_claims_and_unknown_resolution_are_preserved_in_literal_output(tmp_path):
    _, context = make_assessment(tmp_path)
    pack = tmp_path, context; claim(pack)
    a = lambda name: loc(document='notes', anchor=name)
    context['open_items'] = [{'item':a('item'),'affected':[loc('Functional requirements','REQ-01')],
                             'effect':a('effect'),'resolver':a('resolver'),'next_action':a('action')}]
    save_context(tmp_path, context)
    result = check_task(tmp_path, 'request.json'); report = result['content_report']
    assert result['outcome'] == 'checked'
    mapped = next(g for g in report['open_acceptance_items'] if g.get('kind') == 'mapped_open_item')
    assert mapped['affected_scopes'][0]['document'] == 'req'
    assert mapped['resolver']['path'] == mapped['next_action']['path'] == 'notes.md'
    assert any(g.get('resolution_detail') == 'not_assessed' for g in report['open_acceptance_items'])
    assert report['coverage']['claims'][0]['evidence_status'] == 'local_hashed_not_authenticated'
    text = render_text(result)
    assert text.startswith(result['task']['scope']) and 'acceptance not_assessed' in text
    assert 'affected_scopes' in text and 'not_assessed' in text and 'resolver' in text
    report['findings'].append({'rule_id':'TEST', 'severity':'warning','location':{'path':'literal.md','line':2},'message':'[red]literal\x1b[31m'})
    text = render_text(result)
    assert '[red]literal' in text and '\x1b' not in text and '\\u001b' in text


@pytest.mark.parametrize('path', ['../outside.md','.ENV','secrets/file.md','ubongo/projects/foreign/private.md'])
def test_declared_source_safety_precedes_checker_reads(tmp_path, monkeypatch, path):
    _, context = make_assessment(tmp_path)
    context['documents'][0]['path'] = path; save_context(tmp_path, context)
    monkeypatch.setattr(m2, 'check_content', lambda *a: pytest.fail('Unsafe declared path reached checker'))
    assert check_task(tmp_path, 'request.json')['outcome'] == 'blocked'
