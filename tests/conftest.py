"""Keep test-generated harness state out of the developer's runtime stores."""

from pathlib import Path
import shutil

import pytest

REPOSITORY = Path(__file__).resolve().parents[1]
RUNTIME = REPOSITORY / ".karakana"


def _reject_checkout_runtime(path):
    resolved = Path(path).resolve()
    if resolved == RUNTIME or resolved.is_relative_to(RUNTIME):
        raise AssertionError("Test attempted to write real .karakana state; use isolated_repo or tmp_path.")


@pytest.fixture(autouse=True)
def protect_checkout_runtime(monkeypatch):
    """Guard the pathlib write paths used by stores; not a subprocess sandbox."""
    original_open, original_mkdir = Path.open, Path.mkdir

    def guarded_open(path, mode="r", *args, **kwargs):
        if any(flag in mode for flag in "wax+"):
            _reject_checkout_runtime(path)
        return original_open(path, mode, *args, **kwargs)

    def guarded_mkdir(path, *args, **kwargs):
        _reject_checkout_runtime(path)
        return original_mkdir(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    monkeypatch.setattr(Path, "mkdir", guarded_mkdir)


@pytest.fixture
def isolated_repo(tmp_path, monkeypatch):
    """Copy explicit public source/config inputs, never existing runtime state."""
    root = tmp_path / "repository"
    root.mkdir()
    for name in ("karakana", "skills", "skillpacks", "ubongo", "protocols", "templates",
                 "prompts", "profiles", "okf", "workspaces", "docs", "evals", "scripts", "tests", ".github"):
        source = REPOSITORY / name
        if source.exists():
            shutil.copytree(source, root / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".env*"))
    for name in ("KARAKANA.md", "AGENTS.md", "README.md", "KARAKANA_AGENT_GUIDE.md", "pyproject.toml", ".gitignore"):
        shutil.copy2(REPOSITORY / name, root / name)
    monkeypatch.chdir(root)
    return root
