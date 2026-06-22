"""Validate Karakana configuration."""

from __future__ import annotations

from pathlib import Path

from karakana.config.schemas import KarakanaConfig


def validate_config(config: KarakanaConfig, repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if config.models.live_mode_default:
        warnings.append("Live model mode is enabled by default.")
    if config.safety.allow_live_models_by_default:
        errors.append("Live models must not be allowed by default for the stable profile.")
    if config.safety.allow_github_writes_by_default:
        errors.append("GitHub writes must not be allowed by default.")
    if not config.safety.dry_run_default:
        errors.append("dry_run_default must remain true.")
    if not config.safety.require_explicit_write:
        errors.append("require_explicit_write must remain true.")

    artifact_path = Path(config.paths.artifacts)
    if artifact_path.is_absolute():
        warnings.append("Artifact path is absolute; prefer .karakana under the repo.")
    elif artifact_path.parts and artifact_path.parts[0] != ".karakana":
        errors.append("Artifact path must stay under .karakana unless explicitly reviewed.")

    for label, value in {
        "ubongo": config.paths.ubongo,
        "skills": config.paths.skills,
        "skillpacks": config.paths.skillpacks,
        "workspaces": config.paths.workspaces,
    }.items():
        path = Path(value)
        if path.is_absolute():
            warnings.append(f"{label} path is absolute: {value}")
        if ".." in path.parts:
            errors.append(f"{label} path must not contain '..': {value}")

    for relative in [config.paths.ubongo, config.paths.skills, config.paths.skillpacks, config.paths.workspaces]:
        if not (repo_root / relative).exists():
            warnings.append(f"Configured path does not exist: {relative}")

    return errors, warnings
