from typer.testing import CliRunner

from karakana.cli import app


def test_model_list_config_check_cli():
    runner = CliRunner()

    list_result = runner.invoke(app, ["model", "list"])
    config_result = runner.invoke(app, ["model", "config"])
    check_result = runner.invoke(app, ["model", "check"])

    assert list_result.exit_code == 0
    assert "mock" in list_result.output
    assert config_result.exit_code == 0
    assert '"default_provider": "mock"' in config_result.output
    assert check_result.exit_code == 0
    assert "mock: configured" in check_result.output


def test_model_complete_mock_dry_runs_without_live(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "complete", "--provider", "mock", "--model", "mock-model", "--prompt", "Hello"])

    assert result.exit_code == 0
    assert "Dry run: would call mock/mock-model" in result.output
    assert not (tmp_path / ".karakana" / "model-response.md").exists()


def test_model_complete_non_mock_dry_run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "complete", "--provider", "github", "--model", "gpt-5-mini", "--prompt", "Hello"])

    assert result.exit_code == 0
    assert "Dry run: would call github/gpt-5-mini" in result.output


def test_model_complete_live_missing_credentials_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    result = CliRunner().invoke(app, ["model", "complete", "--provider", "github", "--model", "gpt-5-mini", "--prompt", "Hello", "--live"])

    assert result.exit_code == 1
    assert "Provider is not configured" in result.output
