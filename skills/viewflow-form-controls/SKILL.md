---
name: viewflow-form-controls
description: Use this skill when designing, implementing, or auditing Viewflow/Django form controls, including normal fields, grouped layouts, dynamic workflow forms, date/time widgets, AJAX model selects, multi-selects, dependent controls, validation, and Material-accessible form behavior.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - Viewflow form
    - form controls
    - Django form widget
    - AjaxModelSelect
    - AjaxMultipleModelSelect
    - FormAjaxCompleteMixin
    - InlineCalendar
    - date picker
    - timestamp field
    - dynamic workflow form
    - workflow task form
    - form validation
    - autocomplete select
  required_files: []
  optional_tools:
    - grep
    - pytest
    - browser-test
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - frontend_design_system_change
  - accessibility_pattern_change
  - workflow_form_contract_change
  - permission_change
---
# Viewflow Form Controls

## Purpose

Guide agents to build and audit Viewflow/Django form experiences using
Viewflow’s form layout and widget model, Material-compatible controls,
human-centered grouping, accessible semantics, and project design-system rules.

This skill bridges backend workflow definitions and operator-facing form UX. It
keeps agents from hand-rendering fields, scattering widget behavior through
templates, or treating complex controls such as AJAX selects and timestamp
pickers as one-off UI patches.

## When to use this skill

Use for:

- Viewflow task forms, CRUD forms, setup forms, and dynamic workflow forms;
- normal text, number, date/time, boolean, select, file, and textarea controls;
- large foreign-key or many-to-many selections that need autocomplete;
- `AjaxModelSelect`, `AjaxMultipleModelSelect`, `FormAjaxCompleteMixin`, and
  autocomplete endpoint behavior;
- date, timestamp, and calendar picker behavior such as `InlineCalendar`;
- dependent fields, conditional field visibility, formsets, and inline rows;
- validation, error, help-text, required/optional, disabled, and readonly states;
- browser-level verification of form rendering and interactions.

## When not to use this skill

Do not use for backend-only model changes with no rendered form impact. Do not
use this skill to redesign the whole page hierarchy; combine with
`material-hcd-interface` for screen composition, `design-system-governance`
for reusable token/component changes, and `accessibility-wcag-audit` for
formal accessibility review. Use `interaction-state-design` when a form has
async submit, validation, loading, conflict, stale-data, permission, or
success/queued states. Use `ux-writing` for labels, help text, validation
messages, confirmations, and submit-action labels. Use `design-qa-playwright`
when form/control behavior needs browser evidence, keyboard interaction checks,
screenshots, or end-to-end verification.

## Quick Reference

- Viewflow form logic belongs in Python form/layout definitions; templates own
  rendering and should stay thin.
- Render ordinary form fields through Viewflow/Material form rendering. Do not
  hand-render Django fields unless building a reusable missing widget adapter.
- Use visible labels. Place help text near the control. Show field-level and
  form-level errors in the user’s task context.
- Use `ux-writing` when revising labels, placeholders, help text, validation
  errors, confirmation copy, or submit/cancel actions.
- Group fields by the operator’s decision path, not by model order.
- Use AJAX autocomplete for large or dynamic model choices; do not load large
  option lists into a select.
- Use a calendar/date/time control for date/timestamp fields where direct
  typing is error-prone, while preserving keyboard entry and explicit formats.
- Define empty, loading, no-results, permission-denied, validation-error,
  network-error, disabled, readonly, conflict, stale-data, queued, and
  successful-submit states for complex controls.
- Keep UI visibility separate from authorization. Autocomplete endpoints and
  form submit handlers must enforce permissions server-side.
- Verify with focused render tests and browser tests for dynamic controls.

## Core concepts

- **Form contract**: the form declares fields, order, grouping, widgets, help,
  validation, and permissions. The template renders that contract consistently.
- **Control semantics**: choose controls by data shape and task risk. Short
  enumerations can be selects/radios; large lookups need autocomplete; dates
  need date/time affordances; repeated rows need formsets or inlines.
- **Material-accessible behavior**: every control needs label, state, feedback,
  focus, keyboard path, and error semantics. Material appearance is not enough;
  use `accessibility-wcag-audit` for accessibility gates.
- **Progressive disclosure**: reveal dependent fields only when relevant, but
  never hide required information needed to complete the primary task.
- **Server authority**: AJAX suggestions, disabled fields, hidden fields, and
  client state are hints only. The server validates identity, permission,
  allowed choices, and workflow state.
- **Dynamic workflow safety**: generated forms must produce predictable,
  auditable controls and must not turn workflow metadata into unsafe arbitrary
  HTML.

## Evidence-backed basis

Viewflow’s forms documentation states that form logic is separated from HTML
rendering: field layout is defined in Python and templates handle the HTML.
Viewflow also renders forms using Google Material Web Components and supports
Hotwire/Turbo style submission through `<vf-form/>`.

Viewflow widget documentation includes:

- `InlineCalendar` for full-sized month calendar date selection;
- `AjaxModelSelect` for ModelChoiceField autocomplete;
- `AjaxMultipleModelSelect` for ModelMultipleChoiceField autocomplete;
- `FormAjaxCompleteMixin` for serving autocomplete suggestions from the form
  view.

Use current project source and installed Viewflow version as the final
implementation authority.

## Standard workflow

1. **Classify the form.** Name whether it is a task, setup, CRUD, review,
   approval, dynamic workflow, or inline/formset form.
2. **Map the transaction.** Identify the user, object, workflow state, primary
   submit outcome, cancellation/back path, and permission boundary.
3. **Inspect existing form system.** Check project base templates, form
   partials, Viewflow layouts, widgets, CSS tokens, and comparable forms.
4. **Choose field groups.** Group by operator task sequence: identify object,
   enter required facts, add measurements/evidence, confirm outcome.
5. **Choose controls by data shape.**
   - Short fixed choices: select, radio, segmented choice, or chips based on
     density and risk.
   - Long model choices: `AjaxModelSelect`.
   - Long multi-model choices: `AjaxMultipleModelSelect`.
   - Date-only values: date picker/calendar plus keyboard input.
   - Date/time or timestamps: date/time control with timezone/format help.
   - Repeated child rows: formset/inline pattern with add/remove states.
   - Dependent values: conditional controls with server revalidation.
6. **Define complex-control states.** Cover initial, focus, loading, results,
   no results, selected, cleared, invalid, disabled, readonly, network failure,
   permission denial, and stale workflow state.
7. **Implement through Viewflow.** Prefer form/layout/widget definitions and
   reusable widget adapters over template conditionals or page-local JavaScript.
8. **Secure AJAX and submit paths.** Validate permissions, tenant/lab/study
   context, allowed queryset, workflow state, and submitted IDs server-side.
9. **Apply design-system rules.** Use project spacing, density, field width,
   error, help, chip, and autocomplete styling. Add a reusable rule when a
   pattern recurs.
10. **Verify.** Add focused tests for render output, autocomplete JSON,
    validation, permissions, browser-level interaction, and accessibility gates
    where available.

## Required checks

- Is the form rendered through the project’s Viewflow/Material renderer?
- Are fields ordered/grouped by the user’s work sequence?
- Does every visible control have a visible label?
- Is help text near the field and written for the operator?
- Has field/help/error/action copy been checked through `ux-writing`?
- Are required/optional states clear without relying only on color?
- Are field-level and form-level errors visible, associated, and actionable?
- Are large model choices served through autocomplete rather than huge selects?
- Does autocomplete enforce permission and queryset scope server-side?
- Does the widget define loading, no-results, network-error, selected, and
  cleared states?
- Are form and widget states planned with `interaction-state-design` when the
  behavior has async, stale, conflict, or recovery implications?
- Do date/timestamp controls provide calendar/time selection and typed fallback?
- Is timezone/format meaning explicit for timestamp fields?
- Are dependent controls revalidated by the server?
- Are disabled/readonly controls used only when their meaning is clear?
- Are hidden fields treated as untrusted input?
- Does the test plan include render assertions and browser interaction checks
  for complex controls?
- Does accessibility verification include keyboard, focus, labels, errors, and
  ARIA/combobox behavior through `accessibility-wcag-audit` where relevant?

## Safety rules

- Do not bypass Viewflow/Django validation with client-only checks.
- Do not expose unauthorized model records through autocomplete suggestions.
- Do not trust submitted IDs just because they were suggested by the UI.
- Do not hand-render ordinary fields when Viewflow rendering can be extended.
- Do not inject workflow-provided labels/help/options as raw HTML.
- Do not hide critical workflow requirements behind conditional controls without
  a visible explanation.
- Do not introduce broad JavaScript/CSS that changes unrelated forms.

## Output format

```markdown
## Viewflow Form Controls Plan

- Form/job:
- Primary users:
- Data/control inventory:
- Field grouping:
- Widget decisions:
- Complex-control states:
- Permissions/server validation:
- Design-system rules:
- Implementation slices:
- Verification:
- Remaining risk:
```

## Examples

- A specimen intake timestamp field should render with a date/time affordance,
  format help, validation errors, and typed fallback.
- A storage position field with thousands of positions should use scoped AJAX
  autocomplete and never expose positions outside the active lab context.
- A workflow task assigning several specimens should use an AJAX multiple model
  select or a task-specific selection table, not a full unfiltered multiselect.
- A dynamic DBS extraction form should group sample identity, extraction inputs,
  measurements, and confirmation separately instead of mirroring metadata order.

## Pitfalls

- Letting database field order define the form experience.
- Loading thousands of model choices into a normal select.
- Treating autocomplete as only a frontend concern.
- Adding date widgets without timezone/format clarity.
- Using placeholders instead of labels.
- Creating a custom widget without empty/loading/error/no-results states.
- Fixing one form with page-local CSS instead of adding a reusable field/control
  rule.

## Verification

- `karakana skill validate skills/viewflow-form-controls`
- `karakana eval run --case skills/viewflow-form-controls/evals/viewflow-form-controls.yml`
- `karakana skill validate-all`
- For projects: focused Django tests for form rendering/autocomplete plus
  browser tests for dynamic control interaction.
