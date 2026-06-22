"""Configuration helpers for Karakana."""

from __future__ import annotations

from pathlib import Path

from karakana.config.loader import load_config
from karakana.config.schemas import KarakanaConfig

ROOT = Path(".")
UBONGO_DIR = ROOT / "ubongo"
SKILLS_DIR = ROOT / "skills"

__all__ = ["KarakanaConfig", "load_config", "ROOT", "UBONGO_DIR", "SKILLS_DIR"]
