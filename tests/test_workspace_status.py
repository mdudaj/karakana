from pathlib import Path

from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.status import collect_workspace_status


def test_workspace_status_collects_project_data():
    workspace = WorkspaceLoader(Path.cwd()).load("default")

    status = collect_workspace_status(Path.cwd(), workspace)

    assert status.project_statuses[0].project_id == "karakana"
    assert status.project_statuses[0].path_exists
    assert status.project_statuses[0].skillpack_valid is True
