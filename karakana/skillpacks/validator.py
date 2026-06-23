"""Validate project skillpacks."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.models.router import DEFAULT_MODEL_ROUTING
from karakana.protocols.loader import ProtocolLoader
from karakana.protocols.schemas import WORK_CATEGORIES
from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.schemas import ALLOWED_SKILLPACK_STATUSES, SkillpackValidationResult
from karakana.skills.loader import SkillLoader

KNOWN_PROVIDERS = {"github", "openai", "anthropic", "openai_codex", "mock"}


class SkillpackValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.loader = SkillpackLoader(repo_root)
        self.protocol_loader = ProtocolLoader(repo_root)
        self.skill_loader = SkillLoader(repo_root / "skills")

    def validate(self, name: str, strict: bool = False) -> SkillpackValidationResult:
        path = self.loader._path_for(name)
        result = SkillpackValidationResult(name=name, path=str(path))
        if not path.exists():
            result.errors.append(f"Skillpack file not found: {path}")
            return result
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            result.errors.append(f"Invalid YAML: {exc}")
            return result
        for field in ["name", "description", "version", "status", "project", "skills"]:
            if field not in raw:
                result.errors.append(f"Missing required field: {field}")
        if raw.get("name") != name:
            result.errors.append(f"Skillpack name '{raw.get('name')}' does not match file name '{name}'")
        status = raw.get("status")
        if status not in ALLOWED_SKILLPACK_STATUSES:
            result.errors.append(f"Invalid status: {status}")
        elif status == "deprecated":
            result.warnings.append("Skillpack is deprecated")
        project = raw.get("project") or {}
        if not project.get("id"):
            result.errors.append("project.id is required")
        memory = project.get("memory")
        if memory and not (self.repo_root / memory).exists():
            result.warnings.append(f"Project memory path does not exist: {memory}")
        skills = raw.get("skills") or {}
        for skill in skills.get("required") or []:
            if not self.skill_loader.skill_exists(skill):
                result.errors.append(f"Required skill not found: {skill}")
        for skill in skills.get("optional") or []:
            if not self.skill_loader.skill_exists(skill):
                result.warnings.append(f"Optional skill not found: {skill}")
        for task_type, route in (raw.get("model_routes") or {}).items():
            if task_type not in DEFAULT_MODEL_ROUTING:
                result.warnings.append(f"Unknown model route task type: {task_type}")
            if not isinstance(route, dict):
                result.errors.append(f"model_routes.{task_type} must be a mapping")
                continue
            if route.get("provider") not in KNOWN_PROVIDERS:
                result.errors.append(f"Unknown provider for route {task_type}: {route.get('provider')}")
            if not route.get("model"):
                result.errors.append(f"Missing model for route: {task_type}")
        protocols = raw.get("protocols") or {}
        if "default" in protocols:
            default_protocol = protocols.get("default")
            if not isinstance(default_protocol, str) or not default_protocol:
                result.errors.append("protocols.default must be a non-empty string")
            elif not self.protocol_loader.exists(default_protocol):
                result.errors.append(f"Referenced protocol not found: {default_protocol}")
        categories = protocols.get("categories") or {}
        if categories and not isinstance(categories, dict):
            result.errors.append("protocols.categories must be a mapping")
        for category, protocol_id in categories.items() if isinstance(categories, dict) else []:
            if category not in WORK_CATEGORIES:
                result.errors.append(f"Unknown protocol category: {category}")
            if not isinstance(protocol_id, str) or not protocol_id:
                result.errors.append(f"protocols.categories.{category} must be a non-empty string")
            elif not self.protocol_loader.exists(protocol_id):
                result.errors.append(f"Referenced protocol not found: {protocol_id}")
        safety = raw.get("safety") or {}
        for field in ["high_risk_paths", "blocked_paths", "requires_approval_for"]:
            if field in safety and not _string_list(safety[field]):
                result.errors.append(f"safety.{field} must be a list of strings")
        tests = raw.get("tests") or {}
        for field in ["commands", "recommended_before_commit"]:
            if field in tests and not _string_list(tests[field]):
                result.errors.append(f"tests.{field} must be a list of strings")
        conventions = raw.get("conventions") or {}
        if "notes" in conventions and not _string_list(conventions["notes"]):
            result.errors.append("conventions.notes must be a list of strings")
        if strict:
            result.errors.extend(result.warnings)
        return result

    def validate_all(self, strict: bool = False) -> list[SkillpackValidationResult]:
        return [self.validate(name, strict=strict) for name in self.loader.list_skillpacks()]


def _string_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)
