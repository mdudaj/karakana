---
name: ux-writing
description: "Use this skill when writing, reviewing, or standardizing user-facing interface copy: labels, buttons, empty states, errors, warnings, confirmations, help text, notifications, navigation names, status messages, and operator-facing workflow language."
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - UX writing
    - microcopy
    - interface copy
    - button labels
    - field labels
    - error messages
    - empty state copy
    - help text
    - confirmation copy
    - notification copy
    - navigation labels
    - status messages
    - content design
  required_files: []
  optional_tools:
    - grep
    - pytest
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - terminology_change
  - workflow_copy_contract_change
  - accessibility_pattern_change
  - frontend_design_system_change
---
# UX Writing

## Purpose

Guide agents to write and audit interface copy that is clear, concise,
consistent, accessible, domain-accurate, and action-oriented. This skill covers
labels, buttons, empty states, errors, warnings, confirmations, help text,
notifications, navigation names, status messages, and workflow language.

Use this skill to prevent production UI from containing implementation guidance,
backend verbs, inconsistent terminology, vague errors, hostile validation,
unsupported recovery actions, or copy that forces users to infer what to do.

## When to use this skill

Use for:

- page titles, subtitles, navigation labels, tabs, filters, buttons, links, and
  action labels;
- field labels, help text, placeholders, required/optional copy, validation
  errors, and form summaries;
- empty, filtered-empty, no-results, loading, success, queued, stale, blocked,
  permission-denied, warning, and system-error messages;
- confirmation dialogs, destructive actions, undo/retry copy, notifications,
  support/help content, and operator instructions;
- terminology alignment in regulated or domain-heavy systems such as LIMS,
  healthcare, finance, and research platforms.

## When not to use this skill

Do not use for long-form documentation, marketing copy, or research writing
unless it appears inside the product UI. Do not rename domain concepts without
checking project terminology, permissions, workflow semantics, and stakeholder
impact.

Combine with:

- `material-hcd-interface` for screen hierarchy;
- `interaction-state-design` for state-specific copy;
- `accessibility-wcag-audit` for labels, instructions, errors, and status
  messages;
- `visual-design-review` for screenshot critique;
- `viewflow-form-controls` for form labels/help/validation;
- `design-system-governance` when copy patterns become reusable components;
- `design-qa-playwright` when critical labels, messages, empty states, or
  notification copy should be asserted in browser tests.

## Quick Reference

- Write for the user’s task, not the database operation.
- Use simple, direct, present-tense language.
- Prefer action labels that name the outcome: `Start intake`, `Claim task`,
  `Send invitation`, `Clear filters`.
- Avoid vague verbs: `Submit`, `Process`, `Manage`, `Handle`, unless the
  domain uses them unambiguously.
- Keep labels consistent across navigation, buttons, headings, filters, and
  help text.
- Empty/error copy should say what happened, why it matters, and what the user
  can do next.
- Do not offer actions the system cannot support.
- Do not blame the user; describe the issue and recovery.
- Keep implementation rationale out of production UI; put it in specs/docs.
- Preserve safety, audit, and permission meaning in operational systems.

## Core concepts

- **Interface copy**: short text that helps users understand, decide, act, and
  recover inside the product.
- **Action label**: button/link text that names the user-visible outcome.
- **State copy**: text for empty, loading, error, success, warning, blocked,
  stale, or permission states.
- **Terminology contract**: approved words for product/domain concepts.
- **Recovery copy**: instructions that help the user correct a problem or take
  the next safe action.
- **Accessible copy**: labels, instructions, errors, and status messages that
  are visible and programmatically usable where required.

## Evidence-backed basis

Read `references/interface-copy-patterns.md` before non-trivial copy revisions.

Key source directions:

- Material communication guidance emphasizes concise, direct language, writing
  for all reading levels, consistent words, present tense, numerals, and
  component-specific writing.
- WCAG requires labels or instructions for user input, text identification of
  input errors, and programmatically determinable status messages.
- W3C WAI form guidance recommends labels, grouping, instructions, validation,
  notifications, and short forms that ask only what is required.
- Google error-message guidance recommends readable placement, progressive
  disclosure for long explanations, and avoiding color-only error cues.
- Material error guidance warns against unsupported recovery actions such as
  offering retry when the system can determine retry will fail.

## Standard workflow

1. **Classify copy.** Navigation, action, form field, help text, state message,
   error, warning, confirmation, notification, or support content.
2. **Identify user/task/context.** Role, object, workflow state, risk, and what
   the user needs to do next.
3. **Check terminology.** Inspect project vocabulary, route names, workflow
   labels, and comparable screens.
4. **Write the minimum useful copy.** Make it specific, direct, and scoped to
   the component.
5. **Use the right formula.**
   - Button/link: verb + object/outcome.
   - Empty state: current state + why + next action.
   - Error: what happened + recovery + support/escalation if needed.
   - Warning: risk + consequence + safe next step.
   - Confirmation: action + affected object + reversibility.
   - Success: completed outcome + next likely action.
6. **Check accessibility.** Labels are visible; instructions/errors are
   associated; status updates are perceivable; icon-only actions have names.
7. **Check operational safety.** Copy must not obscure permission, audit,
   quality, irreversible, or workflow-state implications.
8. **Standardize patterns.** If the copy pattern recurs, add it to reusable
   components/docs rather than rewriting per page.
9. **Verify.** Add assertions for critical labels/messages and browser checks
   for state copy where available.

## Required checks

- Does the copy state the user-visible outcome?
- Is terminology consistent with the project/domain vocabulary?
- Is the copy specific enough to prevent wrong-object or wrong-action errors?
- Does the copy avoid backend-only verbs and implementation details?
- Are field labels visible and descriptive?
- Are placeholders treated as examples/hints, not labels?
- Are errors textual, actionable, and near the problem?
- Are empty/filtered-empty/no-results states distinct?
- Are warnings and destructive confirmations explicit about consequence?
- Does success copy distinguish completed from queued/background work?
- Are status messages accessible and not color-only?
- Are support/escalation actions only shown when actually available?

## Safety rules

- Do not rename regulated, legal, clinical, financial, or laboratory terms
  without checking approved terminology.
- Do not soften warnings or irreversible actions in a way that hides risk.
- Do not expose restricted data in error, empty, permission, or notification
  copy.
- Do not replace labels with placeholders.
- Do not offer retry, undo, reset, support, or escalation unless the product
  supports it.
- Do not blame the user for validation or workflow failures.

## Output format

```markdown
## UX Writing Review

- Copy surface:
- User/task/context:
- Terminology checked:
- Current issue:
- Recommended copy:
- Rationale:
- Accessibility/safety checks:
- Reusable pattern:
- Verification:
- Remaining risk:
```

## Examples

- Button: use `Start specimen intake`, not `Submit`.
- Empty state: `No tasks need your attention. New tasks appear when specimens,
  batches, QC reviews, storage work, or workflows require action.`
- Filtered-empty: `No tasks match these filters. Clear filters or change your
  search.`
- Error: `Storage position is already occupied. Choose another position or open
  the box to review its contents.`
- Queued success: `Manifest upload queued. We’ll notify you when validation is
  complete.`
- Confirmation: `Dispose material DNA-2026-0142-A? This cannot be undone after
  approval is recorded.`

## Pitfalls

- Writing from backend state names instead of user outcomes.
- Using `Manage` for every navigation item.
- Saying `No data` without context.
- Saying `Something went wrong` without recovery.
- Making labels disappear after typing.
- Using `Success` when the operation is only queued.
- Leaving design or implementation notes visible in the UI.

## Verification

- `karakana skill validate skills/ux-writing`
- `karakana eval run --case skills/ux-writing/evals/ux-writing.yml`
- `karakana skill validate-all`
- For projects: render/browser assertions for critical labels, errors, empty
  states, confirmations, notifications, and permission messages.
