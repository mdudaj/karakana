from pathlib import Path

from karakana.okf.context import select_concepts


def test_select_concepts_filters_by_project_type_and_tag():
    concepts = select_concepts(
        Path.cwd(),
        project="msc-platform",
        concept_types={"DesignSystemRule"},
        tags={"dashboard"},
        relationship_depth=0,
    )

    assert [concept.concept_id for concept in concepts] == ["msc-platform.design.dashboard"]


def test_select_concepts_follows_relationships_with_bound():
    concepts = select_concepts(
        Path.cwd(),
        project="karakana",
        tags={"self-improvement"},
        relationship_depth=1,
        limit=10,
    )
    ids = {concept.concept_id for concept in concepts}

    assert "karakana.skill.self-improvement" in ids
    assert "karakana.okf.profile" in ids


def test_select_concepts_respects_limit():
    concepts = select_concepts(Path.cwd(), project="karakana", limit=2)

    assert len(concepts) == 2
