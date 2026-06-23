# Karakana Work Protocols

Work protocols make Karakana tasks deterministic and reproducible. A protocol classifies the work, selects roles, derives required artifacts, records trace evidence, and gates handoff or patch review.

## Loop

```text
protocol start -> template/missing/attach -> check -> handoff/patch gate
```

Use this loop for non-trivial Karakana work:

```bash
karakana protocol start --task "Plan a database schema migration" --project karakana --write-plan
karakana protocol missing --trace <run-id>
karakana protocol template migration_plan --output docs/migrations/example.md
karakana protocol attach --trace <run-id> --kind migration_plan --path docs/migrations/example.md
karakana protocol check --trace <run-id>
karakana handoff refresh --project karakana --skillpack karakana
```

## Start

`karakana protocol start` is the preferred task entry point. It selects a protocol, category, risk level, required artifacts, approval gates, and verification checklist.

Supported sources:

```bash
karakana protocol start --task "Describe the task" --project karakana
karakana protocol start --from-note "Describe the task" --project karakana
karakana protocol start --from-requirements <req-id>
```

Use `--write-plan` to write `.karakana/protocol-starts/<id>/start.json` and `start.md`.

## Artifact Production

List available templates:

```bash
karakana protocol template
```

Write a template:

```bash
karakana protocol template requirements_note --output docs/requirements/example.md
```

Attach an artifact to a trace:

```bash
karakana protocol attach --trace <run-id> --kind requirements_note --path docs/requirements/example.md
```

Inspect missing artifacts and suggested commands:

```bash
karakana protocol missing --trace <run-id>
```

## Gate

Run the artifact gate:

```bash
karakana protocol check --trace <run-id>
```

The check passes only when required artifacts have evidence in the trace or linked files.

## Handoff And Patch Gates

`handoff refresh` and `patch gate` run protocol checks in warning mode by default. Use `--require-protocol-pass` to enforce missing artifacts as failures:

```bash
karakana handoff refresh --project karakana --skillpack karakana --require-protocol-pass
karakana patch gate --patch-run <patch-run-id> --require-protocol-pass
```

This warn-first rollout avoids breaking existing workflows while making reproducibility gaps visible.

## Core Protocols

Karakana maps work categories to protocol IDs through `skillpacks/karakana.yml`:

- `requirements -> requirements-change`
- `architecture -> architecture-decision`
- `frontend -> ux-change`
- `migration -> data-migration`
- `safety -> safety-policy-change`
- `skill -> skill-update`
- `memory -> memory-update`
- `release -> release-change`
- `implementation -> python-code-change`

Run validation after protocol changes:

```bash
karakana protocol validate-all
karakana okf validate
karakana eval run --suite protocols
```

## OKF

Protocol concepts are recorded under `okf/karakana/protocols/`. Keep OKF concepts aligned when adding or changing protocols, gates, templates, or rollout behavior.
