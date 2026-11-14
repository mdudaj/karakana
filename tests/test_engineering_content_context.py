"""M2 real source selection, graph integrity, scoped evidence and recomputation."""
from copy import deepcopy
import json
import re
from pathlib import Path
import shutil

import pytest

from karakana.tools.engineering_content import check_content, main

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def pack(tmp_path):
    for key, source in [('req', 'skills/engineering-requirements/assets/requirements-example.md'),
                        ('design', 'skills/engineering-design-records/assets/system-design-example.md')]:
        shutil.copyfile(ROOT / source, tmp_path / (key + '.md'))
    ctx = {'context_version': '0.2', 'namespace': 'example', 'documents': [
        {'key': 'req', 'path': 'req.md', 'format': 'narrative-0.1', 'profile': {'id': 'requirements', 'version': '0.1'}},
        {'key': 'design', 'path': 'design.md', 'format': 'narrative-0.1', 'profile': {'id': 'system-design', 'version': '0.1'}, 'requirements': ['req']}]}
    return tmp_path, ctx


def run(pack):
    root, ctx = pack
    (root / 'context.json').write_text(json.dumps(ctx))
    return check_content(root, Path('context.json')).to_dict()


def change(pack, old, new, path='req.md'):
    p = pack[0] / path
    assert old in p.read_text()
    p.write_text(p.read_text().replace(old, new))


def loc(heading=None, record=None, field=None, document='req', anchor=None):
    value = {'document': document, **({'anchor': anchor} if anchor else {'heading': [heading] if isinstance(heading, str) else heading})}
    if record is not None: value['record_id'] = record
    if field is not None: value['field'] = field
    return value


def links(pack):
    source = loc('Functional requirements', 'REQ-01', 'Acceptance criteria')
    pack[1]['links'] = [{'from': source, 'to': loc('Acceptance and verification', x)} for x in ('AC-01', 'AC-02')]


def test_m2_empty_context_versions_and_honest_states(pack):
    for version in ['0.1', '0.2']:
        pack[1]['context_version'] = version
        r = run(pack)
        assert r['completeness'] == 'complete'
        assert r['review_required'] and r['acceptance'] == 'not_assessed'
        assert r['coverage']['advanced_context'] == 'supported'
        assert r['coverage']['saved_report_verification'] == 'supported'


def test_canonical_links_and_custom_complete_target_set(pack):
    links(pack)
    assert run(pack)['completeness'] == 'complete'
    change(pack, '| AC-01, AC-02 |', '| intake and permission checks |')
    assert run(pack)['completeness'] == 'complete'
    pack[1]['links'].pop()
    assert run(pack)['completeness'] != 'complete'  # reverse graph detects missing AC-02


@pytest.mark.parametrize('fault', ['missing', 'extra', 'duplicate', 'wrong_kind', 'dangling', 'wrong_baseline', 'empty_source', 'no_field', 'target_field', 'unknown', 'v01'])
def test_explicit_edges_cannot_hide_source_or_contract_errors(pack, fault):
    links(pack)
    edge = pack[1]['links'][0]
    if fault == 'missing': pack[1]['links'].pop()
    elif fault == 'extra': pack[1]['links'].append({'from': edge['from'], 'to': loc('Acceptance and verification', 'AC-03')})
    elif fault == 'duplicate': pack[1]['links'].append(deepcopy(edge))
    elif fault == 'wrong_kind': edge['to'] = loc('Functional requirements', 'REQ-01')
    elif fault == 'dangling': change(pack, '| AC-01, AC-02 |', '| AC-99 |')
    elif fault == 'wrong_baseline': edge['to']['document'] = 'design'
    elif fault == 'empty_source': change(pack, '| AC-01, AC-02 |', '|  |')
    elif fault == 'no_field': edge['from'].pop('field')
    elif fault == 'target_field': edge['to']['field'] = 'Expected outcome'
    elif fault == 'unknown': edge['waive'] = True
    else: pack[1]['context_version'] = '0.1'
    assert run(pack)['completeness'] != 'complete'


def test_heading_paths_support_nested_renamed_content(pack):
    change(pack, '## Functional requirements', '## Change\n\n### Features')
    pack[1]['coverage'] = [{'document': 'req', 'slot': 'functional', 'source': loc(['Change', 'Features'])}]
    r = run(pack)
    assert r['completeness'] == 'complete'
    assert r['documents'][1]['requirements'] == [f'REQ-{i:02}' for i in range(1,7)]


def test_governing_view_is_hashed_and_actual_locations_retained(pack):
    root, ctx = pack
    text = (root/'req.md').read_text()
    start, end = text.index('## Purpose and scope'), text.index('## Context and users')
    section = text[start:end].replace('Purpose and scope', 'Governing purpose')
    (root/'governing.md').write_text('# Governing source\n\n' + section)
    (root/'req.md').write_text(text[:start] + text[end:])
    ctx['references'] = [{'key': 'governing', 'path': 'governing.md', 'format': 'narrative-0.1', 'purpose': 'Current scope'}]
    ctx['coverage'] = [{'document': 'req', 'slot': 'purpose', 'source': loc('Governing purpose', document='governing')}]
    r = run(pack)
    assert r['completeness'] == 'complete'
    assert any(s['path'] == 'governing.md' for s in r['manifest']['sources'])
    coverage = next(d for d in r['documents'] if d['key']=='req')['coverage']
    assert next(x for x in coverage if x['slot']=='purpose')['source']['path']=='governing.md'
    (root/'governing.md').write_text('# Governing source\n\n## Governing purpose\n\n{{purpose}}\n')
    r=run(pack)
    assert any(f['location']['path']=='governing.md' and f['severity']=='error' for f in r['findings'])


@pytest.mark.parametrize('fault', ['absent', 'ambiguous', 'unknown_slot', 'core_omission', 'empty_rationale', 'duplicate_coverage', 'cycle'])
def test_coverage_and_omission_fail_closed(pack, fault):
    root, ctx=pack
    (root/'notes.md').write_text('# Notes\n\n## Rationale\n\nThis change has no external interface.\n')
    ctx['references']=[{'key':'notes','path':'notes.md','format':'narrative-0.1','purpose':'Rationale'}]
    source=loc('Purpose and scope')
    ctx['coverage']=[{'document':'req','slot':'purpose','source':source}]
    if fault=='absent':source['heading']=['Absent']
    elif fault=='ambiguous':change(pack,'## Purpose and scope','## Purpose and scope\n\nOther text.\n\n## Purpose and scope')
    elif fault=='unknown_slot':ctx['coverage'][0]['slot']='arbitrary'
    elif fault in ['core_omission','empty_rationale']:
        ctx.pop('coverage')
        ctx['omissions']=[{'document':'req','slot':'purpose' if fault=='core_omission' else 'interfaces','rationale':loc('Rationale',document='notes')}]
        if fault=='empty_rationale':(root/'notes.md').write_text('# Notes\n\n## Rationale\n')
    elif fault=='duplicate_coverage':ctx['coverage'].append(deepcopy(ctx['coverage'][0]))
    else:
        ctx['coverage']=[{'document':'req','slot':'purpose','source':loc('Purpose and scope',document='design')},
                         {'document':'design','slot':'purpose','source':loc('Purpose and scope',document='req')}]
    assert run(pack)['completeness']!='complete'


def observations(pack):
    root,ctx=pack
    values={'item':'A synthetic unresolved capacity measure.', 'effect':'REQ-01 acceptance remains unresolved.',
            'resolver':'Fixture owner.', 'action':'Measure the synthetic sample.', 'claim':'Synthetic test execution result.',
            'revision':'fixture-1','actor':'Fixture runner','result':'Passed','time':'2026-11-14T10:00:00+03:00',
            'environment':'Isolated fixture','evidence':'evidence.txt'}
    (root/'notes.md').write_text('# Synthetic observations\n\n'+'\n\n'.join(f'<a id="{k}"></a>\n\n{v}' for k,v in values.items())+'\n')
    (root/'evidence.txt').write_text('Synthetic deterministic fixture evidence.\n')
    ctx['references']=[{'key':'notes','path':'notes.md','purpose':'Synthetic source evidence','format':'narrative-0.1'}]
    return lambda name:loc(document='notes',anchor=name)


def test_actual_open_item_fields_and_affected_scopes(pack):
    a=observations(pack)
    pack[1]['open_items']=[{'item':a('item'),'affected':[loc('Functional requirements','REQ-01')],
                         'effect':a('effect'),'resolver':a('resolver'),'next_action':a('action')}]
    r=run(pack)
    assert r['completeness']=='complete'
    item=next(g for g in r['open_acceptance_items'] if g['kind']=='mapped_open_item')
    assert item['resolution_detail']=='declared' and item['affected_scopes'][0]['document']=='req'
    assert item['effect']['path']=='notes.md'


def claim(pack):
    a=observations(pack)
    pack[1]['claims']=[{'source':a('claim'),'kind':'test_result','fields':{k:a(k) for k in ['revision','actor','result','time','environment','evidence']}}]


def test_claim_checks_local_evidence_and_keeps_honest_limits(pack):
    claim(pack)
    r=run(pack)
    assert r['completeness']=='complete'
    assert any(s['path']=='evidence.txt' for s in r['manifest']['sources'])
    assert r['coverage']['claims'][0]['evidence_status']=='local_hashed_not_authenticated'
    assert r['acceptance']=='not_assessed'


@pytest.mark.parametrize('fault',['missing_field','blank','naive_time','planned','missing_evidence','secret','outside','external'])
def test_claim_evidence_and_unknowns_do_not_gain_trust(pack,fault):
    claim(pack);root,ctx=pack
    if fault=='missing_field':ctx['claims'][0]['fields'].pop('actor')
    elif fault=='blank':change(pack,'Fixture runner','', 'notes.md')
    elif fault=='naive_time':change(pack,'2026-11-14T10:00:00+03:00','2026-11-14T10:00:00','notes.md')
    elif fault=='planned':change(pack,'Passed','Planned','notes.md')
    elif fault=='missing_evidence':(root/'evidence.txt').unlink()
    elif fault=='secret':change(pack,'evidence.txt','.env','notes.md')
    elif fault=='outside':change(pack,'evidence.txt','../outside.txt','notes.md')
    else:change(pack,'evidence.txt','https://example.invalid/fixture','notes.md')
    r=run(pack)
    if fault=='external':
        assert r['completeness']=='complete'
        assert r['coverage']['claims'][0]['evidence_status']=='external_not_checked'
        assert any(f['rule_id']=='CP-EVIDENCE-REVIEW' for f in r['findings'])
    else:assert r['completeness']!='complete'


def test_verify_recomputes_and_rejects_tampering_and_byte_changes(pack,capsys):
    root,ctx=pack;r=run(pack);(root/'report.json').write_text(json.dumps(r))
    args=['--root',str(root),'verify','--context','context.json','--report','report.json','--format','json']
    assert main(args)==0
    v=json.loads(capsys.readouterr().out);assert v['verification']=='current'
    # A fabricated saved pass with an equally fabricated digest is not evidence.
    bad=deepcopy(r);bad['documents'][0]['criteria']=[];bad['assessment_digest']='0'*64
    (root/'report.json').write_text(json.dumps(bad));assert main(args)==2;capsys.readouterr()
    (root/'report.json').write_text(json.dumps(r))
    original=(root/'req.md').read_bytes();(root/'req.md').write_bytes(original.replace(b'\n',b'\r\n'))
    current=check_content(root,Path('context.json')).to_dict()
    assert current['assessment_digest']==r['assessment_digest']
    assert main(args)==2
    v=json.loads(capsys.readouterr().out);assert v['verification']=='stale_or_mismatched'


def test_row_anchor_selects_unidentified_design_cell_and_duplicate_alias_fails(pack):
    change(pack,'| REQ-01, REQ-02 | Shared','| <a id="response"></a>REQ-01, REQ-02 | Shared','design.md')
    source=loc(document='design',anchor='response',field='Requirement / concern')
    pack[1]['links']=[{'from':source,'to':loc('Functional requirements',x)} for x in ['REQ-01','REQ-02']]
    assert run(pack)['completeness']=='complete'
    # Heading + field sees four rows, so it must not pick the first one.
    pack[1]['links'][0]['from']=loc('Security and quality',field='Requirement / concern',document='design')
    assert run(pack)['completeness']!='complete'


def test_distinct_anchor_heading_selectors_cannot_duplicate_one_edge(pack):
    change(pack,'| REQ-01 |','| <a id="req-one"></a>REQ-01 |')
    links(pack)
    alias={'from':loc(anchor='req-one',field='Acceptance criteria'),'to':loc('Acceptance and verification','AC-01')}
    pack[1]['links'].append(alias)
    assert run(pack)['completeness']!='complete'


def test_repeated_heading_requires_unique_anchor_and_mapping(pack):
    change(pack,'## Purpose and scope','<a id="actual-purpose"></a>\n\n## Purpose and scope')
    with (pack[0]/'req.md').open('a') as f:f.write('\n## Purpose and scope\n\nUnrelated historical purpose.\n')
    pack[1]['coverage']=[{'document':'req','slot':'purpose','source':loc(anchor='actual-purpose')}]
    assert run(pack)['completeness']=='complete'
    pack[1]['coverage'][0]['source']=loc('Purpose and scope')
    assert run(pack)['completeness']!='complete'


def test_missing_conditional_slot_accepts_actual_rationale(pack):
    a=observations(pack)
    text=(pack[0]/'req.md').read_text();start=text.index('## Interfaces and data');end=text.index('## Acceptance and verification')
    (pack[0]/'req.md').write_text(text[:start]+text[end:])
    pack[1]['omissions']=[{'document':'req','slot':'interfaces','rationale':a('effect')}]
    r=run(pack);assert r['completeness']=='complete'
    c=next(d for d in r['documents'] if d['key']=='req')['coverage']
    assert next(x for x in c if x['slot']=='interfaces')['state']=='omitted_with_rationale'
    assert r['review_required']  # adequacy of a rationale is not mechanically certified


def test_governing_table_uses_real_records_and_does_not_mask_local_errors(pack):
    root,ctx=pack;text=(root/'req.md').read_text();start=text.index('## Functional requirements');end=text.index('## Quality requirements')
    section=text[start:end]
    (root/'governing.md').write_text('# Governing records\n\n'+section)
    ctx['references']=[{'key':'governing','path':'governing.md','purpose':'Canonical records','format':'narrative-0.1'}]
    ctx['coverage']=[{'document':'req','slot':'functional','source':loc('Functional requirements',document='governing')}]
    (root/'req.md').write_text(text[:start]+text[end:])
    assert run(pack)['completeness']=='complete'
    change(pack,'| AC-01, AC-02 |','| AC-99 |','governing.md')
    r=run(pack)
    assert any(f['rule_id']=='CP-REFERENCE-001' and f['location']['path']=='governing.md' for f in r['findings'])


@pytest.mark.parametrize('fault',['malformed','extra_key','digest','manifest','readiness','acceptance','coverage','findings','version','time','number_bool'])
def test_saved_report_is_compared_in_full_not_trusted(pack,capsys,fault):
    root,_=pack;r=run(pack)
    if fault=='extra_key':r['secret_override']=True
    elif fault=='digest':r['assessment_digest']='0'*64
    elif fault=='manifest':r['manifest']['sources']=[]
    elif fault=='readiness':r['readiness']='ready'
    elif fault=='acceptance':r['acceptance']='accepted'
    elif fault=='coverage':r['coverage']['supported']=[]
    elif fault=='findings':r['findings'].append({'severity':'warning','message':'forged'})
    elif fault=='version':r['report_version']='0.1'
    elif fault=='time':r['generated_utc']='not a time'
    elif fault=='number_bool':r['review_required']=1
    (root/'report.json').write_text('{' if fault=='malformed' else json.dumps(r))
    assert main(['--root',str(root),'verify','--context','context.json','--report','report.json','--format','json'])==2
    assert json.loads(capsys.readouterr().out)['verification']=='stale_or_mismatched'


def test_context_order_semantics_and_raw_freshness_are_separate(pack,capsys):
    links(pack);root,ctx=pack;r=run(pack);(root/'report.json').write_text(json.dumps(r))
    ctx['links'].reverse();ctx['documents'].reverse();new=run(pack)
    assert r['assessment_digest']==new['assessment_digest']
    assert r['manifest']!=new['manifest']
    assert main(['--root',str(root),'verify','--context','context.json','--report','report.json','--format','json'])==2
    capsys.readouterr()


def test_evidence_change_and_reference_symlink_retarget_are_stale(pack,capsys):
    claim(pack);root,ctx=pack;r=run(pack);(root/'report.json').write_text(json.dumps(r))
    (root/'evidence.txt').write_text('Changed evidence; identical declared finding set.\n')
    now=run(pack);assert now['assessment_digest']==r['assessment_digest'];assert now['manifest']!=r['manifest']
    args=['--root',str(root),'verify','--context','context.json','--report','report.json','--format','json']
    assert main(args)==2;capsys.readouterr()
    # Equal bytes at a different physical source are also a different manifest.
    shutil.copyfile(root/'notes.md',root/'same.md');(root/'selected.md').symlink_to('notes.md')
    ctx['references'][0]['path']='selected.md';r=run(pack);(root/'report.json').write_text(json.dumps(r))
    (root/'selected.md').unlink();(root/'selected.md').symlink_to('same.md')
    assert main(args)==2;capsys.readouterr()


@pytest.mark.parametrize('field',['effect','resolver','next_action'])
def test_open_item_missing_actual_detail_is_an_error(pack,field):
    a=observations(pack)
    pack[1]['open_items']=[{'item':a('item'),'affected':[loc('Functional requirements','REQ-01')],
                         'effect':a('effect'),'resolver':a('resolver'),'next_action':a('action')}]
    locator=pack[1]['open_items'][0][field];locator['anchor']='missing'
    r=run(pack);assert r['completeness']!='complete';assert r['acceptance']=='not_assessed'


def test_unrelated_document_readiness_is_independent_of_mapped_item(pack):
    # Isolate from intentional Q/design gaps in the accepted packs.
    root,ctx=pack
    for path in ['req.md','design.md']:
        lines=(root/path).read_text().splitlines()
        if path=='req.md':
            lines=[x for x in lines if not x.startswith('| Q-')]
        else:
            edited=[]
            for line in lines:
                if line.startswith('| REQ-'):
                    cells=line.split('|');cells[-2]='  ';line='|'.join(cells)
                edited.append(line)
            lines=edited
        (root/path).write_text('\n'.join(lines)+'\n')
    # A fresh two-document requirement-only context avoids design source gaps.
    ctx['documents']=ctx['documents'][:1]
    text=(root/'req.md').read_text()
    for q in ['Q-01','Q-02']:text=re.sub(r'\b'+q+r'\b','unconfirmed',text)
    (root/'req.md').write_text(text)
    other=text.replace('EX-REQ','EX-OTHER')
    for i in range(1,7):other=other.replace(f'REQ-{i:02}',f'RQM-{i:02}').replace(f'AC-{i:02}',f'CR-{i:02}')
    (root/'other.md').write_text(other)
    doc=deepcopy(ctx['documents'][0]);doc.update(key='other',path='other.md');ctx['documents'].append(doc)
    a=observations(pack)
    ctx['open_items']=[{'item':a('item'),'affected':[loc('Functional requirements','REQ-01')],
                       'effect':a('effect'),'resolver':a('resolver'),'next_action':a('action')}]
    r=run(pack);assert r['completeness']=='complete'
    docs={d['key']:d for d in r['documents']}
    assert docs['req']['readiness']=='unresolved'
    assert docs['other']['readiness']=='not_assessed'


def test_cross_slot_governing_cycle_is_refused(pack):
    pack[1]['coverage']=[{'document':'req','slot':'purpose','source':loc('System context',document='design')},
                         {'document':'design','slot':'context','source':loc('Purpose and scope')}]
    r=run(pack)
    assert any(f['rule_id']=='CP-COVERAGE-001' and 'cycle' in f['message'] for f in r['findings'])


def test_bad_mapping_keeps_detected_source_questions_visible(pack):
    pack[1]['coverage']=[{'document':'req','slot':'purpose','source':loc('Absent')}]
    r=run(pack)
    assert r['completeness']!='complete'
    assert {g['record_id'] for g in r['open_acceptance_items'] if g['record_id']} >= {'Q-01','Q-02'}


def test_local_rows_are_not_suppressed_by_governing_replacement(pack):
    root,ctx=pack
    text=(root/'req.md').read_text();start=text.index('## Functional requirements');end=text.index('## Quality requirements')
    (root/'governing.md').write_text('# Governing source\n\n'+text[start:end])
    change(pack,'| AC-01, AC-02 |','| AC-99 |')
    ctx['references']=[{'key':'governing','path':'governing.md','purpose':'View','format':'narrative-0.1'}]
    ctx['coverage']=[{'document':'req','slot':'functional','source':loc('Functional requirements',document='governing')}]
    r=run(pack)
    assert any(f['rule_id']=='CP-REFERENCE-001' and f['location']['path']=='req.md' for f in r['findings'])


def test_open_mapping_enriches_existing_question_without_removing_unresolved_state(pack):
    a=observations(pack)
    pack[1]['open_items']=[{'item':loc('Unresolved matters','Q-01'),
                           'affected':[loc('Quality requirements and constraints','REQ-06')],
                           'effect':loc('Unresolved matters','Q-01','Effect on acceptance'),
                           'resolver':a('resolver'),'next_action':a('action')}]
    r=run(pack);assert r['completeness']=='complete'
    gaps=[g for g in r['open_acceptance_items'] if g['record_id']=='Q-01']
    assert len(gaps)==1 and gaps[0]['resolution_detail']=='declared'
    assert r['readiness']=='unresolved' and r['acceptance']=='not_assessed'


def test_accepted_decision_requires_actual_located_fields_and_remains_declared(pack):
    a=observations(pack)
    change(pack,'; Proposed |','; Accepted |','design.md')
    change(pack,'| ADR-01:','| <a id="decision"></a>ADR-01:','design.md')
    change(pack,'Passed','Accepted','notes.md')
    pack[1]['claims']=[{'source':loc(document='design',anchor='decision'),'kind':'decision',
                       'fields':{k:a(k) for k in ['revision','actor','result','time','evidence']}}]
    r=run(pack);assert r['completeness']=='complete'
    assert r['coverage']['claims'][0]['kind']=='decision'
    assert r['acceptance']=='not_assessed' and r['review_required']


def test_report_change_during_verify_is_refused(pack,monkeypatch,capsys):
    from karakana.content_profiles.loader import Inputs
    root,_=pack;r=run(pack);(root/'report.json').write_text(json.dumps(r))
    original=Inputs.read
    def changed(self,value,role,*args,**kwargs):
        result=original(self,value,role,*args,**kwargs)
        if role=='saved_report':(root/'report.json').write_text('{}')
        return result
    monkeypatch.setattr(Inputs,'read',changed)
    assert main(['--root',str(root),'verify','--context','context.json','--report','report.json','--format','json'])==2
    assert any(f['rule_id']=='CP-DRIFT-001' for f in json.loads(capsys.readouterr().out)['findings'])


def test_bounded_deep_saved_json_refuses_without_traceback(pack,capsys):
    root,_=pack;run(pack);(root/'report.json').write_text('['*100+'0'+']'*100)
    assert main(['--root',str(root),'verify','--context','context.json','--report','report.json','--format','json'])==2
    assert any(f['rule_id']=='CP-LIMIT-001' for f in json.loads(capsys.readouterr().out)['findings'])


@pytest.mark.parametrize('name',['tailored','evidence'])
def test_shipped_contexts_execute_real_governing_sources_and_preserve_bytes(name):
    path=Path('docs/skills/engineering-artifact-catalogue/content-checks')/(name+'.json')
    fixtures=list((ROOT/'tests/fixtures/engineering_content').iterdir())
    before={p:p.read_bytes() for p in fixtures}
    r=check_content(ROOT,path).to_dict()
    assert r['completeness']=='complete',r['findings']
    assert next(d for d in r['documents'] if d['key']=='req')['requirements']==['REQ-01','REQ-02']
    if name=='evidence':
        assert r['readiness']=='unresolved'
        assert r['open_acceptance_items'][0]['affected_scopes'][0]['document']=='req'
        assert r['coverage']['claims'][0]['evidence_status']=='local_hashed_not_authenticated'
    assert {p:p.read_bytes() for p in fixtures}==before


def test_opaque_reference_is_hashed_but_cannot_supply_coverage(pack):
    root,ctx=pack;(root/'schema.json').write_text('{"type":"object"}')
    ctx['references']=[{'key':'schema','path':'schema.json','purpose':'Machine contract'}]
    r=run(pack);assert r['completeness']=='complete';assert any(s['path']=='schema.json' for s in r['manifest']['sources'])
    ctx['coverage']=[{'document':'req','slot':'purpose','source':loc('Scope',document='schema')}]
    assert run(pack)['completeness']!='complete'


@pytest.mark.parametrize('fault',['same_file','secret_link','escaping_link','too_large','raw_malformed','field_in_prose','unknown_locator_key'])
def test_governing_sources_keep_the_same_bounded_read_and_shape_guards(pack,fault):
    root,ctx=pack;a=observations(pack)
    if fault=='same_file':ctx['references'][0]['path']='req.md'
    elif fault=='secret_link':
        (root/'secrets').mkdir();(root/'secrets/private.md').write_text('private-sentinel');(root/'selected.md').symlink_to('secrets/private.md');ctx['references'][0]['path']='selected.md'
    elif fault=='escaping_link':
        outside=root.parent/(root.name+'-outside.md');outside.write_text('private-sentinel');(root/'selected.md').symlink_to(outside);ctx['references'][0]['path']='selected.md'
    elif fault=='too_large':(root/'notes.md').write_text('x'*2_000_001)
    elif fault=='raw_malformed':(root/'notes.md').write_text('# Notes\n\n| A | B |\n| --- | --- |\n| extra | wide | row |\n')
    else:
        selection=a('rationale')
        if fault=='field_in_prose':selection['field']='Any field'
        else:selection['regex']='.*'
        ctx['coverage']=[{'document':'req','slot':'purpose','source':selection}]
    r=run(pack);assert r['completeness']!='complete';assert 'private-sentinel' not in json.dumps(r)


def test_referenced_profiled_view_reuses_one_physical_record_not_duplicate_facts(pack):
    root,ctx=pack
    text=(root/'req.md').read_text()
    # A second compact requirements view points to the same physical records.
    compact=text.replace('EX-REQ','EX-COMPACT')
    for first,last in [('## Functional requirements','## Quality requirements'),
                       ('## Quality requirements','## Interfaces and data'),
                       ('## Acceptance and verification','## Unresolved matters')]:
        a,b=compact.index(first),compact.index(last);compact=compact[:a]+compact[b:]
    # The canonical unresolved rows belong only to the original source.
    compact=compact[:compact.index('## Unresolved matters')]
    (root/'compact.md').write_text(compact)
    doc=deepcopy(ctx['documents'][0]);doc.update(key='compact',path='compact.md');ctx['documents'].append(doc)
    ctx['coverage']=[{'document':'compact','slot':slot,'source':loc(heading)} for slot,heading in [
        ('functional','Functional requirements'),('quality','Quality requirements and constraints'),('acceptance','Acceptance and verification'),('gaps','Unresolved matters')]]
    r=run(pack)
    assert r['completeness']=='complete',r['findings']
    docs={d['key']:d for d in r['documents']}
    assert docs['compact']['requirements']==docs['req']['requirements']


def test_extra_native_record_table_cannot_disappear_outside_profile_slots(pack):
    with (pack[0]/'req.md').open('a') as f:
        f.write('\n## Extra requirements\n\n| ID | Requirement | Rationale / source | Acceptance criteria |\n| --- | --- | --- | --- |\n| REQ-99 | Additional native record | Actual source | AC-99 |\n')
    r=run(pack)
    assert r['completeness']!='complete'
    assert any(f['rule_id']=='CP-TABLE-001' for f in r['findings'])


def test_test_result_mapping_cannot_supply_accepted_decision_authority(pack):
    a=observations(pack)
    change(pack,'; Proposed |','; Accepted |','design.md')
    change(pack,'| ADR-01:','| <a id="decision"></a>ADR-01:','design.md')
    pack[1]['claims']=[{'source':loc(document='design',anchor='decision'),'kind':'test_result',
                       'fields':{k:a(k) for k in ['revision','actor','result','time','environment','evidence']}}]
    r=run(pack)
    assert r['completeness']!='complete'
    assert any(f['rule_id']=='CP-CLAIM-001' for f in r['findings'])


def test_two_cell_selectors_cannot_override_one_canonical_question_mapping(pack):
    a=observations(pack)
    base={'item':loc('Unresolved matters','Q-01','Unresolved fact / assumption'),
          'affected':[loc('Quality requirements and constraints','REQ-06')],
          'effect':a('effect'),'resolver':a('resolver'),'next_action':a('action')}
    other=deepcopy(base);other['item']['field']='Effect on acceptance'
    other['affected']=[loc('Functional requirements','REQ-01')]
    pack[1]['open_items']=[base,other]
    r=run(pack)
    assert r['completeness']!='complete'
    assert any('once' in f['message'] for f in r['findings'])
