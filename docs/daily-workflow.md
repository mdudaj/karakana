# Karakana Daily Workflow

## Start

```bash
karakana doctor
karakana workspace activate nimr
karakana workspace status
```

## Plan Work

```bash
karakana protocol start --task "Describe the intended change" --project billing --write-plan
karakana workspace plan --project billing --task "Review GePG callback issue"
karakana skill show requirements-elicitation
karakana skill show brainstorm-verbalized-sampling
karakana requirements prd --from-note "Describe the intended change" --project billing --skillpack billing
karakana requirements ready <req-id>
```

For ambiguous work, first produce a reviewed `Requirements Elicitation Result` using `requirements-elicitation`. Run `grill-with-docs` against relevant ADRs and project plans, and use `brainstorm-verbalized-sampling` when multiple valid paths remain. Pass the saved artifact to `requirements prd --from-file`; do not generate implementation issues until the material decisions are resolved.

## Move Toward Implementation

Decide the next bounded milestone from current evidence:

```bash
karakana milestone next --project <project> --skillpack <skillpack> --write-instructions
```

Review the generated `.karakana/milestones/<run-id>/next-milestone.md` before using its instruction artifact.

```bash
karakana action extract --from-response <response-file>
karakana codex handoff <action-run-id>
karakana codex capture-diff
karakana codex review-patch --diff <diff-path>
karakana patch gate --patch-run <patch-run-id>
```

Use `karakana protocol missing --trace <run-id>` and `karakana protocol attach --trace <run-id> --kind <artifact> --path <path>` to close required artifact gaps before handoff or patch gate enforcement.

## Local Review Loop

Patch apply, staging, and commit are dry-run by default and require explicit flags.
Do not work directly on `main`: create a task branch before editing, open a pull request for the completed work, and squash merge the PR after validation when integration is approved.

```bash
karakana patch apply --patch-run <patch-run-id>
karakana patch commit --patch-run <patch-run-id> --message "..."
```

## Learn Safely

```bash
karakana ingest file README.md --project karakana --classify
karakana crosslink scan --workspace nimr
```

Ingestion and crosslink workflows propose reviewable updates. They do not silently update memory or skills.
