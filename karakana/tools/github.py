"""Non-network GitHub Actions context and prompt generation."""

from __future__ import annotations

import json
import os
from pathlib import Path

from karakana.memory.ubongo import UbongoMemory
from karakana.skills.loader import SkillLoader
from karakana.tools.code_search import collect_repository_context

GITHUB_ENV_KEYS = [
    "GITHUB_EVENT_NAME",
    "GITHUB_EVENT_PATH",
    "GITHUB_REPOSITORY",
    "GITHUB_REF_NAME",
    "GITHUB_SHA",
    "GITHUB_ACTOR",
    "GITHUB_WORKFLOW",
    "GITHUB_RUN_ID",
]


def detect_github_context() -> dict:
    """Return known GitHub Actions environment values without network access."""
    return {key: os.environ.get(key) for key in GITHUB_ENV_KEYS if os.environ.get(key)}


def get_event_path() -> Path | None:
    value = os.environ.get("GITHUB_EVENT_PATH")
    return Path(value) if value else None


def load_github_event() -> dict:
    path = get_event_path()
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"GITHUB_EVENT_PATH does not exist: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def get_repository() -> str | None:
    return os.environ.get("GITHUB_REPOSITORY")


def get_ref_name() -> str | None:
    return os.environ.get("GITHUB_REF_NAME")


def get_sha() -> str | None:
    return os.environ.get("GITHUB_SHA")


def get_actor() -> str | None:
    return os.environ.get("GITHUB_ACTOR")


class GitHubPromptGenerator:
    """Generate safe GitHub-related prompts from local event context."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def build_issue_triage_prompt(self, project: str, skill: str) -> str:
        event = load_github_event()
        issue = event.get("issue", {})
        context = {
            "event": detect_github_context(),
            "issue": {
                "title": issue.get("title"),
                "body": issue.get("body"),
                "labels": [label.get("name") for label in issue.get("labels", []) if isinstance(label, dict)],
                "author": (issue.get("user") or {}).get("login"),
                "url": issue.get("html_url"),
            },
        }
        return self._render_prompt(
            template_name="issue_triage.prompt.md",
            task_type="issue_triage",
            github_context=_to_json(context),
            project=project,
            skill=skill,
            repository_context=collect_repository_context(self.repo_root),
            required_output="- issue summary\n- likely project\n- suggested labels\n- suggested skill\n- next steps",
        )

    def build_pr_review_prompt(self, project: str, skill: str) -> str:
        event = load_github_event()
        pull_request = event.get("pull_request", {})
        context = {
            "event": detect_github_context(),
            "pull_request": {
                "number": pull_request.get("number"),
                "title": pull_request.get("title"),
                "body": pull_request.get("body"),
                "author": (pull_request.get("user") or {}).get("login"),
                "base": (pull_request.get("base") or {}).get("ref"),
                "head": (pull_request.get("head") or {}).get("ref"),
                "url": pull_request.get("html_url"),
            },
        }
        base_ref = context["pull_request"]["base"]
        diff = _safe_git_diff(self.repo_root, base_ref)
        repository_context = collect_repository_context(self.repo_root)
        if diff:
            repository_context += "\nPotential PR diff:\n\n```diff\n" + diff + "\n```\n"
        return self._render_prompt(
            template_name="pr_review.prompt.md",
            task_type="pr_review",
            github_context=_to_json(context),
            project=project,
            skill=skill,
            repository_context=repository_context,
            required_output="- summary\n- blocking issues\n- non-blocking suggestions\n- test gaps\n- security risks\n- deployment risks",
        )

    def build_ci_failure_prompt(self, project: str, skill: str, log_file: Path) -> str:
        if not log_file.exists():
            raise FileNotFoundError(f"CI log file does not exist: {log_file}")
        context = {"event": detect_github_context(), "log_file": str(log_file)}
        reduced_log = reduce_ci_log(log_file.read_text(encoding="utf-8"))
        repository_context = collect_repository_context(self.repo_root)
        repository_context += "\nReduced CI log:\n\n```text\n" + reduced_log + "\n```\n"
        return self._render_prompt(
            template_name="ci_failure_analysis.prompt.md",
            task_type="ci_failure_analysis",
            github_context=_to_json(context),
            project=project,
            skill=skill,
            repository_context=repository_context,
            required_output="- failure class\n- likely root cause\n- affected files\n- suggested patch\n- rerun guidance",
        )

    def write_prompt(self, prompt: str, output_path: Path) -> Path:
        path = output_path if output_path.is_absolute() else self.repo_root / output_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")
        return path

    def _render_prompt(
        self,
        template_name: str,
        task_type: str,
        github_context: str,
        project: str,
        skill: str,
        repository_context: str,
        required_output: str,
    ) -> str:
        selected_skill = SkillLoader(self.repo_root / "skills").load_skill(skill)
        memory = UbongoMemory(self.repo_root)
        missing_memory = memory.validate_project(project)
        if missing_memory:
            missing = ", ".join(missing_memory)
            raise FileNotFoundError(f"Project '{project}' is missing required memory files: {missing}")
        template = _read_template(self.repo_root / "prompts" / template_name)
        return template.format(
            task_type=task_type,
            github_context=github_context,
            project=project,
            selected_skill=_render_skill(selected_skill),
            memory=memory.summarize_project_context(project),
            repository_context=repository_context,
            required_output=required_output,
            safety_rules=_safety_rules(),
        ).strip() + "\n"


def reduce_ci_log(log: str, max_lines: int = 80) -> str:
    """Keep likely-failure lines and nearby context without external services."""
    lines = log.splitlines()
    keywords = ("error", "failed", "failure", "traceback", "exception", "fatal")
    selected: list[str] = []
    for index, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in keywords):
            start = max(index - 2, 0)
            end = min(index + 3, len(lines))
            selected.extend(lines[start:end])
            selected.append("---")
    if not selected:
        selected = lines[-max_lines:]
    deduped = []
    for line in selected:
        if len(deduped) >= max_lines:
            break
        if not deduped or deduped[-1] != line:
            deduped.append(line)
    return "\n".join(deduped)


def _render_skill(skill) -> str:
    return f"""Name: {skill.name}
Description: {skill.description}
Version: {skill.version}
Risk level: {skill.risk_level}

{skill.body.strip()}"""


def _safety_rules() -> str:
    return """- Do not post GitHub comments automatically.
- Do not create issues or pull requests.
- Do not push commits.
- Do not deploy.
- Do not read or print secrets.
- Do not call external model APIs.
- Generate reviewable artifacts only under `.karakana/`."""


def _read_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Prompt template does not exist: {path}")
    return path.read_text(encoding="utf-8")


def _safe_git_diff(repo_root: Path, base_ref: str | None) -> str:
    if not base_ref:
        return ""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "diff", f"origin/{base_ref}...HEAD"],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _to_json(value: dict) -> str:
    return json.dumps(value, indent=2, sort_keys=True)
