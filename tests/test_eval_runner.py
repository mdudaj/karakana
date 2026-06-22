from pathlib import Path

from karakana.evals.runner import EvalRunner
from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES


def write_memory_tree(root: Path) -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / "karakana"
    global_root.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal eval context.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject eval context.\n", encoding="utf-8")


def write_skill(root: Path) -> None:
    skill_root = root / "skills" / "karakana-self-improvement"
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        """---
name: karakana-self-improvement
description: Eval skill.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
requires_approval_for: []
---
# Skill

## Purpose

Eval.
""",
        encoding="utf-8",
    )


def write_eval(root: Path) -> None:
    eval_path = root / "evals" / "safety" / "demo.yml"
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text(
        """id: demo
name: Demo
description: Demo
suite: safety
input:
  task: "Plan eval work with tests and approval."
  project: "karakana"
  skill: "karakana-self-improvement"
  task_type: "planning"
expectations:
  expected_provider: "github"
  expected_model: "gpt-5-mini"
  must_include:
    - "tests"
    - "approval"
  required_sections:
    - "Safety Rules"
""",
        encoding="utf-8",
    )


def test_eval_runner_runs_mock_default_and_writes_report(tmp_path):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    write_eval(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")

    report = EvalRunner(tmp_path).run(suite="safety")

    assert report.status == "passed"
    assert report.total_cases == 1
    assert (tmp_path / ".karakana" / "eval-runs" / report.eval_run_id / "report.json").exists()
