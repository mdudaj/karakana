from pathlib import Path

from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.planner import build_workspace_plan


def test_workspace_plan_generates_prompt(tmp_path):
    workspace = WorkspaceLoader(Path.cwd()).load("default")

    path = build_workspace_plan(Path.cwd(), workspace, "karakana", "Review workspace status", output=tmp_path / "plan.md")

    assert path.exists()
    assert "Workspace Context" in path.read_text(encoding="utf-8")
