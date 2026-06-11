from karakana.workspaces.schemas import Workspace, WorkspaceProject


def test_workspace_schema_to_dict():
    workspace = Workspace(name="demo", description="Demo", version="0.1.0", status="stable", projects=[WorkspaceProject(id="karakana", path=".")])

    assert workspace.to_dict()["projects"][0]["id"] == "karakana"
