# Skills

Karakana skills are reusable workflow instructions stored as markdown under `skills/<name>/SKILL.md`.

Skills are for guidance: they describe when to use a workflow, what risks to check, what tools may help, and how to verify the result. Tools are for deterministic execution and safety-gated operations.

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
```

`activation.keywords` describe task words that suggest the skill may apply.
`activation.required_files` describe repository files that make the skill relevant.
`activation.optional_tools` lists local tools that may be useful but are not required by the schema.

Allowed `scope` values are `bundled`, `optional`, and `project`.
Allowed `category` values are `development`, `research`, `infrastructure`, `documentation`, `self-improvement`, and `domain`.

Optional metadata is not required for older skills. Invalid `scope` or malformed `activation` is an error. Unknown `category` is reported as a warning.

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
