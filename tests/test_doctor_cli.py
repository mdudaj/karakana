import json
from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app


def test_doctor_cli_writes_artifacts():
    result = CliRunner().invoke(app, ["doctor", "--json"])

    assert result.exit_code == 0
    assert "Doctor status:" in result.output
    payload = json.loads(result.output[result.output.index("{") :])
    run_id = payload["run_id"]
    assert (Path.cwd() / ".karakana" / "doctor" / run_id / "doctor.json").exists()
    assert (Path.cwd() / ".karakana" / "doctor" / run_id / "doctor.md").exists()

