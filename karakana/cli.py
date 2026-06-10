"""Command line interface for the Karakana skeleton."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

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
from karakana.evals.loader import EvalLoader
from karakana.evals.report import EvalReportStore
from karakana.evals.runner import EvalRunner
from karakana.improvement.proposer import ImprovementProposer
from karakana.improvement.store import ProposalStore
from karakana.memory.ubongo import UbongoMemory
from karakana.models.config import redacted_model_config
from karakana.models.errors import ModelProviderError
from karakana.models.escalation import recommend_escalation
from karakana.models.executor import ModelExecutor
from karakana.models.registry import default_registry
from karakana.models.review.report import render_review_markdown, write_review_artifacts
from karakana.models.review.reviewer import review_response
from karakana.models.router import available_task_types, route_model
from karakana.patch.apply import apply_patch_run
from karakana.patch.branch import create_patch_branch, plan_patch_branch
from karakana.patch.commit import commit_patch_run
from karakana.patch.gates import attach_test_evidence, render_gate_markdown, run_patch_gate
from karakana.patch.status import write_patch_status
from karakana.patch.summary import summarize_patch_lifecycle
from karakana.safety.model_calls import failed_model_checks, validate_model_call
from karakana.safety.model_routing import validate_model_route
from karakana.router import select_model
from karakana.skills.index import generate_skill_index
from karakana.skills.loader import SkillLoader
from karakana.skills.validator import SkillValidator
from karakana.safety.github_writes import MAX_BODY_SIZE, failed_checks, validate_comment_write, validate_issue_create, validate_pr_create
from karakana.tools.codex_executor import CodexExecutor
from karakana.tools.github import GitHubPromptGenerator, load_github_event
from karakana.tools.github_api import GitHubApiClient
from karakana.traces.schemas import SafetyCheck, TraceArtifact
from karakana.traces.store import TraceStore

app = typer.Typer(help="Karakana AI agent harness skeleton.")
action_app = typer.Typer(help="Extract and publish reviewable action artifacts.")
codex_app = typer.Typer(help="Generate Codex-ready task prompts.")
eval_app = typer.Typer(help="Run deterministic Karakana evaluations.")
github_app = typer.Typer(help="Generate safe GitHub workflow artifacts.")
improve_app = typer.Typer(help="Generate self-improvement proposals from traces.")
memory_app = typer.Typer(help="Inspect ubongo durable memory.")
model_app = typer.Typer(help="Inspect and invoke model providers.")
patch_app = typer.Typer(help="Gate, apply, and summarize captured patches.")
skill_app = typer.Typer(help="Inspect and validate Karakana skills.")
trace_app = typer.Typer(help="Inspect local Karakana run traces.")

app.add_typer(action_app, name="action")
app.add_typer(codex_app, name="codex")
app.add_typer(eval_app, name="eval")
app.add_typer(github_app, name="github")
app.add_typer(improve_app, name="improve")
app.add_typer(memory_app, name="memory")
app.add_typer(model_app, name="model")
app.add_typer(patch_app, name="patch")
app.add_typer(skill_app, name="skill")
app.add_typer(trace_app, name="trace")


@app.callback()
def main() -> None:
    """Karakana AI agent harness skeleton."""


@app.command()
def version() -> None:
    """Print the installed Karakana version."""
    typer.echo(f"karakana {__version__}")


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
    project: str = typer.Option(..., "--project", "-p", help="Project memory key."),
    skill: str = typer.Option(..., "--skill", "-s", help="Skill name to include."),
    task: str = typer.Option(..., "--task", "-t", help="Planning task text."),
    output: Path = typer.Option(Path(".karakana/planning-task.md"), "--output", help="Prompt output path."),
    live: bool = typer.Option(False, "--live", help="Execute selected model provider."),
    provider: str | None = typer.Option(None, "--provider", help="Override model provider."),
    model: str | None = typer.Option(None, "--model", help="Override model name."),
    strict_review: bool = typer.Option(False, "--strict-review", help="Block live responses missing expected sections."),
) -> None:
    """Compose a model-ready planning prompt without calling a model."""
    repo_root = Path.cwd()
    model_route = route_model("planning", provider=provider, model=model)
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(
        command="plan",
        project=project,
        skill=skill,
        task=task,
        task_type="planning",
        selected_model=model_route["model"],
        inputs={"project": project, "skill": skill, "task": task, "output": str(output), "live": live, "provider": model_route["provider"], "model": model_route["model"]},
    )
    _record_route_outputs(trace, model_route)
    try:
        prompt = compose_planning_prompt(project=project, skill=skill, task=task, repo_root=repo_root)
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


@codex_app.command("handoff")
def codex_handoff(
    action_run_id: str,
    action_id: str | None = typer.Option(None, "--action-id", help="Generate handoff for one action."),
    project: str | None = typer.Option(None, "--project", help="Override project."),
    skill: str | None = typer.Option(None, "--skill", help="Override skill."),
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
        inputs={"action_run_id": action_run_id, "action_id": action_id, "project": project, "skill": skill, "output": str(output) if output else None, "execute": execute},
    )
    try:
        paths = CodexHandoffBuilder(repo_root).build_from_action_bundle(action_run_id, action_id=action_id, project=project, skill=skill, output_dir=output)
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
    include_staged: bool = typer.Option(False, "--include-staged", help="Capture staged diff too."),
    output: Path | None = typer.Option(None, "--output", help="Custom output directory under .karakana/."),
    json_output: bool = typer.Option(False, "--json", help="Print patch JSON."),
) -> None:
    """Capture current git diff without mutating files."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex capture-diff", task_type="patch_capture", inputs={"source_task": source_task, "include_staged": include_staged, "output": str(output) if output else None})
    try:
        artifact = PatchCapture(repo_root).capture_diff(source_task=source_task, include_staged=include_staged, output_dir=output)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": artifact.patch_run_id, "files_changed": artifact.files_changed, "diff_path": artifact.diff_path, "summary_path": artifact.summary_path})
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
def codex_review_patch(diff: Path = typer.Option(..., "--diff", help="Diff file to review.")) -> None:
    """Review a captured patch diff using deterministic checks."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="codex review-patch", task_type="patch_review", inputs={"diff": str(diff)})
    try:
        review_path = PatchReviewer(repo_root).review_diff(diff)
        data = json.loads(review_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_review_id": review_path.parent.name, "review_status": data.get("status"), "review_blocked": data.get("blocked"), "risk_level": data.get("risk_level"), "review_path": str(review_path)})
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


@patch_app.command("gate")
def patch_gate(patch_run: str = typer.Option(..., "--patch-run", help="Patch run ID."), json_output: bool = typer.Option(False, "--json", help="Print gate JSON.")) -> None:
    """Run patch lifecycle gates for a captured patch."""
    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    trace = trace_store.create_run(command="patch gate", task_type="patch_gate", inputs={"patch_run_id": patch_run})
    try:
        result, gate_path = run_patch_gate(repo_root, patch_run)
    except Exception as exc:
        _fail_trace(trace_store, trace, exc)
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    trace.outputs.update({"patch_run_id": patch_run, "gate_run_id": gate_path.parent.name, "risk_level": result.risk_level, "blocked": result.blocked, "gate_path": str(gate_path)})
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
    risk_level: str | None = typer.Option(None, "--risk-level", help="Optional risk level for safety warnings."),
    json_output: bool = typer.Option(False, "--json", help="Print route JSON."),
) -> None:
    """Show the cost-aware route for a task type."""
    import json

    repo_root = Path.cwd()
    trace_store = TraceStore(repo_root)
    signal_list = [signal.strip() for signal in signals.split(",") if signal.strip()]
    route = route_model(task_type, provider=provider, model=model)
    escalation = recommend_escalation(route["provider"], route["model"], signal_list)
    warnings = validate_model_route(task_type, route["provider"], route["model"], risk_level=risk_level)
    trace = trace_store.create_run(
        command="model route",
        task_type="model_routing",
        selected_model=route["model"],
        inputs={"task_type": task_type, "signals": signal_list, "provider": provider, "model": model, "risk_level": risk_level},
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
    """Validate one skill directory or SKILL.md file."""
    trace_store = TraceStore(Path.cwd())
    trace = trace_store.create_run(
        command="skill validate",
        skill=path.parent.name if path.name == "SKILL.md" else path.name,
        task_type="skill_validation",
        inputs={"path": str(path)},
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
    trace.outputs["cost_tier"] = route.get("cost_tier")
    trace.outputs["capability_tier"] = route.get("capability_tier")


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
    trace.finish("success")
    trace_store.save(trace)


def _fail_trace(trace_store: TraceStore, trace, exc: Exception) -> None:
    trace.errors.append(str(exc))
    trace.next_actions.append("Inspect command inputs and required local files.")
    trace.finish("failed")
    trace_store.save(trace)
