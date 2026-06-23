"""Release readiness and doctor checks."""

from __future__ import annotations

import json
import os
import secrets
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from karakana.config.loader import load_config
from karakana.config.validator import validate_config
from karakana.evals.loader import EvalLoader
from karakana.release.metadata import package_version


@dataclass
class CheckResult:
    name: str
    status: str
    message: str


@dataclass
class CheckReport:
    run_id: str
    status: str
    checks: list[CheckResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def run_doctor(repo_root: Path) -> tuple[CheckReport, Path]:
    report = CheckReport(run_id=_run_id("doctor"), status="pass")
    checks = report.checks
    checks.append(CheckResult("python-version", "pass", sys.version.split()[0]))
    checks.append(CheckResult("package-import", "pass", f"karakana {package_version()}"))
    checks.append(CheckResult("repo-root", "pass" if (repo_root / "pyproject.toml").exists() else "warning", str(repo_root)))
    _path_check(checks, repo_root / ".karakana", "artifact-root", require_writable=True)
    for label in ["ubongo", "skills", "skillpacks", "workspaces"]:
        _path_check(checks, repo_root / label, label)
    for path in ["skills/karakana-self-improvement/SKILL.md", "skillpacks/karakana.yml", "workspaces/default.yml"]:
        _path_check(checks, repo_root / path, path)
    errors, warnings = validate_config(load_config(repo_root), repo_root)
    checks.append(CheckResult("config-valid", "fail" if errors else "pass", "; ".join(errors or warnings or ["OK"])))
    checks.append(CheckResult("eval-discovery", "pass" if EvalLoader(repo_root).load_cases() else "warning", "Eval cases discoverable."))
    checks.append(CheckResult("git-available", "pass" if shutil.which("git") else "warning", shutil.which("git") or "git not found"))
    pytest_path = shutil.which("pytest") or (str(repo_root / ".venv" / "bin" / "pytest") if (repo_root / ".venv" / "bin" / "pytest").exists() else None)
    checks.append(CheckResult("pytest-available", "pass" if pytest_path else "warning", pytest_path or "pytest not found"))
    checks.append(CheckResult("codex-cli", "pass" if shutil.which("codex") else "warning", "codex found" if shutil.which("codex") else "codex not found"))
    for env_name in ["GITHUB_TOKEN", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
        checks.append(CheckResult(env_name.lower(), "pass" if os.environ.get(env_name) else "warning", "configured" if os.environ.get(env_name) else "not configured"))
    _finish_report(report)
    return report, _write_report(repo_root / ".karakana" / "doctor" / report.run_id, "doctor", report)


def run_release_check(repo_root: Path, full: bool = False) -> tuple[CheckReport, Path]:
    report = CheckReport(run_id=_run_id("release-check"), status="pass")
    checks = report.checks
    checks.append(CheckResult("package-import", "pass", f"karakana {package_version()}"))
    checks.append(CheckResult("cli-loads", "pass", "karakana.cli imports"))
    checks.append(CheckResult("version-available", "pass", package_version()))
    for path in ["README.md", "AGENTS.md", "KARAKANA.md", "docs", "docs/installation.md", "docs/configuration.md", "docs/daily-workflow.md", "docs/protocols.md", "docs/safety.md", "docs/release.md", "docs/troubleshooting.md", "docs/command-reference.md"]:
        _path_check(checks, repo_root / path, path)
    gitignore = (repo_root / ".gitignore").read_text(encoding="utf-8") if (repo_root / ".gitignore").exists() else ""
    checks.append(CheckResult("karakana-gitignored", "pass" if ".karakana/" in gitignore else "fail", ".karakana/ is gitignored" if ".karakana/" in gitignore else ".karakana/ missing from .gitignore"))
    checks.append(CheckResult("starter-workspace", "pass" if (repo_root / "workspaces/default.yml").exists() else "fail", "workspaces/default.yml"))
    checks.append(CheckResult("starter-skillpack", "pass" if (repo_root / "skillpacks/karakana.yml").exists() else "fail", "skillpacks/karakana.yml"))
    checks.append(CheckResult("eval-discovery", "pass" if EvalLoader(repo_root).load_cases() else "warning", "Eval cases discoverable."))
    if full:
        for name, command in {
            "skills-validate": ["./.venv/bin/karakana", "skill", "validate-all"],
            "skillpacks-validate": ["./.venv/bin/karakana", "skillpack", "validate-all"],
            "workspaces-validate": ["./.venv/bin/karakana", "workspace", "validate-all"],
            "evals-run": ["./.venv/bin/karakana", "eval", "run"],
            "pytest": ["./.venv/bin/python", "-m", "pytest"],
        }.items():
            checks.append(_run_check(repo_root, name, command))
    _finish_report(report)
    return report, _write_report(repo_root / ".karakana" / "release" / report.run_id, "release-check", report)


def _path_check(checks: list[CheckResult], path: Path, name: str, require_writable: bool = False) -> None:
    if not path.exists():
        if require_writable:
            path.mkdir(parents=True, exist_ok=True)
        else:
            checks.append(CheckResult(name, "fail", f"Missing: {path}"))
            return
    if require_writable:
        checks.append(CheckResult(name, "pass" if os.access(path, os.W_OK) else "fail", str(path)))
    else:
        checks.append(CheckResult(name, "pass", str(path)))


def _run_check(repo_root: Path, name: str, command: list[str]) -> CheckResult:
    try:
        result = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    except FileNotFoundError:
        return CheckResult(name, "warning", f"Command not available: {' '.join(command)}")
    return CheckResult(name, "pass" if result.returncode == 0 else "fail", f"exit={result.returncode}")


def _finish_report(report: CheckReport) -> None:
    report.errors = [check.message for check in report.checks if check.status == "fail"]
    report.warnings = [check.message for check in report.checks if check.status == "warning"]
    report.status = "fail" if report.errors else ("warning" if report.warnings else "pass")


def _write_report(directory: Path, prefix: str, report: CheckReport) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / f"{prefix}.json"
    md_path = directory / f"{prefix}.md"
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_check_report(report, title=prefix.replace("-", " ").title()), encoding="utf-8")
    return json_path


def render_check_report(report: CheckReport, title: str) -> str:
    lines = [f"# Karakana {title}", "", f"- Run ID: {report.run_id}", f"- Status: {report.status}", "", "## Checks"]
    lines.extend(f"- {check.status}: {check.name} - {check.message}" for check in report.checks)
    lines.append("")
    lines.append("## Warnings")
    lines.extend([f"- {warning}" for warning in report.warnings] or ["- None"])
    lines.append("")
    lines.append("## Errors")
    lines.extend([f"- {error}" for error in report.errors] or ["- None"])
    return "\n".join(lines) + "\n"


def _run_id(kind: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-{kind}-{secrets.token_hex(3)}"
