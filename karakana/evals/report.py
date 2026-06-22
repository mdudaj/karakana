"""Evaluation report storage and markdown rendering."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.evals.schemas import EvalCase, EvalCaseResult, EvalRunReport


class EvalReportStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.runs_root = repo_root / ".karakana" / "eval-runs"

    def save(self, report: EvalRunReport, cases: list[EvalCase]) -> Path:
        run_dir = self.run_dir(report.eval_run_id)
        cases_dir = run_dir / "cases"
        cases_dir.mkdir(parents=True, exist_ok=True)
        case_by_id = {case.id: case for case in cases}
        for result in report.results:
            case = case_by_id.get(result.case_id)
            (cases_dir / f"{result.case_id}.json").write_text(
                json.dumps({"case": case.to_dict() if case else None, "result": result.to_dict()}, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            (cases_dir / f"{result.case_id}.md").write_text(render_case_markdown(result, case), encoding="utf-8")
            result.artifacts.extend(
                [
                    str((cases_dir / f"{result.case_id}.json").relative_to(self.repo_root)),
                    str((cases_dir / f"{result.case_id}.md").relative_to(self.repo_root)),
                ]
            )
        report_path = run_dir / "report.json"
        report_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (run_dir / "report.md").write_text(render_report_markdown(report, cases), encoding="utf-8")
        self._write_latest(report.eval_run_id)
        return report_path

    def load(self, eval_run_id: str) -> EvalRunReport:
        path = self.run_dir(eval_run_id) / "report.json"
        if not path.exists():
            raise FileNotFoundError(f"Eval report not found: {eval_run_id}")
        return EvalRunReport.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def latest(self) -> EvalRunReport | None:
        latest_path = self.runs_root / "latest"
        if latest_path.exists():
            eval_run_id = latest_path.read_text(encoding="utf-8").strip()
            if eval_run_id:
                try:
                    return self.load(eval_run_id)
                except FileNotFoundError:
                    pass
        reports = self.list_reports(limit=1)
        return reports[0] if reports else None

    def list_reports(self, limit: int = 20) -> list[EvalRunReport]:
        if not self.runs_root.exists():
            return []
        reports: list[EvalRunReport] = []
        for path in self.runs_root.iterdir():
            report_path = path / "report.json"
            if path.is_dir() and report_path.exists():
                reports.append(EvalRunReport.from_dict(json.loads(report_path.read_text(encoding="utf-8"))))
        return sorted(reports, key=lambda report: report.started_at, reverse=True)[:limit]

    def run_dir(self, eval_run_id: str) -> Path:
        return self.runs_root / eval_run_id

    def _write_latest(self, eval_run_id: str) -> None:
        self.runs_root.mkdir(parents=True, exist_ok=True)
        (self.runs_root / "latest").write_text(eval_run_id + "\n", encoding="utf-8")


def generate_eval_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-eval-{secrets.token_hex(3)}"


def render_report_markdown(report: EvalRunReport, cases: list[EvalCase]) -> str:
    case_by_id = {case.id: case for case in cases}
    lines = [
        "# Karakana Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Eval run ID: {report.eval_run_id}",
        f"- Status: {report.status}",
        f"- Started: {report.started_at}",
        f"- Finished: {report.finished_at or ''}",
        f"- Total cases: {report.total_cases}",
        f"- Passed: {report.passed}",
        f"- Failed: {report.failed}",
        f"- Warnings: {report.warnings}",
        "",
        "## Cases",
        "",
    ]
    for result in report.results:
        lines.extend(render_case_section(result, case_by_id.get(result.case_id)))
    return "\n".join(lines).rstrip() + "\n"


def render_case_markdown(result: EvalCaseResult, case: EvalCase | None = None) -> str:
    lines = ["# Karakana Evaluation Case", ""]
    lines.extend(render_case_section(result, case))
    return "\n".join(lines).rstrip() + "\n"


def render_case_section(result: EvalCaseResult, case: EvalCase | None = None) -> list[str]:
    title = f"{result.case_id}: {case.name}" if case else result.case_id
    return [
        f"### {title}",
        "",
        f"- Status: {result.status}",
        f"- Score: {result.score}",
        f"- Suite: {case.suite if case else ''}",
        f"- Risk: {case.risk_level if case else ''}",
        f"- Tags: {', '.join(case.tags) if case else ''}",
        "",
        "#### Passed Checks",
        "",
        *_list_lines(result.passed_checks),
        "",
        "#### Failed Checks",
        "",
        *_list_lines(result.failed_checks),
        "",
        "#### Warnings",
        "",
        *_list_lines(result.warnings),
        "",
        "#### Output Excerpt",
        "",
        result.output_excerpt or "",
        "",
    ]


def _list_lines(values: list[str]) -> list[str]:
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]
