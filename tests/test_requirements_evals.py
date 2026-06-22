from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_requirements_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="requirements")

    assert {case.id for case in cases} >= {
        "requirements-prd-from-action",
        "requirements-prd-has-harness-subsystems",
        "requirements-no-auto-publish",
    }
