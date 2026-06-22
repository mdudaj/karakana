from pathlib import Path

import pytest

from karakana.evals.loader import EvalLoader


def write_case(root: Path, path: str, case_id: str = "case", suite: str = "skills", skill: str = "demo-skill") -> Path:
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        f"""id: {case_id}
name: Demo case
description: Demo
suite: {suite}
input:
  task: "Do work"
  project: "karakana"
  skill: "{skill}"
  task_type: "planning"
expectations:
  must_include:
    - "Do work"
""",
        encoding="utf-8",
    )
    return file_path


def test_eval_discovery_and_filters(tmp_path):
    write_case(tmp_path, "evals/safety/demo.yml", case_id="safety-demo", suite="safety", skill="safety-skill")
    write_case(tmp_path, "skills/demo-skill/evals/demo.yml", case_id="skill-demo", suite="skills")

    loader = EvalLoader(tmp_path)

    assert len(loader.discover()) == 2
    assert [case.id for case in loader.load_cases(suite="safety")] == ["safety-demo"]
    assert [case.id for case in loader.load_cases(skill="demo-skill")] == ["skill-demo"]


def test_eval_load_case_path(tmp_path):
    path = write_case(tmp_path, "evals/demo.yml", case_id="one")

    cases = EvalLoader(tmp_path).load_cases(case_path=path)

    assert len(cases) == 1
    assert cases[0].id == "one"


def test_invalid_eval_file_reports_readable_error(tmp_path):
    path = tmp_path / "evals" / "bad.yml"
    path.parent.mkdir(parents=True)
    path.write_text("name: Missing required fields\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires id"):
        EvalLoader(tmp_path).load_case(path)
