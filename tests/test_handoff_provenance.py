from pathlib import Path

import pytest
from typer.testing import CliRunner

from karakana.cli import app, _latest_project_protocol_trace
from karakana.handoffs.builder import create_handoff
from karakana.handoffs.store import HandoffStore
from karakana.okf.context import select_concepts
from karakana.okf.schemas import OkfConcept, OkfValidationResult
from karakana.traces.store import TraceStore
from tests.test_session_handoff import write_project_context, write_milestone


def make_trace(root, project="demo", command="protocol start", required=None):
    store = TraceStore(root)
    trace = store.create_run(command=command, project=project, protocol_id="python-code-change",
                             work_category="implementation", risk_level="low",
                             required_artifacts=required if required is not None else ["trace"])
    store.save(trace)
    return trace


def test_graph_edges_preserve_project_and_status(monkeypatch, tmp_path):
    def concept(name, project="demo", status="active", tags=None, links=None):
        return OkfConcept(Path(name), {"id": name, "project": project, "status": status,
                          "tags": tags or [], "relationships": {"related": links or []}}, "")
    nodes = [concept("start", tags=["entry"], links=["foreign", "retired", "related"]),
             concept("foreign", project="other", links=["bridge"]),
             concept("retired", status="deprecated"), concept("related", links=["start"]),
             concept("bridge")]
    monkeypatch.setattr("karakana.okf.context.OkfValidator.validate",
                        lambda self: OkfValidationResult(tmp_path, concepts=nodes))
    result = select_concepts(tmp_path, project="demo", tags={"entry"}, statuses={"active"},
                             relationship_depth=3)
    assert {item.concept_id for item in result} == {"start", "related"}


def test_classification_does_not_replace_task_trace(tmp_path):
    task = make_trace(tmp_path)
    make_trace(tmp_path, command="protocol classify")
    assert _latest_project_protocol_trace(tmp_path, "demo").run_id == task.run_id


def test_project_filter_precedes_trace_limit(tmp_path):
    task = make_trace(tmp_path)
    for _ in range(55):
        make_trace(tmp_path, project="other")
    assert _latest_project_protocol_trace(tmp_path, "demo").run_id == task.run_id


def test_exact_trace_binding_and_wrong_project_rejected(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    task = make_trace(tmp_path)
    make_trace(tmp_path, required=["requirements_note"])
    runner = CliRunner()
    result = runner.invoke(app, ["handoff", "refresh", "--project", "demo",
                                 "--protocol-trace", task.run_id, "--require-protocol-pass"])
    assert result.exit_code == 0, result.output
    foreign = make_trace(tmp_path, project="other")
    result = runner.invoke(app, ["handoff", "refresh", "--project", "demo",
                                 "--protocol-trace", foreign.run_id])
    assert result.exit_code == 1
    assert "project mismatch" in result.output
    assert len(HandoffStore(tmp_path).list(project="demo")) == 1


def test_strict_refresh_fails_without_protocol_trace(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["handoff", "refresh", "--project", "demo", "--require-protocol-pass"])
    assert result.exit_code == 1
    assert "No eligible protocol trace" in result.output


@pytest.mark.parametrize("kind", ["classification", "missing", "traversal"])
def test_invalid_explicit_trace_rejected(tmp_path, monkeypatch, kind):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    trace_id = {"missing": "does-not-exist", "traversal": "../trace"}.get(kind)
    if trace_id is None:
        trace_id = make_trace(tmp_path, command="protocol classify").run_id
    result = CliRunner().invoke(app, ["handoff", "refresh", "--project", "demo",
                                     "--protocol-trace", trace_id])
    assert result.exit_code == 1
    assert not HandoffStore(tmp_path).list(project="demo")


def test_recovery_stores_filter_before_limit(tmp_path):
    from karakana.dogfood.summary import DogfoodStore, new_dogfood_run
    from karakana.ingestion.store import IngestionStore, create_bundle

    dogs, ingests = DogfoodStore(tmp_path), IngestionStore(tmp_path)
    original_dog = new_dogfood_run("demo", None)
    original_ingest = create_bundle("demo", None, [], [], False, [])
    original_dog.created_at = original_ingest.created_at = "2000-01-01T00:00:00+00:00"
    dogs.save(original_dog)
    ingests.save(original_ingest)
    for _ in range(22):
        dogs.save(new_dogfood_run("other", None))
        ingests.save(create_bundle("other", None, [], [], False, []))
    assert dogs.list(limit=1, project="demo")[0].dogfood_id == original_dog.dogfood_id
    assert ingests.list(limit=1, project="demo")[0].ingest_id == original_ingest.ingest_id


def test_runtime_write_guard_and_empty_fixture(isolated_repo):
    from tests.conftest import RUNTIME

    assert not (isolated_repo / ".karakana").exists()
    with pytest.raises(AssertionError, match="real .karakana"):
        (RUNTIME / "must-not-exist.txt").write_text("synthetic")
    local = isolated_repo / ".karakana"
    local.mkdir()
    (local / "test.txt").write_text("isolated")
    assert (local / "test.txt").read_text() == "isolated"


def test_explicit_state_can_omit_recovery_without_deleting_history(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    old = write_milestone(tmp_path)
    store = HandoffStore(tmp_path)
    previous = create_handoff(tmp_path, "demo")
    store.save(previous)
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["handoff", "refresh", "--project", "demo",
                         "--no-recover-artifacts", "--current-milestone", "Current work",
                         "--next-task", "Continue current work"])
    assert result.exit_code == 0, result.output
    handoff = store.latest("demo")
    assert str(old) not in handoff.reference_artifacts
    assert str(old) not in handoff.inspect_first
    assert handoff.previous_handoff_id == previous.handoff_id
    assert old.exists()


def test_skillpack_filter_precedes_handoff_limit(tmp_path):
    write_project_context(tmp_path)
    store = HandoffStore(tmp_path)
    original = create_handoff(tmp_path, "demo")
    original.created_at = original.updated_at = "2000-01-01T00:00:00+00:00"
    store.save(original)
    for _ in range(22):
        other = create_handoff(tmp_path, "demo")
        other.skillpack = "other-pack"
        store.save(other)
    assert store.latest("demo", "demo").handoff_id == original.handoff_id
