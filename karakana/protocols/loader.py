"""Load deterministic work protocol YAML files."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.protocols.schemas import ProtocolArtifactRule, ProtocolStep, WorkProtocol


class ProtocolLoader:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.protocols_root = repo_root / "protocols"

    def discover_paths(self) -> list[Path]:
        if not self.protocols_root.exists():
            return []
        return sorted([*self.protocols_root.glob("*.yml"), *self.protocols_root.glob("*.yaml")])

    def list_protocols(self) -> list[str]:
        return [path.stem for path in self.discover_paths()]

    def exists(self, protocol_id: str) -> bool:
        return self._path_for(protocol_id).exists()

    def load(self, protocol_id: str) -> WorkProtocol:
        path = self._path_for(protocol_id)
        if not path.exists():
            raise FileNotFoundError(f"Protocol not found: {protocol_id}")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return protocol_from_dict(data, path)

    def _path_for(self, protocol_id: str) -> Path:
        yml = self.protocols_root / f"{protocol_id}.yml"
        if yml.exists():
            return yml
        return self.protocols_root / f"{protocol_id}.yaml"


def protocol_from_dict(data: dict, path: Path | None = None) -> WorkProtocol:
    reserved = {
        "protocol_id",
        "name",
        "version",
        "category",
        "roles",
        "risk_floor",
        "summary",
        "standards",
        "required_inputs",
        "steps",
        "artifacts",
        "approval_gates",
        "verification",
        "blocked_actions",
    }
    return WorkProtocol(
        protocol_id=str(data.get("protocol_id", path.stem if path else "")),
        name=str(data.get("name", "")),
        version=str(data.get("version", "")),
        category=str(data.get("category", "")),
        roles=list(data.get("roles") or []),
        risk_floor=str(data.get("risk_floor", "low")),
        summary=str(data.get("summary", "")),
        standards=list(data.get("standards") or []),
        required_inputs=list(data.get("required_inputs") or []),
        steps=[ProtocolStep(**step) for step in data.get("steps") or []],
        artifacts=[ProtocolArtifactRule(**artifact) for artifact in data.get("artifacts") or []],
        approval_gates=list(data.get("approval_gates") or []),
        verification=list(data.get("verification") or []),
        blocked_actions=list(data.get("blocked_actions") or []),
        metadata={key: value for key, value in data.items() if key not in reserved},
        path=str(path) if path else None,
    )
