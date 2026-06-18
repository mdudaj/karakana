"""Durable storage and project-aware selection for handoffs."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.handoffs.schemas import HandoffArtifact
from karakana.handoffs.summary import render_handoff


class HandoffStore:
    def __init__(self, repo_root: Path):
        self.root = repo_root / ".karakana" / "handoffs"

    def save(self, handoff: HandoffArtifact) -> tuple[Path, Path]:
        run_dir = self.run_dir(handoff.handoff_id)
        run_dir.mkdir(parents=True, exist_ok=False)
        json_path = run_dir / "handoff.json"
        markdown_path = run_dir / "handoff.md"
        json_path.write_text(json.dumps(handoff.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        markdown_path.write_text(render_handoff(handoff), encoding="utf-8")
        return markdown_path, json_path

    def load(self, handoff_id: str) -> HandoffArtifact:
        path = self.run_dir(handoff_id) / "handoff.json"
        if not path.exists():
            raise FileNotFoundError(f"Handoff not found: {handoff_id}")
        return HandoffArtifact.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list(self, project: str | None = None, limit: int = 20) -> list[HandoffArtifact]:
        if not self.root.exists():
            return []
        handoffs: list[HandoffArtifact] = []
        for path in self.root.glob("*/handoff.json"):
            try:
                handoff = HandoffArtifact.from_dict(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError, TypeError):
                continue
            if project is None or handoff.project == project:
                handoffs.append(handoff)
        handoffs.sort(key=_handoff_sort_key, reverse=True)
        return handoffs[:limit]

    def latest(self, project: str, skillpack: str | None = None) -> HandoffArtifact | None:
        return next(
            (
                item for item in self.list(project=project)
                if skillpack is None or item.skillpack == skillpack
            ),
            None,
        )

    def run_dir(self, handoff_id: str) -> Path:
        if not handoff_id or Path(handoff_id).name != handoff_id:
            raise ValueError(f"Invalid handoff ID: {handoff_id}")
        return self.root / handoff_id


def generate_handoff_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-handoff-{secrets.token_hex(3)}"


def _handoff_sort_key(handoff: HandoffArtifact) -> tuple[str, str, str]:
    return (handoff.updated_at, handoff.created_at, handoff.handoff_id)
