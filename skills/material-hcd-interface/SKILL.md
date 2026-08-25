---
name: material-hcd-interface
description: Use this skill when planning, reviewing, or implementing user-facing screens where Material 3 components, layout, grid, navigation, cards, tabs, filters, empty states, forms, or action organization must follow human-centered task hierarchy rather than page-local styling.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - human centered design
    - HCD
    - Material 3
    - screen layout
    - component organization
    - UI critique
    - UX critique
    - dashboard layout
    - form layout
    - filters
    - empty state
    - cards
    - tabs
    - navigation
  required_files: []
  optional_tools:
    - grep
    - pytest
    - web_search
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - run_tests
requires_approval_for:
  - design_system_contract_change
  - frontend_design_system_change
  - accessibility_pattern_change
  - navigation_information_architecture_change
---
# Material HCD Interface

## Purpose

Guide agents to construct and critique user-facing interfaces by combining
human-centered task hierarchy with Material 3 component, layout, and adaptive
composition rules.

Use this skill to prevent repeated page-local fixes such as “move this button,”
“make this card better,” or “add spacing here” from becoming isolated CSS
patches. The expected outcome is a screen that answers the user’s job in the
right order, uses Material components for their intended role, and applies
project styling through reusable design-system tokens/components.

## When to use this skill

Use for:

- dashboards, landing pages, worklists, admin surfaces, operational cockpits,
  help centers, forms, detail pages, and configuration pages;
- critique or redesign of spacing, hierarchy, density, action placement,
  filters, empty states, tabs, cards, tables, and navigation;
- conversion of repeated UX critique into durable project design rules;
- planning browser-visible UI before implementation.

## When not to use this skill

Do not use for backend-only work, visual branding/logo generation, copy-only
edits, or a tiny one-off CSS correction that does not reveal a reusable rule.
For framework-specific implementation, combine with the project skill such as
`viewflow-material-ui`, `viewflow-form-controls`, `material-component-spec`,
`design-token-system`, `visual-design-review`, `interaction-state-design`,
`ux-writing`, `accessibility-wcag-audit`, `design-qa-playwright`,
`viewflow-framework`, or a
product-specific design system skill.

## Quick Reference

- Start from the user's job, not the database model or available features.
- Use `ux-skill-router` first when the request could require several UX
  specializations and the right sequence is unclear.
- Use `visual-design-review` when the user asks for screenshot critique,
  visual polish, hierarchy/density review, or why a UI “does not look right.”
- Order content by urgency and actionability: attention, ready work, context,
  metrics, secondary actions, details.
- Choose Material components by role: navigation for destinations, tabs for
  sibling views, cards for grouped summaries/actions, chips for compact
  filters/status, badges for small counts, tables/lists for dense comparison,
  dialogs/sheets for temporary focused decisions.
- Use progressive disclosure for advanced or conditional controls, but keep the
  primary task path complete without opening hidden panels.
- Put actions where their scope is clear: page actions in the page/header action
  lane, section actions in section headers, row actions at row end, destructive
  or high-risk actions behind confirmation/permission gates.
- Use the project grid, stack, spacing, typography, color, elevation, density,
  and breakpoint tokens. Do not invent page-local styling when the issue is
  reusable.
- Use `material-component-spec` when a repeated screen pattern needs reusable
  anatomy, variants, states, token mapping, and acceptance criteria.
- Use `design-token-system` when screen critique points to repeated color,
  type, spacing, density, focus, elevation, or theme decisions.
- Empty states must be contextual: what happened, why it matters, what can be
  done next, and whether the action is permitted for this user.
- Use `ux-writing` when labels, buttons, errors, empty states, confirmations,
  help text, notifications, or navigation names affect the user experience.
- Use `interaction-state-design` when the work includes loading,
  filtered-empty, no-results, error, permission, stale-data, async, disabled, or
  success states.
- Use `design-qa-playwright` when the final UI change needs rendered browser
  evidence, screenshot review, responsive checks, or end-to-end interaction
  proof.
- Forms must have visible labels, grouped related fields, clear validation, and
  only fields needed for the transaction.
- Interface hiding is not authorization. Route/service permissions must still
  enforce access.

## Core concepts

- **Human-centered hierarchy**: order the page by the user’s decision path:
  attention, available action, context, details, then advanced controls.
- **Material semantics**: choose components by their job. Tabs switch sibling
  views; chips hold compact selections/status/filter tokens; badges attach
  small counts to another element; cards group related meaning; lists/tables
  support dense comparison.
- **Surface hierarchy**: use page background, containers, elevation, spacing,
  and typography to show priority. Avoid nesting bordered rectangles unless
  each level carries distinct meaning.
- **Action scope**: place actions next to the object they affect. Page actions,
  section actions, row actions, and risky actions should not share the same
  visual lane.
- **Progressive disclosure**: keep the common path visible and move rare,
  advanced, dependent, or diagnostic controls into a clear reveal path.
- **Design-system durability**: repeated spacing, filter, empty-state, card, or
  action-placement issues should become reusable tokens/components/specs, not
  one-off page CSS.

## Research-backed basis

Before making non-trivial UI decisions, read
`references/research-synthesis.md`. It summarizes Material 3, Android adaptive
layout, accessibility, progressive-disclosure, dashboard, and public design-skill
patterns used to shape this skill.

For implementation composition, read
`references/screen-composition-patterns.md`.

## Standard workflow

1. **State the boundary.** Name the screen, primary users, work environment,
   task, and non-goals.
2. **Map the job.** Write the top user question the screen must answer, then
   list primary, secondary, and advanced tasks.
3. **Classify the screen.** Choose one dominant type: dashboard, worklist, form,
   detail, configuration, help/index, or review/approval surface.
4. **Select the layout.** Use the project shell/grid and a Material-compatible
   page stack. For adaptive products, define compact, medium, and expanded
   behavior instead of scaling one desktop layout down.
5. **Choose components by semantics.** Pick Material components for their
   intended job, not for appearance.
6. **Set hierarchy.** Ensure the highest-priority content is visually dominant,
   visible above secondary controls, and scannable in a few seconds.
7. **Place actions by scope.** Page-level actions go in the page/header action
   lane; section actions stay with the section; row actions stay on the row.
8. **Control disclosure.** Put rare, advanced, or dependent controls in clearly
   labeled reveal paths such as “More filters” or a side sheet. Do not hide the
   main task path.
9. **Apply the design system.** Reuse tokens, components, partials, and CSS
   recipes. If a reusable rule is missing, add or propose that rule first.
10. **Check states.** Cover loading, empty, populated, filtered-empty, error,
    disabled, permission-denied, success, and stale-data states.
11. **Verify.** Add DOM/component assertions and, where available, browser or
    screenshot checks for the affected screen.

## Required checks

- Does the screen answer “What should I know or do next?”
- Has screenshot/visual critique been routed through `visual-design-review`
  when the issue is visual hierarchy, grouping, density, typography, color,
  component consistency, or polish?
- Is the primary action visible and scoped correctly?
- Are unavailable actions hidden, disabled with reason, or moved deeper based
  on the user’s real task?
- Are filters/search lower emphasis than the results they refine?
- Are active filters represented as chips with clear removal when filters are
  non-obvious?
- Is there exactly one active tab/selection indicator in a sibling navigation
  group?
- Are cards internally balanced: icon/visual anchor, value/title, supporting
  text, and action region?
- Should a repeated pattern become a component contract through
  `material-component-spec`?
- Are labels and values separated by structure, not concatenated text?
- Are badges used only for compact counts/status signals, not as large labels?
- Are empty states role-aware and contextual?
- Has interface copy been routed through `ux-writing` when labels, buttons,
  errors, empty states, confirmations, help text, or notifications are part of
  the change?
- Are empty, filtered-empty, no-results, loading, error, stale, permission, and
  success states routed through `interaction-state-design` when they affect the
  page behavior?
- Are forms accessible: visible labels, related groups, instructions, errors,
  and keyboard/screen-reader semantics?
- Has accessibility work been routed through `accessibility-wcag-audit` when
  the screen includes forms, custom controls, dynamic state, or keyboard risk?
- Has final rendered verification been planned through `design-qa-playwright`
  when the change affects layout, component anatomy, responsive behavior,
  visible state, or a critical user path?
- Are project tokens/components used instead of page-local colors, margins, and
  custom layouts?
- Are route/service permissions enforced independently from visible UI state?

## Safety rules

- Do not use this skill to bypass project approval gates for permission,
  authentication, migration, safety, or production changes.
- Do not copy another design system’s brand tokens or proprietary visual
  identity into a project without permission.
- Do not make every screen dashboard-like; match the page to the job.
- Do not hide critical warnings behind tabs, drawers, or advanced filters.
- Do not add broad CSS resets or global component changes without checking
  affected pages.
- Do not leave user-facing implementation guidance in production UI copy; move
  rationale to specifications or design-system docs.

## Output format

```markdown
## Material HCD Interface Review

- Screen/job:
- Primary users:
- Current issue:
- Recommended hierarchy:
- Material components:
- Design-system changes:
- Accessibility/permission checks:
- Implementation slices:
- Verification:
- Remaining risk:
```

## Examples

- Worklist: workload metrics, task-mode tabs, search/filter chips, dense task
  rows, contextual empty state, row-scoped actions.
- Dashboard: attention strip, ready work, key metrics, quick actions, health
  summaries, drilldown links; avoid listing every unavailable capability.
- Form: page context, one transaction, grouped fields, attached context as
  low-emphasis metadata, primary submit action, cancellation/back path.
- Viewflow form: use `viewflow-form-controls` for widget choice, AJAX model
  selects, date/time controls, dynamic workflow fields, validation, and browser
  interaction checks.
- Help center: search-first entry, common tasks, intent-based pathways,
  compact references, support escalation.

## Pitfalls

- Designing from a capability catalogue instead of user tasks.
- Letting filters visually dominate the result surface.
- Showing walls of disabled actions on landing pages.
- Using cards for dense records that should be lists or tables.
- Treating chips and badges as interchangeable.
- Creating one-off spacing fixes instead of a page-stack/component rule.
- Duplicating route context already owned by the shell.
- Making screenshots look polished while leaving empty/error/loading states
  undefined.

## Verification

- `karakana skill validate skills/material-hcd-interface`
- `karakana eval run --skill material-hcd-interface`
- `karakana skill validate-all`
- For project UI changes, run the project’s focused render/browser tests.
