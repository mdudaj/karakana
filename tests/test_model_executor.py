import json

import pytest

from karakana.models.errors import ModelProviderError
from karakana.models.executor import ModelExecutor


def test_model_executor_dry_run_writes_prompt_only(tmp_path):
    output_dir = tmp_path / ".karakana" / "model-runs" / "run"

    response = ModelExecutor(tmp_path).execute_prompt("Hello", "mock", "mock-model", live=False, output_dir=output_dir)

    assert response is None
    assert (output_dir / "prompt.md").exists()
    assert not (output_dir / "model-response.md").exists()


def test_model_executor_live_mock_writes_artifacts(tmp_path):
    output_dir = tmp_path / ".karakana" / "model-runs" / "run"

    response = ModelExecutor(tmp_path).execute_prompt("Hello", "mock", "mock-model", live=True, output_dir=output_dir)

    assert response.content.startswith("[MOCK MODEL RESPONSE]")
    for name in ["prompt.md", "model-request.json", "model-response.md", "model-response.json", "response-review.json", "response-review.md"]:
        assert (output_dir / name).exists()
    review = json.loads((output_dir / "response-review.json").read_text(encoding="utf-8"))
    assert review["status"] in {"passed", "warning"}


def test_model_executor_unknown_provider_blocked(tmp_path):
    with pytest.raises(ModelProviderError, match="Provider is unknown"):
        ModelExecutor(tmp_path).execute_prompt("Hello", "missing", "model", live=True, output_dir=tmp_path / ".karakana" / "model-runs" / "run")


def test_model_executor_unconfigured_provider_blocked(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)

    with pytest.raises(ModelProviderError, match="Provider is not configured"):
        ModelExecutor(tmp_path).execute_prompt("Hello", "github", "gpt-5-mini", live=True, output_dir=tmp_path / ".karakana" / "model-runs" / "run")


def test_model_executor_secret_prompt_blocked(tmp_path):
    with pytest.raises(ModelProviderError, match="secret-like"):
        ModelExecutor(tmp_path).execute_prompt("client_secret=abc", "mock", "mock-model", live=True, output_dir=tmp_path / ".karakana" / "model-runs" / "run")


def test_model_executor_unsafe_output_dir_blocked(tmp_path):
    with pytest.raises(ModelProviderError, match="Output directory"):
        ModelExecutor(tmp_path).execute_prompt("Hello", "mock", "mock-model", live=True, output_dir=tmp_path / "outside")
