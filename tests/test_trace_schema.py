import re

from karakana.traces.schemas import RunTrace, SafetyCheck, redact_value
from karakana.traces.store import generate_run_id


def test_run_id_generation_shape():
    run_id = generate_run_id()

    assert re.match(r"^\d{8}-\d{6}-[0-9a-f]{6}$", run_id)


def test_secret_like_inputs_are_redacted():
    value = redact_value(
        {
            "client_secret": "abc",
            "nested": {"api_key": "def"},
            "normal": "visible",
        }
    )

    assert value["client_secret"] == "[REDACTED]"
    assert value["nested"]["api_key"] == "[REDACTED]"
    assert value["normal"] == "visible"


def test_secret_like_string_values_are_redacted():
    value = redact_value({"prompt": "client_secret=abc Bearer xyz visible text"})

    assert value["prompt"] == "client_secret=[REDACTED] Bearer [REDACTED] visible text"
    assert "abc" not in value["prompt"]
    assert "xyz" not in value["prompt"]


def test_invalid_trace_status_fails():
    try:
        RunTrace(
            run_id="run",
            command="cmd",
            project=None,
            skill=None,
            task=None,
            task_type=None,
            selected_model=None,
            status="bad",
            started_at="now",
        )
    except ValueError as exc:
        assert "Invalid trace status" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_invalid_safety_status_fails():
    try:
        SafetyCheck(name="check", status="bad")
    except ValueError as exc:
        assert "Invalid safety check status" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
