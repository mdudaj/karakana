"""Source-tree entrypoint for Karakana."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def main() -> None:
    if _should_prebootstrap(sys.argv[1:]):
        repo_root = Path.cwd()
        venv_python = _venv_python(repo_root / ".venv")
        if _is_running_in_project_venv(venv_python):
            from karakana.cli import app

            app()
            return
        if not venv_python.exists():
            print("Project .venv was not found; creating it and installing Karakana.", flush=True)
            subprocess.run([sys.executable, "-m", "venv", str(repo_root / ".venv")], cwd=repo_root, check=True)
            subprocess.run([str(venv_python), "-m", "pip", "install", "-e", ".[dev]"], cwd=repo_root, check=True)
            print("Project .venv is ready.", flush=True)
        os.environ["KARAKANA_PREBOOTSTRAPPED"] = "1"
        os.execv(str(venv_python), [str(venv_python), "-m", "karakana", *sys.argv[1:]])

    from karakana.cli import app

    app()


def _should_prebootstrap(args: list[str]) -> bool:
    if os.environ.get("KARAKANA_PREBOOTSTRAPPED") == "1":
        return False
    if len(args) < 2 or args[:2] != ["codex", "start"]:
        return False
    if "--print-only" in args or "--no-bootstrap" in args:
        return False
    return True


def _is_running_in_project_venv(venv_python: Path) -> bool:
    return Path(sys.prefix) == venv_python.parent.parent


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


if __name__ == "__main__":
    main()
