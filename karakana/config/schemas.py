"""Configuration schemas for Karakana."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value


@dataclass
class ModelConfig:
    live_mode_default: bool = False
    default_provider: str = "mock"
    default_model: str = "mock-model"


@dataclass
class PathConfig:
    ubongo: str = "ubongo"
    skills: str = "skills"
    skillpacks: str = "skillpacks"
    workspaces: str = "workspaces"
    artifacts: str = ".karakana"


@dataclass
class SafetyConfig:
    dry_run_default: bool = True
    require_explicit_write: bool = True
    allow_live_models_by_default: bool = False
    allow_github_writes_by_default: bool = False


@dataclass
class ReleaseConfig:
    package_name: str = "karakana"
    status: str = "in-progress"


@dataclass
class KarakanaConfig:
    version: str = "0.1.0"
    default_workspace: str = "default"
    default_skillpack: str = "karakana"
    models: ModelConfig = field(default_factory=ModelConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    release: ReleaseConfig = field(default_factory=ReleaseConfig)
    source_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: str | None = None) -> "KarakanaConfig":
        return cls(
            version=str(data.get("version", "0.1.0")),
            default_workspace=str(data.get("default_workspace", "default")),
            default_skillpack=str(data.get("default_skillpack", "karakana")),
            models=ModelConfig(**(data.get("models") or {})),
            paths=PathConfig(**(data.get("paths") or {})),
            safety=SafetyConfig(**(data.get("safety") or {})),
            release=ReleaseConfig(**(data.get("release") or {})),
            source_path=source_path,
            metadata=dict(data.get("metadata") or {}),
        )
