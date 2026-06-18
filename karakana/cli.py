"""Command line interface for the Karakana skeleton."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

import typer

from karakana import __version__
from karakana.actions.extractor import ActionExtractor
from karakana.actions.publisher import ActionPublisher
from karakana.actions.store import ActionStore
from karakana.agents.planner import compose_planning_prompt, write_planning_prompt
from karakana.codex.executor import CodexExecution
from karakana.codex.handoff import CodexHandoffBuilder
from karakana.codex.patch import PatchCapture
from karakana.codex.reviewer import PatchReviewer
from karakana.codex.summary import summarize_patch
from karakana.crosslinks.apply import apply_crosslink
from karakana.crosslinks.proposer import generate_proposals
from karakana.crosslinks.reviewer import review_crosslink
from karakana.crosslinks.scanner import scan_workspace
from karakana.crosslinks.store import CrosslinkStore
from karakana.config.loader import load_config
from karakana.config.summary import render_config, render_config_validation, render_paths
from karakana.config.validator import validate_config
from karakana.docs.generator import check_docs, command_reference
from karakana.dogfood.backlog import generate_backlog
from karakana.dogfood.checklist import generate_checklist
from karakana.dogfood.findings import analyze_dogfood
from karakana.dogfood.report import generate_report
from karakana.dogfood.requirements import requirements_from_dogfood
from karakana.dogfood.runner import run_dogfood
from karakana.dogfood.summary import DogfoodStore
from karakana.evals.loader import EvalLoader
from karakana.evals.report import EvalReportStore
from karakana.evals.runner import EvalRunner
from karakana.improvement.proposer import ImprovementProposer
from karakana.improvement.store import ProposalStore
from karakana.ingestion.apply import apply_ingestion_bundle
from karakana.ingestion.generator import generate_candidates
from karakana.ingestion.reviewer import review_ingestion_bundle
from karakana.ingestion.scanner import scan_sources
from karakana.ingestion.sources import (
    load_action_source,
    load_file_source,
    load_note_source,
    load_patch_review_source,
    load_proposal_source,
    load_trace_source,
)
from karakana.ingestion.store import IngestionStore, create_bundle
from karakana.handoffs.builder import create_handoff
from karakana.handoffs.doctor import diagnose_handoff
from karakana.handoffs.store import HandoffStore
from karakana.handoffs.summary import render_handoff, render_session_start
from karakana.memory.ubongo import UbongoMemory
from karakana.models.config import redacted_model_config
from karakana.models.errors import ModelProviderError
from karakana.models.escalation import recommend_escalation
from karakana.models.executor import ModelExecutor
from karakana.models.registry import default_registry
from karakana.models.review.report import render_review_markdown, write_review_artifacts
from karakana.models.review.reviewer import review_response
from karakana.models.router import available_task_types, route_model
from karakana.milestones.decision import generate_next_milestone
from karakana.milestones.store import MilestoneStore
from karakana.patch.apply import apply_patch_run
from karakana.patch.branch import create_patch_branch, plan_patch_branch
from karakana.patch.commit import commit_patch_run
from karakana.patch.gates import attach_test_evidence, render_gate_markdown, run_patch_gate
from karakana.patch.status import write_patch_status
from karakana.patch.summary import summarize_patch_lifecycle
from karakana.requirements.issues import generate_issues
from karakana.requirements.prd import generate_prd
from karakana.requirements.publisher import RequirementsPublisher
from karakana.requirements.readiness import check_readiness
from karakana.requirements.sources import (
    load_action_requirement_source,
    load_file_requirement_source,
    load_ingest_requirement_source,
    load_note_requirement_source,
    load_patch_review_requirement_source,
    load_proposal_requirement_source,
)
from karakana.requirements.store import RequirementsStore
from karakana.requirements.stories import generate_stories
from karakana.requirements.summary import render_requirement_summary
from karakana.release.checklist import write_release_checklist
from karakana.release.checks import run_doctor, run_release_check
from karakana.release.metadata import version_summary
from karakana.release.notes import generate_release_notes
from karakana.safety.model_calls import failed_model_checks, validate_model_call
from karakana.safety.model_routing import validate_model_route
from karakana.router import select_model
from karakana.skills.index import generate_skill_index
from karakana.skills.loader import SkillLoader
from karakana.skills.validator import SkillValidator
from karakana.skillpacks.activation import SkillpackActivation
from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.resolver import SkillpackResolver
from karakana.skillpacks.summary import render_skillpack_summary
from karakana.skillpacks.validator import SkillpackValidator
from karakana.safety.github_writes import MAX_BODY_SIZE, failed_checks, validate_comment_write, validate_issue_create, validate_pr_create
from karakana.tools.codex_executor import CodexExecutor
from karakana.tools.github import GitHubPromptGenerator, load_github_event
from karakana.tools.github_api import GitHubApiClient
from karakana.traces.schemas import SafetyCheck, TraceArtifact
from karakana.traces.store import TraceStore
from karakana.workspaces.activation import WorkspaceActivation
from karakana.workspaces.handoff import write_workspace_handoff
from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.planner import build_workspace_plan
from karakana.workspaces.status import collect_workspace_status
from karakana.workspaces.summary import render_workspace_summary
from karakana.workspaces.validator import WorkspaceValidator

app = typer.Typer(help="Karakana AI agent harness skeleton.")
action_app = typer.Typer(help="Extract and publish reviewable action artifacts.")
codex_app = typer.Typer(help="Generate Codex-ready task prompts.")
config_app = typer.Typer(help="Inspect and validate Karakana configuration.")
copilot_app = typer.Typer(help="Start GitHub Copilot CLI with Karakana handoff context.")
crosslink_app = typer.Typer(help="Detect reusable cross-project knowledge.")
dogfood_app = typer.Typer(help="Dogfood Karakana on itself.")
docs_app = typer.Typer(help="Generate and check Karakana documentation.")
eval_app = typer.Typer(help="Run deterministic Karakana evaluations.")
github_app = typer.Typer(help="Generate safe GitHub workflow artifacts.")
improve_app = typer.Typer(help="Generate self-improvement proposals from traces.")
ingest_app = typer.Typer(help="Distill selected sources into reviewable candidates.")
handoff_app = typer.Typer(help="Create and load project session handoffs.")
memory_app = typer.Typer(help="Inspect ubongo durable memory.")
milestone_app = typer.Typer(help="Decide and generate instructions for the next project milestone.")
model_app = typer.Typer(help="Inspect and invoke model providers.")
patch_app = typer.Typer(help="Gate, apply, and summarize captured patches.")
requirements_app = typer.Typer(help="Generate PRDs, stories, and issue drafts.")
release_app = typer.Typer(help="Run local release readiness commands.")
skill_app = typer.Typer(help="Inspect and validate Karakana skills.")
skillpack_app = typer.Typer(help="Inspect and activate project skillpacks.")
trace_app = typer.Typer(help="Inspect local Karakana run traces.")
workspace_app = typer.Typer(help="Coordinate read-only multi-project workspaces.")

app.add_typer(action_app, name="action")
app.add_typer(codex_app, name="codex")
app.add_typer(config_app, name="config")
app.add_typer(copilot_app, name="copilot")
app.add_typer(crosslink_app, name="crosslink")
app.add_typer(dogfood_app, name="dogfood")
app.add_typer(docs_app, name="docs")
app.add_typer(eval_app, name="eval")
app.add_typer(github_app, name="github")
app.add_typer(improve_app, name="improve")
app.add_typer(ingest_app, name="ingest")
app.add_typer(handoff_app, name="handoff")
app.add_typer(memory_app, name="memory")
app.add_typer(milestone_app, name="milestone")
app.add_typer(model_app, name="model")
app.add_typer(patch_app, name="patch")
app.add_typer(requirements_app, name="requirements")
app.add_typer(release_app, name="release")
app.add_typer(skill_app, name="skill")
app.add_typer(skillpack_app, name="skillpack")
app.add_typer(trace_app, name="trace")
app.add_typer(workspace_app, name="workspace")


@app.callback()
def main() -> None:
    """Karakana AI agent harness skeleton."""


@app.command()
def version() -> None:
    """Print the installed Karakana version."""
    metadata = version_summary()
    typer.echo(f"Karakana version: {metadata['version']}")
    typer.echo(f"karakana {metadata['version']}")
    typer.echo(f"Package: {metadata['package']}")
    typer.echo(f"Python: {metadata['python']}")
    typer.echo(f"Status: {metadata['status']}")


@app.command()
def doctor(json_output: bool = typer.Option(False, "--json", help="Print doctor JSON.")) -> None:
    """Run local health checks without network access."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="doctor", task_type="doctor", inputs={})
    try:
        report, path = run_doctor(repo_root)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"operation": "doctor", "doctor_run_id": report.run_id, "status": report.status, "warnings": report.warnings, "errors": report.errors})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="doctor", description="Doctor report JSON"))
    _success_trace(trace_store, trace)
    typer.echo(f"Doctor status: {report.status}")
    typer.echo(f"Doctor report: {path.parent}")
    for check in report.checks:
        typer.echo(f"{check.status}: {check.name} - {check.message}")
    if json_output:
        typer.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))


@config_app.command("show")
def config_show() -> None:
    """Print effective Karakana configuration with redaction."""
    typer.echo(render_config(load_config(Path.cwd())), nl=False)


@config_app.command("validate")
def config_validate() -> None:
    """Validate effective Karakana configuration."""
    repo_root = Path.cwd()
    errors, warnings = validate_config(load_config(repo_root), repo_root)
    typer.echo(render_config_validation(errors, warnings), nl=False)
    if errors:
        raise typer.Exit(code=1)


@config_app.command("paths")
def config_paths() -> None:
    """Print resolved Karakana paths."""
    repo_root = Path.cwd()
    typer.echo(render_paths(repo_root, load_config(repo_root)), nl=False)


@release_app.command("check")
def release_check(full: bool = typer.Option(False, "--full", help="Run full local validation, evals, and tests."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Run local release readiness checks."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="release check", task_type="release_check", inputs={"full": full})
    try:
        report, path = run_release_check(repo_root, full=full)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"operation": "release_check", "release_check_id": report.run_id, "status": report.status, "warnings": report.warnings, "errors": report.errors})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="release_check", description="Release check JSON"))
    _success_trace(trace_store, trace)
    typer.echo(f"Release check status: {report.status}")
    typer.echo(f"Release check report: {path.parent}")
    if json_output:
        typer.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    if report.errors:
        raise typer.Exit(code=1)


@release_app.command("notes")
def release_notes(since: str | None = typer.Option(None, "--since", help="Git ref or date."), version: str | None = typer.Option(None, "--version", help="Version label."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Generate draft release notes from local evidence."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="release notes", task_type="release_notes", inputs={"since": since, "version": version})
    try:
        notes_id, path = generate_release_notes(repo_root, version=version, since=since)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"operation": "release_notes", "release_notes_id": notes_id, "artifacts": [str(path)]})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="release_notes", description="Draft release notes"))
    _success_trace(trace_store, trace)
    typer.echo(f"Release notes written to: {path}")
    if json_output:
        typer.echo(json.dumps({"release_notes_id": notes_id, "path": str(path)}, indent=2, sort_keys=True))


@release_app.command("checklist")
def release_checklist(json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Generate a copy-ready release checklist."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="release checklist", task_type="release_checklist", inputs={})
    try:
        checklist_id, path = write_release_checklist(repo_root)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"operation": "release_checklist", "release_checklist_id": checklist_id, "artifacts": [str(path)]})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="release_checklist", description="Release checklist"))
    _success_trace(trace_store, trace)
    typer.echo(f"Release checklist written to: {path}")
    if json_output:
        typer.echo(json.dumps({"release_checklist_id": checklist_id, "path": str(path)}, indent=2, sort_keys=True))


@docs_app.command("command-reference")
def docs_command_reference(write: bool = typer.Option(False, "--write", help="Write docs/command-reference.md.")) -> None:
    """Preview or write the CLI command reference."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="docs command-reference", task_type="docs", inputs={"write": write})
    try:
        text, path = command_reference(repo_root, write=write)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"operation": "docs_command_reference", "docs_generated": write, "artifacts": [str(path)]})
    if write:
        trace.artifacts.append(TraceArtifact(path=str(path), kind="docs", description="Command reference"))
    _success_trace(trace_store, trace)
    if write:
        typer.echo(f"Command reference written to: {path}")
    else:
        typer.echo(text)


@docs_app.command("check")
def docs_check() -> None:
    """Check that required documentation files exist."""
    repo_root = Path.cwd()
    missing, warnings = check_docs(repo_root)
    status = "passed" if not missing else "warning"
    typer.echo(f"Docs check: {status}")
    for warning in warnings:
        typer.echo(f"warning: {warning}")
    if not warnings:
        typer.echo("All required docs exist.")


@dogfood_app.command("checklist")
def dogfood_checklist(project: str = typer.Option("karakana", "--project", help="Project being dogfooded."), skillpack: str | None = typer.Option("karakana", "--skillpack", help="Skillpack context."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Generate a dogfood checklist without executing commands."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="dogfood checklist", project=project, skill=skillpack, task_type="dogfood", inputs={"project": project, "skillpack": skillpack})
    try:
        dogfood_id, path = generate_checklist(repo_root, project, skillpack)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"dogfood_id": dogfood_id, "project": project, "skillpack": skillpack, "operation": "checklist", "commands_planned": [], "commands_executed": [], "status": "draft", "artifacts": [str(path)]})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="dogfood_checklist", description="Dogfood checklist"))
    _success_trace(trace_store, trace)
    typer.echo(f"Dogfood checklist written to: {path}")
    typer.echo(f"Dogfood ID: {dogfood_id}")
    if json_output:
        typer.echo(json.dumps({"dogfood_id": dogfood_id, "path": str(path)}, indent=2, sort_keys=True))


@dogfood_app.command("run")
def dogfood_run(project: str = typer.Option("karakana", "--project", help="Project being dogfooded."), skillpack: str | None = typer.Option("karakana", "--skillpack", help="Skillpack context."), full: bool = typer.Option(False, "--full", help="Run full allowlisted workflow."), command: str | None = typer.Option(None, "--command", help="Run or plan one allowlisted command ID."), dry_run: bool = typer.Option(False, "--dry-run/--no-dry-run", help="Plan commands instead of executing the safe allowlist."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Plan or run the safe allowlisted dogfood workflow."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="dogfood run", project=project, skill=skillpack, task_type="dogfood", inputs={"project": project, "skillpack": skillpack, "full": full, "command": command, "dry_run": dry_run})
    try:
        run, path = run_dogfood(repo_root, project, skillpack, full=full, command_id=command, dry_run=dry_run)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    nested_artifacts = []
    for command_result in run.command_results:
        nested_artifacts.extend(command_result.artifact_paths)
    trace_artifacts = [str(path), *nested_artifacts]
    trace.outputs.update({"dogfood_id": run.dogfood_id, "project": project, "skillpack": skillpack, "operation": "run", "commands_planned": [result.command for result in run.command_results if result.status == "planned"], "commands_executed": [result.command for result in run.command_results if result.status != "planned"], "status": run.status, "warnings": run.warnings, "errors": run.errors, "artifacts": trace_artifacts})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="dogfood_run", description="Dogfood run JSON"))
    for artifact_path in nested_artifacts:
        trace.artifacts.append(TraceArtifact(path=artifact_path, kind="dogfood_nested_artifact", description="Artifact generated during dogfood run"))
    _success_trace(trace_store, trace)
    typer.echo(f"Dogfood run written to: {path.parent}")
    typer.echo(f"Dogfood ID: {run.dogfood_id}")
    typer.echo(f"Status: {run.status}")
    typer.echo(f"Commands: {len(run.command_results)}")
    if json_output:
        typer.echo(json.dumps(run.to_dict(), indent=2, sort_keys=True))


@dogfood_app.command("analyze")
def dogfood_analyze(dogfood_id: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Classify findings from a dogfood run."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="dogfood analyze", task_type="dogfood", inputs={"dogfood_id": dogfood_id})
    try:
        findings, path = analyze_dogfood(repo_root, dogfood_id)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"dogfood_id": dogfood_id, "operation": "analyze", "findings_count": len(findings), "status": "completed", "artifacts": [str(path)]})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="dogfood_findings", description="Dogfood findings"))
    _success_trace(trace_store, trace)
    typer.echo(f"Dogfood findings written to: {path}")
    typer.echo(f"Findings: {len(findings)}")
    if json_output:
        typer.echo(json.dumps([finding.to_dict() for finding in findings], indent=2, sort_keys=True))


@dogfood_app.command("backlog")
def dogfood_backlog(dogfood_id: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Generate v1 hardening backlog from dogfood findings."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="dogfood backlog", task_type="dogfood", inputs={"dogfood_id": dogfood_id})
    try:
        items, path = generate_backlog(repo_root, dogfood_id)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"dogfood_id": dogfood_id, "operation": "backlog", "backlog_count": len(items), "status": "completed", "artifacts": [str(path)]})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="dogfood_backlog", description="Dogfood backlog"))
    _success_trace(trace_store, trace)
    typer.echo(f"Dogfood backlog written to: {path}")
    typer.echo(f"Backlog items: {len(items)}")
    if json_output:
        typer.echo(json.dumps([item.to_dict() for item in items], indent=2, sort_keys=True))


@dogfood_app.command("report")
def dogfood_report(dogfood_id: str) -> None:
    """Generate dogfood report markdown."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="dogfood report", task_type="dogfood", inputs={"dogfood_id": dogfood_id})
    try:
        path = generate_report(repo_root, dogfood_id)
        run = DogfoodStore(repo_root).load(dogfood_id)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"dogfood_id": dogfood_id, "operation": "report", "findings_count": len(run.findings), "backlog_count": len(run.backlog), "status": run.status, "artifacts": [str(path)]})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="dogfood_report", description="Dogfood report"))
    _success_trace(trace_store, trace)
    typer.echo(f"Dogfood report written to: {path}")


@dogfood_app.command("requirements")
def dogfood_requirements(dogfood_id: str, project: str | None = typer.Option(None, "--project", help="Project override."), skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack override."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Convert dogfood backlog into requirements, stories, issues, and readiness artifacts."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="dogfood requirements", project=project, skill=skillpack, task_type="dogfood", inputs={"dogfood_id": dogfood_id, "project": project, "skillpack": skillpack})
    try:
        req_id, paths = requirements_from_dogfood(repo_root, dogfood_id, project=project, skillpack=skillpack)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"dogfood_id": dogfood_id, "operation": "requirements", "req_id": req_id, "artifacts": [str(path) for path in paths]})
    for path in paths:
        trace.artifacts.append(TraceArtifact(path=str(path), kind="dogfood_requirements", description="Dogfood requirements artifact"))
    _success_trace(trace_store, trace)
    typer.echo(f"Dogfood requirements written for: {req_id}")
    if json_output:
        typer.echo(json.dumps({"req_id": req_id, "paths": [str(path) for path in paths]}, indent=2, sort_keys=True))


@dogfood_app.command("list")
def dogfood_list(limit: int = typer.Option(20, "--limit", help="Maximum runs to show.")) -> None:
    """List recent dogfood runs."""
    runs = DogfoodStore(Path.cwd()).list(limit=limit)
    if not runs:
        typer.echo("No dogfood runs found.")
        return
    for run in runs:
        typer.echo(f"{run.dogfood_id}\t{run.project}\t{run.status}\t{len(run.command_results)} command(s)\t{len(run.findings)} finding(s)")


@dogfood_app.command("show")
def dogfood_show(dogfood_id: str) -> None:
    """Show dogfood report markdown."""
    store = DogfoodStore(Path.cwd())
    try:
        store.load(dogfood_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo((store.run_dir(dogfood_id) / "dogfood.md").read_text(encoding="utf-8"))


@dogfood_app.command("latest")
def dogfood_latest() -> None:
    """Show latest dogfood report markdown."""
    store = DogfoodStore(Path.cwd())
    run = store.latest()
    if not run:
        typer.echo("No dogfood runs found.")
        return
    typer.echo((store.run_dir(run.dogfood_id) / "dogfood.md").read_text(encoding="utf-8"))


@handoff_app.command("create")
def handoff_create(
    project: str = typer.Option(..., "--project", help="Project identity."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack; defaults to project."),
    workspace: str | None = typer.Option(None, "--workspace", help="Optional workspace identity."),
    purpose: str | None = typer.Option(None, "--purpose", help="Purpose of the next session."),
    current_milestone: str | None = typer.Option(None, "--current-milestone", help="Explicit current milestone."),
    from_note: str | None = typer.Option(None, "--from-note", help="Additional current state."),
    from_dogfood: str | None = typer.Option(None, "--from-dogfood", help="Specific dogfood artifact."),
    from_requirements: str | None = typer.Option(None, "--from-requirements", help="Specific requirements artifact."),
    from_milestone: str | None = typer.Option(None, "--from-milestone", help="Specific milestone decision."),
    write: bool = typer.Option(True, "--write/--no-write", help="Write the durable artifact."),
    json_output: bool = typer.Option(False, "--json", help="Print handoff JSON."),
) -> None:
    """Create a project-aware continuation handoff."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="handoff create", project=project, skill="karakana-handoff", task_type="handoff", inputs={"project": project, "skillpack": skillpack, "workspace": workspace, "purpose": purpose, "current_milestone": current_milestone, "from_note": from_note, "from_dogfood": from_dogfood, "from_requirements": from_requirements, "from_milestone": from_milestone, "write": write})
    try:
        handoff = create_handoff(repo_root, project, skillpack, workspace, purpose, current_milestone, from_note, from_dogfood, from_requirements, from_milestone)
        markdown_path = json_path = None
        if write:
            markdown_path, json_path = HandoffStore(repo_root).save(handoff)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"handoff_id": handoff.handoff_id, "project": project, "skillpack": handoff.skillpack, "written": write, "markdown_path": str(markdown_path) if markdown_path else None})
    if markdown_path and json_path:
        trace.artifacts.extend([
            TraceArtifact(path=str(markdown_path), kind="session_handoff", description="Project session handoff"),
            TraceArtifact(path=str(json_path), kind="session_handoff_json", description="Project session handoff JSON"),
        ])
    trace.finish("success")
    trace_store.save(trace)
    typer.echo(f"Handoff ID: {handoff.handoff_id}")
    if markdown_path:
        typer.echo(f"Handoff written to: {markdown_path}")
    else:
        typer.echo(render_handoff(handoff))
    if json_output:
        typer.echo(json.dumps(handoff.to_dict(), indent=2, sort_keys=True))


@handoff_app.command("show")
def handoff_show(
    project: str = typer.Option(..., "--project", help="Project identity."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Optional skillpack filter."),
    full: bool = typer.Option(False, "--full", help="Print the complete handoff."),
) -> None:
    """Show the latest project handoff path and summary."""
    store = HandoffStore(Path.cwd())
    handoff = store.latest(project, skillpack)
    if not handoff:
        typer.echo(f"No handoff found for project: {project}")
        raise typer.Exit(code=1)
    path = store.run_dir(handoff.handoff_id) / "handoff.md"
    typer.echo(f"Handoff: {path}")
    typer.echo(f"Purpose: {handoff.purpose}")
    typer.echo(f"Current milestone: {handoff.current_milestone}")
    typer.echo(f"Exact next action: {handoff.exact_next_action}")
    if full:
        typer.echo(path.read_text(encoding="utf-8"))


@handoff_app.command("load")
def handoff_load(
    project: str = typer.Option(..., "--project", help="Project identity."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack; defaults to project."),
    workspace: str | None = typer.Option(None, "--workspace", help="Optional workspace identity."),
    no_create: bool = typer.Option(False, "--no-create", help="Do not recover a handoff when none exists."),
) -> None:
    """Load compact session-start context, recovering bounded state if absent."""
    repo_root = Path.cwd()
    store = HandoffStore(repo_root)
    skillpack_name = skillpack or project
    handoff = store.latest(project, skillpack_name)
    if not handoff:
        if no_create:
            typer.echo(f"No handoff found for project: {project}")
            raise typer.Exit(code=1)
        try:
            handoff = create_handoff(repo_root, project, skillpack_name, workspace, purpose="Recovered session entry handoff", recovered=True)
            store.save(handoff)
        except Exception as exc:
            typer.echo(str(exc))
            raise typer.Exit(code=1) from exc
    path = store.run_dir(handoff.handoff_id) / "handoff.md"
    typer.echo(render_session_start(handoff, str(path)))


@handoff_app.command("refresh")
def handoff_refresh(
    project: str = typer.Option(..., "--project", help="Project identity."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack; defaults to project."),
    workspace: str | None = typer.Option(None, "--workspace", help="Optional workspace identity."),
    purpose: str = typer.Option("End of task handoff", "--purpose", help="Purpose of the next session."),
    current_milestone: str | None = typer.Option(None, "--current-milestone", help="Explicit current milestone."),
    from_note: str | None = typer.Option(None, "--from-note", help="Additional current state."),
) -> None:
    """Append a refreshed handoff while preserving prior handoff history."""
    repo_root = Path.cwd()
    store = HandoffStore(repo_root)
    skillpack_name = skillpack or project
    previous = store.latest(project, skillpack_name)
    try:
        handoff = create_handoff(repo_root, project, skillpack_name, workspace, purpose, current_milestone, from_note, previous_handoff_id=previous.handoff_id if previous else None)
        markdown_path, _ = store.save(handoff)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo(f"Handoff refreshed: {handoff.handoff_id}")
    typer.echo(f"Previous handoff: {handoff.previous_handoff_id or 'None'}")
    typer.echo(f"Handoff written to: {markdown_path}")


@handoff_app.command("list")
def handoff_list(
    project: str | None = typer.Option(None, "--project", help="Optional project filter."),
    limit: int = typer.Option(20, "--limit", help="Maximum handoffs."),
) -> None:
    """List recent project handoffs."""
    handoffs = HandoffStore(Path.cwd()).list(project=project, limit=limit)
    if not handoffs:
        typer.echo("No handoffs found.")
        return
    for item in handoffs:
        typer.echo(f"{item.handoff_id}\t{item.project}\t{item.updated_at}\t{item.purpose}\t{item.current_milestone}")


@handoff_app.command("doctor")
def handoff_doctor(
    project: str = typer.Option(..., "--project", help="Project identity."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Optional skillpack filter."),
    stale_after_days: int = typer.Option(7, "--stale-after-days", min=0, help="Staleness threshold."),
    json_output: bool = typer.Option(False, "--json", help="Print report JSON."),
) -> None:
    """Check latest handoff freshness, references, skills, scope, and redaction."""
    report = diagnose_handoff(Path.cwd(), project, skillpack, stale_after_days)
    typer.echo(f"Handoff doctor: {report.status}")
    for name, passed in report.checks.items():
        typer.echo(f"{'passed' if passed else 'failed'}: {name}")
    for warning in report.warnings:
        typer.echo(f"warning: {warning}")
    for error in report.errors:
        typer.echo(f"error: {error}")
    if json_output:
        typer.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    if report.errors:
        raise typer.Exit(code=1)


@milestone_app.command("next")
def milestone_next(
    project: str = typer.Option(..., "--project", help="Project context."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context; defaults to the project name."),
    workspace: str | None = typer.Option(None, "--workspace", help="Optional workspace to inspect."),
    from_dogfood: str | None = typer.Option(None, "--from-dogfood", help="Use one dogfood run instead of the latest project run."),
    from_requirements: str | None = typer.Option(None, "--from-requirements", help="Use one requirements artifact instead of the latest project artifact."),
    from_note: str | None = typer.Option(None, "--from-note", help="Add current user-reported state."),
    write_instructions: bool = typer.Option(False, "--write-instructions", help="Write a separate copy-ready instructions.md file."),
    output_format: str = typer.Option("markdown", "--format", help="Console output: markdown or json."),
    no_brainstorm: bool = typer.Option(False, "--no-brainstorm", help="Use deterministic ranking without the brainstorming step."),
    strict: bool = typer.Option(False, "--strict", help="Block on unresolved P0/P1 or missing required planning context."),
    no_handoff_refresh: bool = typer.Option(False, "--no-handoff-refresh", help="Do not append a session handoff for this decision."),
) -> None:
    """Decide the next project milestone and write copy-ready instructions."""
    if output_format not in {"markdown", "json"}:
        typer.echo("--format must be markdown or json")
        raise typer.Exit(code=2)
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="milestone next",
        project=project,
        skill="next-milestone-decision",
        task_type="planning",
        inputs={
            "project": project,
            "skillpack": skillpack,
            "workspace": workspace,
            "from_dogfood": from_dogfood,
            "from_requirements": from_requirements,
            "from_note": from_note,
            "write_instructions": write_instructions,
            "format": output_format,
            "no_brainstorm": no_brainstorm,
            "strict": strict,
        },
    )
    try:
        decision = generate_next_milestone(
            repo_root,
            project=project,
            skillpack=skillpack,
            workspace=workspace,
            from_dogfood=from_dogfood,
            from_requirements=from_requirements,
            from_note=from_note,
            no_brainstorm=no_brainstorm,
            strict=strict,
        )
        markdown_path, json_path = MilestoneStore(repo_root).save(decision, write_instructions=write_instructions)
        handoff_path = None
        if not no_handoff_refresh:
            handoff = create_handoff(
                repo_root,
                project,
                skillpack or project,
                workspace,
                purpose=f"Continue after milestone decision: {decision.recommended_milestone}",
                current_milestone=decision.recommended_milestone,
                from_milestone=decision.run_id,
            )
            handoff_path, _ = HandoffStore(repo_root).save(handoff)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update(
        {
            "milestone_run_id": decision.run_id,
            "recommended_milestone": decision.recommended_milestone,
            "blocked": decision.blocked,
            "blockers": decision.blockers,
            "markdown_path": str(markdown_path),
            "json_path": str(json_path),
            "handoff_path": str(handoff_path) if handoff_path else None,
        }
    )
    trace.warnings.extend(decision.warnings)
    trace.artifacts.append(TraceArtifact(path=str(markdown_path), kind="next_milestone", description="Next-milestone decision markdown"))
    trace.artifacts.append(TraceArtifact(path=str(json_path), kind="next_milestone_json", description="Next-milestone decision JSON"))
    if write_instructions:
        trace.artifacts.append(TraceArtifact(path=str(markdown_path.parent / "instructions.md"), kind="next_milestone_instructions", description="Copy-ready milestone instructions"))
    if handoff_path:
        trace.artifacts.append(TraceArtifact(path=str(handoff_path), kind="session_handoff", description="Automatic post-milestone session handoff"))
    trace.safety_checks.append(SafetyCheck("artifact-only", "passed", "The command generated local artifacts and did not execute, push, or deploy the recommendation."))
    if decision.blocked:
        trace.errors.extend(decision.blockers)
        trace.next_actions.append("Resolve strict-mode blockers and rerun milestone next.")
        trace.finish("failed")
        trace_store.save(trace)
    else:
        _success_trace(trace_store, trace)
    typer.echo(f"Milestone run ID: {decision.run_id}")
    typer.echo(f"Recommended milestone: {decision.recommended_milestone}")
    typer.echo(f"Artifact: {markdown_path}")
    if output_format == "json":
        typer.echo(json.dumps(decision.to_dict(), indent=2, sort_keys=True))
    else:
        typer.echo(markdown_path.read_text(encoding="utf-8"))
    if decision.blocked:
        raise typer.Exit(code=1)


@action_app.command("extract")
def action_extract(
    from_response: Path = typer.Option(..., "--from-response", help="Model response artifact path."),
    project: str | None = typer.Option(None, "--project", help="Project context."),
    skill: str | None = typer.Option(None, "--skill", help="Skill context."),
    require_passed_review: bool = typer.Option(False, "--require-passed-review", help="Require passed or warning response review."),
    output: Path | None = typer.Option(None, "--output", help="Custom output directory under .karakana/."),
    json_output: bool = typer.Option(False, "--json", help="Print action bundle JSON."),
) -> None:
    """Extract reviewable action artifacts from a model response."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="action extract",
        project=project,
        skill=skill,
        task_type="action_extraction",
        inputs={"from_response": str(from_response), "project": project, "skill": skill, "require_passed_review": require_passed_review, "output": str(output) if output else None},
    )
    try:
        bundle = ActionExtractor(repo_root).extract_from_response(from_response, project=project, skill=skill, require_passed_review=require_passed_review)
        path = ActionStore(repo_root).save(bundle, output_dir=output)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update(
        {
            "action_run_id": bundle.action_run_id,
            "source_response_path": str(from_response),
            "source_run_id": bundle.source.run_id,
            "response_review_status": bundle.source.review_status,
            "actions_count": len(bundle.actions),
            "action_types": [action.action_type for action in bundle.actions],
            "suggested_skills": bundle.suggested_skills,
            "risk_levels": [action.risk_level for action in bundle.actions],
            "actions_json": str(path),
            "actions_markdown": str(path.parent / "actions.md"),
            "handoff_markdown": str(path.parent / "handoff.md"),
        }
    )
    trace.warnings.extend(bundle.warnings)
    trace.artifacts.append(TraceArtifact(path=str(path), kind="actions_json", description="Extracted action bundle JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "actions.md"), kind="actions_markdown", description="Extracted action bundle markdown"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "handoff.md"), kind="actions_handoff", description="Extracted action handoff markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Action bundle written to: {path.parent}")
    typer.echo(f"Status: {bundle.status}")
    typer.echo(f"Actions: {len(bundle.actions)}")
    if json_output:
        typer.echo(json.dumps(bundle.to_dict(), indent=2, sort_keys=True))


@action_app.command("list")
def action_list(limit: int = typer.Option(20, "--limit", help="Maximum bundles to show.")) -> None:
    """List recent action bundles."""
    bundles = ActionStore(Path.cwd()).list_bundles(limit=limit)
    if not bundles:
        typer.echo("No action bundles found.")
        return
    for bundle in bundles:
        typer.echo(f"{bundle.action_run_id}\t{bundle.created_at}\t{bundle.status}\t{len(bundle.actions)} action(s)")


@action_app.command("show")
def action_show(action_run_id: str) -> None:
    """Print an action bundle summary."""
    store = ActionStore(Path.cwd())
    try:
        store.load(action_run_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo((store.bundle_dir(action_run_id) / "actions.md").read_text(encoding="utf-8"))


@action_app.command("latest")
def action_latest() -> None:
    """Print the latest action bundle summary."""
    store = ActionStore(Path.cwd())
    bundle = store.latest()
    if bundle is None:
        typer.echo("No action bundles found.")
        return
    typer.echo((store.bundle_dir(bundle.action_run_id) / "actions.md").read_text(encoding="utf-8"))


@action_app.command("publish")
def action_publish(
    action_run_id: str,
    create_issues: bool = typer.Option(False, "--create-issues", help="Create GitHub issues from issue draft actions."),
    create_proposals: bool = typer.Option(False, "--create-proposals", help="Create formal proposal handoff artifacts."),
    create_codex_tasks: bool = typer.Option(False, "--create-codex-tasks", help="Copy Codex task artifacts to .karakana/codex-tasks/."),
) -> None:
    """Dry-run or explicitly publish an action bundle."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="action publish",
        task_type="action_publish",
        inputs={"action_run_id": action_run_id, "create_issues": create_issues, "create_proposals": create_proposals, "create_codex_tasks": create_codex_tasks},
    )
    store = ActionStore(repo_root)
    try:
        bundle = store.load(action_run_id)
        result = ActionPublisher(repo_root).publish(bundle, create_issues=create_issues, create_proposals=create_proposals, create_codex_tasks=create_codex_tasks)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"action_run_id": action_run_id, "publish_mode": "write" if any([create_issues, create_proposals, create_codex_tasks]) else "dry_run", "publish_result": result})
    _success_trace(trace_store, trace)
    if result.get("dry_run"):
        typer.echo("Dry run: no actions published.")
        typer.echo(f"Would create issues: {result['would_create_issues']}")
        typer.echo(f"Would create proposals: {result['would_create_proposals']}")
        typer.echo(f"Would create Codex tasks: {result['would_create_codex_tasks']}")
    else:
        typer.echo("Publish completed.")
        typer.echo(json.dumps(result, indent=2, sort_keys=True))


@app.command()
def plan(
    project: str | None = typer.Option(None, "--project", "-p", help="Project memory key."),
    skill: str | None = typer.Option(None, "--skill", "-s", help="Skill name to include."),
    task: str = typer.Option(..., "--task", "-t", help="Planning task text."),
    output: Path = typer.Option(Path(".karakana/planning-task.md"), "--output", help="Prompt output path."),
    live: bool = typer.Option(False, "--live", help="Execute selected model provider."),
    provider: str | None = typer.Option(None, "--provider", help="Override model provider."),
    model: str | None = typer.Option(None, "--model", help="Override model name."),
    strict_review: bool = typer.Option(False, "--strict-review", help="Block live responses missing expected sections."),
    use_skillpack: bool = typer.Option(False, "--use-skillpack", help="Load skillpack matching --project."),
    use_current_skillpack: bool = typer.Option(False, "--use-current-skillpack", help="Use active local skillpack."),
    no_handoff: bool = typer.Option(False, "--no-handoff", help="Skip session handoff autoload/recovery."),
) -> None:
    """Compose a model-ready planning prompt without calling a model."""
    repo_root = Path.cwd()
    resolved_skillpack = None
    if use_skillpack or use_current_skillpack:
        try:
            resolver = SkillpackResolver(repo_root)
            resolved_skillpack = resolver.resolve_current() if use_current_skillpack else resolver.resolve_for_project(project)
            project = project or resolved_skillpack.skillpack.project.id
            skill = skill or (resolved_skillpack.required_skills[0] if resolved_skillpack.required_skills else None)
        except Exception as exc:
            typer.echo(str(exc))
            raise typer.Exit(code=1) from exc
    if not project or not skill:
        typer.echo("--project and --skill are required unless a skillpack supplies them.")
        raise typer.Exit(code=1)
    model_route = route_model("planning", provider=provider, model=model, skillpack_routes=resolved_skillpack.model_routes if resolved_skillpack else None)
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="plan",
        project=project,
        skill=skill,
        task=task,
        task_type="planning",
        selected_model=model_route["model"],
        inputs={"project": project, "skill": skill, "task": task, "output": str(output), "live": live, "provider": model_route["provider"], "model": model_route["model"], "use_skillpack": use_skillpack, "use_current_skillpack": use_current_skillpack, "skillpack": resolved_skillpack.skillpack.name if resolved_skillpack else None},
    )
    _record_route_outputs(trace, model_route)
    try:
        prompt = compose_planning_prompt(project=project, skill=skill, task=task, repo_root=repo_root, skillpack_context=_render_resolved_skillpack_context(resolved_skillpack), allow_missing_memory=bool(resolved_skillpack))
        if not no_handoff:
            skillpack_name = resolved_skillpack.skillpack.name if resolved_skillpack else project
            try:
                handoff, handoff_path = _ensure_session_handoff(repo_root, project, skillpack_name)
            except (FileNotFoundError, ValueError) as exc:
                trace.warnings.append(f"Session handoff autoload skipped: {exc}")
            else:
                prompt = prompt.rstrip() + "\n\n" + render_session_start(handoff, str(handoff_path))
                trace.outputs["session_handoff"] = str(handoff_path)
        output_path = write_planning_prompt(prompt, repo_root=repo_root, output_path=output)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    trace.outputs["prompt_path"] = str(output_path)
    trace.artifacts.append(TraceArtifact(path=str(output_path), kind="planning_prompt", description="Generated planning prompt"))
    if live:
        try:
            artifacts = _execute_model_to_artifacts(repo_root, prompt, model_route["provider"], model_route["model"], trace, task_type="planning", project=project, skill=skill, expected="plan", strict_review=strict_review)
            _print_live_artifacts(artifacts)
        except Exception as exc:
            _fail_trace(trace_store, trace, exc)
            typer.echo(str(exc))
            raise typer.Exit(code=1) from exc
    _success_trace(trace_store, trace)
    typer.echo(f"Selected model: {model_route['model']}")
    typer.echo(f"Selected provider: {model_route['provider']}")
    typer.echo(f"Prompt written to: {output_path}")
    typer.echo("")
    typer.echo(prompt)


@codex_app.command("run")
def codex_run(
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skill: str = typer.Option(..., "--skill", "-s", help="Skill name to include."),
    task: str = typer.Option(..., "--task", "-t", help="Codex task text."),
    focus: str | None = typer.Option(None, "--focus", help="Optional task focus."),
    output: Path = typer.Option(Path(".karakana/codex-task.md"), "--output", help="Prompt output path."),
    print_prompt: bool = typer.Option(False, "--print", help="Print the generated prompt."),
) -> None:
    """Generate a Codex-ready task prompt without executing Codex."""
    repo_root = Path.cwd()
    executor = CodexExecutor(repo_root)
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="codex run",
        project=project,
        skill=skill,
        task=task,
        task_type="codex_task_generation",
        selected_model=route_model("codex_task_drafting")["model"],
        inputs={"project": project, "skill": skill, "task": task, "focus": focus, "output": str(output), "print": print_prompt},
    )
    try:
        prompt = executor.build_task_prompt(project=project, skill=skill, task=task, focus=focus)
        output_path = executor.write_task_prompt(prompt, output_path=output)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    trace.outputs["prompt_path"] = str(output_path)
    trace.artifacts.append(TraceArtifact(path=str(output_path), kind="codex_task_prompt", description="Generated Codex task prompt"))
    _success_trace(trace_store, trace)
    typer.echo(f"Codex task prompt written to: {output_path}")
    typer.echo("Codex execution was not run.")
    if print_prompt:
        typer.echo("")
        typer.echo(prompt)


@codex_app.command("start", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def codex_start(
    ctx: typer.Context,
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skillpack: str | None = typer.Option(None, "--skillpack", "-s", help="Skillpack to load; defaults to project."),
    workspace: str | None = typer.Option(None, "--workspace", help="Optional workspace name."),
    no_create: bool = typer.Option(False, "--no-create", help="Do not recover a handoff when none exists."),
    no_pause: bool = typer.Option(False, "--no-pause", help="Do not pause before launching Codex."),
    bootstrap: bool = typer.Option(True, "--bootstrap/--no-bootstrap", help="Create .venv and install Karakana when the project environment is missing."),
    inline: bool = typer.Option(False, "--inline", help="Pass --no-alt-screen to Codex unless already supplied."),
    inject_prompt: bool = typer.Option(True, "--inject-prompt/--no-inject-prompt", help="Pass Karakana session-start context as Codex's initial prompt for fresh interactive launches."),
    print_only: bool = typer.Option(False, "--print-only", help="Print startup context and launch command without starting Codex."),
) -> None:
    """Print Karakana session context, then start Codex CLI."""
    forwarded = list(ctx.args)
    if inline and "--no-alt-screen" not in forwarded:
        forwarded.append("--no-alt-screen")
    _start_agent_cli(
        binary="codex",
        display_name="Codex",
        project=project,
        skillpack=skillpack,
        workspace=workspace,
        forwarded_args=forwarded,
        no_create=no_create,
        no_pause=no_pause,
        bootstrap_venv=bootstrap,
        inject_codex_prompt=inject_prompt,
        print_only=print_only,
    )


@copilot_app.command("start", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def copilot_start(
    ctx: typer.Context,
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skillpack: str | None = typer.Option(None, "--skillpack", "-s", help="Skillpack to load; defaults to project."),
    workspace: str | None = typer.Option(None, "--workspace", help="Optional workspace name."),
    no_create: bool = typer.Option(False, "--no-create", help="Do not recover a handoff when none exists."),
    no_pause: bool = typer.Option(False, "--no-pause", help="Do not pause before launching Copilot."),
    print_only: bool = typer.Option(False, "--print-only", help="Print startup context and launch command without starting Copilot."),
) -> None:
    """Print Karakana session context, then start GitHub Copilot CLI."""
    _start_agent_cli(
        binary="copilot",
        display_name="Copilot",
        project=project,
        skillpack=skillpack,
        workspace=workspace,
        forwarded_args=list(ctx.args),
        no_create=no_create,
        no_pause=no_pause,
        bootstrap_venv=False,
        inject_codex_prompt=False,
        print_only=print_only,
    )


@codex_app.command("handoff")
def codex_handoff(
    action_run_id: str,
    action_id: str | None = typer.Option(None, "--action-id", help="Generate handoff for one action."),
    project: str | None = typer.Option(None, "--project", help="Override project."),
    skill: str | None = typer.Option(None, "--skill", help="Override skill."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context to include."),
    output: Path | None = typer.Option(None, "--output", help="Custom output directory under .karakana/."),
    json_output: bool = typer.Option(False, "--json", help="Print generated task paths as JSON."),
    execute: bool = typer.Option(False, "--execute", help="Explicitly execute generated Codex task if safe."),
) -> None:
    """Generate Codex handoff tasks from an action bundle."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="codex handoff",
        task_type="codex_handoff",
        inputs={"action_run_id": action_run_id, "action_id": action_id, "project": project, "skill": skill, "skillpack": skillpack, "output": str(output) if output else None, "execute": execute},
    )
    try:
        skillpack_context = _resolve_optional_skillpack(repo_root, skillpack)
        paths = CodexHandoffBuilder(repo_root).build_from_action_bundle(action_run_id, action_id=action_id, project=project, skill=skill, output_dir=output, skillpack_context=skillpack_context)
        task_records = []
        for path in paths:
            task_json = path.with_name("codex-task.json")
            if task_json.exists():
                task_records.append(json.loads(task_json.read_text(encoding="utf-8")))
        execution_paths = []
        if execute:
            for path in paths:
                try:
                    execution_paths.append(str(CodexExecution(repo_root).execute(path, explicit=True)))
                except Exception as exc:
                    trace.warnings.append(str(exc))
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update(
        {
            "action_run_id": action_run_id,
            "action_id": action_id,
            "codex_task_ids": [record.get("task_id") for record in task_records],
            "codex_task_paths": [str(path) for path in paths],
            "recommended_provider": task_records[0].get("recommended_provider") if task_records else None,
            "recommended_model": task_records[0].get("recommended_model") if task_records else None,
            "escalation_model": task_records[0].get("escalation_model") if task_records else None,
            "risk_levels": [record.get("risk_level") for record in task_records],
            "skillpack": skillpack_context.skillpack.name if skillpack_context else None,
            "execution_requested": execute,
            "execution_performed": bool(execution_paths),
            "execution_paths": execution_paths,
        }
    )
    for path in paths:
        trace.artifacts.append(TraceArtifact(path=str(path), kind="codex_handoff_task", description="Codex handoff task"))
    _success_trace(trace_store, trace)
    for path in paths:
        typer.echo(f"Codex handoff task written to: {path}")
    if not execute:
        typer.echo("Codex execution was not run.")
    if json_output:
        typer.echo(json.dumps({"codex_task_paths": [str(path) for path in paths], "execution_paths": execution_paths}, indent=2, sort_keys=True))


@codex_app.command("execute")
def codex_execute(codex_task_path: Path, execute: bool = typer.Option(False, "--execute", help="Required to execute Codex.")) -> None:
    """Safely execute a Codex task only with explicit --execute."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex execute", task_type="codex_execution", inputs={"codex_task_path": str(codex_task_path), "execute": execute})
    try:
        result = CodexExecution(repo_root).execute(codex_task_path, explicit=execute)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs["execution_result"] = str(result)
    trace.artifacts.append(TraceArtifact(path=str(result), kind="codex_execution_result", description="Codex execution result"))
    _success_trace(trace_store, trace)
    typer.echo(f"Codex execution result: {result}")


@codex_app.command("capture-diff")
def codex_capture_diff(
    source_task: str | None = typer.Option(None, "--source-task", help="Source Codex task ID."),
    project: str | None = typer.Option(None, "--project", help="Project identity for artifact scoping."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack identity for artifact scoping."),
    include_staged: bool = typer.Option(False, "--include-staged", help="Capture staged diff too."),
    output: Path | None = typer.Option(None, "--output", help="Custom output directory under .karakana/."),
    json_output: bool = typer.Option(False, "--json", help="Print patch JSON."),
) -> None:
    """Capture current git diff without mutating files."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex capture-diff", project=project, skill=skillpack, task_type="patch_capture", inputs={"source_task": source_task, "project": project, "skillpack": skillpack, "include_staged": include_staged, "output": str(output) if output else None})
    try:
        artifact = PatchCapture(repo_root).capture_diff(source_task=source_task, include_staged=include_staged, output_dir=output, project=project, skillpack=skillpack)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": artifact.patch_run_id, "project": artifact.project, "skillpack": artifact.skillpack, "repository_path": artifact.repository_path, "files_changed": artifact.files_changed, "diff_path": artifact.diff_path, "summary_path": artifact.summary_path})
    trace.warnings.extend(artifact.warnings)
    trace.artifacts.append(TraceArtifact(path=str(artifact.diff_path), kind="patch_diff", description="Captured working tree diff"))
    trace.artifacts.append(TraceArtifact(path=str(artifact.summary_path), kind="patch_summary", description="Patch summary"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch captured: {Path(artifact.summary_path).parent}")
    typer.echo(f"Patch run ID: {artifact.patch_run_id}")
    if artifact.warnings:
        for warning in artifact.warnings:
            typer.echo(f"WARNING: {warning}")
    if json_output:
        typer.echo(json.dumps(artifact.to_dict(), indent=2, sort_keys=True))


@codex_app.command("capture-tests")
def codex_capture_tests(command: str = typer.Option(..., "--command", help="Explicit test command to run.")) -> None:
    """Run and capture an explicit safe test command."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex capture-tests", task_type="test_capture", inputs={"command": command})
    try:
        result_path = PatchCapture(repo_root).capture_tests(command)
        result_data = json.loads(result_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"test_run_id": result_data.get("test_run_id"), "test_result_path": str(result_path), "exit_code": result_data.get("exit_code"), "refused": result_data.get("refused")})
    trace.warnings.extend(result_data.get("warnings") or [])
    trace.artifacts.append(TraceArtifact(path=str(result_path), kind="test_result", description="Captured test result JSON"))
    _success_trace(trace_store, trace)
    typer.echo(f"Test result captured: {result_path}")


@codex_app.command("review-patch")
def codex_review_patch(diff: Path = typer.Option(..., "--diff", help="Diff file to review."), project: str | None = typer.Option(None, "--project", help="Project identity for artifact scoping."), skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context for high-risk paths.")) -> None:
    """Review a captured patch diff using deterministic checks."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex review-patch", project=project, skill=skillpack, task_type="patch_review", inputs={"diff": str(diff), "project": project, "skillpack": skillpack})
    try:
        skillpack_context = _resolve_optional_skillpack(repo_root, skillpack)
        review_path = PatchReviewer(repo_root).review_diff(diff, skillpack_context=skillpack_context, project=project)
        data = json.loads(review_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_review_id": review_path.parent.name, "review_status": data.get("status"), "review_blocked": data.get("blocked"), "risk_level": data.get("risk_level"), "review_path": str(review_path), "skillpack": skillpack_context.skillpack.name if skillpack_context else None})
    trace.artifacts.append(TraceArtifact(path=str(review_path), kind="patch_review", description="Patch review JSON"))
    trace.artifacts.append(TraceArtifact(path=str(review_path.parent / "review.md"), kind="patch_review_markdown", description="Patch review markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch review written to: {review_path.parent}")
    typer.echo(f"Status: {data.get('status')}")
    typer.echo(f"Risk level: {data.get('risk_level')}")


@codex_app.command("summarize-patch")
def codex_summarize_patch(patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."), review: bool = typer.Option(False, "--review", help="Also run patch review.")) -> None:
    """Summarize a captured patch."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex summarize-patch", task_type="patch_summary", inputs={"patch_run": patch_run, "review": review})
    try:
        summary_path = summarize_patch(repo_root, patch_run)
        review_path = None
        if review:
            review_path = PatchReviewer(repo_root).review_diff(repo_root / ".karakana" / "patches" / patch_run / "changes.diff")
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "summary_path": str(summary_path), "review_path": str(review_path) if review_path else None})
    trace.artifacts.append(TraceArtifact(path=str(summary_path), kind="patch_summary", description="Patch summary"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch summary written to: {summary_path}")


@crosslink_app.command("scan")
def crosslink_scan(
    workspace: str = typer.Option(..., "--workspace", help="Workspace name."),
    projects: str | None = typer.Option(None, "--projects", help="Comma-separated project IDs."),
    include: list[str] | None = typer.Option(None, "--include", help="Artifact kind to include."),
    since: str | None = typer.Option(None, "--since", help="Reserved future scan window."),
    max_artifacts: int = typer.Option(20, "--max-artifacts", help="Maximum artifacts to inspect per kind."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
) -> None:
    """Scan a workspace for reusable cross-project patterns."""
    repo_root = Path.cwd()
    project_ids = [item.strip() for item in projects.split(",") if item.strip()] if projects else None
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="crosslink scan", task_type="crosslink_scan", inputs={"workspace": workspace, "projects": project_ids, "include": include, "since": since, "max_artifacts": max_artifacts})
    try:
        bundle = scan_workspace(repo_root, workspace, project_ids=project_ids, includes=include, max_artifacts=max_artifacts)
        path = CrosslinkStore(repo_root).save(bundle)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"crosslink_id": bundle.crosslink_id, "workspace": workspace, "projects": [project.project_id for project in bundle.projects], "source_artifact_types": include or ["workspace", "skillpacks", "skills"], "patterns_detected": len(bundle.patterns), "risk_levels": [pattern.risk_level for pattern in bundle.patterns], "crosslink_path": str(path)})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="crosslink_bundle", description="Crosslink bundle JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "crosslink.md"), kind="crosslink_markdown", description="Crosslink markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Crosslink written to: {path.parent}")
    typer.echo(f"Crosslink ID: {bundle.crosslink_id}")
    typer.echo(f"Patterns: {len(bundle.patterns)}")
    if json_output:
        typer.echo(json.dumps(bundle.to_dict(), indent=2, sort_keys=True))


@crosslink_app.command("list")
def crosslink_list(limit: int = typer.Option(20, "--limit", help="Maximum crosslinks to show.")) -> None:
    """List recent crosslink bundles."""
    bundles = CrosslinkStore(Path.cwd()).list(limit=limit)
    if not bundles:
        typer.echo("No crosslinks found.")
        return
    for bundle in bundles:
        typer.echo(f"{bundle.crosslink_id}\t{bundle.workspace}\t{bundle.status}\t{len(bundle.patterns)} pattern(s)")


@crosslink_app.command("show")
def crosslink_show(crosslink_id: str) -> None:
    """Show a crosslink markdown summary."""
    store = CrosslinkStore(Path.cwd())
    try:
        store.load(crosslink_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo((store.bundle_dir(crosslink_id) / "crosslink.md").read_text(encoding="utf-8"))


@crosslink_app.command("review")
def crosslink_review(crosslink_id: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Review a crosslink for boundary and safety issues."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="crosslink review", task_type="crosslink_review", inputs={"crosslink_id": crosslink_id})
    try:
        result, path = review_crosslink(repo_root, crosslink_id)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"crosslink_id": crosslink_id, "review_status": result["status"], "blocked": result["blocked"], "review_path": str(path)})
    trace.warnings.extend(result.get("warnings") or [])
    trace.artifacts.append(TraceArtifact(path=str(path), kind="crosslink_review", description="Crosslink review markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Crosslink review written to: {path}")
    typer.echo(f"Status: {result['status']}")
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))


@crosslink_app.command("propose")
def crosslink_propose(crosslink_id: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Generate proposal artifacts for crosslink patterns."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="crosslink propose", task_type="crosslink_propose", inputs={"crosslink_id": crosslink_id})
    try:
        proposals, path = generate_proposals(repo_root, crosslink_id)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"crosslink_id": crosslink_id, "proposals_generated": len(proposals), "proposal_types": [proposal.proposal_type for proposal in proposals], "crosslink_path": str(path)})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="crosslink_bundle", description="Crosslink with proposals"))
    _success_trace(trace_store, trace)
    typer.echo(f"Crosslink proposals written under: {path.parent / 'proposed-updates'}")
    typer.echo(f"Proposals: {len(proposals)}")
    if json_output:
        typer.echo(json.dumps([proposal.to_dict() for proposal in proposals], indent=2, sort_keys=True))


@crosslink_app.command("apply")
def crosslink_apply(crosslink_id: str, write: bool = typer.Option(False, "--write", help="Apply eligible proposals."), proposal: str | None = typer.Option(None, "--proposal", help="Apply one proposal ID."), allow_high_risk: bool = typer.Option(False, "--allow-high-risk", help="Allow high-risk writes."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Dry-run or explicitly apply crosslink proposals."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="crosslink apply", task_type="crosslink_apply", inputs={"crosslink_id": crosslink_id, "write": write, "proposal": proposal, "allow_high_risk": allow_high_risk})
    try:
        result, path = apply_crosslink(repo_root, crosslink_id, write=write, proposal_id=proposal, allow_high_risk=allow_high_risk)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"crosslink_id": crosslink_id, "apply_requested": True, "write_requested": write, "applied_proposals": result.get("applied_proposals"), "blocked_proposals": result.get("blocked_proposals"), "apply_path": str(path)})
    trace.warnings.extend(result.get("warnings") or [])
    trace.artifacts.append(TraceArtifact(path=str(path), kind="crosslink_apply", description="Crosslink apply result"))
    _success_trace(trace_store, trace)
    typer.echo("Dry run: no files written." if not write else "Crosslink apply completed.")
    typer.echo(f"Status: {result['status']}")
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))


@patch_app.command("gate")
def patch_gate(patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."), skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context for path gates."), json_output: bool = typer.Option(False, "--json", help="Print gate JSON.")) -> None:
    """Run patch lifecycle gates for a captured patch."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch gate", task_type="patch_gate", inputs={"patch_run_id": patch_run, "skillpack": skillpack})
    try:
        skillpack_context = _resolve_optional_skillpack(repo_root, skillpack)
        result, gate_path = run_patch_gate(repo_root, patch_run, skillpack_context=skillpack_context)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "gate_run_id": gate_path.parent.name, "risk_level": result.risk_level, "blocked": result.blocked, "gate_path": str(gate_path), "skillpack": skillpack_context.skillpack.name if skillpack_context else None})
    trace.warnings.extend(result.warnings)
    trace.artifacts.append(TraceArtifact(path=str(gate_path), kind="patch_gate", description="Patch gate JSON"))
    trace.artifacts.append(TraceArtifact(path=str(gate_path.parent / "gate.md"), kind="patch_gate_markdown", description="Patch gate markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch gate written to: {gate_path.parent}")
    typer.echo(f"Status: {result.status}")
    typer.echo(f"Risk level: {result.risk_level}")
    typer.echo(f"Blocked: {result.blocked}")
    if json_output:
        typer.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))


@patch_app.command("branch")
def patch_branch(
    patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."),
    base: str = typer.Option("main", "--base", help="Base branch."),
    name: str | None = typer.Option(None, "--name", help="Branch name."),
    create: bool = typer.Option(False, "--create", help="Create local branch."),
    allow_dirty: bool = typer.Option(False, "--allow-dirty", help="Allow branch creation from a dirty worktree."),
    reuse: bool = typer.Option(False, "--reuse", help="Reuse existing branch."),
    json_output: bool = typer.Option(False, "--json", help="Print branch JSON."),
) -> None:
    """Plan or create a local patch branch."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch branch", task_type="patch_branch", inputs={"patch_run_id": patch_run, "base": base, "name": name, "create": create, "allow_dirty": allow_dirty, "reuse": reuse})
    try:
        plan = create_patch_branch(repo_root, patch_run, base=base, name=name, allow_dirty=allow_dirty, reuse=reuse) if create else plan_patch_branch(repo_root, patch_run, base=base, name=name)
        branch_dir = repo_root / ".karakana" / "patch-branches" / trace.run_id
        branch_dir.mkdir(parents=True, exist_ok=True)
        branch_json = branch_dir / "branch.json"
        branch_md = branch_dir / "branch.md"
        branch_json.write_text(json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        branch_md.write_text(_render_branch_plan(plan.to_dict(), create), encoding="utf-8")
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "current_branch": plan.current_branch, "target_branch": plan.proposed_branch, "branch_create_requested": create, "can_create": plan.can_create, "branch_path": str(branch_json)})
    trace.warnings.extend(plan.warnings)
    trace.artifacts.append(TraceArtifact(path=str(branch_json), kind="patch_branch_plan", description="Patch branch JSON"))
    _success_trace(trace_store, trace)
    typer.echo(f"Branch plan written to: {branch_dir}")
    typer.echo(f"Proposed branch: {plan.proposed_branch}")
    typer.echo("Branch created." if create and plan.can_create else "Branch was not created.")
    if plan.warnings:
        for warning in plan.warnings:
            typer.echo(f"WARNING: {warning}")
    if json_output:
        typer.echo(json.dumps(plan.to_dict(), indent=2, sort_keys=True))


@patch_app.command("apply")
def patch_apply(
    patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."),
    write: bool = typer.Option(False, "--write", help="Apply the patch."),
    stage: bool = typer.Option(False, "--stage", help="Stage changed files after applying."),
    allow_high_risk: bool = typer.Option(False, "--allow-high-risk", help="Allow high-risk patch apply."),
    allow_main: bool = typer.Option(False, "--allow-main", help="Allow apply on main/master."),
    json_output: bool = typer.Option(False, "--json", help="Print apply JSON."),
) -> None:
    """Dry-run or explicitly apply a captured patch."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch apply", task_type="patch_apply", inputs={"patch_run_id": patch_run, "write": write, "stage": stage, "allow_high_risk": allow_high_risk, "allow_main": allow_main})
    try:
        result = apply_patch_run(repo_root, patch_run, write=write, stage=stage, allow_high_risk=allow_high_risk, allow_main=allow_main)
        result_dir = repo_root / ".karakana" / "patch-apply" / trace.run_id
        result_dir.mkdir(parents=True, exist_ok=True)
        result_json = result_dir / "result.json"
        result_json.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (result_dir / "result.md").write_text(_render_apply_result(result.to_dict()), encoding="utf-8")
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "operation": "apply", "dry_run": result.dry_run, "write_requested": write, "stage_requested": stage, "applied": result.applied, "status": result.status, "files_changed": result.files_changed})
    trace.warnings.extend(result.warnings)
    trace.errors.extend(result.errors)
    trace.artifacts.append(TraceArtifact(path=str(result_json), kind="patch_apply_result", description="Patch apply result"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch apply result written to: {result_dir}")
    typer.echo(f"Status: {result.status}")
    typer.echo(f"Applied: {result.applied}")
    if json_output:
        typer.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))


@patch_app.command("attach-test")
def patch_attach_test(patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."), test_run: str = typer.Option(..., "--test-run", help="Test run ID.")) -> None:
    """Attach captured test evidence to a patch run."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch attach-test", task_type="patch_test_evidence", inputs={"patch_run_id": patch_run, "test_run_id": test_run})
    try:
        output = attach_test_evidence(repo_root, patch_run, test_run)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "test_run_id": test_run, "test_evidence_path": str(output)})
    trace.artifacts.append(TraceArtifact(path=str(output), kind="patch_test_evidence", description="Patch test evidence"))
    _success_trace(trace_store, trace)
    typer.echo(f"Test evidence attached: {output}")


@patch_app.command("status")
def patch_status(patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID.")) -> None:
    """Write and print patch lifecycle status."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch status", task_type="patch_status", inputs={"patch_run_id": patch_run})
    try:
        status_path, data = write_patch_status(repo_root, patch_run)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "status_path": str(status_path), "blocked": (data.get("gate") or {}).get("blocked"), "risk_level": (data.get("gate") or {}).get("risk_level")})
    trace.artifacts.append(TraceArtifact(path=str(status_path), kind="patch_status", description="Patch status markdown"))
    _success_trace(trace_store, trace)
    typer.echo(status_path.read_text(encoding="utf-8"))


@patch_app.command("summary")
def patch_summary(patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID.")) -> None:
    """Write patch lifecycle summary artifacts."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch summary", task_type="patch_summary", inputs={"patch_run_id": patch_run})
    try:
        path = summarize_patch_lifecycle(repo_root, patch_run)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "summary_path": str(path)})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="patch_lifecycle_summary", description="Patch lifecycle summary"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch summary written to: {path}")


@patch_app.command("commit")
def patch_commit(
    patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."),
    message: str = typer.Option(..., "--message", help="Commit message."),
    write: bool = typer.Option(False, "--write", help="Create local commit."),
    stage: bool = typer.Option(False, "--stage", help="Stage patch files before committing."),
    allow_high_risk: bool = typer.Option(False, "--allow-high-risk", help="Allow high-risk patch commit."),
    allow_main: bool = typer.Option(False, "--allow-main", help="Allow commit on main/master."),
    json_output: bool = typer.Option(False, "--json", help="Print commit JSON."),
) -> None:
    """Dry-run or explicitly create a local commit for an applied patch."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch commit", task_type="patch_commit", inputs={"patch_run_id": patch_run, "message": message, "write": write, "stage": stage, "allow_high_risk": allow_high_risk, "allow_main": allow_main})
    try:
        result = commit_patch_run(repo_root, patch_run, message, write=write, stage=stage, allow_high_risk=allow_high_risk, allow_main=allow_main)
        result_dir = repo_root / ".karakana" / "patch-commits" / trace.run_id
        result_dir.mkdir(parents=True, exist_ok=True)
        result_json = result_dir / "result.json"
        result_json.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (result_dir / "result.md").write_text(_render_commit_result(result.to_dict()), encoding="utf-8")
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "operation": "commit", "commit_requested": write, "stage_requested": stage, "committed": result.committed, "commit_sha": result.commit_sha, "status": result.status})
    trace.warnings.extend(result.warnings)
    trace.errors.extend(result.errors)
    trace.artifacts.append(TraceArtifact(path=str(result_json), kind="patch_commit_result", description="Patch commit result"))
    _success_trace(trace_store, trace)
    typer.echo(f"Patch commit result written to: {result_dir}")
    typer.echo(f"Status: {result.status}")
    typer.echo(f"Committed: {result.committed}")
    if result.commit_sha:
        typer.echo(f"Commit SHA: {result.commit_sha}")
    if json_output:
        typer.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))


def _render_branch_plan(data: dict, create: bool) -> str:
    return f"""# Karakana Patch Branch Plan

## Summary

- Patch run ID: {data.get("patch_run_id")}
- Current branch: {data.get("current_branch") or ""}
- Proposed branch: {data.get("proposed_branch")}
- Base branch: {data.get("base_branch")}
- Create requested: {create}
- Can create: {data.get("can_create")}

## Warnings

{_markdown_bullets(data.get("warnings") or [])}

## Safety

- No remote push was performed.
- No pull request was created.
"""


def _render_apply_result(data: dict) -> str:
    return f"""# Karakana Patch Apply Result

## Summary

- Patch run ID: {data.get("patch_run_id")}
- Status: {data.get("status")}
- Dry run: {data.get("dry_run")}
- Applied: {data.get("applied")}

## Files Changed

{_markdown_bullets(data.get("files_changed") or [])}

## Conflicts

{_markdown_bullets(data.get("conflicts") or [])}

## Warnings

{_markdown_bullets(data.get("warnings") or [])}

## Errors

{_markdown_bullets(data.get("errors") or [])}
"""


def _render_commit_result(data: dict) -> str:
    return f"""# Karakana Patch Commit Result

## Summary

- Patch run ID: {data.get("patch_run_id")}
- Status: {data.get("status")}
- Committed: {data.get("committed")}
- Commit SHA: {data.get("commit_sha") or ""}
- Message: {data.get("message") or ""}

## Warnings

{_markdown_bullets(data.get("warnings") or [])}

## Errors

{_markdown_bullets(data.get("errors") or [])}
"""


def _markdown_bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)


@eval_app.command("list")
def eval_list() -> None:
    """List discovered eval cases."""
    loader = EvalLoader(Path.cwd())
    for case in loader.load_cases():
        typer.echo(f"{case.id}\t{case.suite}\t{case.input.skill or ''}\t{case.name}")


@eval_app.command("show")
def eval_show(eval_id: str) -> None:
    """Show eval metadata and expectations."""
    import json

    loader = EvalLoader(Path.cwd())
    for case in loader.load_cases():
        if case.id == eval_id:
            typer.echo(json.dumps(case.to_dict(), indent=2, sort_keys=True))
            return
    typer.echo(f"Eval case not found: {eval_id}")
    raise typer.Exit(code=1)


@eval_app.command("run")
def eval_run(
    suite: str | None = typer.Option(None, "--suite", help="Run only one suite."),
    skill: str | None = typer.Option(None, "--skill", help="Run evals for one skill."),
    case: Path | None = typer.Option(None, "--case", help="Run one eval YAML file."),
    live: bool = typer.Option(False, "--live", help="Execute configured provider instead of judging prompt output only."),
    provider: str | None = typer.Option(None, "--provider", help="Override expected provider route."),
    model: str | None = typer.Option(None, "--model", help="Override expected model route."),
    json_output: bool = typer.Option(False, "--json", help="Print report JSON."),
    fail_fast: bool = typer.Option(False, "--fail-fast", help="Stop after first failed or errored case."),
) -> None:
    """Run deterministic eval cases."""
    import json

    try:
        report = EvalRunner(Path.cwd()).run(suite=suite, skill=skill, case_path=case, live=live, provider=provider, model=model, fail_fast=fail_fast)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    report_path = EvalReportStore(Path.cwd()).run_dir(report.eval_run_id) / "report.json"
    typer.echo(f"Eval report written to: {report_path.parent}")
    typer.echo(f"Status: {report.status}")
    typer.echo(f"Cases: {report.total_cases}, passed: {report.passed}, failed: {report.failed}, warnings: {report.warnings}")
    if json_output:
        typer.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    if report.failed:
        raise typer.Exit(code=1)


@eval_app.command("latest")
def eval_latest() -> None:
    """Print the latest eval report markdown."""
    store = EvalReportStore(Path.cwd())
    report = store.latest()
    if report is None:
        typer.echo("No eval reports found.")
        return
    path = store.run_dir(report.eval_run_id) / "report.md"
    typer.echo(path.read_text(encoding="utf-8"))


@eval_app.command("report")
def eval_report(eval_run_id: str) -> None:
    """Print an eval report markdown file."""
    store = EvalReportStore(Path.cwd())
    try:
        store.load(eval_run_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    path = store.run_dir(eval_run_id) / "report.md"
    typer.echo(path.read_text(encoding="utf-8"))


@github_app.command("issue-triage")
def github_issue_triage(
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skill: str = typer.Option(..., "--skill", "-s", help="Skill name to include."),
    output: Path = typer.Option(Path(".karakana/issue-triage.md"), "--output", help="Prompt output path."),
    post_comment: bool = typer.Option(False, "--post-comment", help="Post generated artifact as an issue comment."),
    live: bool = typer.Option(False, "--live", help="Execute selected model provider."),
    provider: str | None = typer.Option(None, "--provider", help="Override model provider."),
    model: str | None = typer.Option(None, "--model", help="Override model name."),
    strict_review: bool = typer.Option(False, "--strict-review", help="Block live responses missing expected sections."),
) -> None:
    """Generate an issue triage prompt from the GitHub event payload."""
    repo_root = Path.cwd()
    generator = GitHubPromptGenerator(repo_root)
    trace_store = TraceStore(repo_root)
    model_route = route_model("issue_triage", provider=provider, model=model)
    trace = trace_store.create_run(
        command="github issue-triage",
        project=project,
        skill=skill,
        task_type="issue_triage",
        selected_model=model_route["model"],
        inputs={"project": project, "skill": skill, "output": str(output), "post_comment": post_comment, "live": live, "provider": model_route["provider"], "model": model_route["model"]},
    )
    _record_route_outputs(trace, model_route)
    try:
        prompt = generator.build_issue_triage_prompt(project=project, skill=skill)
        output_path = generator.write_prompt(prompt, output)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs["prompt_path"] = str(output_path)
    trace.artifacts.append(TraceArtifact(path=str(output_path), kind="github_issue_triage_prompt", description="Generated issue triage prompt"))
    if live:
        try:
            artifacts = _execute_model_to_artifacts(repo_root, prompt, model_route["provider"], model_route["model"], trace, task_type="issue_triage", project=project, skill=skill, expected="issue-triage", strict_review=strict_review)
            _print_live_artifacts(artifacts)
        except Exception as exc:
            _fail_trace(trace_store, trace, exc)
            typer.echo(str(exc))
            raise typer.Exit(code=1) from exc
    if post_comment:
        issue_number = _event_issue_number()
        body = _bounded_github_comment_body(output_path.read_text(encoding="utf-8"), output_path)
        if body != output_path.read_text(encoding="utf-8"):
            trace.warnings.append("GitHub comment body was truncated to satisfy body_size_reasonable.")
        client = GitHubApiClient()
        checks = validate_comment_write(client, post_comment, issue_number, body)
        _record_github_checks(trace, checks)
        if failed_checks(checks):
            trace.errors.extend(check.message for check in failed_checks(checks))
            trace.finish("failed")
            trace_store.save(trace)
            typer.echo("GitHub comment safety checks failed.")
            raise typer.Exit(code=1)
        result = client.post_issue_comment(issue_number, body)
        trace.outputs["comment_url"] = result.get("html_url")
    _success_trace(trace_store, trace)
    typer.echo(f"Issue triage prompt written to: {output_path}")
    if post_comment:
        typer.echo(f"Posted issue comment: {trace.outputs.get('comment_url') or 'created'}")


@github_app.command("pr-review")
def github_pr_review(
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skill: str = typer.Option(..., "--skill", "-s", help="Skill name to include."),
    output: Path = typer.Option(Path(".karakana/pr-review.md"), "--output", help="Prompt output path."),
    post_comment: bool = typer.Option(False, "--post-comment", help="Post generated artifact as a PR conversation comment."),
    live: bool = typer.Option(False, "--live", help="Execute selected model provider."),
    provider: str | None = typer.Option(None, "--provider", help="Override model provider."),
    model: str | None = typer.Option(None, "--model", help="Override model name."),
    strict_review: bool = typer.Option(False, "--strict-review", help="Block live responses missing expected sections."),
) -> None:
    """Generate a PR review prompt from the GitHub event payload."""
    repo_root = Path.cwd()
    generator = GitHubPromptGenerator(repo_root)
    trace_store = TraceStore(repo_root)
    model_route = route_model("pr_review", provider=provider, model=model)
    trace = trace_store.create_run(
        command="github pr-review",
        project=project,
        skill=skill,
        task_type="pr_review",
        selected_model=model_route["model"],
        inputs={"project": project, "skill": skill, "output": str(output), "post_comment": post_comment, "live": live, "provider": model_route["provider"], "model": model_route["model"]},
    )
    _record_route_outputs(trace, model_route)
    try:
        prompt = generator.build_pr_review_prompt(project=project, skill=skill)
        output_path = generator.write_prompt(prompt, output)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs["prompt_path"] = str(output_path)
    trace.artifacts.append(TraceArtifact(path=str(output_path), kind="github_pr_review_prompt", description="Generated PR review prompt"))
    if live:
        try:
            artifacts = _execute_model_to_artifacts(repo_root, prompt, model_route["provider"], model_route["model"], trace, task_type="pr_review", project=project, skill=skill, expected="pr-review", strict_review=strict_review)
            _print_live_artifacts(artifacts)
        except Exception as exc:
            _fail_trace(trace_store, trace, exc)
            typer.echo(str(exc))
            raise typer.Exit(code=1) from exc
    if post_comment:
        pr_number = _event_pr_number()
        body = _bounded_github_comment_body(output_path.read_text(encoding="utf-8"), output_path)
        if body != output_path.read_text(encoding="utf-8"):
            trace.warnings.append("GitHub comment body was truncated to satisfy body_size_reasonable.")
        client = GitHubApiClient()
        checks = validate_comment_write(client, post_comment, pr_number, body)
        _record_github_checks(trace, checks)
        if failed_checks(checks):
            trace.errors.extend(check.message for check in failed_checks(checks))
            trace.finish("failed")
            trace_store.save(trace)
            typer.echo("GitHub comment safety checks failed.")
            raise typer.Exit(code=1)
        result = client.post_issue_comment(pr_number, body)
        trace.outputs["comment_url"] = result.get("html_url")
    _success_trace(trace_store, trace)
    typer.echo(f"PR review prompt written to: {output_path}")
    if post_comment:
        typer.echo(f"Posted PR comment: {trace.outputs.get('comment_url') or 'created'}")


@github_app.command("ci-failure")
def github_ci_failure(
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skill: str = typer.Option(..., "--skill", "-s", help="Skill name to include."),
    log_file: Path | None = typer.Option(None, "--log-file", help="Path to a CI log file."),
    output: Path = typer.Option(Path(".karakana/ci-failure-analysis.md"), "--output", help="Prompt output path."),
    live: bool = typer.Option(False, "--live", help="Execute selected model provider."),
    provider: str | None = typer.Option(None, "--provider", help="Override model provider."),
    model: str | None = typer.Option(None, "--model", help="Override model name."),
    strict_review: bool = typer.Option(False, "--strict-review", help="Block live responses missing expected sections."),
) -> None:
    """Generate a CI failure analysis prompt from a local log file."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    model_route = route_model("ci_failure_analysis", provider=provider, model=model)
    trace = trace_store.create_run(
        command="github ci-failure",
        project=project,
        skill=skill,
        task_type="ci_failure_analysis",
        selected_model=model_route["model"],
        inputs={"project": project, "skill": skill, "log_file": str(log_file) if log_file else None, "output": str(output), "live": live, "provider": model_route["provider"], "model": model_route["model"]},
    )
    _record_route_outputs(trace, model_route)
    if log_file is None:
        trace.errors.append("--log-file is required")
        trace.next_actions.append("Provide --log-file with a local CI log path.")
        trace.finish("failed")
        trace_store.save(trace)
        typer.echo("--log-file is required")
        raise typer.Exit(code=1)
    generator = GitHubPromptGenerator(repo_root)
    try:
        prompt = generator.build_ci_failure_prompt(project=project, skill=skill, log_file=log_file)
        output_path = generator.write_prompt(prompt, output)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs["prompt_path"] = str(output_path)
    trace.artifacts.append(TraceArtifact(path=str(output_path), kind="github_ci_failure_prompt", description="Generated CI failure analysis prompt"))
    if live:
        try:
            artifacts = _execute_model_to_artifacts(repo_root, prompt, model_route["provider"], model_route["model"], trace, task_type="ci_failure_analysis", project=project, skill=skill, expected="ci-failure", strict_review=strict_review)
            _print_live_artifacts(artifacts)
        except Exception as exc:
            _fail_trace(trace_store, trace, exc)
            typer.echo(str(exc))
            raise typer.Exit(code=1) from exc
    _success_trace(trace_store, trace)
    typer.echo(f"CI failure analysis prompt written to: {output_path}")


@improve_app.command("propose")
def improve_propose(
    project: str | None = typer.Option(None, "--project", "-p", help="Project to analyze."),
    since: str = typer.Option("7 days", "--since", help="Trace window to inspect."),
    limit: int = typer.Option(20, "--limit", help="Maximum traces to inspect."),
    json_output: bool = typer.Option(False, "--json", help="Print proposal JSON."),
) -> None:
    """Generate a reviewable self-improvement proposal from run traces."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="improve propose",
        project=project,
        task_type="self_improvement_proposal",
        inputs={"project": project, "since": since, "limit": limit},
    )
    proposal_store = ProposalStore(repo_root)
    try:
        proposal = ImprovementProposer(repo_root).propose(project=project, since=since, limit=limit)
        proposal_path = proposal_store.save(proposal)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    trace.outputs["proposal_id"] = proposal.proposal_id
    trace.outputs["findings_count"] = len(proposal.changes)
    trace.outputs["proposed_changes_count"] = len(proposal.changes)
    trace.warnings.extend(proposal.warnings)
    trace.artifacts.append(TraceArtifact(path=str(proposal_path), kind="improvement_proposal_json", description="Generated proposal JSON"))
    trace.artifacts.append(
        TraceArtifact(
            path=str(proposal_path.parent / "proposal.md"),
            kind="improvement_proposal_markdown",
            description="Generated proposal markdown",
        )
    )
    _success_trace(trace_store, trace)
    typer.echo(f"Improvement proposal written to: {proposal_path.parent}")
    if json_output:
        typer.echo(json.dumps(proposal.to_dict(), indent=2, sort_keys=True))


@improve_app.command("list")
def improve_list(limit: int = typer.Option(20, "--limit", help="Maximum proposals to show.")) -> None:
    """List recent self-improvement proposals."""
    proposals = ProposalStore(Path.cwd()).list_proposals(limit=limit)
    if not proposals:
        typer.echo("No proposals found.")
        return
    for proposal in proposals:
        typer.echo(
            f"{proposal.proposal_id}\t{proposal.created_at}\t{proposal.status}\t"
            f"{proposal.project or ''}\t{len(proposal.changes)} change(s)"
        )


@improve_app.command("show")
def improve_show(proposal_id: str) -> None:
    """Print a proposal markdown summary."""
    store = ProposalStore(Path.cwd())
    try:
        proposal = store.load(proposal_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    summary_path = store.write_summary(proposal)
    typer.echo(summary_path.read_text(encoding="utf-8"))


@improve_app.command("latest")
def improve_latest() -> None:
    """Print the latest proposal markdown summary."""
    store = ProposalStore(Path.cwd())
    proposal = store.latest()
    if proposal is None:
        typer.echo("No proposals found.")
        return
    summary_path = store.write_summary(proposal)
    typer.echo(summary_path.read_text(encoding="utf-8"))


@model_app.command("list")
def model_list() -> None:
    """List registered model providers."""
    registry = default_registry()
    for provider_name in registry.list_providers():
        typer.echo(provider_name)


@model_app.command("config")
def model_config() -> None:
    """Print redacted model configuration."""
    import json

    typer.echo(json.dumps(redacted_model_config(), indent=2, sort_keys=True))


@model_app.command("check")
def model_check() -> None:
    """Show configured model providers without revealing secrets."""
    registry = default_registry()
    configured = set(registry.configured_providers())
    for provider_name in registry.list_providers():
        status = "configured" if provider_name in configured else "not configured"
        typer.echo(f"{provider_name}: {status}")


@model_app.command("route")
def model_route(
    task_type: str = typer.Option(..., "--task-type", help="Task type to route."),
    signals: str = typer.Option("", "--signals", help="Comma-separated escalation signals."),
    provider: str | None = typer.Option(None, "--provider", help="Manual provider override."),
    model: str | None = typer.Option(None, "--model", help="Manual model override."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Use skillpack route overrides."),
    risk_level: str | None = typer.Option(None, "--risk-level", help="Optional risk level for safety warnings."),
    json_output: bool = typer.Option(False, "--json", help="Print route JSON."),
) -> None:
    """Show the cost-aware route for a task type."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    signal_list = [signal.strip() for signal in signals.split(",") if signal.strip()]
    skillpack_context = _resolve_optional_skillpack(repo_root, skillpack) if skillpack else None
    route = route_model(task_type, provider=provider, model=model, skillpack_routes=skillpack_context.model_routes if skillpack_context else None)
    escalation = recommend_escalation(route["provider"], route["model"], signal_list)
    warnings = validate_model_route(task_type, route["provider"], route["model"], risk_level=risk_level)
    trace = trace_store.create_run(
        command="model route",
        task_type="model_routing",
        selected_model=route["model"],
        inputs={"task_type": task_type, "signals": signal_list, "provider": provider, "model": model, "skillpack": skillpack, "risk_level": risk_level},
    )
    trace.outputs.update(
        {
            "task_type": task_type,
            "selected_provider": route["provider"],
            "selected_model": route["model"],
            "routing_rationale": route.get("rationale"),
            "escalation_signals": signal_list,
            "escalation_recommendation": escalation,
            "manual_override": route.get("manual_override", False),
            "route_source": route.get("route_source"),
            "skillpack": skillpack_context.skillpack.name if skillpack_context else None,
            "override_reason": "Manual --provider/--model override" if route.get("manual_override") else None,
            "cost_tier": route.get("cost_tier"),
            "risk_tier": risk_level,
            "capability_tier": route.get("capability_tier"),
            "warnings": warnings,
        }
    )
    trace.warnings.extend(warnings)
    _success_trace(trace_store, trace)
    output = {
        "task_type": task_type,
        "provider": route["provider"],
        "model": route["model"],
        "mode": route.get("mode"),
        "rationale": route.get("rationale"),
        "cost_tier": route.get("cost_tier"),
        "capability_tier": route.get("capability_tier"),
        "manual_override": route.get("manual_override", False),
        "route_source": route.get("route_source"),
        "skillpack": skillpack_context.skillpack.name if skillpack_context else None,
        "escalation": escalation,
        "warnings": warnings,
    }
    if json_output:
        typer.echo(json.dumps(output, indent=2, sort_keys=True))
        return
    typer.echo(f"Task type: {task_type}")
    typer.echo(f"Provider: {route['provider']}")
    typer.echo(f"Model: {route['model']}")
    typer.echo(f"Mode: {route.get('mode')}")
    typer.echo(f"Cost tier: {route.get('cost_tier')}")
    typer.echo(f"Capability tier: {route.get('capability_tier')}")
    typer.echo(f"Rationale: {route.get('rationale')}")
    typer.echo(f"Route source: {route.get('route_source')}")
    if skillpack_context:
        typer.echo(f"Skillpack: {skillpack_context.skillpack.name}")
    if signal_list:
        typer.echo(f"Escalation signals: {', '.join(signal_list)}")
    typer.echo(f"Escalation notes: {escalation['rationale']}")
    if escalation["should_escalate"]:
        typer.echo(f"Recommended escalation: {escalation['to_provider']}/{escalation['to_model']}")
    if warnings:
        typer.echo("Warnings:")
        for warning in warnings:
            typer.echo(f"- {warning}")


@model_app.command("complete")
def model_complete(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Prompt text."),
    provider: str = typer.Option("mock", "--provider", help="Provider name."),
    model: str = typer.Option("mock-model", "--model", help="Model name."),
    live: bool = typer.Option(False, "--live", help="Execute provider live."),
    output: Path = typer.Option(Path(".karakana/model-response.md"), "--output", help="Response artifact path."),
    strict_review: bool = typer.Option(False, "--strict-review", help="Block live responses missing expected sections."),
) -> None:
    """Complete a prompt through a provider, dry-run unless --live is passed."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="model complete",
        task_type="model_complete",
        selected_model=model,
        inputs={"provider": provider, "model": model, "prompt": prompt, "live": live, "output": str(output)},
    )
    try:
        if live:
            artifacts = _execute_model_to_artifacts(repo_root, prompt, provider, model, trace, task_type="model_complete", expected="generic", strict_review=strict_review)
            _success_trace(trace_store, trace)
            _print_live_artifacts(artifacts)
            typer.echo(f"Model response written to: {artifacts['response']}")
        else:
            trace.outputs["dry_run"] = True
            trace.outputs["provider"] = provider
            trace.outputs["model"] = model
            trace.next_actions.append("Run with --live to execute this provider.")
            _success_trace(trace_store, trace)
            typer.echo(f"Dry run: would call {provider}/{model}. Use --live to execute.")
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@model_app.command("review")
def model_review(
    response_file: Path,
    strict: bool = typer.Option(False, "--strict", help="Block missing expected sections."),
    expected: str = typer.Option("generic", "--expected", help="Expected response profile."),
    json_output: bool = typer.Option(False, "--json", help="Print review JSON."),
) -> None:
    """Review a saved model response artifact."""
    import json

    try:
        response = response_file.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    review = review_response(response, expected=expected, strict=strict)
    write_review_artifacts(review, response_file.parent)
    typer.echo(f"Review status: {review.status}")
    typer.echo(f"Review: {response_file.parent / 'response-review.md'}")
    if json_output:
        typer.echo(json.dumps(review.to_dict(), indent=2, sort_keys=True))
    if review.blocked:
        raise typer.Exit(code=1)


@improve_app.command("publish")
def improve_publish(
    proposal_id: str,
    create_issue: bool = typer.Option(False, "--create-issue", help="Create a GitHub issue from the proposal."),
    create_pr: bool = typer.Option(False, "--create-pr", help="Create a draft pull request from the current branch."),
    labels: str = typer.Option("karakana,self-improvement,needs-review", "--labels", help="Comma-separated issue labels."),
    base: str = typer.Option("main", "--base", help="Base branch for PR creation."),
    head: str | None = typer.Option(None, "--head", help="Head branch for PR creation."),
    ready: bool = typer.Option(False, "--ready", help="Create PR as ready for review instead of draft."),
) -> None:
    """Publish a proposal to GitHub only when explicit write flags are used."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="improve publish", task_type="proposal_publish", inputs={"proposal_id": proposal_id, "create_issue": create_issue, "create_pr": create_pr, "base": base, "head": head})
    store = ProposalStore(repo_root)
    try:
        proposal = store.load(proposal_id)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    body_path = store.proposals_root / proposal_id / "proposal.md"
    body = body_path.read_text(encoding="utf-8")
    title = f"karakana: {proposal.summary[:80]}"
    client = GitHubApiClient()

    if create_issue:
        issue_labels = [label.strip() for label in labels.split(",") if label.strip()]
        max_risk = _max_risk(proposal)
        if max_risk in {"high", "critical"}:
            issue_labels.append(f"risk:{max_risk}")
        checks = validate_issue_create(client, True, title, body)
        _record_github_checks(trace, checks)
        if failed_checks(checks):
            trace.errors.extend(check.message for check in failed_checks(checks))
            trace.finish("failed")
            trace_store.save(trace)
            typer.echo("GitHub issue safety checks failed.")
            raise typer.Exit(code=1)
        result = client.create_issue(title=title, body=body, labels=issue_labels)
        trace.outputs["created_issue_url"] = result.get("html_url")
        _success_trace(trace_store, trace)
        typer.echo(f"Created GitHub issue: {trace.outputs.get('created_issue_url') or 'created'}")
        return

    if create_pr:
        pr_head = head or _current_branch(repo_root)
        checks = validate_pr_create(client, True, title, body, pr_head, base)
        _record_github_checks(trace, checks)
        if _has_no_local_changes(repo_root):
            trace.errors.append("No local changes detected for PR creation.")
        if failed_checks(checks) or trace.errors:
            trace.finish("failed")
            trace_store.save(trace)
            typer.echo("GitHub PR safety checks failed.")
            raise typer.Exit(code=1)
        result = client.create_pull_request(title=title, body=body, head=pr_head, base=base, draft=not ready)
        trace.outputs["created_pr_url"] = result.get("html_url")
        _success_trace(trace_store, trace)
        typer.echo(f"Created draft pull request: {trace.outputs.get('created_pr_url') or 'created'}")
        return

    trace.outputs["dry_run"] = True
    trace.outputs["title"] = title
    trace.outputs["labels"] = labels
    trace.next_actions.append("Run with --create-issue or --create-pr to perform an explicit GitHub write.")
    _success_trace(trace_store, trace)
    typer.echo("Dry run: no GitHub write performed.")
    typer.echo(f"Would publish proposal: {proposal_id}")
    typer.echo(f"Title: {title}")


@improve_app.command("apply")
def improve_apply(
    proposal_id: str,
    write: bool = typer.Option(False, "--write", help="Apply eligible low-risk proposal changes."),
    branch: str | None = typer.Option(None, "--branch", help="Optional local branch to create before writing."),
) -> None:
    """Dry-run or apply eligible low-risk proposal changes locally."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="improve apply", task_type="proposal_apply", inputs={"proposal_id": proposal_id, "write": write, "branch": branch})
    store = ProposalStore(repo_root)
    try:
        proposal = store.load(proposal_id)
    except FileNotFoundError as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    typer.echo(f"Proposal: {proposal_id}")
    for change in proposal.changes:
        typer.echo(f"- {change.change_type}: {change.target_path} ({change.risk_level})")
    if not write:
        trace.outputs["dry_run"] = True
        trace.next_actions.append("Run with --write to apply eligible low-risk changes.")
        _success_trace(trace_store, trace)
        typer.echo("Dry run: no files modified. Use --write to apply eligible low-risk changes.")
        return

    if branch:
        _create_branch(repo_root, branch)
        trace.outputs["branch"] = branch
    backups_dir = store.proposals_root / proposal_id / "backups"
    changed = []
    for change in proposal.changes:
        if change.risk_level != "low" or not change.proposed_content:
            trace.warnings.append(f"Skipped {change.target_path}: only low-risk changes with proposed_content are applied.")
            continue
        try:
            target = _safe_apply_path(repo_root, change.target_path)
        except ValueError as exc:
            trace.errors.append(str(exc))
            continue
        backups_dir.mkdir(parents=True, exist_ok=True)
        if target.exists():
            backup = backups_dir / (change.target_path.replace("/", "__") + ".bak")
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(change.proposed_content), encoding="utf-8")
        changed.append(str(target))
    trace.outputs["changed_files"] = changed
    if trace.errors:
        trace.finish("failed")
        trace_store.save(trace)
        for error in trace.errors:
            typer.echo(f"ERROR: {error}")
        raise typer.Exit(code=1)
    _success_trace(trace_store, trace)
    typer.echo(f"Applied {len(changed)} file(s).")


@ingest_app.command("file")
def ingest_file(
    path: Path,
    project: str | None = typer.Option(None, "--project", help="Project context."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context."),
    classify: bool = typer.Option(False, "--classify", help="Classify and generate candidates."),
    max_size: int = typer.Option(200_000, "--max-size", help="Maximum source size in bytes."),
    json_output: bool = typer.Option(False, "--json", help="Print bundle JSON."),
) -> None:
    """Ingest one selected text file into reviewable candidates."""
    repo_root = Path.cwd()
    try:
        source_tuple = load_file_source(repo_root, path, project=project, skillpack=skillpack, max_size=max_size)
        _save_ingestion_from_sources(repo_root, "ingest file", [source_tuple], project, skillpack, classify=classify, json_output=json_output)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("trace")
def ingest_trace(run_id: str, project: str | None = typer.Option(None, "--project"), skillpack: str | None = typer.Option(None, "--skillpack"), classify: bool = typer.Option(False, "--classify"), json_output: bool = typer.Option(False, "--json")) -> None:
    """Ingest a local Karakana trace."""
    repo_root = Path.cwd()
    try:
        source_tuple = load_trace_source(repo_root, run_id, project=project, skillpack=skillpack)
        _save_ingestion_from_sources(repo_root, "ingest trace", [source_tuple], project, skillpack, classify=classify, json_output=json_output)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("action")
def ingest_action(action_run_id: str, project: str | None = typer.Option(None, "--project"), skillpack: str | None = typer.Option(None, "--skillpack"), classify: bool = typer.Option(False, "--classify"), json_output: bool = typer.Option(False, "--json")) -> None:
    """Ingest an extracted action bundle."""
    repo_root = Path.cwd()
    try:
        source_tuple = load_action_source(repo_root, action_run_id, project=project, skillpack=skillpack)
        _save_ingestion_from_sources(repo_root, "ingest action", [source_tuple], project, skillpack, classify=classify, json_output=json_output)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("patch-review")
def ingest_patch_review(patch_review_id: str, project: str | None = typer.Option(None, "--project"), skillpack: str | None = typer.Option(None, "--skillpack"), classify: bool = typer.Option(False, "--classify"), json_output: bool = typer.Option(False, "--json")) -> None:
    """Ingest a patch review artifact."""
    repo_root = Path.cwd()
    try:
        source_tuple = load_patch_review_source(repo_root, patch_review_id, project=project, skillpack=skillpack)
        _save_ingestion_from_sources(repo_root, "ingest patch-review", [source_tuple], project, skillpack, classify=classify, json_output=json_output)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("proposal")
def ingest_proposal(proposal_id: str, project: str | None = typer.Option(None, "--project"), skillpack: str | None = typer.Option(None, "--skillpack"), classify: bool = typer.Option(False, "--classify"), json_output: bool = typer.Option(False, "--json")) -> None:
    """Ingest a self-improvement proposal."""
    repo_root = Path.cwd()
    try:
        source_tuple = load_proposal_source(repo_root, proposal_id, project=project, skillpack=skillpack)
        _save_ingestion_from_sources(repo_root, "ingest proposal", [source_tuple], project, skillpack, classify=classify, json_output=json_output)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("note")
def ingest_note(
    text: str = typer.Option(..., "--text", help="Manual note to classify."),
    project: str | None = typer.Option(None, "--project"),
    skillpack: str | None = typer.Option(None, "--skillpack"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Create ingestion candidates from a manual note."""
    repo_root = Path.cwd()
    try:
        source_tuple = load_note_source(text, project=project, skillpack=skillpack)
        _save_ingestion_from_sources(repo_root, "ingest note", [source_tuple], project, skillpack, classify=True, json_output=json_output)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("scan")
def ingest_scan(
    project: str | None = typer.Option(None, "--project", help="Project context."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context."),
    include: list[str] | None = typer.Option(None, "--include", help="Source kind to include: docs, traces, actions, patch-reviews, proposals."),
    max_files: int = typer.Option(20, "--max-files", help="Maximum sources to inspect."),
    since: str | None = typer.Option(None, "--since", help="Reserved future scan window."),
    classify: bool = typer.Option(False, "--classify", help="Classify and generate candidates."),
    json_output: bool = typer.Option(False, "--json", help="Print bundle JSON."),
) -> None:
    """Conservatively scan documentation and selected Karakana artifacts."""
    repo_root = Path.cwd()
    try:
        sources = scan_sources(repo_root, project=project, skillpack=skillpack, includes=include, max_files=max_files)
        _save_ingestion_from_sources(repo_root, "ingest scan", sources, project, skillpack, classify=classify, json_output=json_output, extra_inputs={"include": include, "max_files": max_files, "since": since})
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@ingest_app.command("list")
def ingest_list(limit: int = typer.Option(20, "--limit", help="Maximum bundles to show.")) -> None:
    """List recent ingestion bundles."""
    bundles = IngestionStore(Path.cwd()).list(limit=limit)
    if not bundles:
        typer.echo("No ingestion bundles found.")
        return
    for bundle in bundles:
        typer.echo(f"{bundle.ingest_id}\t{bundle.created_at}\t{bundle.status}\t{bundle.project or ''}\t{len(bundle.candidates)} candidate(s)")


@ingest_app.command("show")
def ingest_show(ingest_id: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Show an ingestion bundle."""
    store = IngestionStore(Path.cwd())
    try:
        bundle = store.load(ingest_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    if json_output:
        typer.echo(json.dumps(bundle.to_dict(), indent=2, sort_keys=True))
    else:
        typer.echo((store.bundle_dir(ingest_id) / "candidates.md").read_text(encoding="utf-8"))


@ingest_app.command("review")
def ingest_review(ingest_id: str, json_output: bool = typer.Option(False, "--json", help="Print review JSON.")) -> None:
    """Review an ingestion bundle without applying it."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="ingest review", task_type="ingestion_review", inputs={"ingest_id": ingest_id})
    try:
        result, review_path = review_ingestion_bundle(repo_root, ingest_id)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"ingest_id": ingest_id, "review_status": result["status"], "blocked": result["blocked"], "review_path": str(review_path)})
    trace.warnings.extend(result.get("warnings") or [])
    trace.artifacts.append(TraceArtifact(path=str(review_path), kind="ingestion_review", description="Ingestion review markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Ingestion review written to: {review_path}")
    typer.echo(f"Status: {result['status']}")
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))


@ingest_app.command("apply")
def ingest_apply(
    ingest_id: str,
    write: bool = typer.Option(False, "--write", help="Apply candidates."),
    candidate: str | None = typer.Option(None, "--candidate", help="Apply one candidate ID."),
    allow_high_risk: bool = typer.Option(False, "--allow-high-risk", help="Allow high-risk candidate apply."),
    allow_behavior_update: bool = typer.Option(False, "--allow-behavior-update", help="Allow behavior memory updates."),
    json_output: bool = typer.Option(False, "--json", help="Print apply JSON."),
) -> None:
    """Dry-run or explicitly apply ingestion candidates."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="ingest apply", task_type="ingestion_apply", inputs={"ingest_id": ingest_id, "write": write, "candidate": candidate, "allow_high_risk": allow_high_risk, "allow_behavior_update": allow_behavior_update})
    try:
        result, result_path = apply_ingestion_bundle(repo_root, ingest_id, write=write, candidate_id=candidate, allow_high_risk=allow_high_risk, allow_behavior_update=allow_behavior_update)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"ingest_id": ingest_id, "apply_requested": True, "write_requested": write, "applied_candidates": result.get("applied_candidates"), "blocked_candidates": result.get("blocked_candidates"), "apply_path": str(result_path)})
    trace.warnings.extend(result.get("warnings") or [])
    trace.artifacts.append(TraceArtifact(path=str(result_path), kind="ingestion_apply", description="Ingestion apply result"))
    _success_trace(trace_store, trace)
    typer.echo("Dry run: no files written." if not write else "Ingestion apply completed.")
    typer.echo(f"Status: {result['status']}")
    typer.echo(f"Result: {result_path}")
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))


@memory_app.command("list-projects")
def memory_list_projects() -> None:
    """List projects available under ubongo/projects."""
    projects = UbongoMemory(root=Path.cwd()).list_projects()
    if not projects:
        typer.echo("No projects found.")
        return
    for project in projects:
        typer.echo(project)


@memory_app.command("validate")
def memory_validate(
    project: str = typer.Option(..., "--project", "-p", help="Project memory directory to validate."),
) -> None:
    """Validate required memory files for a project."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="memory validate",
        project=project,
        task_type="memory_validation",
        inputs={"project": project},
    )
    missing = UbongoMemory(root=repo_root).validate_project(project)
    if missing:
        trace.outputs["missing_files"] = missing
        trace.errors.append(f"Missing required memory files: {', '.join(missing)}")
        trace.next_actions.append("Create the missing memory files under ubongo/projects/<project>/.")
        trace.finish("failed")
        trace_store.save(trace)
        typer.echo(f"Project '{project}' is missing required memory files:")
        for filename in missing:
            typer.echo(f"- {filename}")
        raise typer.Exit(code=1)
    trace.outputs["missing_files"] = []
    _success_trace(trace_store, trace)
    typer.echo(f"Project '{project}' memory is complete.")


@memory_app.command("show")
def memory_show(
    project: str = typer.Option(..., "--project", "-p", help="Project memory directory to show."),
) -> None:
    """Print a readable project memory summary."""
    memory = UbongoMemory(root=Path.cwd())
    missing = memory.validate_project(project)
    if missing:
        typer.echo(f"Project '{project}' is missing required memory files:")
        for filename in missing:
            typer.echo(f"- {filename}")
        raise typer.Exit(code=1)
    typer.echo(memory.summarize_project_context(project))


@requirements_app.command("prd")
def requirements_prd(
    from_action: str | None = typer.Option(None, "--from-action", help="Action bundle ID."),
    from_ingest: str | None = typer.Option(None, "--from-ingest", help="Ingestion bundle ID."),
    from_patch_review: str | None = typer.Option(None, "--from-patch-review", help="Patch review ID."),
    from_proposal: str | None = typer.Option(None, "--from-proposal", help="Improvement proposal ID."),
    from_file: Path | None = typer.Option(None, "--from-file", help="Markdown or text file."),
    from_note: str | None = typer.Option(None, "--from-note", help="Manual note text."),
    project: str | None = typer.Option(None, "--project", help="Project context."),
    skillpack: str | None = typer.Option(None, "--skillpack", help="Skillpack context."),
    no_current_skillpack: bool = typer.Option(False, "--no-current-skillpack", help="Do not use active skillpack."),
    json_output: bool = typer.Option(False, "--json", help="Print PRD JSON."),
) -> None:
    """Generate a reviewable PRD from one selected source."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="requirements prd",
        project=project,
        task_type="requirements_prd",
        inputs={
            "from_action": from_action,
            "from_ingest": from_ingest,
            "from_patch_review": from_patch_review,
            "from_proposal": from_proposal,
            "from_file": str(from_file) if from_file else None,
            "from_note": from_note,
            "project": project,
            "skillpack": skillpack,
            "no_current_skillpack": no_current_skillpack,
        },
    )
    try:
        skillpack_context = SkillpackResolver(repo_root).resolve_for_project(skillpack) if skillpack else (None if no_current_skillpack else _resolve_optional_skillpack(repo_root, None))
        source, content = _load_requirement_source(repo_root, from_action, from_ingest, from_patch_review, from_proposal, from_file, from_note, project, skillpack_context.skillpack.name if skillpack_context else skillpack)
        prd = generate_prd(source, content, project=project, skillpack_context=skillpack_context)
        path = RequirementsStore(repo_root).save_prd(prd)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"req_id": prd.req_id, "source_type": source.source_type, "source_id": source.source_id, "project": prd.project, "skillpack": prd.skillpack, "generated_prd": str(path), "warnings": source.metadata.get("warnings", [])})
    trace.warnings.extend(source.metadata.get("warnings", []))
    trace.artifacts.append(TraceArtifact(path=str(path), kind="requirements_prd", description="Requirement PRD JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "prd.md"), kind="requirements_prd_markdown", description="Requirement PRD markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Requirement PRD written to: {path.parent}")
    typer.echo(f"Requirement ID: {prd.req_id}")
    if json_output:
        typer.echo(json.dumps(prd.to_dict(), indent=2, sort_keys=True))


@requirements_app.command("stories")
def requirements_stories(from_prd: str = typer.Option(..., "--from-prd", help="Requirement ID."), json_output: bool = typer.Option(False, "--json", help="Print stories JSON.")) -> None:
    """Generate user stories from a PRD."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="requirements stories", task_type="requirements_stories", inputs={"req_id": from_prd})
    try:
        store = RequirementsStore(repo_root)
        prd = store.load_prd(from_prd)
        stories = generate_stories(prd)
        path = store.save_stories(from_prd, stories)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"req_id": from_prd, "generated_stories": str(path), "story_count": len(stories)})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="requirements_stories", description="User stories JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "stories.md"), kind="requirements_stories_markdown", description="User stories markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"User stories written to: {path.parent / 'stories.md'}")
    typer.echo(f"Stories: {len(stories)}")
    if json_output:
        typer.echo(json.dumps([story.to_dict() for story in stories], indent=2, sort_keys=True))


@requirements_app.command("issues")
def requirements_issues(from_prd: str = typer.Option(..., "--from-prd", help="Requirement ID."), json_output: bool = typer.Option(False, "--json", help="Print issues JSON.")) -> None:
    """Generate issue drafts from a PRD."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="requirements issues", task_type="requirements_issues", inputs={"req_id": from_prd})
    try:
        store = RequirementsStore(repo_root)
        prd = store.load_prd(from_prd)
        try:
            stories = store.load_stories(from_prd)
        except FileNotFoundError:
            stories = generate_stories(prd)
            store.save_stories(from_prd, stories)
        issues = generate_issues(prd, stories)
        path = store.save_issues(from_prd, issues)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"req_id": from_prd, "generated_issues": str(path), "issue_count": len(issues)})
    trace.artifacts.append(TraceArtifact(path=str(path), kind="requirements_issues", description="Issue drafts JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "issues.md"), kind="requirements_issues_markdown", description="Issue drafts markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Issue drafts written to: {path.parent / 'issues.md'}")
    typer.echo(f"Issues: {len(issues)}")
    if json_output:
        typer.echo(json.dumps([issue.to_dict() for issue in issues], indent=2, sort_keys=True))


@requirements_app.command("ready")
def requirements_ready(req_id: str, json_output: bool = typer.Option(False, "--json", help="Print readiness JSON.")) -> None:
    """Run Definition of Ready checks."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="requirements ready", task_type="requirements_readiness", inputs={"req_id": req_id})
    try:
        store = RequirementsStore(repo_root)
        prd = store.load_prd(req_id)
        try:
            issues = store.load_issues(req_id)
        except FileNotFoundError:
            issues = None
        check = check_readiness(prd, issues)
        path = store.save_readiness(check)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"req_id": req_id, "readiness_status": check.status, "ready": check.ready, "readiness_path": str(path)})
    trace.warnings.extend(check.warnings)
    trace.artifacts.append(TraceArtifact(path=str(path), kind="requirements_readiness", description="Readiness JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "readiness.md"), kind="requirements_readiness_markdown", description="Readiness markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Readiness written to: {path.parent / 'readiness.md'}")
    typer.echo(f"Status: {check.status}")
    typer.echo(f"Ready: {check.ready}")
    if json_output:
        typer.echo(json.dumps(check.to_dict(), indent=2, sort_keys=True))


@requirements_app.command("list")
def requirements_list(limit: int = typer.Option(20, "--limit", help="Maximum requirements to show.")) -> None:
    """List recent requirements."""
    items = RequirementsStore(Path.cwd()).list_requirements(limit=limit)
    if not items:
        typer.echo("No requirements found.")
        return
    for req_id in items:
        typer.echo(req_id)


@requirements_app.command("latest")
def requirements_latest() -> None:
    """Show latest requirement summary."""
    store = RequirementsStore(Path.cwd())
    req_id = store.latest()
    if not req_id:
        typer.echo("No requirements found.")
        return
    _print_requirement_summary(store, req_id)


@requirements_app.command("show")
def requirements_show(req_id: str) -> None:
    """Show one requirement summary."""
    store = RequirementsStore(Path.cwd())
    try:
        store.load_prd(req_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    _print_requirement_summary(store, req_id)


@requirements_app.command("publish")
def requirements_publish(req_id: str, create_issues: bool = typer.Option(False, "--create-issues", help="Create GitHub issues if implemented."), json_output: bool = typer.Option(False, "--json", help="Print publish JSON.")) -> None:
    """Dry-run publish requirement issue drafts."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="requirements publish", task_type="requirements_publish", inputs={"req_id": req_id, "create_issues": create_issues})
    try:
        result = RequirementsPublisher(repo_root).publish(req_id, create_issues=create_issues)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"req_id": req_id, "publish_requested": create_issues, "issues_created": result.get("created_issues", []), "publish_result": result})
    _success_trace(trace_store, trace)
    typer.echo(result["message"])
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))


@skill_app.command("list")
def skill_list() -> None:
    """List available skills under skills/."""
    skills = SkillLoader(Path.cwd() / "skills").list_skills()
    if not skills:
        typer.echo("No skills found.")
        return
    for skill in skills:
        typer.echo(skill)


@skill_app.command("show")
def skill_show(name: str) -> None:
    """Show metadata and a short body summary for a skill."""
    try:
        skill = SkillLoader(Path.cwd() / "skills").load_skill(name)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    typer.echo(f"Name: {skill.name}")
    typer.echo(f"Description: {skill.description}")
    typer.echo(f"Version: {skill.version}")
    typer.echo(f"Risk level: {skill.risk_level}")
    typer.echo(f"Allowed tools: {', '.join(skill.allowed_tools)}")
    typer.echo(f"Requires approval for: {', '.join(skill.requires_approval_for)}")
    typer.echo("")
    typer.echo("Summary:")
    typer.echo(skill.body.strip().splitlines()[0] if skill.body.strip() else "No body content.")


@skill_app.command("validate")
def skill_validate(path: Path) -> None:
    """Validate one skill by name, directory, or SKILL.md file."""
    requested_path = path
    if not path.exists() and len(path.parts) == 1:
        named_skill = Path.cwd() / "skills" / path
        if named_skill.exists():
            path = named_skill
    trace_store = TraceStore(Path.cwd())
    trace = trace_store.create_run(
        command="skill validate",
        skill=path.parent.name if path.name == "SKILL.md" else path.name,
        task_type="skill_validation",
        inputs={"path": str(path), "requested_path": str(requested_path)},
    )
    result = SkillValidator().validate(path)
    trace.outputs["errors"] = result.errors
    trace.warnings.extend(result.warnings)
    _print_validation_result(result)
    if not result.is_valid:
        trace.errors.extend(result.errors)
        trace.next_actions.append("Fix skill validation errors.")
        trace.finish("failed")
        trace_store.save(trace)
        raise typer.Exit(code=1)
    _success_trace(trace_store, trace)


@skill_app.command("validate-all")
def skill_validate_all() -> None:
    """Validate all skills under skills/."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="skill validate-all", task_type="skill_validation", inputs={})
    skills_root = repo_root / "skills"
    loader = SkillLoader(skills_root)
    validator = SkillValidator()
    failures = 0

    for skill_name in loader.list_skills():
        result = validator.validate(skills_root / skill_name)
        _print_validation_result(result)
        trace.outputs[skill_name] = {"errors": result.errors, "warnings": result.warnings}
        trace.warnings.extend([f"{skill_name}: {warning}" for warning in result.warnings])
        if not result.is_valid:
            failures += 1
            trace.errors.extend([f"{skill_name}: {error}" for error in result.errors])

    if failures:
        trace.next_actions.append("Fix invalid skills.")
        trace.finish("failed")
        trace_store.save(trace)
        raise typer.Exit(code=1)
    _success_trace(trace_store, trace)


@skill_app.command("index")
def skill_index(write: bool = typer.Option(False, "--write", help="Write skills/README.md instead of dry-running.")) -> None:
    """Generate the public skill index."""
    repo_root = Path.cwd()
    index_text = generate_skill_index(repo_root / "skills")
    output_path = repo_root / "skills" / "README.md"
    if write:
        output_path.write_text(index_text, encoding="utf-8")
        typer.echo(f"Skill index written to: {output_path}")
        return
    typer.echo("Dry run: no files written. Use --write to update skills/README.md.")
    typer.echo("")
    typer.echo(index_text)


@skillpack_app.command("list")
def skillpack_list() -> None:
    """List available project skillpacks."""
    for name in SkillpackLoader(Path.cwd()).list_skillpacks():
        typer.echo(name)


@skillpack_app.command("show")
def skillpack_show(name: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Show one skillpack."""
    try:
        skillpack = SkillpackLoader(Path.cwd()).load(name)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(skillpack.to_dict(), indent=2, sort_keys=True) if json_output else render_skillpack_summary(skillpack))


@skillpack_app.command("validate")
def skillpack_validate(name: str, strict: bool = typer.Option(False, "--strict", help="Treat warnings as errors.")) -> None:
    """Validate one skillpack."""
    result = SkillpackValidator(Path.cwd()).validate(name, strict=strict)
    _print_skillpack_validation(result)
    if not result.ok:
        raise typer.Exit(code=1)


@skillpack_app.command("validate-all")
def skillpack_validate_all(strict: bool = typer.Option(False, "--strict", help="Treat warnings as errors.")) -> None:
    """Validate all skillpacks."""
    failed = False
    for result in SkillpackValidator(Path.cwd()).validate_all(strict=strict):
        _print_skillpack_validation(result)
        failed = failed or not result.ok
    if failed:
        raise typer.Exit(code=1)


@skillpack_app.command("activate")
def skillpack_activate(name: str) -> None:
    """Activate a skillpack locally under .karakana/."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="skillpack activate", task_type="skillpack_activation", inputs={"skillpack": name})
    try:
        state = SkillpackActivation(repo_root).activate(name)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update(state)
    _success_trace(trace_store, trace)
    typer.echo(f"Activated skillpack: {state['skillpack']}")
    typer.echo(f"Project: {state['project']}")


@skillpack_app.command("current")
def skillpack_current(json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Show current active skillpack."""
    state = SkillpackActivation(Path.cwd()).current()
    if not state:
        typer.echo("No active skillpack.")
        return
    if json_output:
        typer.echo(json.dumps(state, indent=2, sort_keys=True))
    else:
        typer.echo(f"Skillpack: {state['skillpack']}")
        typer.echo(f"Project: {state['project']}")
        typer.echo(f"Activated at: {state['activated_at']}")


@skillpack_app.command("summary")
def skillpack_summary(name: str) -> None:
    """Print a readable skillpack summary."""
    try:
        typer.echo(render_skillpack_summary(SkillpackLoader(Path.cwd()).load(name)))
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc


@workspace_app.command("list")
def workspace_list() -> None:
    """List available workspaces."""
    for name in WorkspaceLoader(Path.cwd()).list_workspaces():
        typer.echo(name)


@workspace_app.command("show")
def workspace_show(name: str, json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Show one workspace."""
    try:
        workspace = WorkspaceLoader(Path.cwd()).load(name)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(workspace.to_dict(), indent=2, sort_keys=True) if json_output else render_workspace_summary(workspace))


@workspace_app.command("validate")
def workspace_validate(name: str) -> None:
    """Validate one workspace."""
    result = WorkspaceValidator(Path.cwd()).validate(name)
    _print_workspace_validation(result)
    if not result.ok:
        raise typer.Exit(code=1)


@workspace_app.command("validate-all")
def workspace_validate_all() -> None:
    """Validate all workspaces."""
    failed = False
    for result in WorkspaceValidator(Path.cwd()).validate_all():
        _print_workspace_validation(result)
        failed = failed or not result.ok
    if failed:
        raise typer.Exit(code=1)


@workspace_app.command("activate")
def workspace_activate(name: str) -> None:
    """Activate a workspace locally."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="workspace activate", task_type="workspace_activation", inputs={"workspace": name})
    try:
        state = WorkspaceActivation(repo_root).activate(name)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"workspace": name, "workspace_path": str(repo_root / "workspaces" / f"{name}.yml"), "operation": "activate"})
    _success_trace(trace_store, trace)
    typer.echo(f"Activated workspace: {state['workspace']}")
    typer.echo(f"Activated at: {state['activated_at']}")


@workspace_app.command("current")
def workspace_current(json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Show current active workspace."""
    state = WorkspaceActivation(Path.cwd()).current()
    if not state:
        typer.echo("No active workspace.")
        return
    typer.echo(json.dumps(state, indent=2, sort_keys=True) if json_output else f"Workspace: {state['workspace']}\nActivated at: {state['activated_at']}")


@workspace_app.command("status")
def workspace_status_cmd(
    workspace_name: str | None = typer.Option(None, "--workspace", help="Workspace name."),
    project: str | None = typer.Option(None, "--project", help="Project ID."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
) -> None:
    """Collect read-only workspace status."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="workspace status", project=project, task_type="workspace_status", inputs={"workspace": workspace_name, "project": project})
    try:
        workspace = _load_workspace_for_cli(repo_root, workspace_name)
        status = collect_workspace_status(repo_root, workspace, project_id=project)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"workspace": workspace.name, "project": project, "status_collected": True, "project_count": len(status.project_statuses), "warnings": status.warnings, "errors": status.errors})
    trace.warnings.extend(status.warnings)
    trace.errors.extend(status.errors)
    _success_trace(trace_store, trace)
    if json_output:
        typer.echo(json.dumps(status.to_dict(), indent=2, sort_keys=True))
    else:
        typer.echo(render_workspace_summary(workspace, status))


@workspace_app.command("summary")
def workspace_summary_cmd(name: str) -> None:
    """Print workspace summary."""
    repo_root = Path.cwd()
    try:
        workspace = WorkspaceLoader(repo_root).load(name)
        status = collect_workspace_status(repo_root, workspace)
    except Exception as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo(render_workspace_summary(workspace, status))


@workspace_app.command("plan")
def workspace_plan(
    project: str = typer.Option(..., "--project", help="Project ID."),
    task: str = typer.Option(..., "--task", help="Planning task."),
    workspace_name: str | None = typer.Option(None, "--workspace", help="Workspace name."),
    live: bool = typer.Option(False, "--live", help="Reserved: workspace plan remains dry-run in this milestone."),
    provider: str | None = typer.Option(None, "--provider", help="Reserved model override."),
    model: str | None = typer.Option(None, "--model", help="Reserved model override."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
    no_handoff: bool = typer.Option(False, "--no-handoff", help="Skip session handoff autoload/recovery."),
) -> None:
    """Generate a project-specific workspace planning prompt."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="workspace plan", project=project, task=task, task_type="workspace_plan", inputs={"workspace": workspace_name, "project": project, "task": task, "live": live, "provider": provider, "model": model})
    if live:
        trace.warnings.append("Workspace planning does not execute live models in this milestone.")
    try:
        workspace = _load_workspace_for_cli(repo_root, workspace_name)
        project_config = next(item for item in workspace.projects if item.id == project)
        handoff_context = None
        if not no_handoff:
            handoff, handoff_path = _ensure_session_handoff(repo_root, project, project_config.skillpack or project, workspace.name)
            handoff_context = render_session_start(handoff, str(handoff_path))
            trace.outputs["session_handoff"] = str(handoff_path)
        output = build_workspace_plan(repo_root, workspace, project, task, handoff_context=handoff_context)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"workspace": workspace.name, "project": project, "prompt_artifact": str(output), "operation": "plan"})
    trace.artifacts.append(TraceArtifact(path=str(output), kind="workspace_plan", description="Workspace project planning prompt"))
    _success_trace(trace_store, trace)
    typer.echo(f"Workspace plan written to: {output}")
    if json_output:
        typer.echo(json.dumps({"workspace": workspace.name, "project": project, "prompt_artifact": str(output)}, indent=2, sort_keys=True))


@workspace_app.command("handoff")
def workspace_handoff(project: str = typer.Option(..., "--project", help="Project ID."), workspace_name: str | None = typer.Option(None, "--workspace", help="Workspace name."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")) -> None:
    """Generate a project-specific workspace handoff."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="workspace handoff", project=project, task_type="workspace_handoff", inputs={"workspace": workspace_name, "project": project})
    try:
        workspace = _load_workspace_for_cli(repo_root, workspace_name)
        status = collect_workspace_status(repo_root, workspace, project_id=project)
        handoff_id, path = write_workspace_handoff(repo_root, workspace, status, project)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"workspace": workspace.name, "project": project, "handoff_id": handoff_id, "handoff_path": str(path), "operation": "handoff"})
    trace.warnings.extend(status.warnings)
    trace.artifacts.append(TraceArtifact(path=str(path), kind="workspace_handoff", description="Workspace project handoff"))
    _success_trace(trace_store, trace)
    typer.echo(f"Workspace handoff written to: {path}")
    if json_output:
        typer.echo(json.dumps({"workspace": workspace.name, "project": project, "handoff_id": handoff_id, "handoff_path": str(path)}, indent=2, sort_keys=True))


@trace_app.command("list")
def trace_list(limit: int = typer.Option(20, "--limit", help="Maximum runs to show.")) -> None:
    """List recent local run traces."""
    runs = TraceStore(Path.cwd()).list_runs(limit=limit)
    if not runs:
        typer.echo("No traces found.")
        return
    for trace in runs:
        typer.echo(
            f"{trace.run_id}\t{trace.started_at}\t{trace.command}\t{trace.status}\t"
            f"{trace.project or ''}\t{trace.skill or ''}"
        )


@trace_app.command("show")
def trace_show(run_id: str) -> None:
    """Print full trace JSON for a run."""
    import json

    try:
        trace = TraceStore(Path.cwd()).load(run_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(trace.to_dict(), indent=2, sort_keys=True))


@trace_app.command("latest")
def trace_latest() -> None:
    """Print the latest run trace JSON."""
    import json

    trace = TraceStore(Path.cwd()).latest()
    if trace is None:
        typer.echo("No traces found.")
        return
    typer.echo(json.dumps(trace.to_dict(), indent=2, sort_keys=True))


@trace_app.command("summary")
def trace_summary(run_id: str) -> None:
    """Print the markdown summary for a run."""
    store = TraceStore(Path.cwd())
    try:
        trace = store.load(run_id)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    summary_path = store.runs_root / run_id / "summary.md"
    if not summary_path.exists():
        store.write_summary(trace)
    typer.echo(summary_path.read_text(encoding="utf-8"))


def _print_validation_result(result) -> None:
    typer.echo(f"Validating: {result.path}")
    for error in result.errors:
        typer.echo(f"ERROR: {error}")
    for warning in result.warnings:
        typer.echo(f"WARNING: {warning}")
    if result.is_valid:
        typer.echo("OK")


def _event_issue_number() -> int | None:
    issue = load_github_event().get("issue", {})
    return issue.get("number")


def _bounded_github_comment_body(body: str, artifact_path: Path) -> str:
    """Keep explicit GitHub comments within the API safety limit."""
    if len(body) <= MAX_BODY_SIZE:
        return body
    notice = (
        "Karakana generated a full review artifact, but it exceeded the safe GitHub comment size.\n\n"
        f"Full local artifact: `{artifact_path}`\n\n"
        "Preview:\n\n"
    )
    suffix = "\n\n[Comment truncated by Karakana safety gate. Review the uploaded artifact for full context.]\n"
    limit = max(MAX_BODY_SIZE - len(notice) - len(suffix), 0)
    return notice + body[:limit].rstrip() + suffix


def _event_pr_number() -> int | None:
    event = load_github_event()
    pull_request = event.get("pull_request", {})
    return pull_request.get("number")


def _record_github_checks(trace, checks) -> None:
    for check in checks:
        trace.safety_checks.append(
            SafetyCheck(
                name=check.name,
                status="passed" if check.passed else "failed",
                message=check.message,
            )
        )


def _record_model_checks(trace, checks) -> None:
    for check in checks:
        trace.safety_checks.append(
            SafetyCheck(name=check.name, status="passed" if check.passed else "failed", message=check.message)
        )


def _execute_model_to_artifacts(
    repo_root: Path,
    prompt: str,
    provider_name: str,
    model_name: str,
    trace,
    task_type: str | None = None,
    project: str | None = None,
    skill: str | None = None,
    expected: str = "generic",
    strict_review: bool = False,
) -> dict[str, Path | str | bool]:
    artifacts_dir = repo_root / ".karakana" / "runs" / trace.run_id / "artifacts"
    registry = default_registry()
    try:
        provider = registry.get(provider_name)
        provider_known = True
    except ModelProviderError:
        provider_known = False
        provider = None
    checks = validate_model_call(True, bool(provider and provider.is_configured()), provider_known, prompt, model_name, artifacts_dir, repo_root)
    _record_model_checks(trace, checks)
    failures = failed_model_checks(checks)
    if failures:
        raise ModelProviderError("; ".join(check.message for check in failures))
    response = ModelExecutor(repo_root).execute_prompt(
        prompt,
        provider_name,
        model_name,
        live=True,
        task_type=task_type,
        project=project,
        skill=skill,
        output_dir=artifacts_dir,
        expected=expected,
        strict_review=strict_review,
    )
    prompt_path = artifacts_dir / "prompt.md"
    request_path = artifacts_dir / "model-request.json"
    response_path = artifacts_dir / "model-response.md"
    response_json_path = artifacts_dir / "model-response.json"
    review_path = artifacts_dir / "response-review.md"
    review_json_path = artifacts_dir / "response-review.json"
    import json

    review_data = json.loads(review_json_path.read_text(encoding="utf-8"))
    trace.outputs["provider"] = response.provider
    trace.outputs["model"] = response.model
    trace.outputs["live"] = True
    trace.outputs["prompt_artifact"] = str(prompt_path)
    trace.outputs["model_request_artifact"] = str(request_path)
    trace.outputs["model_response_artifact"] = str(response_path)
    trace.outputs["model_response_json_artifact"] = str(response_json_path)
    trace.outputs["response_review_artifact"] = str(review_path)
    trace.outputs["response_review_json_artifact"] = str(review_json_path)
    trace.outputs["response_review_status"] = review_data.get("status")
    trace.outputs["response_blocked"] = review_data.get("blocked")
    if response.usage:
        trace.outputs["token_usage"] = response.usage.__dict__
    trace.artifacts.extend(
        [
            TraceArtifact(path=str(prompt_path), kind="model_prompt", description="Run-scoped prompt artifact"),
            TraceArtifact(path=str(request_path), kind="model_request", description="Redacted model request metadata"),
            TraceArtifact(path=str(response_path), kind="model_response", description="Model response markdown"),
            TraceArtifact(path=str(response_json_path), kind="model_response_json", description="Model response JSON"),
            TraceArtifact(path=str(review_path), kind="model_response_review", description="Model response review markdown"),
            TraceArtifact(path=str(review_json_path), kind="model_response_review_json", description="Model response review JSON"),
        ]
    )
    if review_data.get("blocked"):
        raise ModelProviderError(f"Model response review blocked output: {review_data.get('status')}")
    return {
        "prompt": prompt_path,
        "request": request_path,
        "response": response_path,
        "review": review_path,
        "review_status": str(review_data.get("status")),
        "blocked": bool(review_data.get("blocked")),
    }


def _print_live_artifacts(artifacts: dict[str, Path | str | bool]) -> None:
    typer.echo(f"Prompt: {artifacts['prompt']}")
    typer.echo(f"Response: {artifacts['response']}")
    typer.echo(f"Review: {artifacts['review']}")
    typer.echo(f"Review status: {artifacts['review_status']}")


def _record_route_outputs(trace, route: dict) -> None:
    trace.outputs["selected_provider"] = route.get("provider")
    trace.outputs["selected_model"] = route.get("model")
    trace.outputs["routing_rationale"] = route.get("rationale")
    trace.outputs["manual_override"] = route.get("manual_override", False)
    trace.outputs["route_source"] = route.get("route_source")
    trace.outputs["cost_tier"] = route.get("cost_tier")
    trace.outputs["capability_tier"] = route.get("capability_tier")


def _render_resolved_skillpack_context(context) -> str | None:
    if context is None:
        return None
    skillpack = context.skillpack
    return f"""# Skillpack: {skillpack.name}

Description: {skillpack.description}
Project memory: {context.memory_path or ""}

## Required Skills

{_markdown_bullets(context.required_skills)}

## Optional Skills

{_markdown_bullets(context.optional_skills)}

## Safety

High-risk paths:
{_markdown_bullets(context.high_risk_paths)}

Blocked paths:
{_markdown_bullets(context.blocked_paths)}

Approval requirements:
{_markdown_bullets(skillpack.safety.requires_approval_for)}

## Recommended Tests

{_markdown_bullets(context.test_commands)}

## Conventions

{_markdown_bullets(context.conventions)}
"""


def _resolve_optional_skillpack(repo_root: Path, name: str | None):
    if name:
        return SkillpackResolver(repo_root).resolve_for_project(name)
    return SkillpackResolver(repo_root).resolve_current()


def _save_ingestion_from_sources(
    repo_root: Path,
    command: str,
    source_tuples: list[tuple],
    project: str | None,
    skillpack: str | None,
    *,
    classify: bool,
    json_output: bool,
    extra_inputs: dict | None = None,
) -> None:
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command=command, project=project, task_type="ingestion", inputs={"project": project, "skillpack": skillpack, "classify": classify, **(extra_inputs or {})})
    try:
        skillpack_context = _resolve_optional_skillpack(repo_root, skillpack)
    except Exception:
        skillpack_context = None
    try:
        sources = []
        candidates = []
        warnings = []
        redaction_applied = False
        for source, content, applied, source_warnings in source_tuples:
            sources.append(source)
            redaction_applied = redaction_applied or applied
            warnings.extend(source_warnings)
            if classify:
                candidates.extend(generate_candidates(source, content, project=project, skillpack_context=skillpack_context))
        bundle = create_bundle(project, skillpack_context.skillpack.name if skillpack_context else skillpack, sources, candidates, redaction_applied, warnings)
        path = IngestionStore(repo_root).save(bundle)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        raise
    trace.outputs.update(
        {
            "ingest_id": bundle.ingest_id,
            "project": project,
            "skillpack": bundle.skillpack,
            "source_types": [source.source_type for source in bundle.sources],
            "source_paths": [source.path for source in bundle.sources],
            "candidate_count": len(bundle.candidates),
            "candidate_types": [candidate.candidate_type for candidate in bundle.candidates],
            "redaction_applied": bundle.redaction_applied,
            "risk_levels": [candidate.risk_level for candidate in bundle.candidates],
            "candidates_path": str(path),
            "candidates_markdown": str(path.parent / "candidates.md"),
        }
    )
    trace.warnings.extend(bundle.warnings)
    trace.artifacts.append(TraceArtifact(path=str(path), kind="ingestion_candidates", description="Ingestion candidates JSON"))
    trace.artifacts.append(TraceArtifact(path=str(path.parent / "candidates.md"), kind="ingestion_candidates_markdown", description="Ingestion candidates markdown"))
    _success_trace(trace_store, trace)
    typer.echo(f"Ingestion bundle written to: {path.parent}")
    typer.echo(f"Ingest ID: {bundle.ingest_id}")
    typer.echo(f"Sources: {len(bundle.sources)}")
    typer.echo(f"Candidates: {len(bundle.candidates)}")
    if bundle.redaction_applied:
        typer.echo("Redaction applied: true")
    if json_output:
        typer.echo(json.dumps(bundle.to_dict(), indent=2, sort_keys=True))


def _load_requirement_source(
    repo_root: Path,
    from_action: str | None,
    from_ingest: str | None,
    from_patch_review: str | None,
    from_proposal: str | None,
    from_file: Path | None,
    from_note: str | None,
    project: str | None,
    skillpack: str | None,
):
    selected = [
        bool(from_action),
        bool(from_ingest),
        bool(from_patch_review),
        bool(from_proposal),
        bool(from_file),
        bool(from_note),
    ]
    if sum(selected) != 1:
        raise ValueError("Provide exactly one requirements source.")
    if from_action:
        return load_action_requirement_source(repo_root, from_action, project=project, skillpack=skillpack)
    if from_ingest:
        return load_ingest_requirement_source(repo_root, from_ingest, project=project, skillpack=skillpack)
    if from_patch_review:
        return load_patch_review_requirement_source(repo_root, from_patch_review, project=project, skillpack=skillpack)
    if from_proposal:
        return load_proposal_requirement_source(repo_root, from_proposal, project=project, skillpack=skillpack)
    if from_file:
        return load_file_requirement_source(repo_root, from_file, project=project, skillpack=skillpack)
    return load_note_requirement_source(str(from_note), project=project, skillpack=skillpack)


def _print_requirement_summary(store: RequirementsStore, req_id: str) -> None:
    req_dir = store.req_dir(req_id)
    paths = {
        "PRD": str(req_dir / "prd.md"),
        "Stories": str(req_dir / "stories.md") if (req_dir / "stories.md").exists() else "not generated",
        "Issues": str(req_dir / "issues.md") if (req_dir / "issues.md").exists() else "not generated",
        "Readiness": str(req_dir / "readiness.md") if (req_dir / "readiness.md").exists() else "not generated",
    }
    typer.echo(render_requirement_summary(req_id, paths))


def _print_skillpack_validation(result) -> None:
    typer.echo(f"Validating skillpack: {result.name}")
    for error in result.errors:
        typer.echo(f"ERROR: {error}")
    for warning in result.warnings:
        typer.echo(f"WARNING: {warning}")
    if result.ok:
        typer.echo("OK")


def _load_workspace_for_cli(repo_root: Path, name: str | None):
    if name:
        return WorkspaceLoader(repo_root).load(name)
    current = WorkspaceActivation(repo_root).current()
    if current:
        return WorkspaceLoader(repo_root).load(current["workspace"])
    return WorkspaceLoader(repo_root).load("default")


def _print_workspace_validation(result) -> None:
    typer.echo(f"Validating workspace: {result.name}")
    for error in result.errors:
        typer.echo(f"ERROR: {error}")
    for warning in result.warnings:
        typer.echo(f"WARNING: {warning}")
    if result.ok:
        typer.echo("OK")


def _max_risk(proposal) -> str:
    order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    risk = "low"
    for change in proposal.changes:
        if order.get(change.risk_level, 0) > order[risk]:
            risk = change.risk_level
    return risk


def _current_branch(repo_root: Path) -> str | None:
    result = subprocess.run(["git", "branch", "--show-current"], cwd=repo_root, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _has_no_local_changes(repo_root: Path) -> bool:
    result = subprocess.run(["git", "status", "--short"], cwd=repo_root, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return True
    return not bool(result.stdout.strip())


def _create_branch(repo_root: Path, branch: str) -> None:
    subprocess.run(["git", "switch", "-c", branch], cwd=repo_root, check=True, capture_output=True, text=True)


def _safe_apply_path(repo_root: Path, target_path: str) -> Path:
    target = Path(target_path)
    if target.is_absolute() or ".." in target.parts:
        raise ValueError(f"Refusing unsafe path: {target_path}")
    if target.name == ".env" or target.name.startswith(".env."):
        raise ValueError(f"Refusing to modify env file: {target_path}")
    blocked_roots = {".github", "karakana"}
    if target.parts and target.parts[0] in blocked_roots:
        raise ValueError(f"Refusing to modify blocked path: {target_path}")
    blocked_files = {"pyproject.toml"}
    if str(target) in blocked_files:
        raise ValueError(f"Refusing to modify blocked file: {target_path}")
    allowed_roots = {"ubongo", "skills", "prompts", "evals", "docs"}
    if not target.parts or target.parts[0] not in allowed_roots:
        raise ValueError(f"Path is not in an allowed proposal apply root: {target_path}")
    resolved = (repo_root / target).resolve()
    if not resolved.is_relative_to(repo_root.resolve()):
        raise ValueError(f"Refusing path outside repository: {target_path}")
    return resolved


def _success_trace(trace_store: TraceStore, trace) -> None:
    if trace.project and not trace.command.startswith("handoff "):
        trace.next_actions.append(
            f"Before ending the task, run `karakana handoff refresh --project {trace.project} --purpose \"End of task handoff\"`."
        )
    trace.finish("success")
    trace_store.save(trace)


def _ensure_session_handoff(repo_root: Path, project: str, skillpack: str, workspace: str | None = None):
    store = HandoffStore(repo_root)
    handoff = store.latest(project, skillpack)
    if handoff is None:
        handoff = create_handoff(
            repo_root,
            project,
            skillpack,
            workspace,
            purpose="Recovered session entry handoff",
            recovered=True,
        )
        store.save(handoff)
    return handoff, store.run_dir(handoff.handoff_id) / "handoff.md"


def _start_agent_cli(
    *,
    binary: str,
    display_name: str,
    project: str,
    skillpack: str | None,
    workspace: str | None,
    forwarded_args: list[str],
    no_create: bool,
    no_pause: bool,
    bootstrap_venv: bool,
    inject_codex_prompt: bool,
    print_only: bool,
) -> None:
    repo_root = Path.cwd()
    skillpack_name = skillpack or project
    store = HandoffStore(repo_root)
    handoff = store.latest(project, skillpack_name)
    if handoff is None:
        if no_create:
            typer.echo(f"No handoff found for project: {project}")
            raise typer.Exit(code=1)
        handoff = create_handoff(
            repo_root,
            project,
            skillpack_name,
            workspace,
            purpose="Recovered session entry handoff",
            recovered=True,
        )
        store.save(handoff)
    handoff_path = store.run_dir(handoff.handoff_id) / "handoff.md"
    session_start = render_session_start(handoff, str(handoff_path))
    session_start_path = repo_root / ".karakana" / "session-start.md"
    session_start_path.parent.mkdir(parents=True, exist_ok=True)
    session_start_path.write_text(session_start, encoding="utf-8")
    initial_prompt_path = repo_root / ".karakana" / "codex-initial-prompt.md"

    launch_args = list(forwarded_args)
    if binary == "codex" and inject_codex_prompt and _codex_accepts_initial_prompt(launch_args):
        initial_prompt = _render_codex_initial_prompt(session_start, session_start_path)
        initial_prompt_path.write_text(initial_prompt, encoding="utf-8")
        launch_args.append(initial_prompt)
    elif binary == "codex" and initial_prompt_path.exists():
        initial_prompt_path.unlink()

    typer.echo(session_start)
    typer.echo(f"Session start written to: {session_start_path}")
    if binary == "codex" and initial_prompt_path.exists():
        typer.echo(f"Codex initial prompt written to: {initial_prompt_path}")
    display_command = [binary, *_display_launch_args(binary, launch_args)]
    typer.echo(f"{'Would launch' if print_only else 'Launching'} {display_name}: {_quote_command(display_command)}")
    _flush_terminal_output()
    if print_only:
        return

    if bootstrap_venv:
        _ensure_project_venv(repo_root)
        _flush_terminal_output()

    executable = shutil.which(binary)
    if not executable:
        typer.echo(f"{display_name} CLI was not found on PATH: {binary}")
        _flush_terminal_output()
        raise typer.Exit(code=127)
    if not no_pause and sys.stdin.isatty() and sys.stdout.isatty():
        _flush_terminal_output()
        input(f"Press Enter to launch {display_name}...")
    _flush_terminal_output()
    os.execvp(executable, [executable, *launch_args])


_CODEX_OPTIONS_WITH_VALUES = {
    "-c",
    "--config",
    "--remote",
    "--remote-auth-token-env",
    "-i",
    "--image",
    "-m",
    "--model",
    "-p",
    "--profile",
    "-s",
    "--sandbox",
    "-C",
    "--cd",
    "--add-dir",
    "-a",
    "--ask-for-approval",
    "--enable",
    "--disable",
}


def _codex_accepts_initial_prompt(args: list[str]) -> bool:
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--":
            return index == len(args) - 1
        if arg.startswith("--") and "=" in arg:
            index += 1
            continue
        if arg in _CODEX_OPTIONS_WITH_VALUES:
            index += 2
            continue
        if arg.startswith("-"):
            index += 1
            continue
        return False
    return True


def _render_codex_initial_prompt(session_start: str, session_start_path: Path) -> str:
    return (
        "Karakana session-start context was loaded before the first user task.\n\n"
        f"Durable copy: `{session_start_path}`\n\n"
        "Use this as startup context, then wait for the user's task. Do not modify files, run commands, "
        "push, deploy, or continue the milestone until the user asks.\n\n"
        f"{session_start.rstrip()}\n"
    )


def _display_launch_args(binary: str, args: list[str]) -> list[str]:
    if binary != "codex" or not args:
        return args
    if _looks_like_karakana_initial_prompt(args[-1]):
        return [*args[:-1], "<karakana-session-start-prompt>"]
    return args


def _looks_like_karakana_initial_prompt(value: str) -> bool:
    return value.startswith("Karakana session-start context was loaded before the first user task.")


def _ensure_project_venv(repo_root: Path) -> bool:
    venv_dir = repo_root / ".venv"
    venv_python = _venv_python(venv_dir)
    if venv_python.exists():
        return False

    typer.echo("Project .venv was not found; creating it and installing Karakana.")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], cwd=repo_root, check=True)
    subprocess.run([str(venv_python), "-m", "pip", "install", "-e", ".[dev]"], cwd=repo_root, check=True)
    typer.echo("Project .venv is ready.")
    return True


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _quote_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def _flush_terminal_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        flush = getattr(stream, "flush", None)
        if callable(flush):
            flush()


def _fail_trace(trace_store: TraceStore, trace, exc: Exception) -> None:
    trace.errors.append(str(exc))
    trace.next_actions.append("Inspect command inputs and required local files.")
    trace.finish("failed")
    trace_store.save(trace)
