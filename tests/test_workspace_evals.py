from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_workspace_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="workspaces")

    assert {case.id for case in cases} >= {
        "workspaces-list-workspaces",
        "workspaces-status-preserves-boundaries",
        "workspaces-no-cross-project-memory-mixing",
    }
