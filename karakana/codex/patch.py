"""Capture git diffs and explicit test command results."""

from __future__ import annotations

import json
import secrets
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from karakana.codex.schemas import PatchArtifact
from karakana.safety.codex import validate_test_command
from karakana.tools.code_search import _git_branch
from karakana.traces.schemas import redact_value


class PatchCapture:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def capture_diff(self, source_task: str | None = None, include_staged: bool = False, output_dir: Path | None = None) -> PatchArtifact:
        patch_run_id = generate_patch_run_id()
        root = _safe_output_root(self.repo_root, output_dir, "patches", patch_run_id)
        root.mkdir(parents=True, exist_ok=True)
        branch = _git_branch(self.repo_root)
        status = _run(self.repo_root, ["git", "status", "--short"])
        diff = _run(self.repo_root, ["git", "diff"])
        staged = _run(self.repo_root, ["git", "diff", "--staged"]) if include_staged else ""
        files = _changed_files(status)
        warnings = []
        if not diff.strip() and not staged.strip():
            warnings.append("No working tree changes detected.")
        (root / "changes.diff").write_text(diff, encoding="utf-8")
        (root / "staged.diff").write_text(staged, encoding="utf-8")
        (root / "git-status.txt").write_text(status, encoding="utf-8")
        (root / "files-changed.txt").write_text("\n".join(files) + ("\n" if files else ""), encoding="utf-8")
        artifact = PatchArtifact(
            patch_run_id=patch_run_id,
            source_task_id=source_task,
            created_at=now_utc(),
            git_branch=branch,
            git_status=status,
            diff_path=str(root / "changes.diff"),
            summary_path=str(root / "summary.md"),
            tests_path=None,
            files_changed=files,
            warnings=warnings,
        )
        (root / "patch.json").write_text(json.dumps(artifact.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (root / "summary.md").write_text(render_patch_summary(artifact), encoding="utf-8")
        return artifact

    def capture_tests(self, command: str, output_dir: Path | None = None, timeout: int = 120) -> Path:
        warnings = validate_test_command(command)
        test_run_id = generate_test_run_id()
        root = _safe_output_root(self.repo_root, output_dir, "test-runs", test_run_id)
        root.mkdir(parents=True, exist_ok=True)
        (root / "command.json").write_text(json.dumps({"command": command, "warnings": warnings}, indent=2) + "\n", encoding="utf-8")
        if warnings:
            (root / "stdout.log").write_text("", encoding="utf-8")
            (root / "stderr.log").write_text("\n".join(warnings), encoding="utf-8")
            result = {"test_run_id": test_run_id, "command": command, "exit_code": None, "refused": True, "warnings": warnings}
        else:
            try:
                completed = subprocess.run(shlex.split(command), cwd=self.repo_root, capture_output=True, text=True, check=False, timeout=timeout)
                stdout = completed.stdout
                stderr = completed.stderr
                exit_code = completed.returncode
                run_warnings = []
            except (OSError, subprocess.TimeoutExpired) as exc:
                stdout = ""
                stderr = str(exc)
                exit_code = None
                run_warnings = [f"Test command could not be completed: {exc}"]
            (root / "stdout.log").write_text(redact_value(stdout), encoding="utf-8")
            (root / "stderr.log").write_text(redact_value(stderr), encoding="utf-8")
            result = {"test_run_id": test_run_id, "command": command, "exit_code": exit_code, "refused": False, "warnings": run_warnings}
        (root / "result.json").write_text(json.dumps(redact_value(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (root / "summary.md").write_text(render_test_summary(result), encoding="utf-8")
        return root / "result.json"


def render_patch_summary(artifact: PatchArtifact) -> str:
    return f"""# Karakana Patch Summary

## Summary

- Patch run ID: {artifact.patch_run_id}
- Source task ID: {artifact.source_task_id or ""}
- Git branch: {artifact.git_branch or ""}
- Diff: {artifact.diff_path or ""}
- Files changed: {len(artifact.files_changed)}

## Files Changed

{_bullets(artifact.files_changed)}

## Warnings

{_bullets(artifact.warnings)}
"""


def render_test_summary(result: dict) -> str:
    return f"""# Karakana Test Capture

## Summary

- Test run ID: {result.get("test_run_id")}
- Command: `{result.get("command")}`
- Exit code: {result.get("exit_code")}
- Refused: {result.get("refused")}

## Warnings

{_bullets(result.get("warnings") or [])}
"""


def generate_patch_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-patch-{secrets.token_hex(3)}"


def generate_test_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-test-{secrets.token_hex(3)}"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(repo_root: Path, command: list[str]) -> str:
    try:
        result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True, check=False, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return redact_value(result.stdout)


def _changed_files(status: str) -> list[str]:
    files = []
    for line in status.splitlines():
        if len(line) > 3:
            files.append(line[3:].strip())
    return sorted(set(files))


def _safe_output_root(repo_root: Path, output_dir: Path | None, kind: str, run_id: str) -> Path:
    if output_dir is None:
        return repo_root / ".karakana" / kind / run_id
    path = output_dir if output_dir.is_absolute() else repo_root / output_dir
    resolved = path.resolve()
    root = (repo_root / ".karakana").resolve()
    if not (resolved == root or resolved.is_relative_to(root)):
        raise ValueError("Output must be under .karakana/.")
    return path


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
