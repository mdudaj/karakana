"""Storage for requirement decomposition artifacts."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.requirements.schemas import IssueDraft, ReadinessCheck, RequirementPRD, UserStory
from karakana.requirements.summary import render_issues, render_prd, render_readiness, render_stories


class RequirementsStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / ".karakana" / "requirements"

    def save_prd(self, prd: RequirementPRD) -> Path:
        req_dir = self.req_dir(prd.req_id)
        req_dir.mkdir(parents=True, exist_ok=True)
        (req_dir / "source.json").write_text(json.dumps(prd.source.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        path = req_dir / "prd.json"
        path.write_text(json.dumps(prd.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (req_dir / "prd.md").write_text(render_prd(prd), encoding="utf-8")
        self._write_latest(prd.req_id)
        return path

    def load_prd(self, req_id: str) -> RequirementPRD:
        path = self.req_dir(req_id) / "prd.json"
        if not path.exists():
            raise FileNotFoundError(f"Requirement not found: {req_id}")
        return RequirementPRD.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save_stories(self, req_id: str, stories: list[UserStory]) -> Path:
        req_dir = self.req_dir(req_id)
        req_dir.mkdir(parents=True, exist_ok=True)
        path = req_dir / "stories.json"
        path.write_text(json.dumps([story.to_dict() for story in stories], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (req_dir / "stories.md").write_text(render_stories(stories), encoding="utf-8")
        return path

    def load_stories(self, req_id: str) -> list[UserStory]:
        path = self.req_dir(req_id) / "stories.json"
        if not path.exists():
            raise FileNotFoundError(f"Stories not found for requirement: {req_id}")
        return [UserStory.from_dict(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def save_issues(self, req_id: str, issues: list[IssueDraft]) -> Path:
        req_dir = self.req_dir(req_id)
        req_dir.mkdir(parents=True, exist_ok=True)
        path = req_dir / "issues.json"
        path.write_text(json.dumps([issue.to_dict() for issue in issues], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (req_dir / "issues.md").write_text(render_issues(issues), encoding="utf-8")
        return path

    def load_issues(self, req_id: str) -> list[IssueDraft]:
        path = self.req_dir(req_id) / "issues.json"
        if not path.exists():
            raise FileNotFoundError(f"Issues not found for requirement: {req_id}")
        return [IssueDraft.from_dict(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def save_readiness(self, check: ReadinessCheck) -> Path:
        req_dir = self.req_dir(check.req_id)
        req_dir.mkdir(parents=True, exist_ok=True)
        path = req_dir / "readiness.json"
        path.write_text(json.dumps(check.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (req_dir / "readiness.md").write_text(render_readiness(check), encoding="utf-8")
        return path

    def load_readiness(self, req_id: str) -> ReadinessCheck:
        path = self.req_dir(req_id) / "readiness.json"
        if not path.exists():
            raise FileNotFoundError(f"Readiness not found for requirement: {req_id}")
        return ReadinessCheck.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_requirements(self, limit: int = 20) -> list[str]:
        if not self.root.exists():
            return []
        req_ids = [path.name for path in self.root.iterdir() if path.is_dir() and (path / "prd.json").exists()]
        return sorted(req_ids, reverse=True)[:limit]

    def latest(self) -> str | None:
        latest = self.root / "latest"
        if latest.exists():
            req_id = latest.read_text(encoding="utf-8").strip()
            if req_id and (self.req_dir(req_id) / "prd.json").exists():
                return req_id
        items = self.list_requirements(limit=1)
        return items[0] if items else None

    def req_dir(self, req_id: str) -> Path:
        return self.root / req_id

    def _write_latest(self, req_id: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "latest").write_text(req_id + "\n", encoding="utf-8")


def generate_req_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-req-{secrets.token_hex(3)}"
