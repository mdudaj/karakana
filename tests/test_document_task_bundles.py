import json

import pytest

from karakana.document_tasks import prepare_task
from tests.document_task_support import make_task


@pytest.mark.parametrize("target", ["existing", "empty", "outside", "parent"])
def test_output_refusal_preserves_existing_sources_and_outputs(tmp_path, target):
    make_task(tmp_path)
    output = ".karakana/chosen"
    old = None
    if target in {"existing", "empty"}:
        directory = tmp_path / output; directory.mkdir(parents=True)
        if target == "existing":
            old = directory / "result.json"; old.write_text("Retained owner annotation")
    if target == "outside": output = "docs/new-bundle"
    if target == "parent": output = ".karakana/../docs/new-bundle"
    before = {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    result = prepare_task(tmp_path, "request.json", output)
    assert result["outcome"] == "failed"
    assert all(p.read_bytes() == raw for p, raw in before.items())
    assert not (tmp_path / "docs/new-bundle").exists()


def test_input_drift_after_prompt_write_never_publishes_success_result(tmp_path, monkeypatch):
    from karakana.document_tasks import bundles
    make_task(tmp_path); original = bundles.write_new; calls = 0

    def writer(root, outputs):
        nonlocal calls
        original(root, outputs); calls += 1
        if calls == 1: (tmp_path / "docs/guide.md").write_text("Changed source after capture")

    monkeypatch.setattr(bundles, "write_new", writer)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "failed"
    target = tmp_path / result["run"]["bundle"]
    assert (target / "prompt.md").is_file() and not (target / "result.json").exists()
    assert result["diagnostics"][0]["code"] == "DT-DRIFT-001"


def test_nonempty_partial_output_is_retained_and_failure_is_truthful(tmp_path, monkeypatch):
    from karakana.document_tasks import bundles
    make_task(tmp_path); original = bundles.write_new; calls = 0

    def writer(root, outputs):
        nonlocal calls
        calls += 1
        if calls == 2:
            next(iter(outputs)).write_text('{"partial":')
            raise OSError("Synthetic disk failure")
        original(root, outputs)

    monkeypatch.setattr(bundles, "write_new", writer)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "failed"
    target = tmp_path / result["run"]["bundle"]
    assert (target / "result.json").read_text() == '{"partial":'
    assert (target / "prompt.md").is_file()


def test_code_fingerprint_drift_refuses_publication(tmp_path, monkeypatch):
    from karakana.document_tasks import prepare
    make_task(tmp_path); original = prepare.fingerprint; calls = 0

    def changed():
        nonlocal calls
        calls += 1
        data = original()
        if calls > 1: data["sha256"] = "changed-code"
        return data

    monkeypatch.setattr(prepare, "fingerprint", changed)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "failed" and result["freshness"]["inputs"] == "unresolved"
    assert result["diagnostics"][0]["code"] == "DT-DRIFT-001"


def test_oversized_saved_result_refuses_before_publication(tmp_path, monkeypatch):
    from karakana.document_tasks import bundles
    make_task(tmp_path); monkeypatch.setattr(bundles, "MAX_SOURCE_BYTES", 100)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "failed"
    assert not list(tmp_path.glob('.karakana/**/result.json'))


@pytest.mark.parametrize('operation', ['check','verify'])
@pytest.mark.parametrize('fault', ['existing','outside','partial','resource_drift','source_drift','code_drift','limit','target_drift'])
def test_assessment_output_safety_preserves_sources_and_incomplete_evidence(tmp_path, monkeypatch, operation, fault):
    from karakana.document_tasks import bundles, assessment, check_task, verify_task
    from tests.document_task_support import make_assessment
    make_assessment(tmp_path)
    saved=check_task(tmp_path,'request.json') if operation=='verify' else None
    before={p:p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    output='.karakana/output';writer=bundles.write_new;calls=0
    if fault=='existing':
        d=tmp_path/output;d.mkdir(parents=True);(d/'result.json').write_text('Retained owner annotation')
    elif fault=='outside':output='docs/output'
    elif fault=='limit':monkeypatch.setattr(bundles,'MAX_SOURCE_BYTES',100)
    elif fault=='code_drift':
        original=assessment.fingerprint;n=0
        def code():
            nonlocal n
            n+=1;x=original()
            if n>1:x['sha256']='changed'
            return x
        monkeypatch.setattr(assessment,'fingerprint',code)
    def write(root,outputs):
        nonlocal calls
        calls+=1
        if fault=='partial' and calls==2:
            next(iter(outputs)).write_text('{"partial":');raise OSError('Synthetic disk failure')
        writer(root,outputs)
        if calls==1:
            if fault=='resource_drift':(tmp_path/'docs/guide.md').write_text('Changed guide during output')
            elif fault=='source_drift':
                p=tmp_path/'req.md';p.write_text(p.read_text()+'\nChanged source during output.\n')
            elif fault=='target_drift':
                d=tmp_path/output;d.rename(tmp_path/'.karakana/retained-partial');d.symlink_to(tmp_path/'docs',target_is_directory=True)
    monkeypatch.setattr(bundles,'write_new',write)
    result=(verify_task(tmp_path,'request.json',saved['run']['bundle'],output) if saved
            else check_task(tmp_path,'request.json',output))
    assert result['outcome'] not in {'checked','verified'}
    if fault=='partial':
        assert (tmp_path/output/'result.json').read_text()=='{"partial":'
        assert (tmp_path/output/'content-report.json').is_file()
    elif fault in {'resource_drift','source_drift'}:
        assert not (tmp_path/output/'result.json').exists()
        assert (tmp_path/output/'content-report.json').is_file()
    elif fault=='existing':assert (tmp_path/output/'result.json').read_text()=='Retained owner annotation'
    elif fault=='target_drift':
        assert not (tmp_path/'docs/result.json').exists()
        assert (tmp_path/'.karakana/retained-partial/content-report.json').is_file()
    else:
        assert all(p.read_bytes()==raw for p,raw in before.items())
