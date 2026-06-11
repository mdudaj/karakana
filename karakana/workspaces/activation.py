"""Local workspace activation state."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.traces.schemas import now_utc
from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.validator import WorkspaceValidator


class WorkspaceActivation:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.path = repo_root / ".karakana" / "current-workspace.json"

    def activate(self, name: str) -> dict:
        result = WorkspaceValidator(self.repo_root).validate(name)
        if not result.ok:
            raise ValueError("; ".join(result.errors))
        WorkspaceLoader(self.repo_root).load(name)
        state = {"workspace": name, "activated_at": now_utc()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return state

    def current(self) -> dict | None:
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def current_workspace(self):
        state = self.current()
        return WorkspaceLoader(self.repo_root).load(state["workspace"]) if state else None
