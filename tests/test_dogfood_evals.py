from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_dogfood_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="dogfood")

    assert {case.id for case in cases} >= {
        "dogfood-checklist-covers-core-loop",
        "dogfood-run-is-safe-by-default",
        "dogfood-no-codex-execution",
    }

