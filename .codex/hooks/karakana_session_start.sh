#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

if command -v karakana >/dev/null 2>&1; then
  karakana_cmd=(karakana)
elif [ -x "$repo_root/.venv/bin/karakana" ]; then
  karakana_cmd=("$repo_root/.venv/bin/karakana")
else
  echo "Karakana handoff hook skipped: no karakana CLI found on PATH or at .venv/bin/karakana." >&2
  exit 0
fi

mkdir -p "$repo_root/.karakana"
output_path="$repo_root/.karakana/session-start.md"

if "${karakana_cmd[@]}" handoff load --project karakana --skillpack karakana > "$output_path"; then
  cat "$output_path"
else
  status=$?
  echo "Karakana handoff hook failed while loading project handoff." >&2
  exit "$status"
fi
