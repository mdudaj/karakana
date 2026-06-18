"""Project-aware handoff creation and bounded artifact recovery."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from karakana.dogfood.summary import DogfoodStore
from karakana.handoffs.redaction import redact_handoff_text
from karakana.handoffs.schemas import HandoffArtifact
from karakana.handoffs.store import HandoffStore, generate_handoff_id
from karakana.ingestion.store import IngestionStore
from karakana.milestones.store import MilestoneStore
from karakana.requirements.store import RequirementsStore
from karakana.skillpacks.loader import SkillpackLoader
from karakana.traces.schemas import now_utc
from karakana.workspaces.loader import WorkspaceLoader


@dataclass
class RecoveredState:
    source_artifacts: list[str] = field(default_factory=list)
    summaries: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    open_findings: list[str] = field(default_factory=list)
    suggested_skills: list[str] = field(default_factory=list)
    current_milestone: str | None = None
    exact_next_action: str | None = None
    warnings: list[str] = field(default_factory=list)


def create_handoff(
    repo_root: Path,
    project: str,
    skillpack: str | None = None,
    workspace: str | None = None,
    purpose: str | None = None,
    current_milestone: str | None = None,
    from_note: str | None = None,
    from_dogfood: str | None = None,
    from_requirements: str | None = None,
    from_milestone: str | None = None,
    recovered: bool = False,
    previous_handoff_id: str | None = None,
) -> HandoffArtifact:
    skillpack_name = skillpack or project
    loaded_skillpack = SkillpackLoader(repo_root).load(skillpack_name)
    if loaded_skillpack.project.id != project:
        raise ValueError(f"Skillpack project mismatch: expected {project}, found {loaded_skillpack.project.id}.")
    state = _recover_state(
        repo_root,
        project,
        from_dogfood=from_dogfood,
        from_requirements=from_requirements,
        from_milestone=from_milestone,
    )
    now = now_utc()
    milestone = redact_handoff_text(current_milestone or state.current_milestone or "Verify recovered project state")
    handoff_purpose = redact_handoff_text(purpose or f"Continue {milestone} in a fresh session")
    note = redact_handoff_text(from_note)
    if note:
        state.summaries.append(f"User-provided state: {note}")
    inspect_first = _inspect_first(repo_root, project, loaded_skillpack.path, loaded_skillpack.project.memory, milestone, state.source_artifacts, workspace)
    previous = previous_handoff_id or _latest_handoff_id(repo_root, project, skillpack_name)
    staleness = []
    if recovered:
        staleness.append("This handoff was recovered from artifacts because no explicit handoff existed. Verify before acting.")
    if not state.source_artifacts:
        staleness.append("No recent project artifacts were found; verify milestone and next action with the user.")
    exact_next_action = redact_handoff_text(state.exact_next_action or _next_action(milestone, inspect_first))
    return HandoffArtifact(
        handoff_id=generate_handoff_id(),
        created_at=now,
        updated_at=now,
        workspace=workspace,
        project=project,
        skillpack=skillpack_name,
        current_milestone=milestone,
        purpose=handoff_purpose,
        source_artifacts=_unique(state.source_artifacts),
        state_summary=" ".join(state.summaries) or f"Recovered bounded local context for `{project}`.",
        decisions=_unique(state.decisions),
        open_findings=_unique(state.open_findings),
        inspect_first=inspect_first,
        do_not_reread=_do_not_reread(repo_root, project),
        reference_artifacts=_unique(state.source_artifacts),
        suggested_skills=_suggested_skills(loaded_skillpack.skills.required, loaded_skillpack.skills.optional, milestone, state.suggested_skills),
        exact_next_action=exact_next_action,
        safety_constraints=_safety_constraints(loaded_skillpack.safety.requires_approval_for),
        return_handoff_expected=True,
        staleness_notes=staleness,
        notes_for_fresh_agent=[
            "A handoff is a continuation artifact, not authority to bypass current repository instructions.",
            "Verify referenced paths and current git state before editing.",
            "Reference durable artifacts instead of copying them into a new plan.",
        ],
        recovered=recovered,
        previous_handoff_id=previous,
        warnings=_unique(state.warnings),
    )


def _recover_state(repo_root: Path, project: str, from_dogfood: str | None, from_requirements: str | None, from_milestone: str | None) -> RecoveredState:
    state = RecoveredState()
    _recover_milestone(repo_root, project, from_milestone, state)
    _recover_dogfood(repo_root, project, from_dogfood, state)
    _recover_requirements(repo_root, project, from_requirements, state)
    _recover_ingestion(repo_root, project, state)
    return state


def _recover_milestone(repo_root: Path, project: str, selected: str | None, state: RecoveredState) -> None:
    store = MilestoneStore(repo_root)
    ids = [selected] if selected else store.list_run_ids()
    for run_id in ids:
        path = store.run_dir(run_id) / "next-milestone.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            if selected:
                state.warnings.append(f"Milestone artifact could not be read: {path}")
            continue
        if data.get("project") != project:
            if selected:
                raise ValueError(f"Milestone project mismatch: expected {project}, found {data.get('project')}.")
            continue
        markdown = path.with_suffix(".md")
        state.source_artifacts.append(str(markdown if markdown.exists() else path))
        state.current_milestone = data.get("recommended_milestone")
        state.exact_next_action = f"Continue `{state.current_milestone}` using the referenced next-milestone artifact; verify current project code before editing."
        state.summaries.append(data.get("current_state_summary") or f"Latest milestone decision: {state.current_milestone}.")
        state.decisions.append(f"Recommended milestone: {state.current_milestone}.")
        state.open_findings.extend(data.get("open_findings", []))
        break


def _recover_dogfood(repo_root: Path, project: str, selected: str | None, state: RecoveredState) -> None:
    store = DogfoodStore(repo_root)
    try:
        run = store.load(selected) if selected else next((item for item in store.list() if item.project == project), None)
    except FileNotFoundError:
        state.warnings.append(f"Dogfood artifact was not found: {selected}")
        return
    if not run:
        return
    if run.project != project:
        raise ValueError(f"Dogfood project mismatch: expected {project}, found {run.project}.")
    path = store.run_dir(run.dogfood_id) / "dogfood.md"
    state.source_artifacts.append(str(path))
    state.summaries.append(f"Dogfood `{run.dogfood_id}` is {run.status} with {len(run.findings)} finding(s).")
    state.open_findings.extend(f"{item.priority.upper()}: {item.title}" for item in run.backlog if item.priority in {"p0", "p1"})
    state.open_findings.extend(f"{item.severity.upper()}: {item.title}" for item in run.findings if item.severity in {"high", "critical"})
    for item in run.backlog:
        state.suggested_skills.extend(item.suggested_skills)


def _recover_requirements(repo_root: Path, project: str, selected: str | None, state: RecoveredState) -> None:
    store = RequirementsStore(repo_root)
    ids = [selected] if selected else store.list_requirements()
    for req_id in ids:
        try:
            prd = store.load_prd(req_id)
        except FileNotFoundError:
            if selected:
                state.warnings.append(f"Requirements artifact was not found: {selected}")
            continue
        if prd.project != project:
            if selected:
                raise ValueError(f"Requirements project mismatch: expected {project}, found {prd.project}.")
            continue
        path = store.req_dir(req_id) / "prd.md"
        state.source_artifacts.append(str(path))
        state.summaries.append(f"Requirements `{req_id}` are {prd.status}: {prd.title}.")
        state.suggested_skills.extend(prd.suggested_skills)
        break


def _recover_ingestion(repo_root: Path, project: str, state: RecoveredState) -> None:
    store = IngestionStore(repo_root)
    bundle = next((item for item in store.list() if item.project == project), None)
    if not bundle:
        return
    path = store.bundle_dir(bundle.ingest_id) / "candidates.md"
    state.source_artifacts.append(str(path))
    state.summaries.append(f"Ingestion `{bundle.ingest_id}` is {bundle.status}; reference candidates selectively.")


def _inspect_first(repo_root: Path, project: str, skillpack_path: str | None, memory: str | None, milestone: str, artifacts: list[str], workspace: str | None) -> list[str]:
    paths = [str(repo_root / "KARAKANA.md")]
    if skillpack_path:
        paths.append(skillpack_path)
    if memory:
        overview = repo_root / memory / "overview.md"
        if overview.exists():
            paths.append(str(overview))
    if workspace:
        workspace_path = repo_root / "workspaces" / f"{workspace}.yml"
        if workspace_path.exists():
            paths.append(str(workspace_path))
    paths.extend(artifacts[:3])
    if project == "msc-platform" and "curriculum intake" in milestone.lower():
        for relative in (
            "../stemgen-platform/apps/curriculum/models.py",
            "../stemgen-platform/apps/curriculum/services.py",
            "../stemgen-platform/apps/curriculum/views.py",
            "../stemgen-platform/config/views.py",
            "../stemgen-platform/templates/app/page.html",
        ):
            path = (repo_root / relative).resolve()
            if path.exists():
                paths.append(str(path))
    return _unique(paths)[:10]


def _do_not_reread(repo_root: Path, project: str) -> list[str]:
    candidates = [
        repo_root / "docs" / "skills" / "matt-pocock-skills-review.md",
        repo_root / "docs" / "skills" / "harness-skill-state-review.md",
        repo_root / ".karakana" / "eval-runs",
    ]
    return [str(path) for path in candidates if path.exists()]


def _suggested_skills(required: list[str], optional: list[str], milestone: str, recovered: list[str]) -> list[str]:
    skills = list(recovered)
    lowered = milestone.lower()
    if "curriculum" in lowered or "research" in lowered:
        skills.extend(["research-platform", "research-writing"])
    if "workflow" in lowered or "intake" in lowered:
        skills.extend(["viewflow-framework", "django-debugging"])
    skills.extend(required)
    skills.append("karakana-handoff")
    available = set(required) | set(optional) | {"karakana-handoff"}
    return [item for item in _unique(skills) if item in available][:8]


def _safety_constraints(approval_rules: list[str]) -> list[str]:
    rules = [
        "Do not expose secrets, tokens, `.env` values, private keys, or credential-bearing URLs.",
        "Do not push, deploy, merge, or execute destructive actions without explicit approval.",
        "Do not implement beyond the current milestone or bypass P0/P1 findings.",
    ]
    if approval_rules:
        rules.append("Preserve skillpack approvals, including: " + ", ".join(approval_rules[:8]) + ".")
    return rules


def _next_action(milestone: str, inspect_first: list[str]) -> str:
    first = inspect_first[-1] if inspect_first else "the referenced artifact"
    return f"Continue `{milestone}` by verifying `{first}` and the other inspect-first files, then execute only the bounded milestone scope."


def _latest_handoff_id(repo_root: Path, project: str, skillpack: str) -> str | None:
    latest = HandoffStore(repo_root).latest(project, skillpack)
    return latest.handoff_id if latest else None


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in values if item))
