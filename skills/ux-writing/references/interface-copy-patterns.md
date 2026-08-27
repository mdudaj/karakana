# Interface Copy Patterns

Use this reference when writing or reviewing product UI copy.

## General rules

- Prefer short, direct, present-tense sentences.
- Use consistent terms for the same concept.
- Use numerals when they improve scanning.
- Say what the user can do, not what the system implementation is doing.
- Use user-facing operational language. Avoid implementation or delivery-process
  terms in normal product UI, including `protocol`, `harness`, `artifact`,
  `readiness`, `migration`, `fixture`, `seed`, `projection`, `purge`, and
  backend-only state names, unless the screen is explicitly a technical
  diagnostic/admin surface.
- Avoid unnecessary explanation in the default UI; use help/progressive
  disclosure for details.
- Keep copy close to the control/state it explains.

## Component patterns

### Navigation

Navigation labels should name destinations, not actions.

Good:

- `Tasks`
- `Specimens`
- `Storage`
- `Reports`
- `Setup`

Avoid:

- `Manage Tasks`
- `Do Specimen Things`
- `Misc`

### Buttons and links

Use verb + object/outcome.

Good:

- `Claim task`
- `Start intake`
- `Move to storage`
- `Clear filters`
- `Send invitation`

Avoid vague labels:

- `Submit`
- `Process`
- `OK`
- `Here`

### Field labels

Labels should remain visible and describe expected input.

Good:

- `Collection date`
- `Storage position`
- `Extraction timestamp`

Placeholder/hint:

- `Example: BX-001 / B07`

The placeholder is not the label.

### Help text

Use help text for format, consequence, or local rules.

Good:

- `Use the time the physical extraction started.`
- `Search by box, rack, or position code.`

### Empty states

Formula:

```text
Current state.
Why/when this changes.
Next action if available.
```

Examples:

- `No tasks need your attention. New tasks appear when specimens, batches, QC
  reviews, storage work, or workflows require action.`
- `No storage positions are configured for this lab. Import a storage template
  or create positions before putaway.`

### Filtered-empty and no-results

Filtered-empty:

```text
No tasks match these filters. Clear filters or change your search.
```

No-results:

```text
No specimen matches “SMP-2026-9999”. Check the identifier or broaden your search.
```

### Errors

Formula:

```text
What happened.
What remains safe/unsafe.
What to do next.
```

Examples:

- `Storage position is already occupied. Choose another position or open the box
  to review its contents.`
- `Email was not sent. Copy the invitation link and send it manually.`

Avoid:

- `Invalid input`
- `Error`
- `Failed`

### Warnings

Warnings should name the risk and consequence.

Example:

```text
This material is on quality hold. You need manager approval before it can be
used in downstream processing.
```

### Confirmations

Formula:

```text
Action + affected object + consequence/reversibility.
```

Examples:

- `Deactivate user Asha M.? They will lose access after their current session
  expires.`
- `Reverse this storage movement? A compensating movement will be recorded.`

### Success and queued states

Distinguish completed from queued.

Completed:

```text
Task completed. The specimen is ready for QC review.
```

Queued:

```text
Manifest upload queued. We’ll notify you when validation is complete.
```

### Permission states

Explain the boundary without leaking restricted details.

Example:

```text
You do not have permission to approve this task. Ask a lab manager to review it.
```

### Policy and system-status copy

State the current user-visible status and consequence. Keep implementation
details in documentation or diagnostics.

Good:

- `Default retention settings are active. Records are not automatically deleted.`
- `Email was not sent. Copy the invitation link and send it manually.`
- `Storage setup is incomplete. Add locations before recording putaway.`

Avoid:

- `Default until a laboratory retention policy is recorded. No automated purge is implemented.`
- `SMTP backend failed. Render fallback command.`
- `Artifact readiness is missing.`

## LIMS/operator-specific rules

- Include object identity when wrong-object action is plausible.
- Preserve audit meaning: `recorded`, `approved`, `reversed`, `disposed`, and
  `queued` are not interchangeable.
- Use `occurred at` and `recorded at` only when both timestamps matter.
- Avoid patient/person identifiers in copy where specimen IDs are sufficient.
- Use role names users recognize: `Lab manager`, `Technician`, `Reviewer`.
- Keep manual fallback copy explicit when automation can fail.

## Review checklist

- Does this copy help the user act or recover?
- Is it shorter without losing safety?
- Does it use approved terminology?
- Does it expose restricted data?
- Does it imply unsupported functionality?
- Does it distinguish completed, queued, failed, and blocked?
- Is it testable in render/browser assertions if critical?
