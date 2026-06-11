from pathlib import Path

from karakana.workspaces.handoff import write_workspace_handoff
from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.status import collect_workspace_status


def test_workspace_handoff_writes_artifacts(tmp_path):
    workspace = WorkspaceLoader(Path.cwd()).load("default")
    status = collect_workspace_status(Path.cwd(), workspace, project_id="karakana")

    handoff_id, path = write_workspace_handoff(tmp_path, workspace, status, "karakana")

    assert handoff_id
    assert path.exists()
    assert "Workspace Project Handoff" in path.read_text(encoding="utf-8")
