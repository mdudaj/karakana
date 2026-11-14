import hashlib
import json
from pathlib import Path
import socket
import subprocess

import pytest

from karakana.agents.planner import compose_planning_prompt
from karakana.document_tasks import prepare_task
from tests.document_task_support import make_task, save_request, FIXTURES
from tests.test_planner import write_memory_tree, write_skill


@pytest.mark.parametrize("case", json.loads((FIXTURES / "legacy-prompts.json").read_text())["cases"], ids=lambda row: row["case"])
def test_complete_legacy_prompt_bytes_match_pre_refactor_baseline(tmp_path, case):
    write_memory_tree(tmp_path); write_skill(tmp_path)
    if case["case"] != "fallback": (tmp_path / "KARAKANA.md").write_text("# Contract\n\nProject contract content.\n")
    if case["case"] == "missing_memory": (tmp_path / "ubongo/projects/karakana/overview.md").unlink()
    raw = compose_planning_prompt("karakana", "example-skill", "Review selected scope", tmp_path, **case["kwargs"]).encode()
    assert len(raw) == case["bytes"]
    assert hashlib.sha256(raw).hexdigest() == case["sha256"]


def test_selected_capture_and_saved_result_are_actual_and_source_preserving(tmp_path):
    make_task(tmp_path)
    (tmp_path / "AGENTS.md").write_text("Repository instruction sentinel")
    before = {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "prepared", result["diagnostics"]
    bundle = tmp_path / result["run"]["bundle"]
    assert json.loads((bundle / "result.json").read_text()) == result
    prompt = (bundle / "prompt.md").read_text()
    assert "Selected synthetic guide" in prompt and "Repository instruction sentinel" in prompt
    assert "BEGIN CAPTURED INPUT" in prompt and "caller_declared" in prompt
    assert result["content_report"] is None
    assert result["freshness"] == {"inputs": "current", "saved_bundle": "not_assessed"}
    assert result["selection"]["instruction_review_required"] is True
    assert result["manifest"]["wrapper"]["version"] == "0.2.0"
    assert all(p.read_bytes() == raw for p, raw in before.items())


def test_unselected_capture_preserves_memory_and_task_scope_without_loading_a_pack(tmp_path):
    request = make_task(tmp_path); request["resources"] = []; save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    prompt = (tmp_path / result["run"]["bundle"] / "prompt.md").read_text()
    assert 'Selected synthetic guide' not in prompt
    assert '# Ubongo Memory: example' in prompt and 'Name: example-skill' in prompt
    assert request['task']['text'] in prompt and 'Draft the requested document' in prompt
    assert 'Return a structured implementation plan with:' not in prompt
    assert result['selection']['state'] == 'not_selected'


def test_no_recursive_reads_other_project_parser_checker_or_execution(tmp_path, monkeypatch):
    request = make_task(tmp_path)
    (tmp_path / "docs/unselected.md").write_text("UNSELECTED_SENTINEL")
    (tmp_path / "docs/unselected.key").write_text("SYNTHETIC_RESTRICTED_SENTINEL")
    original_open = Path.open; reads = []

    def watched(path, mode="r", *args, **kwargs):
        if 'r' in mode and path.is_relative_to(tmp_path): reads.append(path.relative_to(tmp_path).as_posix())
        return original_open(path, mode, *args, **kwargs)

    def forbidden(*args, **kwargs): raise AssertionError("Unexpected execution/network")
    monkeypatch.setattr(Path, "open", watched)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)
    import karakana.tools.engineering_content as checker
    monkeypatch.setattr(checker, "check_content", forbidden)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "prepared"
    assert "docs/unselected.md" not in reads and "docs/unselected.key" not in reads
    assert all(not path.startswith("ubongo/projects/other/") for path in reads)
    assert not any(path.startswith(".karakana/handoffs") for path in reads)


@pytest.mark.parametrize("version", ["0.1", "0.2"])
def test_context_declarations_validate_without_loading_future_source(tmp_path, version):
    request = make_task(tmp_path); request["context"] = "context.json"
    context = {"context_version": version, "namespace": "neutral", "documents": [
        {"key": "future", "path": "future-not-created.md", "format": "narrative-0.1", "profile": {"id": "requirements", "version": "0.1"}}]}
    (tmp_path / "context.json").write_text(json.dumps(context)); save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] == "prepared", result["diagnostics"]
    assert result["selection"]["context"]["namespace"] == "neutral"
    assert result["selection"]["context"]["context_version"] == version
    assert not (tmp_path / "future-not-created.md").exists()
    assert "future-not-created.md" not in {x["requested"] for x in result["manifest"]["inputs"]}
    assert result["content_report"] is None


@pytest.mark.parametrize("fault", ["profile", "format", "links", "type", "unsafe"])
def test_context_refusals_never_strip_or_filter_declarations(tmp_path, fault):
    request = make_task(tmp_path); request["context"] = "context.json"
    doc = {"key": "future", "path": "future.md", "format": "narrative-0.1", "profile": {"id": "requirements", "version": "0.1"}}
    context = {"context_version": "0.1", "namespace": "example", "documents": [doc]}
    if fault == "profile": doc["profile"]["version"] = "9"
    if fault == "format": doc["format"] = "p02"
    if fault == "links": context["links"] = []
    if fault == "type": doc["profile"]["id"] = "system-design"
    if fault == "unsafe": doc["path"] = ".env"
    (tmp_path / "context.json").write_text(json.dumps(context)); save_request(tmp_path, request)
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] != "prepared" and result["content_report"] is None


@pytest.mark.parametrize("missing", ["memory", "skill", "asset", "bad_template", "bad_skill"])
def test_missing_or_malformed_fixed_and_selected_inputs_refuse(tmp_path, missing):
    make_task(tmp_path)
    if missing == "memory": (tmp_path / "ubongo/projects/example/overview.md").unlink()
    if missing == "skill": (tmp_path / "skills/example-skill/SKILL.md").unlink()
    if missing == "asset": (tmp_path / "docs/guide.md").unlink()
    if missing == "bad_template":
        (tmp_path / "prompts").mkdir(); (tmp_path / "prompts/planner.prompt.md").write_text("{unsupported_field}")
    if missing == "bad_skill": (tmp_path / "skills/example-skill/SKILL.md").write_text("---\n[unterminated\n---\nBody")
    result = prepare_task(tmp_path, "request.json")
    assert result["outcome"] != "prepared"
    assert result["diagnostics"]


def test_equivalent_preparations_have_same_deterministic_fields(tmp_path):
    make_task(tmp_path)
    first = prepare_task(tmp_path, "request.json"); second = prepare_task(tmp_path, "request.json")
    assert first["outcome"] == second["outcome"] == "prepared"
    assert first["run"]["id"] != second["run"]["id"]
    assert {k: v for k, v in first.items() if k != "run"} == {k: v for k, v in second.items() if k != "run"}


@pytest.mark.parametrize('source', ['context.json', 'docs/content-policy.json'])
def test_malformed_configuration_error_locates_its_actual_source(tmp_path, source):
    request = make_task(tmp_path)
    if source == 'context.json': request['context'] = source
    (tmp_path / source).write_text('{"duplicate":1,"duplicate":2}')
    save_request(tmp_path, request)
    result = prepare_task(tmp_path, 'request.json')
    assert result['outcome'] == 'blocked'
    assert result['diagnostics'][0]['location']['path'] == source


@pytest.mark.parametrize('action,expected', [
    ('inquiry', 'Return the requested information'), ('analysis', 'Return evidence-grounded analysis'),
    ('review', 'Return source-grounded review findings'), ('author', 'Draft the requested document'),
    ('revise', 'Revise the requested document'), ('plan', 'Return the requested proposed plan'),
    ('mechanical_fix', 'Make only the requested mechanical correction')])
def test_prepared_prompt_preserves_action_audience_scope_revision(tmp_path, action, expected):
    request = make_task(tmp_path); request['task']['action'] = action; request['resources'] = []
    (tmp_path / 'prompts').mkdir()
    (tmp_path / 'prompts/planner.prompt.md').write_text('# Custom template that omits task/output fields')
    save_request(tmp_path, request)
    result = prepare_task(tmp_path, 'request.json')
    assert result['outcome'] == 'prepared'
    prompt = (tmp_path / result['run']['bundle'] / 'prompt.md').read_text()
    assert expected in prompt and 'Return a structured implementation plan with:' not in prompt
    assert request['task']['text'] in prompt
    for key in ('action', 'audience', 'scope', 'revision'):
        assert json.dumps(request['task'][key]) in prompt
