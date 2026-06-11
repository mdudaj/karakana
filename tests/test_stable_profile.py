from pathlib import Path

import yaml


def test_stable_profile_exists_and_safe_defaults():
    path = Path.cwd() / "profiles" / "stable.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert data["defaults"]["dry_run"] is True
    assert data["defaults"]["live_models"] is False
    assert data["defaults"]["github_writes"] is False
    assert data["defaults"]["codex_execution"] is False
    assert data["defaults"]["patch_apply"] is False
    assert data["defaults"]["push"] is False
    assert data["defaults"]["deploy"] is False


def test_changelog_exists_and_karakana_gitignored():
    assert (Path.cwd() / "CHANGELOG.md").exists()
    assert ".karakana/" in (Path.cwd() / ".gitignore").read_text(encoding="utf-8")

