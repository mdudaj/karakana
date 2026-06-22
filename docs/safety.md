# Karakana Safety

Karakana is designed around reviewable local artifacts and explicit opt-in gates.

## Defaults

- Dry-run behavior by default.
- No live model calls unless `--live` is passed on supported commands.
- No GitHub writes unless explicit write flags are passed.
- No Codex execution unless `--execute` is passed.
- No patch apply or commit unless `--write` is passed.
- No push, PR creation, merge, deployment, or package publishing by default.

## Secret Handling

Karakana redacts common secret-like values in traces and artifacts. Do not place `.env` files or private keys in sources intended for ingestion or release notes.

## Human Review

Model responses, actions, patches, ingestion candidates, requirements, and crosslinks remain reviewable artifacts. Human review decides whether anything moves forward.
