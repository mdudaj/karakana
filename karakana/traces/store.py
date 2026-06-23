"""JSON storage for Karakana run traces."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.traces.schemas import RunTrace, SafetyCheck, now_utc
from karakana.traces.summary import render_summary


class TraceStore:
    """Store run traces under `.karakana/runs/`."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.runs_root = repo_root / ".karakana" / "runs"

    def create_run(
        self,
        command: str,
        project: str | None = None,
        skill: str | None = None,
        task: str | None = None,
        task_type: str | None = None,
        selected_model: str | None = None,
        protocol_id: str | None = None,
        work_category: str | None = None,
        risk_level: str | None = None,
        required_artifacts: list[str] | None = None,
        inputs: dict | None = None,
    ) -> RunTrace:
        if task and not protocol_id:
            try:
                from karakana.protocols.classifier import ProtocolClassifier

                classification = ProtocolClassifier(self.repo_root).classify(task, project=project)
                protocol_id = classification.protocol_id
                work_category = classification.work_category
                risk_level = classification.risk_level
                required_artifacts = classification.required_artifacts
            except Exception:
                pass
        return RunTrace(
            run_id=generate_run_id(),
            command=command,
            project=project,
            skill=skill,
            task=task,
            task_type=task_type,
            selected_model=selected_model,
            protocol_id=protocol_id,
            work_category=work_category,
            risk_level=risk_level,
            required_artifacts=required_artifacts or [],
            status="started",
            started_at=now_utc(),
            inputs=inputs or {},
            safety_checks=[
                SafetyCheck("local-only", "passed", "Trace recorded locally under .karakana/."),
                SafetyCheck("secret-redaction", "passed", "Secret-like input keys are redacted."),
            ],
        )

    def save(self, trace: RunTrace) -> Path:
        run_dir = self._run_dir(trace.run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "artifacts").mkdir(exist_ok=True)
        trace_path = run_dir / "trace.json"
        trace_path.write_text(json.dumps(trace.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.write_summary(trace)
        self._write_latest(trace.run_id)
        return trace_path

    def load(self, run_id: str) -> RunTrace:
        trace_path = self._run_dir(run_id) / "trace.json"
        if not trace_path.exists():
            raise FileNotFoundError(f"Trace not found: {run_id}")
        return RunTrace.from_dict(json.loads(trace_path.read_text(encoding="utf-8")))

    def list_runs(self, limit: int = 20) -> list[RunTrace]:
        if not self.runs_root.exists():
            return []
        traces: list[RunTrace] = []
        for path in self.runs_root.iterdir():
            if not path.is_dir():
                continue
            trace_path = path / "trace.json"
            if trace_path.exists():
                traces.append(RunTrace.from_dict(json.loads(trace_path.read_text(encoding="utf-8"))))
        return sorted(traces, key=lambda trace: trace.started_at, reverse=True)[:limit]

    def latest(self) -> RunTrace | None:
        latest_file = self.runs_root / "latest"
        if latest_file.exists():
            run_id = latest_file.read_text(encoding="utf-8").strip()
            if run_id:
                try:
                    return self.load(run_id)
                except FileNotFoundError:
                    pass
        runs = self.list_runs(limit=1)
        return runs[0] if runs else None

    def write_summary(self, trace: RunTrace) -> Path:
        summary_path = self._run_dir(trace.run_id) / "summary.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(render_summary(trace), encoding="utf-8")
        return summary_path

    def _run_dir(self, run_id: str) -> Path:
        return self.runs_root / run_id

    def _write_latest(self, run_id: str) -> None:
        self.runs_root.mkdir(parents=True, exist_ok=True)
        (self.runs_root / "latest").write_text(run_id + "\n", encoding="utf-8")


def generate_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{secrets.token_hex(3)}"
