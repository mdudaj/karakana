"""Storage for extracted action bundles."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.actions.schemas import ActionBundle, ExtractedAction
from karakana.actions.summary import render_action_artifact, render_action_bundle, render_handoff


class ActionStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.actions_root = repo_root / ".karakana" / "actions"

    def save(self, bundle: ActionBundle, output_dir: Path | None = None) -> Path:
        bundle_dir = self._bundle_dir(bundle.action_run_id, output_dir)
        bundle_dir.mkdir(parents=True, exist_ok=True)
        artifact_paths: dict[str, str] = {}
        for subdir in ["codex-tasks", "issue-drafts", "proposals", "checklists"]:
            (bundle_dir / subdir).mkdir(exist_ok=True)
        for action in bundle.actions:
            artifact_path = self._write_action_artifact(bundle_dir, action, bundle.source.path)
            artifact_paths[action.action_id] = str(artifact_path.relative_to(self.repo_root)) if artifact_path.is_relative_to(self.repo_root) else str(artifact_path)
            action.metadata["artifact_path"] = artifact_paths[action.action_id]
        actions_json = bundle_dir / "actions.json"
        actions_json.write_text(json.dumps(bundle.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (bundle_dir / "actions.md").write_text(render_action_bundle(bundle, artifact_paths), encoding="utf-8")
        (bundle_dir / "handoff.md").write_text(render_handoff(bundle, artifact_paths), encoding="utf-8")
        self._write_latest(bundle.action_run_id)
        return actions_json

    def load(self, action_run_id: str) -> ActionBundle:
        path = self.actions_root / action_run_id / "actions.json"
        if not path.exists():
            raise FileNotFoundError(f"Action bundle not found: {action_run_id}")
        return ActionBundle.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_bundles(self, limit: int = 20) -> list[ActionBundle]:
        if not self.actions_root.exists():
            return []
        bundles = []
        for path in self.actions_root.iterdir():
            action_path = path / "actions.json"
            if path.is_dir() and action_path.exists():
                bundles.append(ActionBundle.from_dict(json.loads(action_path.read_text(encoding="utf-8"))))
        return sorted(bundles, key=lambda bundle: bundle.created_at, reverse=True)[:limit]

    def latest(self) -> ActionBundle | None:
        latest_path = self.actions_root / "latest"
        if latest_path.exists():
            action_run_id = latest_path.read_text(encoding="utf-8").strip()
            if action_run_id:
                try:
                    return self.load(action_run_id)
                except FileNotFoundError:
                    pass
        bundles = self.list_bundles(limit=1)
        return bundles[0] if bundles else None

    def bundle_dir(self, action_run_id: str) -> Path:
        return self.actions_root / action_run_id

    def _bundle_dir(self, action_run_id: str, output_dir: Path | None) -> Path:
        if output_dir is None:
            return self.actions_root / action_run_id
        path = output_dir if output_dir.is_absolute() else self.repo_root / output_dir
        resolved = path.resolve()
        karakana = (self.repo_root / ".karakana").resolve()
        if not (resolved == karakana or resolved.is_relative_to(karakana)):
            raise ValueError("Action output must be under .karakana/.")
        return path

    def _write_action_artifact(self, bundle_dir: Path, action: ExtractedAction, source_path: str | None) -> Path:
        if action.action_type == "codex_task":
            path = bundle_dir / "codex-tasks" / f"{action.action_id}.md"
        elif action.action_type == "github_issue_draft":
            path = bundle_dir / "issue-drafts" / f"{action.action_id}.md"
        elif action.action_type in {"improvement_proposal", "memory_update", "skill_update", "prompt_update", "eval_case", "documentation_update"}:
            path = bundle_dir / "proposals" / f"{action.action_id}.md"
        else:
            path = bundle_dir / "checklists" / f"{action.action_id}.md"
        path.write_text(render_action_artifact(action, source_path), encoding="utf-8")
        return path

    def _write_latest(self, action_run_id: str) -> None:
        self.actions_root.mkdir(parents=True, exist_ok=True)
        (self.actions_root / "latest").write_text(action_run_id + "\n", encoding="utf-8")


def generate_action_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-actions-{secrets.token_hex(3)}"
