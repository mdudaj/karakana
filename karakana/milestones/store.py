"""Storage for next-milestone decision artifacts."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.milestones.schemas import NextMilestoneDecision
from karakana.milestones.summary import render_next_milestone


class MilestoneStore:
    def __init__(self, repo_root: Path):
        self.root = repo_root / ".karakana" / "milestones"

    def save(self, decision: NextMilestoneDecision, write_instructions: bool = False) -> tuple[Path, Path]:
        run_dir = self.run_dir(decision.run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        json_path = run_dir / "next-milestone.json"
        markdown_path = run_dir / "next-milestone.md"
        json_path.write_text(json.dumps(decision.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        markdown_path.write_text(render_next_milestone(decision), encoding="utf-8")
        if write_instructions:
            (run_dir / "instructions.md").write_text(decision.generated_instructions.rstrip() + "\n", encoding="utf-8")
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "latest").write_text(decision.run_id + "\n", encoding="utf-8")
        return markdown_path, json_path

    def run_dir(self, run_id: str) -> Path:
        return self.root / run_id

    def list_run_ids(self, limit: int = 20) -> list[str]:
        if not self.root.exists():
            return []
        ids = [path.name for path in self.root.iterdir() if path.is_dir() and (path / "next-milestone.json").exists()]
        return sorted(ids, reverse=True)[:limit]


def generate_milestone_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-milestone-{secrets.token_hex(3)}"
