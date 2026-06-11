from pathlib import Path

from karakana.config.loader import load_config


def test_config_loader_defaults():
    config = load_config(Path.cwd())

    assert config.default_workspace == "default"
    assert config.paths.artifacts == ".karakana"


def test_config_loader_yaml(tmp_path: Path):
    (tmp_path / "karakana.yml").write_text("default_workspace: nimr\nmodels:\n  default_provider: github\n", encoding="utf-8")

    config = load_config(tmp_path)

    assert config.default_workspace == "nimr"
    assert config.models.default_provider == "github"

