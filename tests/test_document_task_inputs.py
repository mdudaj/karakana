import json

import pytest

from karakana.document_tasks.inputs import CapturedInputs
from karakana.document_tasks.schemas import TaskError
from karakana.document_tasks import prepare_task
from tests.document_task_support import make_task, save_request


@pytest.mark.parametrize("path", ["../outside", "/tmp/outside", ".env", "docs/.env.local", "secrets/x", "key.pem", "key.key",
                                  "PRIVATE.PEM", "PRIVATE.KEY", "Secrets/x", ".ENV.local"])
def test_unsafe_resource_paths_are_refused_without_disclosure(tmp_path, path):
    request = make_task(tmp_path); request["resources"][0]["path"] = path; save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] != "prepared"
    assert path not in json.dumps({k: result[k] for k in ("diagnostics", "selection")})
    assert result["diagnostics"][0]["code"] == "DT-PATH-001"


def test_symlink_escape_and_output_escape(tmp_path):
    root = tmp_path / "root"; root.mkdir(); request = make_task(root)
    outside = tmp_path / "outside.md"; outside.write_text("Synthetic private sentinel")
    (root / "docs/escape.md").symlink_to(outside)
    request["resources"][0]["path"] = "docs/escape.md"; save_request(root, request)
    result = prepare_task(root, "request.json")
    assert result["outcome"] == "blocked" and "sentinel" not in json.dumps(result)
    request["resources"] = []; save_request(root, request)
    (root / ".karakana").symlink_to(tmp_path / "new-outside", target_is_directory=True)
    assert prepare_task(root, "request.json")["outcome"] != "prepared"
    assert not (tmp_path / "new-outside").exists()


@pytest.mark.parametrize("change", ["bytes", "presence", "target"])
def test_captured_inputs_detect_bytes_presence_and_equal_byte_retarget(tmp_path, change):
    (tmp_path / "a.md").write_text("original")
    (tmp_path / "b.md").write_text("original")
    inputs = CapturedInputs(tmp_path)
    if change == "presence":
        inputs.read("optional.md", "optional", optional=True); (tmp_path / "optional.md").write_text("now present")
    elif change == "target":
        link = tmp_path / "alias.md"; link.symlink_to("a.md"); inputs.read("alias.md", "source")
        link.unlink(); link.symlink_to("b.md")
    else:
        inputs.read("a.md", "source"); (tmp_path / "a.md").write_text("changed")
    with pytest.raises(TaskError): inputs.recheck()


def test_physical_aliases_share_budget_but_retain_requested_identity(tmp_path, monkeypatch):
    from karakana.document_tasks import inputs as module
    (tmp_path / "a.md").write_text("same"); (tmp_path / "alias.md").symlink_to("a.md")
    monkeypatch.setattr(module, "MAX_FILES", 1)
    captured = CapturedInputs(tmp_path)
    captured.read("a.md", "first"); captured.read("alias.md", "second")
    assert captured.total == 4 and len(captured.manifest()) == 2
    (tmp_path / "b.md").write_text("extra")
    with pytest.raises(TaskError, match="limits"): captured.read("b.md", "other")


def test_read_limits_and_non_utf8(tmp_path, monkeypatch):
    from karakana.document_tasks import inputs as module
    (tmp_path / "a.md").write_bytes(b'123456')
    with pytest.raises(TaskError, match="byte limit"): CapturedInputs(tmp_path).read("a.md", "source", limit=5)
    monkeypatch.setattr(module, "MAX_TOTAL_BYTES", 5)
    with pytest.raises(TaskError, match="limits"): CapturedInputs(tmp_path).read("a.md", "source")
    (tmp_path / "bad.md").write_bytes(b'\xff')
    with pytest.raises(TaskError, match="UTF-8"): CapturedInputs(tmp_path).read("bad.md", "source")


def test_credential_root_does_not_leak_in_result(tmp_path):
    root = tmp_path / "secrets"; root.mkdir()
    result = prepare_task(root, "request.json")
    assert result["outcome"] != "prepared"
    assert result["manifest"]["root"] is None
    assert str(root) not in json.dumps(result)


def test_explicit_foreign_project_memory_is_not_loaded(tmp_path):
    request = make_task(tmp_path)
    foreign = tmp_path / 'ubongo/projects/other/overview.md'; foreign.parent.mkdir(parents=True)
    foreign.write_text('OTHER_PROJECT_MEMORY_SENTINEL')
    request['resources'][0]['path'] = 'ubongo/projects/other/overview.md'; save_request(tmp_path, request)
    result = prepare_task(tmp_path, 'request.json')
    assert result['outcome'] == 'blocked'
    assert result['diagnostics'][0]['code'] == 'DT-PROJECT-001'
    assert not any(row['requested'].startswith('ubongo/projects/other/') for row in result['manifest']['inputs'])
    assert 'OTHER_PROJECT_MEMORY_SENTINEL' not in json.dumps(result)


def test_non_utf8_root_is_a_typed_failure_not_broken_json(tmp_path):
    import os
    import sys
    from karakana.document_tasks.inputs import json_bytes
    if sys.platform == 'win32': pytest.skip('POSIX undecodable filesystem-name case')
    raw = os.fsencode(tmp_path) + b'/nonutf8-\xff'
    os.mkdir(raw)
    result = prepare_task(os.fsdecode(raw), 'request.json')
    assert result['outcome'] == 'blocked'
    assert json.loads(json_bytes(result))['manifest']['root'] is None
