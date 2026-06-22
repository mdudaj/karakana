from pathlib import Path

from karakana.ingestion.generator import generate_candidates
from karakana.ingestion.schemas import IngestionSource
from karakana.skillpacks.resolver import SkillpackResolver


def test_skillpack_guides_skill_update_target():
    context = SkillpackResolver(Path.cwd()).resolve_for_project("nhrdm")
    source = IngestionSource(source_type="manual_note", project="nhrdm")

    candidates = generate_candidates(source, "repeated workflow checklist verification step", project="nhrdm", skillpack_context=context)

    assert candidates[0].target_path == "skills/invenio-framework/SKILL.md"
