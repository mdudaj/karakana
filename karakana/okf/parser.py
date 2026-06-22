"""Parse file-native OKF concept documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from karakana.okf.schemas import OkfConcept


class OkfParseError(ValueError):
    """Raised when an OKF concept cannot be parsed."""


def parse_concept_file(path: Path) -> OkfConcept:
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_markdown_frontmatter(text)
    return OkfConcept(path=path, metadata=metadata, body=body)


def parse_markdown_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise OkfParseError("Missing YAML frontmatter")
    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise OkfParseError("Unclosed YAML frontmatter")
    raw_frontmatter = text[4:closing]
    body = text[closing + 5 :]
    try:
        metadata = yaml.safe_load(raw_frontmatter) or {}
    except yaml.YAMLError as exc:
        raise OkfParseError(f"Invalid YAML frontmatter: {exc}") from exc
    if not isinstance(metadata, dict):
        raise OkfParseError("YAML frontmatter must be a mapping")
    return metadata, body
