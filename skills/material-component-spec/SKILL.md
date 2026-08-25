---
name: material-component-spec
description: Use this skill when specifying, building, or auditing reusable UI components with Material-compatible anatomy, variants, states, slots, tokens, accessibility, responsive behavior, Viewflow/frontend mapping, and acceptance criteria.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - component spec
    - component anatomy
    - reusable component
    - component variants
    - component states
    - slots
    - design tokens
    - Material component
    - Atomic Design
    - component library
    - Viewflow component
    - frontend component
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
  - component_contract_change
---
# Material Component Spec

## Purpose

Guide agents to define, implement, and audit reusable UI components as durable
design-system contracts: anatomy, slots, variants, states, token mapping,
accessibility, responsive behavior, framework/Viewflow mapping, and acceptance
criteria.

Use this skill when a UI issue should become a reusable component rule rather
than a page-local markup or CSS patch.

## When to use this skill

Use for:

- new reusable components, partials, widgets, cards, tables, chips, tabs,
  empty states, banners, shell actions, filters, form controls, and task rows;
- revising component anatomy, variants, density, icons, states, token use, or
  acceptance criteria;
- converting repeated page-level UX critique into a shared component contract;
- mapping Material component semantics into project frameworks such as
  Viewflow/Django templates or frontend component libraries.

## When not to use this skill

Do not use for one-off copy edits or backend-only work. Do not use it to design
full page hierarchy; combine with `material-hcd-interface`. For state behavior
combine with `interaction-state-design`; for WCAG review use
`accessibility-wcag-audit`; for Viewflow forms use `viewflow-form-controls`;
for token policy and token mapping use `design-token-system`; for critique that
decides whether a component contract is needed use `visual-design-review`; for
rendered component verification, screenshots, responsive checks, and DOM
assertions use `design-qa-playwright`.

## Quick Reference

- A component spec is a contract, not a screenshot description.
- Define the component job before styling.
- Specify anatomy: root, required slots, optional slots, action regions,
  metadata regions, icon policy, and content constraints.
- Specify variants by meaning, not by arbitrary color.
- Specify states: enabled, hover, focus, pressed, selected, dragged if relevant,
  disabled, loading, empty, error, warning, success, readonly, permission, and
  stale as applicable.
- Map every visual decision to a token or existing design-system rule; use
  `design-token-system` when token layers, aliases, contrast, or migration are
  involved.
- Include accessibility: name/role/value, keyboard, focus, target size,
  contrast, labels, status messages, and reduced motion.
- Define responsive behavior and density rules.
- Define implementation mapping for the target framework without hardcoding a
  single technology as the universal rule.
- Add tests/evals/browser checks for the component contract.

## Core concepts

- **Component job**: the user task the component helps complete.
- **Anatomy**: root structure and named slots/regions that pages compose.
- **Variant**: intentional semantic variation, such as primary/secondary,
  neutral/warning/error, compact/comfortable, or read-only/editable.
- **State**: interaction/system condition such as enabled, hover, focus,
  pressed, selected, disabled, loading, error, permission-denied, or stale.
- **Token mapping**: color, type, spacing, radius, elevation, motion, and size
  values referenced through design-system tokens.
- **Framework mapping**: how the contract appears in code: Viewflow template,
  Django form widget, web component, React/Vue/Svelte component, CSS class, or
  server-rendered partial.
- **Acceptance criteria**: observable checks that prove the component behaves
  consistently across examples and states.

## Evidence-backed basis

Read `references/component-contracts.md` before non-trivial component work.

Key source directions:

- Material state guidance defines enabled, disabled, hover, focused, pressed,
  and dragged states and emphasizes consistent application across components.
- Atomic Design is useful as a mental model for components from atoms through
  templates/pages, but final implementation language should stay understandable
  to stakeholders.
- DTCG design-token work treats tokens as platform-agnostic named values that
  can be shared across tools/technologies.
- Public UI-agent skill systems split component specification, tokens,
  accessibility, design review, and code/framework adaptation into composable
  skills rather than one overloaded prompt.

## Standard workflow

1. **Classify the component.** Name whether it is an atom/control, molecule,
   organism/section, template/partial, Viewflow widget, or page-specific
   extraction candidate.
2. **State the job.** Identify user role, task, decision risk, and why this
   should be reusable.
3. **Inspect existing system.** Check tokens, CSS, templates, component
   partials, widgets, comparable pages, and Material/Viewflow equivalents.
4. **Define anatomy.** Root, slots, text hierarchy, icon/media area, status
   area, metadata, actions, helper/error area, and allowed nesting.
5. **Define variants.** Semantic variants, density, size, alignment, tone,
   destructive/warning behavior, and permission/readonly treatment.
6. **Define states.** Interaction states, system states, validation states,
   async states, empty/error states, and combinations that can occur.
7. **Map tokens.** Every repeated visual value should reference a token or
   documented design-system rule.
8. **Define accessibility.** Semantics, labels, keyboard, focus, contrast,
   target size, announcements, and reduced motion.
9. **Map implementation.** Name target framework classes/templates/widgets and
   forbid page-local duplication where a reusable abstraction is required.
10. **Define acceptance criteria.** DOM/class assertions, fixture examples,
    browser checks, visual review points, and regression tests.
11. **Update documentation/evals.** If the component creates a reusable rule,
    update the project design-system docs or skill references.

## Required checks

- Is the component job clear?
- Is the component reusable, or should it remain page-local?
- Did `visual-design-review` identify a repeated visual/component issue that
  justifies this contract?
- Are required and optional slots named?
- Are variants semantic and bounded?
- Are all relevant Material interaction states covered?
- Are loading, empty, error, disabled, readonly, permission, and stale states
  covered when applicable?
- Are token mappings explicit?
- Are token layers and contrast-sensitive mappings routed through
  `design-token-system`?
- Are labels, values, metadata, and actions structurally separated?
- Are icon sizes, containers, and alignment specified where icons are used?
- Are keyboard/focus/accessibility requirements specified?
- Is responsive/density behavior specified?
- Is the Viewflow/framework mapping explicit?
- Are acceptance criteria testable?
- Are browser/DOM/screenshot acceptance checks routed through
  `design-qa-playwright` when the component has visible layout, responsive, or
  interaction behavior?

## Safety rules

- Do not create broad global component changes without checking affected pages.
- Do not copy another design system’s brand styling or proprietary tokens.
- Do not use variants as a backdoor for arbitrary page-local colors.
- Do not remove visible labels or focus indicators for visual polish.
- Do not use disabled UI state as a substitute for server permission checks.
- Do not force Atomic Design terminology into user-facing documentation when
  plain component/section/page language is clearer.

## Output format

```markdown
## Material Component Spec

- Component:
- Job/use cases:
- Reuse boundary:
- Anatomy/slots:
- Variants:
- States:
- Token mapping:
- Accessibility:
- Responsive/density:
- Framework/Viewflow mapping:
- Acceptance criteria:
- Verification:
- Remaining risk:
```

## Examples

- KPI card: root card, left accent, icon container, value, label, supporting
  text, optional trend, semantic tone variants, loading/empty/error states,
  tokenized icon size and spacing.
- Filter toolbar: search region, more-filters action, active filter chips,
  filtered-empty behavior, clear action, responsive wrapping rules.
- Viewflow form field group: legend/title, field rows, help/error slots,
  disabled/readonly rules, validation summary behavior.
- Task row: priority marker, task title, object context, status chip, due time,
  owner, row action, blocked/permission/loading states.

## Pitfalls

- Describing only the default screenshot.
- Creating variants for every page request.
- Leaving icon size/alignment unspecified.
- Forgetting hover/focus/pressed/disabled/loading/error states.
- Using page-local CSS instead of tokens.
- Using cards for dense data that should be a list/table component.
- Treating framework code as the design-system contract.

## Verification

- `karakana skill validate skills/material-component-spec`
- `karakana eval run --case skills/material-component-spec/evals/material-component-spec.yml`
- `karakana skill validate-all`
- For projects: component render tests, browser tests for key states, and
  accessibility checks through `accessibility-wcag-audit`.
