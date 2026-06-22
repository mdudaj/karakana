"""Load effective Karakana configuration."""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from karakana.config.schemas import KarakanaConfig


CONFIG_CANDIDATES = ("karakana.yml", "karakana.yaml", ".karakana/config.json")


def load_config(repo_root: Path) -> KarakanaConfig:
    for relative in CONFIG_CANDIDATES:
        path = repo_root / relative
        if not path.exists():
            continue
        data = _load_mapping(path)
        config = KarakanaConfig.from_dict(data, source_path=str(path))
        return _apply_environment(config)
    return _apply_environment(KarakanaConfig())


def _load_mapping(path: Path) -> dict:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _apply_environment(config: KarakanaConfig) -> KarakanaConfig:
    provider = os.environ.get("KARAKANA_DEFAULT_PROVIDER")
    model = os.environ.get("KARAKANA_DEFAULT_MODEL")
    if provider:
        config.models.default_provider = provider
    if model:
        config.models.default_model = model
    return config
