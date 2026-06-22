from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_crosslink_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="crosslinks")

    assert {case.id for case in cases} >= {
        "crosslinks-scan-detects-shared-skill",
        "crosslinks-project-memory-not-mixed",
        "crosslinks-no-cross-project-mutation",
    }

