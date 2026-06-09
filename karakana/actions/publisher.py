"""Explicit opt-in publishing for action bundles."""

from __future__ import annotations

from pathlib import Path

from karakana.actions.schemas import ActionBundle
from karakana.tools.github_api import GitHubApiClient


class ActionPublisher:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def publish(
        self,
        bundle: ActionBundle,
        create_issues: bool = False,
        create_proposals: bool = False,
        create_codex_tasks: bool = False,
    ) -> dict:
        if bundle.status == "blocked":
            raise ValueError("Refusing to publish actions from a blocked response.")
        result = {
            "dry_run": not any([create_issues, create_proposals, create_codex_tasks]),
            "would_create_issues": len([a for a in bundle.actions if a.action_type == "github_issue_draft"]),
            "would_create_proposals": len([a for a in bundle.actions if a.action_type in {"improvement_proposal", "memory_update", "skill_update", "prompt_update", "eval_case", "documentation_update"}]),
            "would_create_codex_tasks": len([a for a in bundle.actions if a.action_type == "codex_task"]),
            "created_issue_urls": [],
            "created_codex_task_paths": [],
        }
        if create_issues:
            client = GitHubApiClient()
            for action in bundle.actions:
                if action.action_type != "github_issue_draft":
                    continue
                created = client.create_issue(action.title, action.description, labels=["karakana", "needs-review"])
                result["created_issue_urls"].append(created.get("html_url"))
        if create_codex_tasks:
            output_root = self.repo_root / ".karakana" / "codex-tasks" / bundle.action_run_id
            output_root.mkdir(parents=True, exist_ok=True)
            for action in bundle.actions:
                if action.action_type != "codex_task":
                    continue
                source = action.metadata.get("artifact_path")
                if source:
                    source_path = self.repo_root / source
                    target = output_root / f"{action.action_id}.md"
                    target.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
                    result["created_codex_task_paths"].append(str(target))
        if create_proposals:
            result["created_proposals"] = "not implemented; action artifacts remain under .karakana/actions/"
        return result
