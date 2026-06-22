# Skills

Karakana skills are reusable workflow instructions stored as markdown under `skills/<name>/SKILL.md`.

Skills are for guidance: they describe when to use a workflow, what risks to check, what tools may help, and how to verify the result. Tools are for deterministic execution and safety-gated operations.

Project skillpacks live under `skillpacks/` and declare which skills, memory, routes, safety paths, tests, and conventions apply to a specific project. See `docs/skillpacks.md`.

## Required Metadata

Every skill must include YAML front matter with:

- `name`
- `description`
- `version`
- `risk_level`
- `allowed_tools`
- `requires_approval_for`

## Optional Governance Metadata

Skills may include activation hints:

```yaml
activation:
  keywords:
    - example
  required_files:
    - pyproject.toml
  optional_tools:
    - pytest
    - git
category: development
scope: bundled
status: stable
visibility: public
bucket: development
```

`activation.keywords` describe task words that suggest the skill may apply.
`activation.required_files` describe repository files that make the skill relevant.
`activation.optional_tools` lists local tools that may be useful but are not required by the schema.

Allowed `scope` values are `bundled`, `optional`, and `project`.
Allowed `category` values are `development`, `research`, `infrastructure`, `documentation`, `self-improvement`, `domain`, and `productivity`.

Optional metadata is not required for older skills. Invalid `scope` or malformed `activation` is an error. Unknown `category` is reported as a warning.

## Lifecycle, Visibility, and Buckets

Skills may also include lifecycle metadata:

- `status`: `stable`, `experimental`, `in-progress`, or `deprecated`
- `visibility`: `public`, `internal`, or `hidden`
- `bucket`: `development`, `domain`, `productivity`, `research`, `infrastructure`, `self-improvement`, or `misc`

Missing lifecycle metadata does not fail validation. Invalid values fail validation. Deprecated skills produce validation warnings. Hidden skills are excluded from the generated public skill index.

Use lifecycle metadata to preserve developer control:

- `in-progress` means the skill is being drafted.
- `experimental` means it is usable with caution.
- `stable` means it has review and verification evidence.
- `deprecated` means it should be avoided unless migration context is needed.

## Recommended Sections

In addition to the standard required sections, bundled skills should include:

- `## Quick Reference`
- `## Pitfalls`
- `## Verification`

Missing recommended sections produce validation warnings, not failures.

## Validation

Run:

```bash
karakana skill validate-all
```

Validation checks required metadata, allowed risk levels, list-valued tool fields, optional governance metadata, and markdown sections.

One skill can be validated by name or path:

```bash
karakana skill validate brainstorm-verbalized-sampling
karakana skill validate skills/brainstorm-verbalized-sampling
```

## Pre-PRD Elicitation

These are general-purpose skills for software, research, infrastructure, documentation, operations, and product projects. They do not require Django, Karakana-specific memory, a particular repository layout, or a PRD-based workflow.

For ambiguous work, use `requirements-elicitation` before the project's existing specification or planning workflow. Use `grill-with-docs` to challenge the plan against whatever authoritative evidence the project provides, and use `brainstorm-verbalized-sampling` only when several plausible approaches remain.

For Karakana-managed projects, save the reviewed elicitation result and pass it into the existing PRD workflow:

```bash
karakana requirements prd \
  --from-file .karakana/requirements-elicitation/<elicit-id>.md \
  --project msc-platform \
  --skillpack msc-platform
karakana requirements stories --from-prd <req-id>
karakana requirements issues --from-prd <req-id>
karakana requirements ready <req-id>
```

Karakana does not currently define a `requirements elicit` command or elicitation store. The markdown handoff preserves the boundary between conversational decision work and the existing structured PRD/story/issue/readiness artifacts. Add a command only after a stable elicitation schema and repeated artifact lifecycle justify it.

## Next-Milestone Decisions

Use `next-milestone-decision` after completing or reviewing a milestone. It gathers project evidence, prioritizes unresolved blockers, compares candidate directions with `brainstorm-verbalized-sampling` when needed, and generates a copy-ready instruction.

```bash
karakana milestone next \
  --project <project> \
  --skillpack <skillpack> \
  --write-instructions
```

Strict mode returns non-zero when required context is missing or P0/P1 planning blockers remain. The command writes local decision artifacts only; execution is always a separate explicit step.

## Session Handoffs

Use `karakana-handoff` to create a compact continuation package, not a conversational summary. Start a task with:

```bash
karakana handoff load --project <project> --skillpack <skillpack>
```

End with:

```bash
karakana handoff refresh --project <project> --skillpack <skillpack> --purpose "End of task handoff"
```

Reference durable artifacts instead of duplicating them. Verify recovered, stale, or missing references with `karakana handoff doctor --project <project>`.

## Skill Indexes

Generate a public skill index in dry-run mode with:

```bash
karakana skill index
```

Write `skills/README.md` only when explicitly requested:

```bash
karakana skill index --write
```

The index groups visible skills by bucket and includes name, status, description, and path. `visibility: hidden` skills are not included in the public index.

## Adding a Skill

Before adding a skill, check whether an existing skill can be safely extended. Add a new skill when the workflow is repeated, focused, and distinct enough to need its own activation guidance.

A new skill should include:

- `SKILL.md`,
- valid metadata,
- activation guidance when useful,
- quick reference,
- core concepts,
- pitfalls,
- verification steps,
- examples,
- safety rules,
- output format,
- eval cases for non-trivial skills,
- documentation or index updates,
- validation with `karakana skill validate`.

## Promotion and Deprecation

Promotion follows `docs/skill-promotion-policy.md`.

Do not promote a skill to `stable` without human review and verification evidence. When deprecating a skill, document why, identify any replacement, and decide whether it should remain visible.

## Evals

Skill-specific evals live under:

```text
skills/<skill>/evals/
```

Run all evals with:

```bash
karakana eval run
```

Run one skill's evals with:

```bash
karakana eval run --skill <skill>
```
