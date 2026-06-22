from pathlib import Path

from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.status import collect_workspace_status
from karakana.workspaces.summary import render_workspace_summary


def test_workspace_summary_contains_projects():
    workspace = WorkspaceLoader(Path.cwd()).load("nimr")
    status = collect_workspace_status(Path.cwd(), workspace)

    summary = render_workspace_summary(workspace, status)

    assert "# Karakana Workspace Summary" in summary
    assert "### karakana" in summary
    assert "### nhrdm" in summary
