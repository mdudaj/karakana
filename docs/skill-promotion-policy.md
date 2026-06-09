# Skill Promotion Policy

Karakana skills move through a simple lifecycle:

```text
in-progress -> experimental -> stable -> deprecated
```

Lifecycle metadata is advisory governance. It helps agents choose the right level of caution without making experimental work impossible.

## In Progress to Experimental

A skill may move from `in-progress` to `experimental` when:

- it has valid metadata,
- it has a clear purpose,
- it passes skill validation,
- it has at least one realistic example,
- safety rules are documented.

## Experimental to Stable

A skill may move from `experimental` to `stable` when:

- it has been used successfully,
- it has passing evals if non-trivial,
- it has clear verification steps,
- it has no unsafe broad tool permissions,
- it appears in the skill index,
- it has human review.

## Deprecation

A skill may become `deprecated` when:

- it is replaced,
- it is no longer useful,
- it is unsafe,
- it conflicts with newer project conventions,
- it is too broad and should be split.

Deprecation should document:

- reason for deprecation,
- replacement skill if available,
- migration guidance,
- whether the skill should remain visible or become hidden.

Deprecated skills may remain in the public index when they are still useful for migration context. Use `visibility: hidden` only when the skill should not be advertised.
