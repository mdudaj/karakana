"""Storage for crosslink bundles."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.crosslinks.schemas import CrosslinkBundle
from karakana.crosslinks.summary import render_crosslink
from karakana.traces.schemas import now_utc


class CrosslinkStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / ".karakana" / "crosslinks"

    def save(self, bundle: CrosslinkBundle) -> Path:
        directory = self.bundle_dir(bundle.crosslink_id)
        for subdir in ["evidence", "proposed-updates/global-ubongo", "proposed-updates/skills", "proposed-updates/evals", "proposed-updates/prompts", "proposed-updates/skillpacks", "proposed-updates/issues"]:
            (directory / subdir).mkdir(parents=True, exist_ok=True)
        path = directory / "crosslink.json"
        path.write_text(json.dumps(bundle.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (directory / "crosslink.md").write_text(render_crosslink(bundle), encoding="utf-8")
        (directory / "boundaries.md").write_text("# Crosslink Boundary Review\n\n- No project memory was copied.\n- Apply is dry-run by default.\n", encoding="utf-8")
        self._write_latest(bundle.crosslink_id)
        return path

    def load(self, crosslink_id: str) -> CrosslinkBundle:
        path = self.bundle_dir(crosslink_id) / "crosslink.json"
        if not path.exists():
            raise FileNotFoundError(f"Crosslink not found: {crosslink_id}")
        return CrosslinkBundle.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list(self, limit: int = 20) -> list[CrosslinkBundle]:
        if not self.root.exists():
            return []
        bundles = []
        for path in self.root.iterdir():
            data = path / "crosslink.json"
            if data.exists():
                bundles.append(CrosslinkBundle.from_dict(json.loads(data.read_text(encoding="utf-8"))))
        return sorted(bundles, key=lambda item: item.created_at, reverse=True)[:limit]

    def latest(self) -> CrosslinkBundle | None:
        latest = self.root / "latest"
        if latest.exists():
            try:
                return self.load(latest.read_text(encoding="utf-8").strip())
            except FileNotFoundError:
                pass
        items = self.list(limit=1)
        return items[0] if items else None

    def bundle_dir(self, crosslink_id: str) -> Path:
        return self.root / crosslink_id

    def _write_latest(self, crosslink_id: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "latest").write_text(crosslink_id + "\n", encoding="utf-8")


def generate_crosslink_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-crosslink-{secrets.token_hex(3)}"


def create_bundle(workspace: str, projects, patterns) -> CrosslinkBundle:
    return CrosslinkBundle(crosslink_id=generate_crosslink_id(), workspace=workspace, status="ready_for_review", created_at=now_utc(), projects=projects, patterns=patterns, warnings=[], next_actions=["Review detected patterns.", "Generate proposals with `karakana crosslink propose <crosslink-id>`.", "Do not apply without explicit review."])
