"""Convert dogfood backlog into requirements artifacts."""

from __future__ import annotations

from pathlib import Path

from karakana.dogfood.summary import DogfoodStore
from karakana.requirements.issues import generate_issues
from karakana.requirements.prd import generate_prd
from karakana.requirements.readiness import check_readiness
from karakana.requirements.sources import load_note_requirement_source
from karakana.requirements.store import RequirementsStore
from karakana.requirements.stories import generate_stories
from karakana.skillpacks.resolver import SkillpackResolver


def requirements_from_dogfood(repo_root: Path, dogfood_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[str, list[Path]]:
    run = DogfoodStore(repo_root).load(dogfood_id)
    project_name = project or run.project
    skillpack_name = skillpack or run.skillpack
    content = _content(run)
    source, text = load_note_requirement_source(content, project=project_name, skillpack=skillpack_name)
    try:
        skillpack_context = SkillpackResolver(repo_root).resolve_for_project(skillpack_name) if skillpack_name else None
    except Exception:
        skillpack_context = None
    prd = generate_prd(source, text, project=project_name, skillpack_context=skillpack_context)
    store = RequirementsStore(repo_root)
    paths = [store.save_prd(prd)]
    stories = generate_stories(prd)
    paths.append(store.save_stories(prd.req_id, stories))
    issues = generate_issues(prd, stories)
    paths.append(store.save_issues(prd.req_id, issues))
    readiness = check_readiness(prd)
    paths.append(store.save_readiness(readiness))
    return prd.req_id, paths


def _content(run) -> str:
    lines = [
        f"Dogfood run: {run.dogfood_id}",
        f"Project: {run.project}",
        f"Status: {run.status}",
        "",
        "Goal: Convert dogfood findings into v1 hardening requirements.",
        "",
        "Findings:",
    ]
    lines.extend(f"- {finding.severity}: {finding.title} ({finding.finding_type})" for finding in run.findings)
    lines.append("")
    lines.append("Backlog:")
    lines.extend(f"- {item.priority}: {item.title} ({item.item_type})" for item in run.backlog)
    lines.append("")
    lines.append("Non-goals: Do not execute Codex. Do not publish GitHub issues. Do not apply patches. Do not deploy.")
    return "\n".join(lines)
