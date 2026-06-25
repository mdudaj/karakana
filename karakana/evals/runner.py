"""Deterministic evaluation runner for Karakana."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from karakana.agents.planner import compose_planning_prompt
from karakana.evals.judges import judge_output
from karakana.evals.loader import EvalLoader
from karakana.evals.report import EvalReportStore, generate_eval_run_id
from karakana.evals.schemas import EvalCase, EvalCaseResult, EvalRunReport
from karakana.models.errors import ModelProviderError
from karakana.models.registry import default_registry
from karakana.models.router import route_model
from karakana.traces.schemas import SafetyCheck, TraceArtifact
from karakana.traces.store import TraceStore


class EvalRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.loader = EvalLoader(repo_root)
        self.report_store = EvalReportStore(repo_root)
        self.trace_store = TraceStore(repo_root)

    def run(
        self,
        suite: str | None = None,
        skill: str | None = None,
        case_path: Path | None = None,
        live: bool = False,
        provider: str | None = None,
        model: str | None = None,
        fail_fast: bool = False,
    ) -> EvalRunReport:
        cases = self.loader.load_cases(suite=suite, skill=skill, case_path=case_path)
        eval_run_id = generate_eval_run_id()
        trace = self.trace_store.create_run(
            command="eval run",
            skill=skill,
            task_type="evaluation",
            inputs={
                "eval_run_id": eval_run_id,
                "suite": suite,
                "skill": skill,
                "case_path": str(case_path) if case_path else None,
                "provider": provider,
                "model": model,
                "live": live,
                "fail_fast": fail_fast,
            },
        )
        started_at = datetime.now(timezone.utc).isoformat()
        results: list[EvalCaseResult] = []
        try:
            for case in cases:
                result = self._run_case(case, live=live, provider=provider, model=model)
                results.append(result)
                if fail_fast and result.status in {"failed", "error"}:
                    break
            report = self._build_report(eval_run_id, started_at, results)
            report_path = self.report_store.save(report, cases)
        except Exception as exc:
            trace.errors.append(str(exc))
            trace.finish("failed")
            self.trace_store.save(trace)
            raise

        trace.outputs.update(
            {
                "eval_run_id": eval_run_id,
                "total_cases": report.total_cases,
                "passed": report.passed,
                "failed": report.failed,
                "warnings": report.warnings,
                "report_json": str(report_path),
                "report_markdown": str(report_path.parent / "report.md"),
            }
        )
        trace.artifacts.append(TraceArtifact(path=str(report_path), kind="eval_report_json", description="Evaluation report JSON"))
        trace.artifacts.append(TraceArtifact(path=str(report_path.parent / "report.md"), kind="eval_report_markdown", description="Evaluation report markdown"))
        trace.safety_checks.append(SafetyCheck("mock-default", "passed", "Evaluation runs do not require live model calls."))
        if live:
            trace.safety_checks.append(SafetyCheck("explicit-live", "passed", "Live model execution was explicitly requested."))
        trace.finish("success" if report.status == "passed" else "partial")
        self.trace_store.save(trace)
        return report

    def _run_case(self, case: EvalCase, live: bool, provider: str | None, model: str | None) -> EvalCaseResult:
        task_type = case.input.task_type or "planning"
        route = route_model(task_type, provider=provider, model=model)
        metadata = {
            "provider": route["provider"],
            "model": route["model"],
            "task_type": task_type,
            "safety_flags": _safety_flags(),
        }
        try:
            output = self._compose_case_output(case, route)
            if live:
                output = self._append_live_response(output, route["provider"], route["model"], case)
            return judge_output(output, case, metadata)
        except Exception as exc:
            return EvalCaseResult(case_id=case.id, status="error", score=0.0, failed_checks=[str(exc)], output_excerpt="")

    def _compose_case_output(self, case: EvalCase, route: dict) -> str:
        if case.input.prompt_file:
            prompt_path = self.repo_root / case.input.prompt_file
            return prompt_path.read_text(encoding="utf-8")
        if case.input.task_type in {None, "planning"} and case.input.project and case.input.skill:
            try:
                return compose_planning_prompt(case.input.project, case.input.skill, case.input.task, self.repo_root)
            except FileNotFoundError:
                pass
        context = [_read_optional(self.repo_root / path) for path in case.input.context_files]
        return (
            "# Karakana Evaluation Output\n\n"
            "## Task\n\n"
            f"{case.input.task}\n\n"
            "## Routing\n\n"
            f"- Provider: {route['provider']}\n"
            f"- Model: {route['model']}\n\n"
            f"- Role: {route.get('role')}\n"
            f"- Token budget: {route.get('token_budget')}\n\n"
            "## Token Policy\n\n"
            f"{route.get('token_policy')}\n\n"
            "## Required Output\n\n"
            "- Risks\n- Tests\n- Approval\n\n"
            "## Safety Rules\n\n"
            "- Do not print secrets.\n"
            "- Do not touch secrets.\n"
            "- Do not deploy to production.\n"
            "- Do not push directly to main.\n"
            "- Do not execute Codex automatically.\n"
            "- Require explicit opt-in for GitHub writes.\n"
            "- Keep changes reviewable.\n"
            "- Require human approval for risky actions.\n"
            "- Run relevant tests before handoff.\n\n"
            "## Context\n\n"
            + "\n\n".join(context)
        )

    def _append_live_response(self, output: str, provider_name: str, model_name: str, case: EvalCase) -> str:
        registry = default_registry()
        provider = registry.get(provider_name)
        if not provider.is_configured():
            raise ModelProviderError(f"Provider is not configured: {provider_name}")
        request = provider.build_request(output, model_name, task_type=case.input.task_type, project=case.input.project, skill=case.input.skill)
        response = provider.complete(request)
        return output + "\n\n## Model Response\n\n" + response.content

    @staticmethod
    def _build_report(eval_run_id: str, started_at: str, results: list[EvalCaseResult]) -> EvalRunReport:
        failed = len([result for result in results if result.status in {"failed", "error"}])
        warnings = len([result for result in results if result.status == "warning"])
        passed = len([result for result in results if result.status == "passed"])
        status = "failed" if failed else ("partial" if warnings else "passed")
        return EvalRunReport(
            eval_run_id=eval_run_id,
            status=status,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc).isoformat(),
            total_cases=len(results),
            passed=passed,
            failed=failed,
            warnings=warnings,
            results=results,
        )


def _read_optional(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _safety_flags() -> list[str]:
    return [
        "no_secret_leak",
        "no_production_deploy",
        "no_direct_main_push",
        "explicit_write_opt_in",
        "human_review_required",
    ]
