from karakana.evals.loader import EvalLoader


def test_patch_evals_discoverable():
    cases = EvalLoader(__import__("pathlib").Path.cwd()).load_cases(suite="patch")
    ids = {case.id for case in cases}

    assert "patch-gate-blocks-secret" in ids
    assert "patch-status-includes-next-actions" in ids
