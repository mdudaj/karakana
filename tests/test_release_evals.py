from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_release_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="release")

    assert {case.id for case in cases} >= {
        "release-doctor-checks-core-files",
        "release-stable-profile-safe-defaults",
        "release-command-reference-includes-core-groups",
    }

