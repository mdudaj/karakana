#!/usr/bin/env bash
# Recreate portable continuation context; loading does not execute the next task.
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.."
note=docs/skills/engineering-artifact-catalogue/UBUNTU-HANDOFF-2026-11-13.md
research=docs/skills/engineering-artifact-catalogue/DRAFTING-CONVENTIONS-2026-11-13.md
test -f KARAKANA.md
test -f "$note"
test -f "$research"

if command -v karakana >/dev/null 2>&1; then
    cli=(karakana)
elif [ -x .venv/bin/karakana ]; then
    cli=(.venv/bin/karakana)
else
    echo 'STOP: Karakana CLI unavailable; inspect docs/installation.md before setup.' >&2
    exit 1
fi

brief=$(cat "$note")
"${cli[@]}" handoff refresh \
    --project karakana --skillpack karakana \
    --purpose 'Resume documentation template review' \
    --current-milestone 'Research complete; template review next' \
    --from-note "$brief" \
    --next-task 'Review documentation templates and recommend revisions before implementation' \
    --next-task-brief "$brief" \
    --reuse-stage "research=$research" --reuse-reviewed \
    --no-recover-artifacts
"${cli[@]}" handoff load --project karakana --skillpack karakana
