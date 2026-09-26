from pathlib import Path

from karakana.workspaces.activation import WorkspaceActivation


def test_workspace_activation_state_written(isolated_repo):
    state = WorkspaceActivation(Path.cwd()).activate("default")

    assert state["workspace"] == "default"
    assert WorkspaceActivation(Path.cwd()).current()["workspace"] == "default"
