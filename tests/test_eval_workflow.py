from pathlib import Path


def test_skill_eval_workflow_runs_eval_command():
    workflow = Path(".github/workflows/skill-eval.yml").read_text(encoding="utf-8")

    assert "karakana eval run" in workflow
    assert "karakana/**" in workflow
    assert "pytest" in workflow
