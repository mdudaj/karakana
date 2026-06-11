from pathlib import Path

import pytest

from karakana.workspaces.loader import WorkspaceLoader


def test_workspace_loader_discovers_and_loads():
    loader = WorkspaceLoader(Path.cwd())

    assert "nimr" in loader.list_workspaces()
    assert loader.load("nimr").projects[0].id == "karakana"


def test_workspace_loader_missing():
    with pytest.raises(FileNotFoundError):
        WorkspaceLoader(Path.cwd()).load("missing")
