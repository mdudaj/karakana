from karakana.evals.runner import EvalRunner
from karakana.traces.store import TraceStore
from tests.test_eval_runner import write_eval, write_memory_tree, write_skill


def test_eval_run_creates_trace(tmp_path):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    write_eval(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")

    report = EvalRunner(tmp_path).run(suite="safety")
    trace = TraceStore(tmp_path).latest()

    assert trace.command == "eval run"
    assert trace.outputs["eval_run_id"] == report.eval_run_id
    assert trace.outputs["total_cases"] == 1
