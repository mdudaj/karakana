"""Dry-run requirements publishing."""

from __future__ import annotations

from pathlib import Path

from karakana.requirements.store import RequirementsStore


class RequirementsPublisher:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.store = RequirementsStore(repo_root)

    def publish(self, req_id: str, *, create_issues: bool = False) -> dict:
        issues = []
        try:
            issues = self.store.load_issues(req_id)
        except FileNotFoundError:
            pass
        if not create_issues:
            return {
                "dry_run": True,
                "req_id": req_id,
                "would_create_issues": len(issues),
                "message": "Dry run: no GitHub issues were created.",
            }
        return {
            "dry_run": False,
            "req_id": req_id,
            "created_issues": [],
            "message": "Issue publishing is not implemented yet. Use the generated issue drafts manually.",
        }
