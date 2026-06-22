"""Deterministic next-milestone evidence collection and decision generation."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from karakana.dogfood.schemas import DogfoodRun
from karakana.dogfood.summary import DogfoodStore
from karakana.ingestion.schemas import IngestionBundle
from karakana.ingestion.store import IngestionStore
from karakana.milestones.schemas import MilestoneCandidate, MilestoneEvidence, NextMilestoneDecision
from karakana.milestones.ranking import DEFAULT_CRITERIA, bm25_relevance, focused_candidate_relevance, rank_candidates
from karakana.milestones.store import MilestoneStore, generate_milestone_run_id
from karakana.requirements.readiness import GENERIC_TITLE_TERMS
from karakana.requirements.schemas import ReadinessCheck, RequirementPRD
from karakana.requirements.store import RequirementsStore
from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.validator import SkillpackValidator
from karakana.traces.schemas import now_utc, redact_value
from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.status import collect_workspace_status


@dataclass
class DecisionContext:
    project: str
    skillpack: str
    workspace: str | None
    note: str | None
    evidence: list[MilestoneEvidence] = field(default_factory=list)
    open_findings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    dogfood: DogfoodRun | None = None
    requirements: RequirementPRD | None = None
    readiness: ReadinessCheck | None = None
    ingestion: IngestionBundle | None = None
    repo_dirty: bool = False
    explicit_requirements: bool = False


def generate_next_milestone(
    repo_root: Path,
    project: str,
    skillpack: str | None = None,
    workspace: str | None = None,
    from_dogfood: str | None = None,
    from_requirements: str | None = None,
    from_note: str | None = None,
    no_brainstorm: bool = False,
    strict: bool = False,
) -> NextMilestoneDecision:
    skillpack_name = skillpack or project
    context = _collect_context(
        repo_root,
        project=project,
        skillpack=skillpack_name,
        workspace=workspace,
        from_dogfood=from_dogfood,
        from_requirements=from_requirements,
        note=from_note,
        strict=strict,
    )
    candidates, sensitivity = _generate_candidates(context)
    recommended = candidates[0]
    instructions = _generate_instructions(context, recommended)
    rejected = [
        f"{candidate.title}: lower evidence-adjusted fit than {recommended.title}."
        for candidate in candidates[1:]
    ]
    rationale = (
        f"{recommended.title} has the highest transparent multi-criteria score across blocker priority, user alignment, "
        "evidence strength, readiness, risk control, reversibility, and cost efficiency. "
        + ("Verbalized sampling supplied the option-generation discipline; it did not supply numeric probabilities. " if not no_brainstorm else "Candidates were generated and ranked deterministically without the brainstorming step. ")
        + f"Sensitivity analysis tested {sensitivity.scenarios_tested} weight scenarios and the ranking was "
        + ("robust. " if sensitivity.robust else "sensitive to the recorded criteria. ")
        + "Decision weights are normalized score shares, not calibrated probabilities."
    )
    return NextMilestoneDecision(
        run_id=generate_milestone_run_id(),
        created_at=now_utc(),
        workspace=workspace,
        project=project,
        skillpack=skillpack_name,
        current_state_summary=_state_summary(context),
        evidence=context.evidence,
        open_findings=context.open_findings,
        criteria=list(DEFAULT_CRITERIA),
        candidates=candidates,
        sensitivity=sensitivity,
        recommended_milestone=recommended.title,
        decision_rationale=rationale,
        rejected_alternatives=rejected,
        generated_instructions=instructions,
        verification_plan=_verification_plan(context, recommended),
        definition_of_done=_definition_of_done(recommended),
        safety_notes=[
            "Do not push or deploy by default.",
            "Do not weaken project skillpack, patch review, patch gate, approval, or secret-handling rules.",
            "Do not begin implementation while P0/P1 planning blockers remain unresolved.",
            "Review generated instructions before execution; this command performs no recommended work.",
            "Decision weights are normalized MCDA score shares, not calibrated probabilities.",
        ],
        brainstorm_used=not no_brainstorm,
        blocked=bool(strict and context.blockers),
        blockers=context.blockers if strict else [],
        warnings=context.warnings,
    )


def _collect_context(
    repo_root: Path,
    project: str,
    skillpack: str,
    workspace: str | None,
    from_dogfood: str | None,
    from_requirements: str | None,
    note: str | None,
    strict: bool,
) -> DecisionContext:
    context = DecisionContext(project=project, skillpack=skillpack, workspace=workspace, note=redact_value(note))
    context.explicit_requirements = from_requirements is not None
    _collect_skillpack(repo_root, context)
    _collect_workspace(repo_root, context)
    _collect_repo_state(repo_root, context)
    _collect_patch_evidence(repo_root, context)
    _collect_dogfood(repo_root, context, from_dogfood)
    _collect_requirements(repo_root, context, from_requirements)
    _collect_ingestion(repo_root, context)
    _collect_previous_milestone(repo_root, context)
    if context.note:
        context.evidence.append(MilestoneEvidence("note", "manual", None, context.note))
        _find_note_priorities(context)
    if strict:
        if context.requirements is None:
            context.blockers.append("Strict mode requires a current, project-specific requirements artifact.")
        elif _requirements_generic(context.requirements):
            context.blockers.append("Strict mode rejected the latest requirements artifact because it is generic or incomplete.")
        if context.dogfood and context.dogfood.status in {"failed", "blocked", "error"}:
            context.blockers.append(f"Latest dogfood status requires cleanup: {context.dogfood.status}.")
    context.blockers = list(dict.fromkeys(context.blockers))
    context.open_findings = list(dict.fromkeys(context.open_findings))
    return context


def _collect_skillpack(repo_root: Path, context: DecisionContext) -> None:
    validation = SkillpackValidator(repo_root).validate(context.skillpack)
    if not validation.ok:
        context.blockers.extend(f"Skillpack error: {item}" for item in validation.errors)
    context.warnings.extend(f"Skillpack warning: {item}" for item in validation.warnings)
    try:
        skillpack = SkillpackLoader(repo_root).load(context.skillpack)
    except (FileNotFoundError, ValueError) as exc:
        context.blockers.append(f"Required project context cannot be resolved: {exc}")
        return
    context.evidence.append(MilestoneEvidence("skillpack", skillpack.name, skillpack.path, skillpack.description))
    if skillpack.project.id != context.project:
        context.blockers.append(f"Skillpack project mismatch: expected {context.project}, found {skillpack.project.id}.")
    memory = skillpack.project.memory
    if memory:
        memory_path = repo_root / memory
        if memory_path.exists():
            files = sorted(path.name for path in memory_path.glob("*.md"))
            context.evidence.append(MilestoneEvidence("project_memory", context.project, memory, f"Available files: {', '.join(files) or 'none'}"))
        else:
            context.blockers.append(f"Required project memory cannot be resolved: {memory}")


def _collect_workspace(repo_root: Path, context: DecisionContext) -> None:
    if not context.workspace:
        return
    try:
        workspace = WorkspaceLoader(repo_root).load(context.workspace)
        status = collect_workspace_status(repo_root, workspace, project_id=context.project)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        context.blockers.append(f"Workspace context cannot be resolved: {exc}")
        return
    if status.errors:
        context.blockers.extend(f"Workspace error: {item}" for item in status.errors)
    context.warnings.extend(f"Workspace warning: {item}" for item in status.warnings)
    if status.project_statuses:
        project_status = status.project_statuses[0]
        context.repo_dirty = bool(project_status.git_status)
        summary = f"path_exists={project_status.path_exists}, branch={project_status.git_branch or 'unknown'}, dirty={context.repo_dirty}"
        context.evidence.append(MilestoneEvidence("workspace_status", context.workspace, project_status.path, summary))
    else:
        context.blockers.append(f"Workspace {context.workspace} does not contain project {context.project}.")


def _collect_repo_state(repo_root: Path, context: DecisionContext) -> None:
    result = subprocess.run(["git", "status", "--short"], cwd=repo_root, check=False, capture_output=True, text=True)
    if result.returncode == 0:
        changes = [line for line in result.stdout.splitlines() if line.strip()]
        context.repo_dirty = context.repo_dirty or bool(changes)
        context.evidence.append(MilestoneEvidence("repository_state", "current", str(repo_root), f"Working tree changes: {len(changes)}"))
    else:
        context.warnings.append("Current repository git status could not be read.")


def _collect_patch_evidence(repo_root: Path, context: DecisionContext) -> None:
    for source_type, root_name, filename in (
        ("patch_review", "patch-reviews", "review.json"),
        ("patch_gate", "patch-gates", "gate.json"),
    ):
        root = repo_root / ".karakana" / root_name
        paths = sorted(root.glob(f"*/{filename}"), reverse=True) if root.exists() else []
        if not paths:
            continue
        path = None
        data = None
        for candidate_path in paths:
            try:
                candidate_data = json.loads(candidate_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            metadata = candidate_data.get("metadata") or {}
            artifact_project = candidate_data.get("project") or metadata.get("project")
            artifact_skillpack = candidate_data.get("skillpack") or metadata.get("skillpack")
            if artifact_project == context.project or artifact_skillpack == context.skillpack:
                path = candidate_path
                data = candidate_data
                break
        if path is None or data is None:
            context.warnings.append(f"No project-scoped {source_type} artifact was found; unscoped artifacts were ignored.")
            continue
        status = data.get("status", "unknown")
        blocked = bool(data.get("blocked", False))
        risk = data.get("risk_level", "unknown")
        context.evidence.append(
            MilestoneEvidence(
                source_type,
                path.parent.name,
                str(path),
                f"status={status}, blocked={blocked}, risk={risk}",
            )
        )


def _collect_dogfood(repo_root: Path, context: DecisionContext, dogfood_id: str | None) -> None:
    store = DogfoodStore(repo_root)
    try:
        run = store.load(dogfood_id) if dogfood_id else next((item for item in store.list() if item.project == context.project), None)
    except FileNotFoundError as exc:
        context.blockers.append(str(exc))
        return
    if run is None:
        context.warnings.append("No project dogfood run was found.")
        return
    if run.project != context.project:
        context.blockers.append(
            f"Dogfood project mismatch: expected {context.project}, found {run.project}."
        )
        return
    context.dogfood = run
    context.evidence.append(MilestoneEvidence("dogfood", run.dogfood_id, str(store.run_dir(run.dogfood_id) / "dogfood.md"), f"status={run.status}, findings={len(run.findings)}, backlog={len(run.backlog)}"))
    for item in run.backlog:
        if item.priority in {"p0", "p1"}:
            finding = f"{item.priority.upper()} dogfood backlog: {item.title}"
            context.open_findings.append(finding)
            context.blockers.append(finding)
    for finding in run.findings:
        if finding.severity in {"high", "critical"}:
            context.open_findings.append(f"{finding.severity.upper()} dogfood finding: {finding.title}")


def _collect_requirements(repo_root: Path, context: DecisionContext, req_id: str | None) -> None:
    store = RequirementsStore(repo_root)
    selected = req_id
    if selected is None:
        for item in store.list_requirements():
            try:
                prd = store.load_prd(item)
            except FileNotFoundError:
                continue
            if prd.project == context.project:
                selected = item
                break
    if selected is None:
        context.warnings.append("No project requirements artifact was found.")
        return
    try:
        prd = store.load_prd(selected)
    except FileNotFoundError as exc:
        context.blockers.append(str(exc))
        return
    if prd.project and prd.project != context.project:
        context.blockers.append(f"Requirements project mismatch: expected {context.project}, found {prd.project}.")
        return
    prd_text = _prd_text(prd)
    corpus = []
    for item in store.list_requirements():
        try:
            corpus_prd = store.load_prd(item)
        except FileNotFoundError:
            continue
        if corpus_prd.project == context.project:
            corpus.append(_prd_text(corpus_prd))
    relevance = bm25_relevance(context.note, prd_text, corpus)
    if relevance.label in {"irrelevant", "low"} and not context.explicit_requirements:
        context.warnings.append(
            f"Latest project requirements `{prd.req_id}` were ignored because BM25-style relevance was "
            f"{relevance.label} ({relevance.score:.4f})."
        )
        return
    context.requirements = prd
    context.evidence.append(MilestoneEvidence("requirements", prd.req_id, str(store.req_dir(prd.req_id) / "prd.md"), f"{prd.title}; status={prd.status}", relevance.label, relevance.score, relevance.matched_terms))
    try:
        readiness = store.load_readiness(prd.req_id)
    except FileNotFoundError:
        readiness = None
    context.readiness = readiness
    if readiness:
        context.evidence.append(MilestoneEvidence("requirements_readiness", prd.req_id, str(store.req_dir(prd.req_id) / "readiness.md"), f"status={readiness.status}, ready={readiness.ready}", relevance.label, relevance.score, relevance.matched_terms))
        context.open_findings.extend(f"Requirements readiness: {item}" for item in readiness.failed)


def _collect_ingestion(repo_root: Path, context: DecisionContext) -> None:
    store = IngestionStore(repo_root)
    bundle = next((item for item in store.list() if item.project == context.project), None)
    if bundle is None:
        context.warnings.append("No project ingestion artifact was found.")
        return
    context.ingestion = bundle
    corpus = [f"{candidate.title} {candidate.summary}" for candidate in bundle.candidates]
    title_corpus = [candidate.title for candidate in bundle.candidates]
    relevance_by_id = {
        candidate.candidate_id: bm25_relevance(context.note, text, corpus)
        for candidate, text in zip(bundle.candidates, corpus)
    }
    title_relevance_by_id = {
        candidate.candidate_id: bm25_relevance(context.note, candidate.title, title_corpus)
        for candidate in bundle.candidates
    }
    relevant_candidates = [
        candidate for candidate in bundle.candidates
        if focused_candidate_relevance(
            title_relevance_by_id[candidate.candidate_id],
            relevance_by_id[candidate.candidate_id],
        )
    ]
    best = max(relevance_by_id.values(), key=lambda item: item.score, default=bm25_relevance(context.note, "", corpus))
    context.evidence.append(MilestoneEvidence("ingestion", bundle.ingest_id, str(store.bundle_dir(bundle.ingest_id) / "candidates.md"), f"status={bundle.status}, candidates={len(bundle.candidates)}, relevant_candidates={len(relevant_candidates)}", best.label, best.score, best.matched_terms))
    for candidate in bundle.candidates:
        if candidate in relevant_candidates and (candidate.status == "blocked" or candidate.risk_level in {"high", "critical"}):
            context.open_findings.append(f"Ingestion candidate needs review: {candidate.title}")


def _collect_previous_milestone(repo_root: Path, context: DecisionContext) -> None:
    store = MilestoneStore(repo_root)
    for run_id in store.list_run_ids():
        json_path = store.run_dir(run_id) / "next-milestone.json"
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("project") != context.project:
            continue
        context.evidence.append(
            MilestoneEvidence(
                "previous_milestone",
                run_id,
                str(store.run_dir(run_id) / "next-milestone.md"),
                "Most recent project-scoped next-milestone decision artifact.",
            )
        )
        break


def _find_note_priorities(context: DecisionContext) -> None:
    note = (context.note or "").lower()
    if "p0" in note:
        finding = "P0 finding reported in the supplied note."
        context.open_findings.append(finding)
        context.blockers.append(finding)
    if "p1" in note:
        finding = "P1 finding reported in the supplied note."
        context.open_findings.append(finding)
        context.blockers.append(finding)


def _requirements_generic(prd: RequirementPRD) -> bool:
    title = prd.title.strip().lower()
    return title in GENERIC_TITLE_TERMS or not prd.functional_requirements or not prd.goal or "needs review" in prd.goal.lower()


def _generate_candidates(context: DecisionContext):
    candidates: list[dict] = []
    note = (context.note or "").lower()
    has_intake_gap = context.project == "msc-platform" and any(
        signal in note for signal in ("0 registered", "zero registered", "no snapshot", "no action button", "curriculum intake management", "tie links", "retrieval actions")
    )
    if context.blockers:
        candidates.append(_candidate("Resolve P0/P1 Planning and Review Blockers", "cleanup", "Blocking findings must be resolved before implementation.", "Delays feature work if blockers are stale.", "Medium", "High", [5, 3, 5, 5, 5, 5, 3]))
    if has_intake_gap:
        candidates.append(_candidate("Slice 1.1: Curriculum Intake Management UX and TIE Source Actions", "implementation_slice", "Closes the reported operator gap while keeping curriculum intake bounded before Slice 2.", "Could expand into extraction or workflow-review scope without strict non-goals.", "Medium", "High", [0 if context.blockers else 4.5, 5, 4, 4, 3.5, 4.5, 3]))
    if context.requirements is None or (context.requirements and _requirements_generic(context.requirements)):
        candidates.append(_candidate("Requirements Elicitation and Specification Regeneration", "requirements_regeneration", "Current project requirements are missing or too generic for a safe implementation handoff.", "Adds planning time before visible implementation.", "Low", "High", [4, 3.5, 4, 4.5, 5, 5, 4]))
    if context.repo_dirty or context.dogfood is None or context.dogfood.status == "draft":
        candidates.append(_candidate("Targeted Dogfood Rerun and Finding Review", "targeted_dogfood", "Recent or unreviewed planning changes should be exercised before the next implementation milestone.", "May repeat checks that are already understood.", "Low", "High", [3, 2, 3, 4, 5, 5, 4]))
    candidates.append(_candidate("Schema and Test Hardening for the Next Data-Producing Slice", "schema_test_hardening", "Schema and verification contracts reduce risk before new data-producing behavior.", "Can over-specify an interface before user scope is settled.", "Medium", "High", [2, 3, 3, 4, 4, 4, 3]))
    if not has_intake_gap:
        candidates.append(_candidate("Next Approved Vertical Implementation Slice", "implementation_slice", "A bounded implementation slice is appropriate once planning and review evidence is ready.", "Unsafe if readiness evidence is incomplete.", "Medium", "Medium", [3 if not context.blockers else 0, 3, 3, 3, 3, 3, 3]))
    candidates.append(_candidate("Documentation and Handoff Hardening", "documentation_hardening", "Consolidates decisions and reduces context loss.", "Does not directly deliver project behavior.", "Low", "High", [1, 2, 2, 3, 5, 5, 4]))
    return rank_candidates(candidates[:6])


def _candidate(title: str, category: str, rationale: str, risks: str, cost: str, reversibility: str, scores: list[float]) -> dict:
    return {
        "title": title,
        "category": category,
        "rationale": rationale,
        "risks": risks,
        "cost": cost,
        "reversibility": reversibility,
        "criterion_scores": {criterion.name: score for criterion, score in zip(DEFAULT_CRITERIA, scores)},
    }


def _prd_text(prd: RequirementPRD) -> str:
    return " ".join([prd.title, prd.context, prd.problem, prd.goal, *prd.functional_requirements])


def _state_summary(context: DecisionContext) -> str:
    parts = [f"Project `{context.project}` uses skillpack `{context.skillpack}`."]
    if context.workspace:
        parts.append(f"Workspace `{context.workspace}` was inspected.")
    if context.note:
        parts.append(f"User-reported state: {context.note}")
    if context.requirements:
        parts.append(f"Latest project requirements: `{context.requirements.req_id}` ({context.requirements.status}).")
    else:
        parts.append("No project-specific requirements artifact was found.")
    if context.dogfood:
        parts.append(f"Latest project dogfood: `{context.dogfood.dogfood_id}` ({context.dogfood.status}).")
    else:
        parts.append("No project-specific dogfood run was found.")
    parts.append(f"The current Karakana repository working tree is {'dirty' if context.repo_dirty else 'clean'}.")
    return " ".join(parts)


def _generate_instructions(context: DecisionContext, candidate: MilestoneCandidate) -> str:
    if candidate.title.startswith("Slice 1.1:"):
        required_work = [
            "Elicit and define the seed, add-source, and capture-snapshot operator actions.",
            "Reuse the existing TIE source registry and snapshot services rather than duplicating command logic.",
            "Add a bounded staff-only curriculum intake management surface with validation, idempotency, and durable status handoff.",
            "Preserve source approval, deterministic snapshot artifacts, checksums, and audit evidence.",
            "Keep extraction, topic screening, automated review, human topic selection, and full workflow review out of scope.",
        ]
    elif candidate.category == "cleanup":
        required_work = ["Resolve every recorded P0/P1 finding.", "Rerun the affected reviews and dogfood checks.", "Regenerate readiness evidence before selecting an implementation slice."]
    elif candidate.category == "requirements_regeneration":
        required_work = ["Run requirements elicitation against current project evidence.", "Resolve material ambiguities with grill-with-docs and verbalized sampling.", "Generate and review a project-specific specification and vertical issue breakdown."]
    elif candidate.category == "targeted_dogfood":
        required_work = ["Run the project-specific dogfood checklist.", "Classify findings and prioritize P0/P1 work.", "Generate a reviewed next-milestone artifact from the updated evidence."]
    else:
        required_work = ["Confirm the milestone scope against current project evidence.", "Implement only the bounded deliverable.", "Add focused tests/evals and update durable documentation."]
    checks = "\n".join(f"- {item}" for item in required_work)
    return f"""# Codex Task: {candidate.title}

## Milestone

**{candidate.title}**

## Context

Use project `{context.project}` with skillpack `{context.skillpack}`. Review the evidence listed in the next-milestone decision artifact before editing.

## Goal

Complete the recommended milestone as one reviewable, evidence-linked unit of work.

## Required Work

{checks}

## Safety Rules

- Do not push or deploy unless explicitly approved through existing gates.
- Do not weaken skillpack, approval, secret-handling, patch-review, or patch-gate rules.
- Stop and return to planning if unresolved P0/P1 blockers are discovered.
- Keep unrelated future milestones out of scope.

## Verification

- Run focused tests for changed behavior.
- Run project-required validation from the active skillpack.
- Review the resulting patch and artifacts against the original evidence.

## Definition of Done

- The bounded milestone behavior and evidence artifacts exist.
- Tests/evals pass or failures are classified.
- Safety gates and non-goals are preserved.
- Remaining risks and the next decision point are documented.
"""


def _verification_plan(context: DecisionContext, candidate: MilestoneCandidate) -> list[str]:
    checks = ["Validate the active project skillpack.", "Run focused tests/evals for the selected milestone.", "Review generated artifacts against the evidence consulted."]
    if context.project == "msc-platform":
        checks.append("Run the msc-platform dogfood checklist and preserve research objective/evidence mapping.")
    if candidate.category == "implementation_slice":
        checks.append("Run patch review and patch gate before any commit or push request.")
    return checks


def _definition_of_done(candidate: MilestoneCandidate) -> list[str]:
    return [
        f"The scope of `{candidate.title}` is completed without implementing rejected alternatives.",
        "Required tests, evals, and artifact validation pass or failures are clearly classified.",
        "No unresolved P0/P1 planning blocker is hidden or bypassed.",
        "Copy-ready instructions, verification evidence, risks, and remaining work are reviewable.",
    ]
