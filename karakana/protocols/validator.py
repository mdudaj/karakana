"""Validate deterministic work protocols."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.protocols.loader import ProtocolLoader, protocol_from_dict
from karakana.protocols.schemas import ProtocolValidationResult


class ProtocolValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.loader = ProtocolLoader(repo_root)

    def validate(self, protocol_id: str, strict: bool = False) -> ProtocolValidationResult:
        path = self.loader._path_for(protocol_id)
        result = ProtocolValidationResult(protocol_id=protocol_id, path=str(path))
        if not path.exists():
            result.errors.append(f"Protocol file not found: {path}")
            return result
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            result.errors.append(f"Invalid YAML: {exc}")
            return result
        for field in ["protocol_id", "name", "version", "category", "roles", "risk_floor", "summary", "steps", "artifacts"]:
            if field not in raw:
                result.errors.append(f"Missing required field: {field}")
        if raw.get("protocol_id") != protocol_id:
            result.errors.append(f"Protocol id '{raw.get('protocol_id')}' does not match file name '{protocol_id}'")
        try:
            protocol = protocol_from_dict(raw, path)
        except (TypeError, ValueError) as exc:
            result.errors.append(str(exc))
            return result
        if not protocol.steps:
            result.errors.append("Protocol must define at least one step")
        if not any(artifact.kind == "trace" for artifact in protocol.artifacts):
            result.warnings.append("Protocol does not require a trace artifact")
        if not any(artifact.kind == "verification_summary" for artifact in protocol.artifacts):
            result.warnings.append("Protocol does not require a verification summary")
        if not protocol.verification:
            result.warnings.append("Protocol does not define verification guidance")
        if strict:
            result.errors.extend(result.warnings)
        return result

    def validate_all(self, strict: bool = False) -> list[ProtocolValidationResult]:
        return [self.validate(protocol_id, strict=strict) for protocol_id in self.loader.list_protocols()]
