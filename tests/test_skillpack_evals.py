from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_skillpack_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="skillpacks")
    ids = {case.id for case in cases}

    assert "skillpacks-list-skillpacks" in ids
    assert "skillpacks-codex-handoff-includes-skillpack-tests" in ids
