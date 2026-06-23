# Karakana Command Reference

## version

Purpose: Show package and runtime version metadata.

Common commands:
```bash
karakana version
```

Safe default behavior: Read-only.

Write/execute flags: None

Example:
```bash
karakana version
```

## doctor

Purpose: Run local health checks.

Common commands:
```bash
karakana doctor
```

Safe default behavior: Read-only plus local artifacts.

Write/execute flags: None

Example:
```bash
karakana doctor
```

## config

Purpose: Inspect and validate configuration.

Common commands:
```bash
karakana config show
karakana config validate
karakana config paths
```

Safe default behavior: Read-only.

Write/execute flags: None

Example:
```bash
karakana config validate
```

## memory

Purpose: Inspect ubongo memory.

Common commands:
```bash
karakana memory validate --project karakana
```

Safe default behavior: Read-only validation.

Write/execute flags: None

Example:
```bash
karakana memory validate --project karakana
```

## handoff

Purpose: Create and load project session handoffs.

Common commands:
```bash
karakana handoff load --project msc-platform --skillpack msc-platform
karakana handoff refresh --project msc-platform --skillpack msc-platform
```

Safe default behavior: Append-only local artifacts; load recovers bounded state when absent.

Write/execute flags: --no-create, --no-write, --no-handoff

Example:
```bash
karakana handoff doctor --project msc-platform
```

## milestone

Purpose: Decide the next project milestone and generate instructions.

Common commands:
```bash
karakana milestone next --project msc-platform --skillpack msc-platform
```

Safe default behavior: Artifact-only; strict mode blocks unresolved planning risk.

Write/execute flags: --write-instructions

Example:
```bash
Review .karakana/milestones/<run-id>/next-milestone.md
```

## skill

Purpose: Inspect, validate, and index skills.

Common commands:
```bash
karakana skill validate-all
karakana skill index
```

Safe default behavior: Dry-run index by default.

Write/execute flags: --write for index writes

Example:
```bash
karakana skill validate-all
```

## skillpack

Purpose: Inspect and activate project skillpacks.

Common commands:
```bash
karakana skillpack list
karakana skillpack activate karakana
```

Safe default behavior: Activation writes local .karakana state only.

Write/execute flags: None

Example:
```bash
karakana skillpack validate-all
```

## workspace

Purpose: Coordinate read-only multi-project state.

Common commands:
```bash
karakana workspace status
karakana workspace handoff --project nhrdm
```

Safe default behavior: Read-only or artifact generation.

Write/execute flags: None

Example:
```bash
karakana workspace status
```

## model

Purpose: Inspect routing and controlled live model calls.

Common commands:
```bash
karakana model route --task-type planning
```

Safe default behavior: Dry-run unless --live is used.

Write/execute flags: --live

Example:
```bash
karakana model route --task-type planning
```

## github

Purpose: Generate GitHub artifacts and explicit writes.

Common commands:
```bash
karakana github issue-draft
```

Safe default behavior: Dry-run/artifact generation by default.

Write/execute flags: Explicit create/comment flags

Example:
```bash
karakana github --help
```

## trace

Purpose: Inspect local traces.

Common commands:
```bash
karakana trace latest
```

Safe default behavior: Read-only.

Write/execute flags: None

Example:
```bash
karakana trace latest
```

## improve

Purpose: Generate reviewable improvement proposals.

Common commands:
```bash
karakana improve from-trace <run-id>
```

Safe default behavior: Proposal only by default.

Write/execute flags: --write or publish flags where supported

Example:
```bash
karakana improve --help
```

## action

Purpose: Extract reviewable actions from model responses.

Common commands:
```bash
karakana action extract --from-response <path>
```

Safe default behavior: Artifact generation only.

Write/execute flags: Publish flags are explicit

Example:
```bash
karakana action list
```

## codex

Purpose: Generate Codex handoffs, capture diffs, review patches, or start Codex with visible Karakana context.

Common commands:
```bash
karakana codex start --project karakana --skillpack karakana -- --model gpt-5.5
karakana codex handoff <action-run-id>
```

Safe default behavior: No Codex execution by default except explicit `codex start`; launcher prints and flushes handoff context before exec, injects session context as Codex's initial prompt for fresh interactive launches, and bootstraps a missing project .venv unless --no-bootstrap is used. If `karakana` is not on PATH and .venv is missing, use `python -m karakana codex start --project <project>` from the source checkout.

Write/execute flags: --execute, --print-only, --no-create, --no-pause, --inline, --no-bootstrap, --no-inject-prompt

Example:
```bash
karakana codex start --project karakana --skillpack karakana --print-only
```

## copilot

Purpose: Start GitHub Copilot CLI with visible Karakana handoff context.

Common commands:
```bash
karakana copilot start --project karakana --skillpack karakana -- --model gpt-5.4
```

Safe default behavior: Explicit launcher prints handoff context before exec; --print-only previews without launch.

Write/execute flags: --print-only, --no-create, --no-pause

Example:
```bash
karakana copilot start --project karakana --skillpack karakana --print-only
```

## patch

Purpose: Gate, branch, apply, and commit reviewed patches locally.

Common commands:
```bash
karakana patch gate --patch-run <id>
```

Safe default behavior: Dry-run by default.

Write/execute flags: --write, --create, --stage

Example:
```bash
karakana patch status --patch-run <id>
```

## ingest

Purpose: Distill selected evidence into reviewable candidates.

Common commands:
```bash
karakana ingest file README.md --classify
```

Safe default behavior: No writes by default.

Write/execute flags: --write

Example:
```bash
karakana ingest list
```

## requirements

Purpose: Generate PRDs, stories, issues, and readiness checks.

Common commands:
```bash
karakana requirements prd --from-note "..."
```

Safe default behavior: Artifact generation only.

Write/execute flags: --create-issues is explicit if supported

Example:
```bash
karakana requirements list
```

## crosslink

Purpose: Detect reusable cross-project patterns.

Common commands:
```bash
karakana crosslink scan --workspace nimr
```

Safe default behavior: Scan/propose only; apply is dry-run.

Write/execute flags: --write, --allow-high-risk

Example:
```bash
karakana crosslink list
```

## protocol

Purpose: Classify work, produce protocol artifacts, and gate reproducibility.

Common commands:
```bash
karakana protocol start --task "Plan a database schema migration" --project karakana
karakana protocol template requirements_note
karakana protocol missing --trace <run-id>
karakana protocol attach --trace <run-id> --kind requirements_note --path docs/requirements/example.md
karakana protocol check --trace <run-id>
```

Safe default behavior: Local artifact generation and trace updates only.

Write/execute flags: --write-plan writes protocol-start artifacts; --output writes templates; handoff and patch gates use --require-protocol-pass for enforcement.

Example:
```bash
karakana protocol validate-all
```

## release

Purpose: Run release checks and generate release artifacts.

Common commands:
```bash
karakana release check
karakana release notes
```

Safe default behavior: No publishing by default.

Write/execute flags: --full runs slower local checks

Example:
```bash
karakana release checklist
```

## docs

Purpose: Generate and check documentation.

Common commands:
```bash
karakana docs command-reference
karakana docs check
```

Safe default behavior: Preview by default.

Write/execute flags: --write

Example:
```bash
karakana docs check
```
