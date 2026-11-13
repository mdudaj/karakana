"""Exercise the portable wrapper without real CLI/runtime/network operations."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
RELATIVE = Path("docs/skills/engineering-artifact-catalogue")
WRAPPER = REPO / RELATIVE / "RESUME-UBUNTU.sh"
BASH = shutil.which("bash")
if os.name == "nt":
    git_bash = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
    BASH = str(git_bash) if git_bash.is_file() else None


@unittest.skipUnless(BASH, "Bash is required for the portable wrapper checks")
class PortableHandoffResumeTests(unittest.TestCase):
    def run_wrapper(self, *, cli_location="bin", refresh_exit=0):
        with tempfile.TemporaryDirectory(prefix="karakana-resume-test-") as directory:
            root = Path(directory)
            destination = root / RELATIVE
            destination.mkdir(parents=True)
            shutil.copyfile(WRAPPER, destination / WRAPPER.name)
            (root / "KARAKANA.md").write_text("# Synthetic project\n", encoding="utf-8")
            brief = "# Synthetic continuation\n\nBranch: synthetic-next\nAcceptance: retain all instructions.\n"
            (destination / "UBUNTU-HANDOFF-2026-11-13.md").write_text(brief, encoding="utf-8")
            (destination / "DRAFTING-CONVENTIONS-2026-11-13.md").write_text("# Research\n", encoding="utf-8")
            tools = root / "tools"
            tools.mkdir()
            for tool in ("cat", "dirname"):
                p = tools / tool
                p.write_text(f'#!/bin/bash\nexec /usr/bin/{tool} "$@"\n', encoding="utf-8")
                p.chmod(0o755)
            (root / "bin").mkdir()
            if cli_location:
                cli = root / cli_location / "karakana"
                cli.parent.mkdir(parents=True, exist_ok=True)
                cli.write_text('''#!/bin/bash
set -eu
printf '%s\\n' "$1 $2" >> calls
case "$1 $2" in
  'handoff refresh')
    if [ "$REFRESH_EXIT" != 0 ]; then exit "$REFRESH_EXIT"; fi
    while [ "$#" -gt 0 ]; do
      if [ "$1" = --next-task-brief ]; then printf '%s\\n' "$2" > brief; fi
      shift
    done
    ;;
  'handoff load') /usr/bin/cat brief ;;
  *) exit 99 ;;
esac
''', encoding="utf-8")
                cli.chmod(0o755)
            history = root / "retained-history"
            history.write_text("preserve", encoding="utf-8")
            env = dict(os.environ, REFRESH_EXIT=str(refresh_exit))
            result = subprocess.run(
                [BASH, "--noprofile", "--norc", "-c",
                 'export PATH="$PWD/tools:$PWD/bin"; exec "$BASH" "$1"',
                 "resume-test", (destination / WRAPPER.name).as_posix()],
                cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", timeout=15,
            )
            calls = (root / "calls").read_text(encoding="utf-8").splitlines() if (root / "calls").exists() else []
            self.assertEqual(history.read_text(encoding="utf-8"), "preserve")
            return result, calls, brief

    def test_path_cli_loads_full_brief(self):
        result, calls, brief = self.run_wrapper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["handoff refresh", "handoff load"])
        self.assertIn(brief, result.stdout)

    def test_venv_cli_loads_full_brief(self):
        result, calls, brief = self.run_wrapper(cli_location=".venv/bin")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["handoff refresh", "handoff load"])
        self.assertIn(brief, result.stdout)

    def test_failed_refresh_does_not_load(self):
        result, calls, _ = self.run_wrapper(refresh_exit=23)
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assertEqual(calls, ["handoff refresh"])

    def test_missing_cli_stops_with_setup_guidance(self):
        result, calls, _ = self.run_wrapper(cli_location=None)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("docs/installation.md", result.stderr)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
