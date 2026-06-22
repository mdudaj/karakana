"""Workspace scanner for cross-project knowledge links."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.crosslinks.detector import detect_patterns
from karakana.crosslinks.schemas import CrosslinkEvidence, CrosslinkProjectRef
from karakana.crosslinks.store import create_bundle
from karakana.skillpacks.loader import SkillpackLoader
from karakana.workspaces.loader import WorkspaceLoader


def scan_workspace(repo_root: Path, workspace_name: str, project_ids: list[str] | None = None, includes: list[str] | None = None, max_artifacts: int = 20):
    workspace = WorkspaceLoader(repo_root).load(workspace_name)
    selected = [project for project in workspace.projects if not project_ids or project.id in project_ids]
    refs: list[CrosslinkProjectRef] = []
    evidence: list[CrosslinkEvidence] = []
    skillpack_loader = SkillpackLoader(repo_root)
    for project in selected:
        refs.append(CrosslinkProjectRef(project_id=project.id, workspace=workspace.name, path=project.path, skillpack=project.skillpack, memory_path=project.memory, tags=list(project.tags)))
        if project.skillpack:
            try:
                skillpack = skillpack_loader.load(project.skillpack)
                summary = f"required={','.join(skillpack.skills.required)} optional={','.join(skillpack.skills.optional)} approvals={','.join(skillpack.safety.requires_approval_for)} high_risk={','.join(skillpack.safety.high_risk_paths)}"
                evidence.append(CrosslinkEvidence(project_id=project.id, source_type="skillpack", source_id=project.skillpack, path=f"skillpacks/{project.skillpack}.yml", summary=summary, risk_level="medium", metadata={"required_skills": skillpack.skills.required, "optional_skills": skillpack.skills.optional, "approvals": skillpack.safety.requires_approval_for}))
            except Exception as exc:
                evidence.append(CrosslinkEvidence(project_id=project.id, source_type="skillpack", source_id=project.skillpack, summary=f"Skillpack load failed: {exc}", risk_level="medium"))
    evidence.extend(_artifact_evidence(repo_root, selected, includes or [], max_artifacts))
    patterns = detect_patterns(refs, evidence)
    return create_bundle(workspace.name, refs, patterns)


def _artifact_evidence(repo_root: Path, projects, includes: list[str], max_artifacts: int) -> list[CrosslinkEvidence]:
    if not includes:
        return []
    evidence = []
    artifact_roots = {
        "requirements": repo_root / ".karakana" / "requirements",
        "actions": repo_root / ".karakana" / "actions",
        "ingestion": repo_root / ".karakana" / "ingestion",
        "patch-reviews": repo_root / ".karakana" / "patch-reviews",
        "traces": repo_root / ".karakana" / "runs",
    }
    for kind in includes:
        root = artifact_roots.get(kind)
        if not root or not root.exists():
            continue
        for item in sorted((path for path in root.iterdir() if path.is_dir()), reverse=True)[:max_artifacts]:
            text = _summary_text(item)
            for project in projects:
                if project.id in text or not any(other.id in text for other in projects):
                    evidence.append(CrosslinkEvidence(project_id=project.id, source_type=kind, source_id=item.name, path=str(item), summary=text[:500], risk_level="medium" if "missing test" in text.lower() else "low"))
                    break
    return evidence


def _summary_text(path: Path) -> str:
    for name in ["summary.md", "crosslink.md", "prd.md", "actions.md", "candidates.md", "review.md", "trace.json"]:
        candidate = path / name
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    jsons = list(path.glob("*.json"))
    return json.dumps(json.loads(jsons[0].read_text(encoding="utf-8"))) if jsons else path.name
