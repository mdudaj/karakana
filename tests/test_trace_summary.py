from karakana.traces.schemas import RunTrace, SafetyCheck, TraceArtifact
from karakana.traces.summary import render_summary


def test_render_summary_contains_sections():
    trace = RunTrace(
        run_id="run",
        command="plan",
        project="karakana",
        skill="karakana-self-improvement",
        task="Task",
        task_type="planning",
        selected_model="gpt-5-mini",
        status="success",
        started_at="start",
        finished_at="finish",
        inputs={"project": "karakana"},
        outputs={"prompt_path": ".karakana/planning-task.md"},
        artifacts=[TraceArtifact(path=".karakana/planning-task.md", kind="planning_prompt")],
        safety_checks=[SafetyCheck(name="local-only", status="passed")],
        warnings=["warning"],
        errors=[],
        next_actions=["next"],
    )

    summary = render_summary(trace)

    assert "# Karakana Run Summary" in summary
    assert "- Run ID: run" in summary
    assert "## Inputs" in summary
    assert "`.karakana/planning-task.md`" in summary
    assert "- local-only: passed" in summary
    assert "- warning" in summary
    assert "- next" in summary
