from pathlib import Path

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
