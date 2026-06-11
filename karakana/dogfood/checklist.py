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


MSC_PLATFORM_CHECKLIST_TEMPLATE = """# msc-platform Dogfood Checklist

## Repository and Workspace

- [ ] Workspace resolves `msc-platform`
- [ ] Repo path resolves to `../stemgen-platform`
- [ ] Remote points to `git@github.com:mdudaj/stemgen-platform.git`
- [ ] Skillpack `msc-platform` validates

## Research Alignment

- [ ] Objective-to-feature-to-evidence matrix exists
- [ ] Each planned slice maps to a research objective
- [ ] Each planned slice produces an evidence artifact
- [ ] Overengineering risks are documented

## Curriculum-Data Readiness

- [ ] TIE source registry exists
- [ ] Source registry includes curriculum, science, mathematics, and geography URLs
- [ ] Snapshot/fetch/checksum pipeline is documented
- [ ] Curriculum data schema exists
- [ ] Topic-screening rules exist

## Automated Review Safety

- [ ] Automated curriculum review is optional
- [ ] LLM review does not overwrite deterministic facts
- [ ] LLM review does not auto-accept topics
- [ ] Verbalized-sampling-inspired output distribution is defined
- [ ] Human topic selection gate is required

## Evaluation Readiness

- [ ] Evaluation workflow is documented
- [ ] Evidence model is documented
- [ ] Rubric is documented
- [ ] Export plan is documented
- [ ] Provenance/replay model is documented

## WhatsApp Channel

- [ ] WhatsApp is secondary, not canonical
- [ ] Web remains canonical review interface
- [ ] Opt-in is required
- [ ] Secure review links are used
- [ ] Message logging is redacted

## Commit and Push Safety

- [ ] No commit by default
- [ ] No push by default
- [ ] No push to main/master
- [ ] No force push
- [ ] Push requires explicit `--push`
- [ ] Patch review and patch gate are required before push

## Slice 1 Readiness

- [ ] Slice 1 issues are vertical
- [ ] Slice 1 schema artifacts are defined
- [ ] Slice 1 verification commands are defined
- [ ] Slice 1 out-of-scope boundaries are defined
"""


def generate_checklist(repo_root: Path, project: str, skillpack: str | None) -> tuple[str, Path]:
    store = DogfoodStore(repo_root)
    run = new_dogfood_run(project, skillpack, status="draft")
    path = store.save(run)
    checklist_path = path.parent / "checklist.md"
    template = MSC_PLATFORM_CHECKLIST_TEMPLATE if project == "msc-platform" and skillpack == "msc-platform" else CHECKLIST_TEMPLATE
    checklist_path.write_text(template, encoding="utf-8")
    return run.dogfood_id, checklist_path
