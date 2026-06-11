from pathlib import Path

from karakana.workspaces.boundaries import ensure_project_path_allowed, resolve_project_root
from karakana.workspaces.loader import WorkspaceLoader


def test_workspace_boundary_checks():
    workspace = WorkspaceLoader(Path.cwd()).load("default")
    root = resolve_project_root(workspace, "karakana", repo_root=Path.cwd())

    assert root == Path.cwd().resolve()
    assert ensure_project_path_allowed(workspace, "karakana", Path.cwd() / "README.md", repo_root=Path.cwd()) == []
    assert ensure_project_path_allowed(workspace, "karakana", Path("/tmp/outside"), repo_root=Path.cwd())
