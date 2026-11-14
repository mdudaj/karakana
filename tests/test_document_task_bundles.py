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
