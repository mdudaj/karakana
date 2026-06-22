"""Local skillpack activation state."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.schemas import Skillpack
from karakana.skillpacks.validator import SkillpackValidator
from karakana.traces.schemas import now_utc


class SkillpackActivation:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.path = repo_root / ".karakana" / "current-skillpack.json"

    def activate(self, name: str) -> dict:
        result = SkillpackValidator(self.repo_root).validate(name)
        if not result.ok:
            raise ValueError("; ".join(result.errors))
        skillpack = SkillpackLoader(self.repo_root).load(name)
        state = {"skillpack": skillpack.name, "activated_at": now_utc(), "project": skillpack.project.id}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return state

    def current(self) -> dict | None:
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def current_skillpack(self) -> Skillpack | None:
        state = self.current()
        if not state:
            return None
        return SkillpackLoader(self.repo_root).load(state["skillpack"])
