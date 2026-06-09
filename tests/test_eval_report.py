from karakana.evals.report import EvalReportStore
from karakana.evals.schemas import EvalCase, EvalCaseResult, EvalExpectation, EvalInput, EvalRunReport


def test_eval_report_writes_json_markdown_and_case_artifacts(tmp_path):
    case = EvalCase(
        id="case",
        name="Case",
        description="",
        suite="safety",
        input=EvalInput(task="Task"),
        expectations=EvalExpectation(),
    )
    report = EvalRunReport(
        eval_run_id="run",
        status="passed",
        started_at="start",
        finished_at="finish",
        total_cases=1,
        passed=1,
        failed=0,
        warnings=0,
        results=[EvalCaseResult(case_id="case", status="passed", score=1.0, output_excerpt="ok")],
    )

    path = EvalReportStore(tmp_path).save(report, [case])

    assert path.exists()
    assert (tmp_path / ".karakana" / "eval-runs" / "run" / "report.md").exists()
    assert (tmp_path / ".karakana" / "eval-runs" / "run" / "cases" / "case.json").exists()
    assert EvalReportStore(tmp_path).latest().eval_run_id == "run"
