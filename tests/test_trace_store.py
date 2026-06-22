from karakana.traces.schemas import TraceArtifact
from karakana.traces.store import TraceStore


def test_create_save_load_trace(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="plan",
        project="karakana",
        skill="karakana-self-improvement",
        task="Task",
        task_type="planning",
        selected_model="gpt-5-mini",
        inputs={"client_secret": "hidden"},
    )
    trace.outputs["prompt_path"] = ".karakana/planning-task.md"
    trace.artifacts.append(TraceArtifact(path=".karakana/planning-task.md", kind="planning_prompt"))
    trace.finish("success")

    trace_path = store.save(trace)
    loaded = store.load(trace.run_id)

    assert trace_path == tmp_path / ".karakana" / "runs" / trace.run_id / "trace.json"
    assert loaded.run_id == trace.run_id
    assert loaded.inputs["client_secret"] == "[REDACTED]"
    assert loaded.artifacts[0].path == ".karakana/planning-task.md"
    assert (tmp_path / ".karakana" / "runs" / trace.run_id / "summary.md").exists()


def test_list_and_latest_runs(tmp_path):
    store = TraceStore(tmp_path)
    first = store.create_run(command="first")
    first.finish("success")
    store.save(first)
    second = store.create_run(command="second")
    second.finish("failed")
    store.save(second)

    runs = store.list_runs()
    latest = store.latest()

    assert [run.command for run in runs[:2]] == ["second", "first"]
    assert latest is not None
    assert latest.command == "second"
