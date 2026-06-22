"""Storage and markdown rendering for dogfood runs."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.dogfood.schemas import DogfoodBacklogItem, DogfoodFinding, DogfoodRun
from karakana.traces.schemas import now_utc


class DogfoodStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / ".karakana" / "dogfood"

    def save(self, run: DogfoodRun) -> Path:
        directory = self.run_dir(run.dogfood_id)
        (directory / "command-results").mkdir(parents=True, exist_ok=True)
        (directory / "artifacts").mkdir(parents=True, exist_ok=True)
        path = directory / "dogfood.json"
        path.write_text(json.dumps(run.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (directory / "dogfood.md").write_text(render_dogfood_report(run), encoding="utf-8")
        (directory / "findings.json").write_text(json.dumps([finding.to_dict() for finding in run.findings], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (directory / "findings.md").write_text(render_findings(run.findings), encoding="utf-8")
        (directory / "backlog.json").write_text(json.dumps([item.to_dict() for item in run.backlog], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (directory / "backlog.md").write_text(render_backlog(run.backlog), encoding="utf-8")
        for result in run.command_results:
            (directory / "command-results" / f"{result.command_id}.json").write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self._write_latest(run.dogfood_id)
        return path

    def load(self, dogfood_id: str) -> DogfoodRun:
        path = self.run_dir(dogfood_id) / "dogfood.json"
        if not path.exists():
            raise FileNotFoundError(f"Dogfood run not found: {dogfood_id}")
        return DogfoodRun.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list(self, limit: int = 20) -> list[DogfoodRun]:
        if not self.root.exists():
            return []
        runs = []
        for path in self.root.iterdir():
            data = path / "dogfood.json"
            if data.exists():
                runs.append(DogfoodRun.from_dict(json.loads(data.read_text(encoding="utf-8"))))
        return sorted(runs, key=lambda run: run.created_at, reverse=True)[:limit]

    def latest(self) -> DogfoodRun | None:
        latest = self.root / "latest"
        if latest.exists():
            try:
                return self.load(latest.read_text(encoding="utf-8").strip())
            except FileNotFoundError:
                pass
        runs = self.list(limit=1)
        return runs[0] if runs else None

    def run_dir(self, dogfood_id: str) -> Path:
        return self.root / dogfood_id

    def _write_latest(self, dogfood_id: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "latest").write_text(dogfood_id + "\n", encoding="utf-8")


def new_dogfood_run(project: str, skillpack: str | None, status: str = "draft") -> DogfoodRun:
    return DogfoodRun(
        dogfood_id=generate_dogfood_id(),
        project=project,
        skillpack=skillpack,
        status=status,
        created_at=now_utc(),
        next_actions=[
            "Review dogfood checklist.",
            "Run `karakana dogfood analyze <dogfood-id>`.",
            "Run `karakana dogfood backlog <dogfood-id>`.",
            "Run `karakana dogfood report <dogfood-id>`.",
        ],
    )


def generate_dogfood_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-dogfood-{secrets.token_hex(3)}"


def render_findings(findings: list[DogfoodFinding]) -> str:
    lines = ["# Karakana Dogfood Findings", ""]
    if not findings:
        lines.append("No findings recorded.")
        return "\n".join(lines) + "\n"
    for finding in findings:
        lines.extend(
            [
                f"## {finding.title}",
                "",
                f"- ID: {finding.finding_id}",
                f"- Type: {finding.finding_type}",
                f"- Severity: {finding.severity}",
                f"- Command: {finding.affected_command or 'None'}",
                f"- Target: {finding.suggested_target or 'None'}",
                "",
                finding.summary,
                "",
                "### Recommended Action",
                "",
                finding.recommended_action or "Needs review.",
                "",
                "### Evidence",
                "",
                *[f"- {item}" for item in finding.evidence],
                "",
            ]
        )
    return "\n".join(lines)


def render_backlog(items: list[DogfoodBacklogItem]) -> str:
    lines = ["# Karakana v1 Hardening Backlog", "", "## Summary", "", f"- Items: {len(items)}", "", "## Release Blockers"]
    lines.extend(_items_for_priority(items, "p0"))
    lines.append("")
    lines.append("## P1: Important Before RC")
    lines.extend(_items_for_priority(items, "p1"))
    lines.append("")
    lines.append("## P2: Useful Improvements")
    lines.extend(_items_for_priority(items, "p2"))
    lines.append("")
    lines.append("## P3: Later")
    lines.extend(_items_for_priority(items, "p3"))
    lines.append("")
    lines.append("## Backlog Items")
    for item in items:
        lines.extend(
            [
                f"### {item.title}",
                "",
                f"- Type: {item.item_type}",
                f"- Priority: {item.priority}",
                f"- Risk: {item.risk_level}",
                f"- Suggested skills: {', '.join(item.suggested_skills) or 'None'}",
                f"- Recommended model route: {item.recommended_model_route or 'Needs review'}",
                "",
                "#### Summary",
                "",
                item.summary,
                "",
                "#### Source Findings",
                "",
                *[f"- {finding_id}" for finding_id in item.source_finding_ids],
                "",
                "#### Acceptance Criteria",
                "",
                *[f"- {criterion}" for criterion in item.acceptance_criteria],
                "",
            ]
        )
    return "\n".join(lines)


def render_dogfood_report(run: DogfoodRun) -> str:
    ready_next = "yes" if run.status in {"completed", "completed_with_warnings"} else "no"
    ready_release = "no" if any(item.priority == "p0" for item in run.backlog) or run.errors else "yes"
    lines = [
        "# Karakana Dogfood Report",
        "",
        "## Run",
        "",
        f"- Dogfood ID: {run.dogfood_id}",
        f"- Project: {run.project}",
        f"- Skillpack: {run.skillpack or 'None'}",
        f"- Status: {run.status}",
        f"- Created: {run.created_at}",
        "",
        "## Executive Summary",
        "",
        f"Commands exercised or planned: {len(run.command_results)}. Findings: {len(run.findings)}. Backlog items: {len(run.backlog)}.",
        "",
        "## Commands Exercised",
        "",
    ]
    lines.extend(f"- {result.status}: `{result.command}`" for result in run.command_results)
    sections = {
        "Findings Summary": run.findings,
        "UX Friction": [f for f in run.findings if f.finding_type == "ux_friction"],
        "Broken Workflows": [f for f in run.findings if f.finding_type == "broken_command"],
        "Missing Evals": [f for f in run.findings if f.finding_type == "missing_eval"],
        "Documentation Corrections": [f for f in run.findings if f.finding_type in {"missing_doc", "weak_doc"}],
        "Safety Refinements": [f for f in run.findings if f.finding_type == "safety_gap"],
    }
    for title, findings in sections.items():
        lines.extend(["", f"## {title}", ""])
        lines.extend([f"- {finding.severity}: {finding.title}" for finding in findings] or ["- None"])
    lines.extend(["", "## v1 Hardening Backlog", ""])
    lines.extend([f"- {item.priority}: {item.title}" for item in run.backlog] or ["- None"])
    lines.extend(["", "## Recommended Next Actions", ""])
    lines.extend([f"- {action}" for action in run.next_actions] or ["- Review dogfood output."])
    lines.extend(["", "## Decision", "", f"- Ready for next dogfood milestone: {ready_next}", f"- Ready for release candidate: {ready_release}", ""])
    return "\n".join(lines)


def _items_for_priority(items: list[DogfoodBacklogItem], priority: str) -> list[str]:
    selected = [item for item in items if item.priority == priority]
    return [f"- {item.title}" for item in selected] or ["- None"]
