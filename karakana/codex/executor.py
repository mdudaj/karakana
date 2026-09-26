"""Safe Codex execution wrapper.

Execution is deliberately conservative. If the Codex CLI is not present, a
manual execution instruction is written instead of pretending success.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from karakana.safety.codex import validate_codex_execution_request
from karakana.tools.code_search import _git_branch


class CodexExecution:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def execute(self, task_file: Path, explicit: bool = False, output_dir: Path | None = None) -> Path:
        output = output_dir or task_file.parent / "execution"
        output.mkdir(parents=True, exist_ok=True)
        branch = _git_branch(self.repo_root)
        checks = validate_codex_execution_request(explicit, branch, task_file, output, self.repo_root)
        if checks:
            _write_stub(output, task_file, checks)
            raise ValueError("; ".join(checks))
        codex = shutil.which("codex")
        if codex is None:
            _write_stub(output, task_file, ["Codex CLI was not found."])
            raise FileNotFoundError("Codex CLI was not found. Run manually with: codex < " + str(task_file))
        metadata_path = task_file.with_name("codex-task.json")
        if not metadata_path.is_file():
            raise ValueError("Explicit execution requires codex-task.json with a recommended Codex model.")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        model = metadata.get("recommended_model")
        if metadata.get("recommended_provider") != "openai_codex" or not isinstance(model, str) or not model.strip():
            raise ValueError("Explicit execution requires a recommended openai_codex model.")
        command = [codex, "exec", "--model", model, "-"]
        effort = metadata.get("reasoning_effort")
        if effort is not None:
            if effort not in {"low", "medium", "high", "xhigh"}:
                raise ValueError("Unsupported reasoning effort in Codex task metadata.")
            command[4:4] = ["-c", f'model_reasoning_effort="{effort}"']
        (output / "command.json").write_text(json.dumps({"command": command, "task_file": str(task_file)}, indent=2) + "\n", encoding="utf-8")
        with task_file.open("r", encoding="utf-8") as stdin:
            result = subprocess.run(command, cwd=self.repo_root, stdin=stdin, capture_output=True, text=True, check=False, timeout=600)
        (output / "stdout.log").write_text(result.stdout, encoding="utf-8")
        (output / "stderr.log").write_text(result.stderr, encoding="utf-8")
        (output / "result.md").write_text(f"# Codex Execution Result\n\nExit code: {result.returncode}\n", encoding="utf-8")
        if result.returncode:
            raise RuntimeError(f"Codex execution failed with exit code {result.returncode}; inspect {output / 'result.md'}.")
        return output / "result.md"


def _write_stub(output: Path, task_file: Path, warnings: list[str]) -> None:
    (output / "command.json").write_text(json.dumps({"manual_command": f"codex < {task_file}", "warnings": warnings}, indent=2) + "\n", encoding="utf-8")
    (output / "stdout.log").write_text("", encoding="utf-8")
    (output / "stderr.log").write_text("\n".join(warnings), encoding="utf-8")
    (output / "result.md").write_text(
        "# Codex Execution Not Performed\n\n"
        + "\n".join(f"- {warning}" for warning in warnings)
        + f"\n\nRun manually if appropriate:\n\n```bash\ncodex < {task_file}\n```\n",
        encoding="utf-8",
    )
