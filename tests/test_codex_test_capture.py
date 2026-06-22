import json
import sys

from karakana.codex.patch import PatchCapture


def test_capture_safe_test_command(tmp_path):
    result_path = PatchCapture(tmp_path).capture_tests(f"{sys.executable} -c 'print(123)'")
    data = json.loads(result_path.read_text(encoding="utf-8"))

    assert data["exit_code"] == 0
    assert data["refused"] is False


def test_capture_refuses_destructive_command(tmp_path):
    result_path = PatchCapture(tmp_path).capture_tests("rm -rf build")
    data = json.loads(result_path.read_text(encoding="utf-8"))

    assert data["refused"] is True
