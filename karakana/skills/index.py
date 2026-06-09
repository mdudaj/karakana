"""Generate public indexes for local Karakana skills."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from karakana.skills.loader import SkillLoader

BUCKET_ORDER = [
    "development",
    "domain",
    "productivity",
    "research",
    "infrastructure",
    "self-improvement",
    "misc",
]


@dataclass(frozen=True)
class SkillIndexEntry:
    name: str
    description: str
    status: str
    bucket: str
    path: str


def collect_skill_index_entries(skills_root: Path) -> list[SkillIndexEntry]:
    """Load visible skills and return normalized public index entries."""
    loader = SkillLoader(skills_root)
    entries: list[SkillIndexEntry] = []
    for name in loader.list_skills():
        skill = loader.load_skill(name)
        visibility = skill.visibility or "public"
        if visibility == "hidden":
            continue
        bucket = skill.bucket or _bucket_from_category(skill.category)
        entries.append(
            SkillIndexEntry(
                name=skill.name,
                description=_one_line(skill.description),
                status=skill.status or "stable",
                bucket=bucket,
                path=f"skills/{name}/",
            )
        )
    return sorted(entries, key=lambda entry: (_bucket_sort_key(entry.bucket), entry.name))


def render_skill_index(entries: list[SkillIndexEntry]) -> str:
    lines = [
        "# Karakana Skills Index",
        "",
        "This index is generated from `skills/*/SKILL.md` metadata.",
        "Hidden skills are excluded from this public index.",
        "",
    ]
    for bucket in BUCKET_ORDER:
        bucket_entries = [entry for entry in entries if entry.bucket == bucket]
        if not bucket_entries:
            continue
        lines.extend(
            [
                f"## {_title(bucket)}",
                "",
                "| Skill | Status | Description | Path |",
                "|---|---|---|---|",
            ]
        )
        for entry in bucket_entries:
            status = _format_status(entry.status)
            lines.append(f"| `{entry.name}` | {status} | {entry.description} | `{entry.path}` |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_skill_index(skills_root: Path) -> str:
    return render_skill_index(collect_skill_index_entries(skills_root))


def _bucket_from_category(category: str | None) -> str:
    if category in BUCKET_ORDER:
        return category
    return "misc"


def _bucket_sort_key(bucket: str) -> tuple[int, str]:
    try:
        return (BUCKET_ORDER.index(bucket), bucket)
    except ValueError:
        return (len(BUCKET_ORDER), bucket)


def _format_status(status: str) -> str:
    if status == "stable":
        return "stable"
    return f"**{status}**"


def _one_line(text: str) -> str:
    return " ".join(text.strip().split())


def _title(bucket: str) -> str:
    return bucket.replace("-", " ").title()
