import pytest

from karakana.evals.schemas import EvalCaseResult, EvalRunReport


def test_eval_case_result_status_validation():
    with pytest.raises(ValueError, match="Invalid eval case status"):
        EvalCaseResult(case_id="case", status="bad", score=0.0)


def test_eval_run_report_serializes_results():
    report = EvalRunReport(
        eval_run_id="run",
        status="passed",
        started_at="start",
        finished_at="finish",
        total_cases=1,
        passed=1,
        failed=0,
        warnings=0,
        results=[EvalCaseResult(case_id="case", status="passed", score=1.0)],
    )

    data = report.to_dict()

    assert data["results"][0]["case_id"] == "case"
    assert EvalRunReport.from_dict(data).results[0].status == "passed"
