"""Dogfood checklist generation."""

from __future__ import annotations

from pathlib import Path

from karakana.dogfood.summary import DogfoodStore, new_dogfood_run


CHECKLIST_TEMPLATE = """# Karakana Dogfood Checklist

## Setup

- [ ] `karakana version`
- [ ] `karakana doctor`
- [ ] `karakana config validate`
- [ ] `karakana release check`
- [ ] `karakana workspace activate default`
- [ ] `karakana workspace current`
- [ ] `karakana workspace status`

## Requirements Workflow

- [ ] Generate PRD from note
- [ ] Generate stories
- [ ] Generate issue drafts
- [ ] Run readiness check

## Action / Codex Workflow

- [ ] Generate or select action bundle
- [ ] Generate Codex handoff
- [ ] Capture diff
- [ ] Review patch
- [ ] Gate patch
- [ ] If no response file exists, prepare a reviewed model-response artifact manually.

## Learning Workflow

- [ ] Ingest Karakana project artifacts
- [ ] Review ingestion candidates
- [ ] Crosslink workspace knowledge

## Release Workflow

- [ ] `karakana eval run`
- [ ] `pytest`
- [ ] `karakana release check --full`

## Review

- [ ] Identify broken commands
- [ ] Identify UX friction
- [ ] Identify missing docs
- [ ] Identify missing evals
- [ ] Identify safety gaps
- [ ] Build v1 hardening backlog
"""


def generate_checklist(repo_root: Path, project: str, skillpack: str | None) -> tuple[str, Path]:
    store = DogfoodStore(repo_root)
    run = new_dogfood_run(project, skillpack, status="draft")
    path = store.save(run)
    checklist_path = path.parent / "checklist.md"
    checklist_path.write_text(CHECKLIST_TEMPLATE, encoding="utf-8")
    return run.dogfood_id, checklist_path
