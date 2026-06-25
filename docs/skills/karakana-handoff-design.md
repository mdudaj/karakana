# Karakana Handoff Design

## Purpose

Define durable, project-aware continuation state for fresh agents and sessions.

## User Problem

Long sessions lose working context, while ordinary summaries duplicate durable files and still omit the exact next action, safety state, or relevant skills.

## Design Goals

- Compact, append-only Markdown and JSON artifacts.
- Project/skillpack selection and bounded recovery.
- Explicit references, redaction, staleness checks, and lifecycle visibility.
- Safe automation with an opt-out instead of global hidden mutation.

## Handoff Artifact Model

Each `.karakana/handoffs/<handoff-id>/` contains `handoff.md` and `handoff.json`. The schema records metadata, milestone, purpose, source references, state, decisions, findings, inspect-first and do-not-reread paths, skills, exact action, safety, return expectations, staleness, recovery state, and previous handoff ID.

## Manual Handoff Flow

`handoff create` writes a new artifact. `show` gives a compact latest summary, `load` prints session-start context, `refresh` appends a successor, `list` shows history, and `doctor` validates it.

## Automatic End-of-Task Handoff Flow

“After each task” means after every bounded Karakana planning, implementation, review, or artifact-producing workflow, not every read-only CLI command. `milestone next` appends a handoff automatically unless `--no-handoff-refresh` is used. Other successful project traces record an explicit refresh next action. Agents follow the End Every Task protocol and refresh the handoff before handing control back.

## Session Entry Handoff Load Flow

“New session/task entrypoint” means `karakana plan`, `karakana workspace plan`, `karakana codex start`, `karakana copilot start`, or an agent following `AGENTS.md`. Planning and agent-start entrypoints load the latest matching handoff into the prompt or write a session-start prompt artifact. `--no-handoff` disables this behavior for planning entrypoints.

## Fallback State Recovery Flow

If no matching handoff exists, `handoff load` and planning entrypoints create a lightweight recovered artifact from only the configured skillpack/workspace, project overview, and latest milestone, dogfood, requirements, and ingestion stores. They do not scan the whole repository. Recovery is explicitly labeled and must be verified.

## Project-Aware Handoff Selection

Selection requires exact project match and, when supplied, exact skillpack match. Multiple handoffs are ordered by append-only ID timestamp. A specific foreign artifact is rejected. Refresh links to but never overwrites the previous handoff.

## Redaction and Safety

All free text passes through shared key/value redaction plus handoff-specific handling for private-key blocks, environment assignments, API-key prefixes, bearer tokens, and credential-bearing URLs. Doctor checks rendered Markdown again. Paths are preserved; raw logs are not imported.

## Suggested Skills

Suggestions come from the project skillpack, artifact metadata, and bounded milestone keywords, then are filtered to installed project skills. The handoff skill remains suggested for the return handoff.

## Return Handoff Expectations

The next agent records completed work, verification, remaining findings, changed references, and one exact next action in a new handoff before ending.

## CLI Design

Commands: `handoff create`, `show`, `load`, `refresh`, `list`, and `doctor`. Create writes by default; load recovers by default and supports `--no-create`; refresh is append-only; doctor supports a configurable staleness threshold.

## Skill Design

The existing `karakana-handoff` skill is updated. It defines continuation content and safety while deterministic execution lives under `karakana/handoffs/`.

## Integration Points

- Formal task entry: `plan`, `workspace plan`, and documented Start Every Task protocol.
- Task transition: automatic post-`milestone next` refresh.
- Other artifact tasks: trace reminder plus documented End Every Task protocol.
- Existing action/Codex/workspace handoffs remain separate source artifacts.

## Risks

- A recent handoff can still be logically stale after external code changes.
- Recovery quality depends on project-scoped metadata in source artifacts.
- Excessive automatic refresh would create noise, so the first implementation avoids a global command callback.
- “Files not to reread” is advisory and never overrides mandatory repository instructions.

## Decision

Implement explicit CLI commands, bounded autoload/recovery at formal planning entrypoints, automatic append after milestone decisions, trace reminders for other task commands, and start/end documentation. This is the least risky semi-automatic behavior that meets continuity needs without brittle hidden mutation.
