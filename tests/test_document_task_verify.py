"""Two independent freshness layers; no saved digest or authority field is trusted."""

from copy import deepcopy
import json

import pytest

from karakana.document_tasks import prepare_task, check_task, verify_task
from tests.document_task_support import make_assessment, save_request, add_policy, save_context
from tests.test_engineering_content_context import claim


def checked(root):
    result = check_task(root, 'request.json')
    assert result['outcome'] == 'checked', result['diagnostics']
    return root / result['run']['bundle'], result


def store(bundle, result):
    (bundle / 'result.json').write_text(json.dumps(result))
    (bundle / 'content-report.json').write_text(json.dumps(result['content_report']))


def test_check_and_successful_verification_bundles_recompute_and_never_overwrite(tmp_path):
    make_assessment(tmp_path); bundle, old = checked(tmp_path)
    before = {p:p.read_bytes() for p in bundle.iterdir()}
    for _ in range(2):
        result = verify_task(tmp_path, 'request.json', bundle.relative_to(tmp_path))
        assert result['outcome'] == 'verified', result['diagnostics']
        assert result['freshness'] == {'inputs':'current','saved_bundle':'current'}
        assert result['content_report']['verification'] == 'current'
        assert result['content_report']['readiness'] == 'unresolved'
        assert result['content_report']['acceptance'] == 'not_assessed'
        bundle = tmp_path / result['run']['bundle']
        assert json.loads((bundle / 'result.json').read_text()) == result
    assert all(p.read_bytes() == b for p,b in before.items())


def test_current_incomplete_check_remains_failed_even_when_saved_bytes_match(tmp_path):
    make_assessment(tmp_path)
    p = tmp_path / 'req.md'; p.write_text(p.read_text().replace('## Purpose and scope','## Missing purpose'))
    old = check_task(tmp_path, 'request.json'); assert old['outcome'] == 'failed'
    result = verify_task(tmp_path, 'request.json', old['run']['bundle'])
    assert result['outcome'] == 'failed' and result['freshness']['saved_bundle'] == 'current'
    assert result['content_report']['verification'] == 'current'


@pytest.mark.parametrize('change', ['guide','policy','agents','contract','revision','scope','action','skill','audience','request_bytes','context','document','evidence'])
def test_actual_input_changes_refuse_with_raw_current_or_stale_distinction(tmp_path, change):
    request, context = make_assessment(tmp_path)
    if change == 'evidence': claim((tmp_path,context)); save_context(tmp_path,context)
    bundle, _ = checked(tmp_path)
    if change == 'guide': (tmp_path / 'docs/guide.md').write_text('Changed selected guide')
    elif change == 'policy': add_policy(tmp_path)
    elif change == 'agents': (tmp_path / 'AGENTS.md').write_text('New optional repository instruction')
    elif change == 'contract': (tmp_path / 'KARAKANA.md').write_text('New optional project contract')
    elif change in {'revision','scope','skill','audience'}:
        if change == 'skill': request['skill'] = 'other-skill'
        else: request['task'][change] = 'Changed synthetic value'
        save_request(tmp_path,request)
    elif change == 'action': request['task']['action']='analysis'; save_request(tmp_path,request)
    elif change == 'request_bytes': (tmp_path / 'request.json').write_text(json.dumps(request,indent=4))
    elif change == 'context': context['context_version']='0.1';save_context(tmp_path,context)
    elif change == 'document':
        p=tmp_path/'req.md';p.write_text(p.read_text()+'\nChanged source prose.\n')
    elif change == 'evidence': (tmp_path/'evidence.txt').write_text('Changed synthetic evidence')
    result = verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))
    assert result['outcome']=='stale_or_mismatched', result['diagnostics']
    assert result['freshness']['saved_bundle']=='stale_or_mismatched'
    assert result['content_report']['verification'] == ('stale_or_mismatched' if change in {'context','document','evidence'} else 'current')


def leaves(value, path=()):
    if isinstance(value,dict) and value:
        for k,v in value.items(): yield from leaves(v,path+(k,))
    elif isinstance(value,list) and value:
        for i,v in enumerate(value): yield from leaves(v,path+(i,))
    else: yield path,value


@pytest.mark.parametrize('operation',['check','verify'])
def test_every_saved_deterministic_leaf_is_recomputed_even_with_equal_report_copies(tmp_path, operation):
    make_assessment(tmp_path);bundle,original=checked(tmp_path)
    if operation=='verify':
        original=verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path));assert original['outcome']=='verified'
        bundle=tmp_path/original['run']['bundle']
    tested=0
    for path,value in leaves(original):
        if path[0]=='run' or path==('content_report','generated_utc'):continue
        changed=deepcopy(original);parent=changed
        for key in path[:-1]:parent=parent[key]
        parent[path[-1]] = (not value if type(value) is bool else value+1 if type(value) is int
                            else value+'-tampered' if isinstance(value,str) else {'unexpected':True})
        store(bundle,changed)
        result=verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))
        assert result['outcome']!='verified',(operation,path,result)
        assert result['freshness']['saved_bundle']=='stale_or_mismatched',path
        tested+=1
    assert tested>120
    store(bundle,original)
    assert verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))['outcome']=='verified'


def test_object_ordering_and_only_documented_valid_volatile_metadata_may_vary(tmp_path):
    make_assessment(tmp_path);bundle,result=checked(tmp_path)
    result['run']={'bundle':'.karakana/other-valid-output','generated_utc':'2026-10-14T01:00:00+03:00','id':'other-run'}
    result['content_report']['generated_utc']='2026-10-14T01:00:00+03:00'
    result=dict(reversed(list(result.items())))
    store(bundle,result)
    assert verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))['outcome']=='verified'


@pytest.mark.parametrize('fault',['report_copy','duplicate','nan','overflow','surrogate','operation_array','deep','large','partial','missing','prepare','foreign','version','naive_time','unsafe_output','extra_field','failed_verify'])
def test_malformed_foreign_partial_and_preparation_bundles_refuse(tmp_path,fault):
    request,_=make_assessment(tmp_path);bundle,result=checked(tmp_path)
    if fault=='report_copy':(bundle/'content-report.json').write_text('{}')
    elif fault=='duplicate':(bundle/'result.json').write_text('{"operation":"check","operation":"verify"}')
    elif fault=='nan':(bundle/'result.json').write_text('{"result":NaN}')
    elif fault=='overflow':(bundle/'result.json').write_text('{"result":1e999}')
    elif fault=='surrogate':(bundle/'result.json').write_text(r'{"result":"\ud800"}')
    elif fault=='deep':(bundle/'result.json').write_text('['*66+'0'+']'*66)
    elif fault=='large':(bundle/'result.json').write_bytes(b' '*2_000_001)
    elif fault=='partial':(bundle/'result.json').write_text('{"partial":')
    elif fault=='missing':(bundle/'content-report.json').unlink()
    elif fault=='prepare':
        old=prepare_task(tmp_path,'request.json');bundle=tmp_path/old['run']['bundle']
    else:
        if fault=='foreign':result['task']['project']='foreign'
        elif fault=='version':result['result_version']='9'
        elif fault=='naive_time':result['run']['generated_utc']='2026-11-14T00:00:00'
        elif fault=='unsafe_output':result['run']['bundle']='docs/unsafe'
        elif fault=='extra_field':result['unexpected']=True
        elif fault=='failed_verify':result.update(operation='verify',outcome='failed')
        elif fault=='operation_array':result['operation']=[]
        store(bundle,result)
    before={p:p.read_bytes() for p in bundle.iterdir()}
    observed=verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))
    assert observed['outcome'] not in {'verified','checked'}
    assert observed['freshness']['saved_bundle']=='stale_or_mismatched'
    assert all(p.read_bytes()==b for p,b in before.items())


@pytest.mark.parametrize('target',['guide','source'])
def test_equal_byte_symlink_target_changes_invalidate_provenance(tmp_path,target):
    request,context=make_assessment(tmp_path)
    original='docs/guide.md' if target=='guide' else 'req.md'
    first=tmp_path/original;second=tmp_path/'equal-copy.md';second.write_bytes(first.read_bytes())
    alias=tmp_path/'alias.md';alias.symlink_to(first)
    if target=='guide':request['resources'][0]['path']='alias.md';save_request(tmp_path,request)
    else:context['documents'][0]['path']='alias.md';save_context(tmp_path,context)
    bundle,_=checked(tmp_path);alias.unlink();alias.symlink_to(second)
    result=verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))
    assert result['outcome']=='stale_or_mismatched'


@pytest.mark.parametrize('identity',['wrapper','checker','parser','profile'])
def test_code_profile_and_parser_changes_are_freshness_inputs(tmp_path,monkeypatch,identity):
    from karakana.document_tasks import assessment
    from karakana.tools import engineering_content as m2
    from karakana.content_profiles import report as reports
    make_assessment(tmp_path);bundle,_=checked(tmp_path)
    if identity=='wrapper':
        original=assessment.fingerprint
        def altered():
            x=original();x['sha256']='changed';return x
        monkeypatch.setattr(assessment,'fingerprint',altered)
    elif identity=='checker':
        original=m2.checker_fingerprint
        def altered():
            x=original();x['sha256']='changed';return x
        monkeypatch.setattr(m2,'checker_fingerprint',altered);monkeypatch.setattr(reports,'checker_fingerprint',altered)
    elif identity=='parser':
        monkeypatch.setattr(m2,'parser_version',lambda:'changed');monkeypatch.setattr(reports,'parser_version',lambda:'changed')
    else:
        original=m2.load_profile
        def altered(*a):
            data,x=original(*a);x['sha256']='changed';return data,x
        monkeypatch.setattr(m2,'load_profile',altered)
    result=verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))
    assert result['outcome']=='stale_or_mismatched'
    assert result['content_report']['verification']==('current' if identity=='wrapper' else 'stale_or_mismatched')


def test_saved_file_changes_during_verification_never_publish_success(tmp_path,monkeypatch):
    from karakana.document_tasks.inputs import CapturedInputs
    make_assessment(tmp_path);bundle,_=checked(tmp_path);original=CapturedInputs.read;changed=False
    def read(self,path,role,**kw):
        nonlocal changed
        raw=original(self,path,role,**kw)
        if role=='saved_report' and not changed:
            changed=True;(bundle/'result.json').write_text('{}')
        return raw
    monkeypatch.setattr(CapturedInputs,'read',read)
    result=verify_task(tmp_path,'request.json',bundle.relative_to(tmp_path))
    assert result['outcome'] not in {'verified','checked'}
