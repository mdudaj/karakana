# Matt Pocock Handoff Skill Review

## Purpose

Assess the external handoff pattern as a reference for durable Karakana session continuity without copying it as a runtime dependency.

## Source Reviewed

- [Matt Pocock handoff skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md)
- [Productivity skill directory](https://github.com/mattpocock/skills/tree/main/skills/productivity)
- [mattpocock/skills repository](https://github.com/mattpocock/skills)

Reviewed on 2026-06-18.

## What the Original Skill Does

The short user-invoked skill compacts a conversation into an OS temporary-file handoff, includes suggested skills, references existing PRDs/plans/ADRs/issues/commits/diffs rather than duplicating them, redacts sensitive information, and tailors output to the stated next-session purpose.

## Core Ideas Worth Adapting

- Treat handoff as a compact continuation artifact.
- Include suggested skills and the next-session purpose.
- Reference existing durable artifacts instead of repeating their contents.
- Redact sensitive details before writing.

## Original Assumptions

The original assumes conversational state is the primary source, a single temporary file is sufficient, explicit user invocation controls creation, and no project-scoped artifact index or lifecycle command exists.

## What Karakana Should Change

- Store append-only artifacts under `.karakana/handoffs/`, not the OS temporary directory.
- Select by project and skillpack, with optional workspace context.
- Add milestone, findings, inspect-first, do-not-reread, exact-next-action, safety, staleness, and return-handoff fields.
- Add explicit create/show/load/refresh/list/doctor commands.
- Add bounded artifact recovery when no explicit handoff exists.
- Add visible, opt-out lifecycle integration at formal planning and milestone boundaries.

## What Karakana Should Not Copy

- Temporary-file-only behavior.
- Unstructured freeform summaries.
- Full transcript compaction when durable artifacts already exist.
- Hidden automatic behavior on every unrelated command.
- External wording that creates unnecessary license ambiguity.

## License / Attribution Considerations

The source repository declares the MIT License. Karakana credits the source and rewrites the small general workflow concepts into its own schema, CLI, safety controls, artifact stores, and tests. It does not vendor the external skill text.

## Adaptation Decision

Update the existing `karakana-handoff` skill rather than create a competing `handoff` skill. Add a project-level handoff subsystem while leaving action, Codex, and workspace handoffs in their existing narrower roles.
