from typer.testing import CliRunner

from karakana.cli import app
from karakana.evals.loader import EvalLoader


def test_viewflow_eval_files_exist_and_load():
    cases = EvalLoader(__import__("pathlib").Path.cwd()).load_cases(skill="viewflow-framework")
    case_ids = {case.id for case in cases}

    assert case_ids == {
        "viewflow-workflow-design-review",
        "viewflow-frontend-form-review",
        "viewflow-permission-regression",
        "viewflow-process-state-transition",
    }


def test_viewflow_skill_eval_run_passes():
    result = CliRunner().invoke(app, ["eval", "run", "--skill", "viewflow-framework"])

    assert result.exit_code == 0
    assert "Status: passed" in result.output
    assert "Cases: 4, passed: 4, failed: 0, warnings: 0" in result.output
