from pathlib import Path
import json
from types import SimpleNamespace

import pytest

from karakana.codex.executor import CodexExecution
from karakana.safety.codex import detect_destructive_command, validate_test_command


def test_codex_execution_requires_explicit_flag(tmp_path):
    task = tmp_path / ".karakana" / "codex" / "task" / "codex-task.md"
    task.parent.mkdir(parents=True)
    task.write_text("# Task\n", encoding="utf-8")

    with pytest.raises(ValueError, match="explicit --execute"):
        CodexExecution(tmp_path).execute(task, explicit=False)


def test_destructive_command_detection():
    assert detect_destructive_command("rm -rf /tmp/app")
    assert validate_test_command("kubectl delete pod")


def test_explicit_execution_passes_structured_model_without_shell(tmp_path, monkeypatch):
    task = tmp_path / ".karakana" / "codex-task.md"
    task.parent.mkdir()
    task.write_text("Write an export test")
    task.with_suffix(".json").write_text(json.dumps({
        "recommended_provider": "openai_codex", "recommended_model": "test-model",
    }))
    monkeypatch.setattr("karakana.codex.executor._git_branch", lambda root: "feature/test")
    monkeypatch.setattr("karakana.codex.executor.shutil.which", lambda binary: "/bin/codex")
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        assert not kwargs.get("shell")
        return SimpleNamespace(returncode=0, stdout="done", stderr="")

    monkeypatch.setattr("karakana.codex.executor.subprocess.run", run)
    CodexExecution(tmp_path).execute(task, explicit=True)
    assert calls == [["/bin/codex", "exec", "--model", "test-model", "-"]]
    task.with_suffix(".json").unlink()
    with pytest.raises(ValueError, match="codex-task.json"):
        CodexExecution(tmp_path).execute(task, explicit=True)
    assert len(calls) == 1
