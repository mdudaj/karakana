from pathlib import Path

from karakana.config.schemas import KarakanaConfig
from karakana.config.validator import validate_config


def test_config_validator_safe_defaults_pass():
    errors, _ = validate_config(KarakanaConfig(), Path.cwd())

    assert errors == []


def test_config_validator_blocks_unsafe_defaults():
    config = KarakanaConfig()
    config.safety.allow_live_models_by_default = True
    config.safety.require_explicit_write = False

    errors, _ = validate_config(config, Path.cwd())

    assert any("Live models" in error for error in errors)
    assert any("require_explicit_write" in error for error in errors)

