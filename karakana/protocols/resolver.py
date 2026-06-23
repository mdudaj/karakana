"""Resolve protocol artifact requirements from task conditions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from karakana.protocols.loader import ProtocolLoader
from karakana.protocols.schemas import ProtocolArtifactRule, WorkProtocol


class ProtocolResolver:
    def __init__(self, repo_root: Path):
        self.loader = ProtocolLoader(repo_root)

    def resolve(self, protocol_id: str) -> WorkProtocol:
        return self.loader.load(protocol_id)

    def required_artifacts(self, protocol_id: str, conditions: dict[str, Any] | None = None) -> list[ProtocolArtifactRule]:
        return self.resolve(protocol_id).required_artifacts_for(conditions or {})
