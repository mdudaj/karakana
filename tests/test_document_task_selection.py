import json

import pytest

from karakana.document_tasks import prepare_task
from karakana.document_tasks.schemas import decode, validate_request, TaskError
from karakana.document_tasks.selection import INVENTORY
from tests.document_task_support import make_task, save_request, add_policy


def test_explicit_selection_keeps_origin_and_unselected_defaults(tmp_path):
    make_task(tmp_path); add_policy(tmp_path)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "prepared", result["diagnostics"]
    selected = result["selection"]["effective"]
    assert [(x["path"], x["origin"], x["revision_basis"]) for x in selected] == [("docs/guide.md", "task", "caller_declared")]
    assert result["selection"]["recommendations"][0]["selected"] is False
    read = {i["requested"] for i in result["manifest"]["inputs"]}
    assert "docs/template.md" not in read
    assert "docs/content-policy.json" in read


def test_opted_in_defaults_and_recorded_override(tmp_path):
    request = make_task(tmp_path); add_policy(tmp_path)
    request["use_project_defaults"] = True; save_request(tmp_path, request)
    first = prepare_task(tmp_path, "request.json")
    assert any(x["role"] == "template" and x["origin"] == "project_default" for x in first["selection"]["effective"])
    (tmp_path / "docs/local.md").write_text("Project-specific selected template")
    request["resources"].append({"artifact_type": "requirements", "role": "template", "path": "docs/local.md", "revision": "2"})
    save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "prepared"
    assert result["selection"]["overrides"][0]["previous"]["path"] == "docs/template.md"
    assert result["selection"]["overrides"][0]["effective"]["path"] == "docs/local.md"


@pytest.mark.parametrize("condition", ["missing", "different", "matching"])
def test_locks_are_explicit_and_cannot_be_waived(tmp_path, condition):
    request = make_task(tmp_path); policy = add_policy(tmp_path, mode="locked")
    request["use_project_defaults"] = True
    if condition != "missing":
        entry = {k: v for k, v in policy["bindings"][0].items() if k != "mode"}
        if condition == "different": entry["path"] = "docs/guide.md"
        request["resources"].append(entry)
    save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == ("prepared" if condition == "matching" else "blocked")
    if condition != "matching": assert result["diagnostics"][0]["code"] == "DT-LOCK-001"


@pytest.mark.parametrize("fault", ["project", "version", "duplicate", "mode", "reference"])
def test_invalid_project_policy_is_not_ignored(tmp_path, fault):
    make_task(tmp_path); policy = add_policy(tmp_path)
    if fault == "project": policy["project"] = "another-project"
    if fault == "version": policy["policy_version"] = "9"
    if fault == "duplicate": policy["bindings"].append(dict(policy["bindings"][0]))
    if fault == "mode": policy["bindings"][0]["mode"] = "ignore"
    if fault == "reference": policy["bindings"][0]["role"] = "reference"
    (tmp_path / "docs/content-policy.json").write_text(json.dumps(policy))
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] != "prepared"
    assert result["content_report"] is None


@pytest.mark.parametrize("action,kind", [("inquiry", "requirements"), ("mechanical_fix", "system-design"), ("review", "runbook")])
def test_unselected_resources_never_become_keyword_requirements(tmp_path, action, kind):
    request = make_task(tmp_path)
    request["task"]["action"] = action; request["task"]["artifact_types"] = [kind]
    request["resources"] = []; save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "prepared"
    assert result["selection"]["state"] == "not_selected"
    assert not result["selection"]["effective"]
    if kind == "runbook": assert not result["selection"]["recommendations"]


@pytest.mark.parametrize("raw", [b'{"a":1,"a":2}', b'{"a":NaN}', b'\xff', b'[' * 70 + b'0' + b']' * 70])
def test_json_refusals(raw):
    with pytest.raises(TaskError): decode(raw)


@pytest.mark.parametrize("fault", ["extra", "missing", "version", "project", "bool", "action", "types", "duplicate", "unknown_type", "control", "surrogate", "length"])
def test_request_contract_refusals(tmp_path, fault):
    request = make_task(tmp_path)
    if fault == "extra": request["extra"] = True
    if fault == "missing": del request["context"]
    if fault == "version": request["request_version"] = "0.2"
    if fault == "project": request["project"] = "../example"
    if fault == "bool": request["use_project_defaults"] = 1
    if fault == "action": request["task"]["action"] = "execute"
    if fault == "types": request["task"]["artifact_types"] *= 2
    if fault == "duplicate": request["resources"] *= 2
    if fault == "unknown_type": request["resources"][0]["artifact_type"] = "other"
    if fault == "control": request["task"]["scope"] = "bad\x1b[31m"
    if fault == "surrogate": request["task"]["scope"] = "\ud800"
    if fault == "length": request["task"]["text"] = "x" * 32769
    with pytest.raises(TaskError): validate_request(request)


def test_duplicate_physical_resource_references_refuse(tmp_path):
    request = make_task(tmp_path)
    (tmp_path / "docs/alias.md").symlink_to("guide.md")
    request["resources"] = [{"artifact_type": "requirements", "role": "reference", "path": path, "revision": "1"}
                            for path in ("docs/guide.md", "docs/alias.md")]
    save_request(tmp_path, request)
    assert prepare_task(tmp_path, "request.json")["outcome"] == "blocked"


def test_inventory_matches_real_document_resources():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    for kind, item in INVENTORY.items():
        assert (root / "skills" / item["owner"] / "SKILL.md").is_file()
        for role in ("guide", "template", "example"):
            assert (root / item[role]).is_file()


def test_unselected_unsafe_policy_binding_refuses_without_echoing_it(tmp_path):
    make_task(tmp_path); policy = add_policy(tmp_path)
    policy["bindings"][0]["path"] = ".env.private"
    (tmp_path / "docs/content-policy.json").write_text(json.dumps(policy))
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] != "prepared"
    assert '.env.private' not in json.dumps(result)


def test_registered_resource_unknown_version_refuses(tmp_path):
    request = make_task(tmp_path)
    entry = request['resources'][0]
    entry.update(path=INVENTORY['requirements']['guide'], revision='9')
    target = tmp_path / entry['path']; target.parent.mkdir(parents=True); target.write_text('Synthetic registered guide')
    save_request(tmp_path, request)
    assert prepare_task(tmp_path, 'request.json')['outcome'] == 'unsupported'
