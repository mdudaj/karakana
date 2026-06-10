import pytest

from karakana.skillpacks.loader import skillpack_from_dict


def test_skillpack_schema_parsing():
    skillpack = skillpack_from_dict(
        {
            "name": "demo",
            "description": "Demo",
            "version": "0.1.0",
            "status": "stable",
            "project": {"id": "demo"},
            "skills": {"required": ["karakana-handoff"], "optional": []},
            "model_routes": {"planning": {"provider": "github", "model": "gpt-5-mini"}},
        }
    )

    assert skillpack.name == "demo"
    assert skillpack.model_routes["planning"].model == "gpt-5-mini"


def test_skillpack_invalid_status():
    with pytest.raises(ValueError):
        skillpack_from_dict({"name": "bad", "description": "Bad", "version": "0", "status": "unknown", "project": {"id": "bad"}, "skills": {}})
