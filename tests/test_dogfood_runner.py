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


@pytest.mark.parametrize(
    ("count", "status", "warnings"),
    [
        (0, "passed", []),
        (2, "warning", ["Cases: 173, passed: 171, failed: 0, warnings: 2"]),
    ],
)
def test_dogfood_runner_classifies_eval_warning_counts(tmp_path: Path, count: int, status: str, warnings: list[str]):
    passed = 173 - count
    fake = Mock(returncode=0, stdout=f"Status: passed\nCases: 173, passed: {passed}, failed: 0, warnings: {count}\n", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="eval_run")

    assert run.command_results[0].status == status
    assert run.command_results[0].warnings == warnings


def test_dogfood_runner_captures_warning_section_message_not_heading(tmp_path: Path):
    output = "# Workspace\n## Warnings\n- Project path missing: crdb-mel\n## Recommended Next Actions\n- Validate workspace.\n"
    fake = Mock(returncode=0, stdout=output, stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="workspace_status")

    assert run.command_results[0].status == "warning"
    assert run.command_results[0].warnings == ["- Project path missing: crdb-mel"]


def test_dogfood_runner_does_not_match_warning_in_branch_or_file_names(tmp_path: Path):
    output = "### karakana\n- Git branch: fix/dogfood-warning-classification\n- Git status: ?? docs/dogfood-warning-classification.md\n## Warnings\n- None\n"
    fake = Mock(returncode=0, stdout=output, stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="workspace_status")

    assert run.command_results[0].status == "passed"
    assert run.command_results[0].warnings == []


def test_dogfood_runner_treats_missing_optional_credentials_as_informational(tmp_path: Path):
    fake = Mock(returncode=0, stdout="Warnings:\n- GitHub token not configured.\n- OpenAI API key missing.\n", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="doctor")

    assert run.command_results[0].status == "passed"
    assert run.command_results[0].warnings == []


def test_dogfood_runner_ignores_optional_doctor_status_and_keeps_real_warning(tmp_path: Path):
    output = "Doctor status: warning\nwarning: gh_token - not configured\nwarning: skillpack validation failed\n"
    fake = Mock(returncode=0, stdout=output, stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="doctor")

    assert run.command_results[0].status == "warning"
    assert run.command_results[0].warnings == ["warning: skillpack validation failed"]


def test_dogfood_runner_does_not_classify_cut_off_warning_line(tmp_path: Path):
    output = "Doctor status: warning\n" + ("x" * 1155) + "\nwarning: anthropic_api_key - not configured\n"
    fake = Mock(returncode=0, stdout=output, stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="doctor")

    assert run.command_results[0].status == "passed"
    assert run.command_results[0].warnings == []


def test_dogfood_runner_keeps_real_warning_beyond_excerpt_limit(tmp_path: Path):
    output = ("x" * 1200) + "\nWARNING: Project memory path does not exist: example\n"
    fake = Mock(returncode=0, stdout=output, stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="skillpack_validate_all")

    assert run.command_results[0].status == "warning"
    assert run.command_results[0].warnings == ["WARNING: Project memory path does not exist: example"]
    assert "Project memory path" not in run.command_results[0].stdout_excerpt


def test_dogfood_runner_redacts_secret_names(tmp_path: Path):
    fake = Mock(returncode=0, stdout="OPENAI_API_KEY=abc", stderr="")
    with patch("karakana.dogfood.runner.subprocess.run", return_value=fake):
        run, _ = run_dogfood(tmp_path, "karakana", "karakana", command_id="version")

    assert "OPENAI_API_KEY" not in run.command_results[0].stdout_excerpt


def test_dogfood_runner_prepares_workflow_fixtures_in_repo(isolated_repo):
    run, _ = run_dogfood(Path.cwd(), "karakana", "karakana", command_id="version", dry_run=True)
    fixture = next(result for result in run.command_results if result.command_id == "workflow_fixtures")

    assert fixture.artifact_paths
    assert any("model-response.md" in path for path in fixture.artifact_paths)
