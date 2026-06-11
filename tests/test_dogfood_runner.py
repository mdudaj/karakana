from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from karakana.dogfood.runner import run_dogfood


def test_dogfood_runner_dry_run_plans_allowlisted_commands(tmp_path: Path):
    run, path = run_dogfood(tmp_path, "karakana", "karakana", dry_run=True)

    assert path.exists()
    assert run.status == "completed"
    assert {result.status for result in run.command_results} >= {"planned"}
    assert any(result.command == "karakana doctor" for result in run.command_results)
    assert any(result.command_id == "workflow_fixtures" for result in run.command_results)


def test_dogfood_runner_rejects_non_allowlisted_command(tmp_path: Path):
    with pytest.raises(ValueError):
        run_dogfood(tmp_path, "karakana", "karakana", command_id="rm_rf")


def test_dogfood_runner_executes_allowlisted_command_with_mocked_subprocess(tmp_path: Path):
    fake = Mock(returncode=0, stdout="ok", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="version")

    assert run.command_results[0].status == "passed"
    assert run.command_results[0].stdout_excerpt == "ok"
    assert run.command_results[0].duration_seconds is not None
    assert run.command_results[0].noise_score >= 1


def test_dogfood_runner_ignores_warnings_none_heading(tmp_path: Path):
    fake = Mock(returncode=0, stdout="Status: passed\nWarnings:\n- None\n", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="config_validate")

    assert run.command_results[0].status == "passed"
    assert run.command_results[0].warnings == []


def test_dogfood_runner_treats_missing_optional_credentials_as_informational(tmp_path: Path):
    fake = Mock(returncode=0, stdout="Warnings:\n- GitHub token not configured.\n- OpenAI API key missing.\n", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="doctor")

    assert run.command_results[0].status == "passed"
    assert run.command_results[0].warnings == []


def test_dogfood_runner_redacts_secret_names(tmp_path: Path):
    fake = Mock(returncode=0, stdout="OPENAI_API_KEY=abc", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="version")

    assert "OPENAI_API_KEY" not in run.command_results[0].stdout_excerpt


def test_dogfood_runner_prepares_workflow_fixtures_in_repo():
    run, _ = run_dogfood(Path.cwd(), "karakana", "karakana", command_id="version", dry_run=True)
    fixture = next(result for result in run.command_results if result.command_id == "workflow_fixtures")

    assert fixture.artifact_paths
    assert any("model-response.md" in path for path in fixture.artifact_paths)
