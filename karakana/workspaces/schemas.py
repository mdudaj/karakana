"""Schemas for multi-project workspaces."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

WORKSPACE_STATUSES = {"stable", "experimental", "in-progress", "deprecated"}


@dataclass
class WorkspaceDefaults:
    root: str = "."
    require_existing_paths: bool = False
    use_current_skillpack_if_missing: bool = True


@dataclass
class WorkspaceCommandSet:
    status: list[str] = field(default_factory=list)
    validate: list[str] = field(default_factory=list)
    test: list[str] = field(default_factory=list)


@dataclass
class WorkspaceProject:
    id: str
    display_name: str | None = None
    path: str | None = None
    skillpack: str | None = None
    memory: str | None = None
    tags: list[str] = field(default_factory=list)
    standard_commands: WorkspaceCommandSet = field(default_factory=WorkspaceCommandSet)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Workspace:
    name: str
    description: str
    version: str
    status: str
    defaults: WorkspaceDefaults = field(default_factory=WorkspaceDefaults)
    projects: list[WorkspaceProject] = field(default_factory=list)
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in WORKSPACE_STATUSES:
            raise ValueError(f"Invalid workspace status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProjectStatus:
    project_id: str
    display_name: str | None
    path: str | None
    path_exists: bool
    git_branch: str | None = None
    git_status: str | None = None
    skillpack: str | None = None
    skillpack_valid: bool | None = None
    memory_path: str | None = None
    memory_exists: bool | None = None
    trace_count: int = 0
    action_count: int = 0
    requirement_count: int = 0
    patch_count: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkspaceStatus:
    workspace: str
    status: str
    project_statuses: list[ProjectStatus] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
