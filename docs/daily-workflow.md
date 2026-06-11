# Karakana Daily Workflow

## Start

```bash
karakana doctor
karakana workspace activate nimr
karakana workspace status
```

## Plan Work

```bash
karakana workspace plan --project billing --task "Review GePG callback issue"
karakana requirements prd --from-note "Describe the intended change" --project billing --skillpack billing
karakana requirements ready <req-id>
```

## Move Toward Implementation

```bash
karakana action extract --from-response <response-file>
karakana codex handoff <action-run-id>
karakana codex capture-diff
karakana codex review-patch --diff <diff-path>
karakana patch gate --patch-run <patch-run-id>
```

## Local Review Loop

Patch apply, staging, and commit are dry-run by default and require explicit flags.

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
