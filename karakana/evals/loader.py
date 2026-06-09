"""YAML evaluation case discovery and loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from karakana.evals.schemas import EvalCase, EvalExpectation, EvalInput


class EvalLoader:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def discover(self) -> list[Path]:
        roots = [self.repo_root / "evals", self.repo_root / "skills"]
        paths: list[Path] = []
        for root in roots:
            if not root.exists():
                continue
            paths.extend(root.glob("**/*.yml"))
            paths.extend(root.glob("**/*.yaml"))
        return sorted(path for path in paths if path.is_file())

    def load_case(self, path: Path) -> EvalCase:
        resolved = path if path.is_absolute() else self.repo_root / path
        try:
            data = yaml.safe_load(resolved.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid eval YAML at {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError(f"Eval file must contain a YAML object: {path}")
        self._require(data, "id", path)
        self._require(data, "name", path)
        self._require(data, "suite", path)
        input_data = data.get("input")
        if not isinstance(input_data, dict) or not input_data.get("task"):
            raise ValueError(f"Eval file requires input.task: {path}")
        expectations = data.get("expectations") or {}
        if not isinstance(expectations, dict):
            raise ValueError(f"Eval expectations must be an object: {path}")
        case = EvalCase(
            id=str(data["id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
            suite=str(data["suite"]),
            input=EvalInput(
                task=str(input_data["task"]),
                project=input_data.get("project"),
                skill=input_data.get("skill"),
                task_type=input_data.get("task_type"),
                prompt_file=input_data.get("prompt_file"),
                context_files=list(input_data.get("context_files") or []),
            ),
            expectations=EvalExpectation(
                must_include=list(expectations.get("must_include") or []),
                must_not_include=list(expectations.get("must_not_include") or []),
                required_sections=list(expectations.get("required_sections") or []),
                forbidden_patterns=list(expectations.get("forbidden_patterns") or []),
                max_length=expectations.get("max_length"),
                min_length=expectations.get("min_length"),
                expected_model=expectations.get("expected_model"),
                expected_provider=expectations.get("expected_provider"),
                safety_flags=list(expectations.get("safety_flags") or []),
            ),
            tags=list(data.get("tags") or []),
            risk_level=str(data.get("risk_level", "low")),
            path=str(resolved.relative_to(self.repo_root)) if resolved.is_relative_to(self.repo_root) else str(resolved),
        )
        return case

    def load_cases(
        self,
        suite: str | None = None,
        skill: str | None = None,
        case_path: Path | None = None,
    ) -> list[EvalCase]:
        paths = [case_path] if case_path else self.discover()
        cases = [self.load_case(path) for path in paths if path is not None]
        if suite:
            cases = [case for case in cases if case.suite == suite]
        if skill:
            cases = [case for case in cases if case.input.skill == skill or (case.path and case.path.startswith(f"skills/{skill}/"))]
        return cases

    @staticmethod
    def _require(data: dict[str, Any], field: str, path: Path) -> None:
        if not data.get(field):
            raise ValueError(f"Eval file requires {field}: {path}")
