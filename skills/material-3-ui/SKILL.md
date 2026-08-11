---
name: material-3-ui
description: Use this skill before implementing or revising Material Design 3 web UI, especially lists, data tables, cards, filters, spacing, typography, tokens, responsive layouts, or accessibility states in Vue, Power Pages, or other web frontends.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - npm_test
requires_approval_for:
  - frontend_design_system_change
  - accessibility_pattern_change
  - dependency_addition
activation:
  keywords:
    - Material 3
    - M3
    - Material Design
    - material-web
    - list
    - data table
    - spacing
    - tokens
    - responsive UI
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
---
# Material 3 UI

## Quick Reference

- Start from project tokens, then map them to Material roles: primary, surface, surface-container, outline, on-surface, on-surface-variant, positive, warning, and error.
- Use 4 px increments and 8 px rhythm for spacing. Prefer 16 px and 24 px gaps between related groups; avoid one-off page-local nudges.
- Use cards for grouped summaries/actions, lists for homogeneous row items, and tables for dense desktop comparison.
- For institutional card consistency, prefer a reusable subtle left accent rail on elevated cards. The rail should be token-driven, about 4 px wide, and semantic by tone rather than decorative.
- For desktop enterprise records, prefer a semantic `<table>` with visible headers, row hover/focus state, status text, and pagination or an explicit prototype limit.
- For mobile, transform tables into stacked record cards instead of shrinking columns until labels become unreadable.
- Keep list rows scannable: leading identity, supporting text, trailing status/metadata/action. Do not mix unrelated content types in one list.
- Use status chips with text and tone. Do not rely on color alone.
- Use visible labels for search and filters. Place active filters as removable chips above the affected list/table when filters are active.
- Preserve route ownership: shell header owns route title and global actions; page content starts with the work surface.
- Use official Material guidance or `@material/web` when adding new component patterns. Do not invent component anatomy without a reason.

## Purpose

Prevent repeated UI corrections by applying Material 3 structure before coding. This skill is tactical: it governs concrete web components, spacing, responsive behavior, and accessible states.

## Core concepts

- Material UI consistency comes from tokens, component anatomy, interaction states, and responsive behavior working together.
- Dense enterprise data still needs semantic HTML; visual polish does not replace table/list semantics.
- The same record collection can be a table on desktop and a card list on mobile, but both must preserve the same information hierarchy.
- Verification should protect the pattern, not only the current pixels.
- Card emphasis should be reusable component anatomy. Do not add one-off borders or shadows to individual cards when the project has a card primitive.

## When to use this skill

Use for Material-style dashboards, management tables, record lists, filters, status chips, cards, route pages, and responsive shells.

## When not to use this skill

Do not use for backend-only changes. Do not add `@material/web` automatically when the existing project already has a compatible component system and tokens; dependency addition still needs a concrete reason and approval.

## Standard workflow

1. Inspect the existing tokens, shell, reusable components, and the closest implemented page.
2. Refresh official Material guidance when the component pattern is unstable, unfamiliar, or has caused repeated misses.
3. Choose the correct pattern:
   - card: summary, goal, action, or grouped metrics;
   - list: homogeneous items with primary/supporting/trailing content;
   - table: dense comparison across stable columns;
   - filter drawer/chips: global or table-scoped filtering.
4. Define behavior and visual requirements before editing: data scope, columns, actions, filters, empty/loading/error/partial states, responsive behavior, and accessibility.
5. Implement via reusable classes/components and project tokens. Avoid page-local hard-coded colors unless adding a token.
6. Add a focused validator or component test for the durable contract that failed or could regress.
7. Build/typecheck and capture render evidence when the page is visible.

## Material list and table rules

- Lists:
  - Use consistent row height and vertical rhythm.
  - Keep leading visual, primary label, secondary/supporting text, and trailing metadata/action in stable positions.
  - Use semantic buttons or links when rows are actionable.
  - Provide empty and loading states that say why data is absent.
- Tables:
  - Use `<table>`, `<thead>`, `<tbody>`, `<th scope="col">`, and a caption or `aria-label`.
  - Align numeric columns consistently.
  - Keep high-priority columns visible at desktop widths.
  - Use sticky headers only when the table scroll area is clear and keyboard-accessible.
  - Pair row hover with focus-visible styling.
- Filters:
  - Search inputs need visible labels or accessible labels.
  - Filter chips show active state in text and are removable.
  - Avoid misleading zeroes before data loads; use states such as “Not yet queried,” “Awaiting submission,” or “No data for the selected period.”

## Safety rules

- Do not weaken route authorization or data scope while adding navigation.
- Do not hide status behind color-only UI.
- Do not shrink dense tables into unreadable mobile layouts.
- Do not add third-party UI dependencies without approval and a migration/compatibility reason.
- Do not let prototype/demo data appear official; label it as demonstration data.

## Required checks

- Did the implementation inspect the existing shell, tokens, and reusable components first?
- Is the component pattern appropriate: card, list, table, filter drawer, or dashboard grid?
- Are colors, spacing, radius, elevation, and focus states token-based or otherwise consistent with the project design profile?
- Do card surfaces use the shared card primitive or an explicitly documented equivalent, including the project’s accent rail when that is part of the design profile?
- Does the page include loading, empty, no-data, partial-data, and error states where data is dynamic?
- Are search and filters visibly labelled and keyboard operable?
- Are status chips text-labelled and not color-only?
- Is desktop density readable without truncating critical labels?
- Does mobile use a deliberate stacked layout instead of an unreadable compressed table?
- Is there a validator, test, screenshot, or render check for the reusable rule?

## Examples

- Beneficiary registry: desktop semantic table with scoped column headers, search/filter controls above, status chips in the verification column, and mobile record cards.
- KPI dashboard: 12-column grid, reusable elevated cards, shared footer/action slot, and chart options separated from page markup.
- Accent card rail: `DashboardCard`, `KpiCard`, or `SurfaceCard` owns the left rail and accepts a tone prop; pages choose tone, not rail CSS.
- Data submissions list: two-line list rows with region/reporting period as primary/supporting text and submission status/time as trailing content.

## Pitfalls

- Building a table visually with nested divs and losing screen-reader/table semantics.
- Shrinking too many columns into mobile instead of switching to cards.
- Creating one-off colors for every chip instead of using status tones.
- Moving actions based on content length instead of using a shared card footer/action slot.
- Adding page-local left borders instead of updating the shared card primitive.
- Leaving demo data unlabeled so prototype values look official.
- Adding `@material/web` before checking whether the existing Vue component system can express the same M3 rule.

## Verification

- Required source checks: existing shell/tokens, affected page, and current reusable components.
- Required implementation checks: typecheck/build plus a focused DOM/CSS validator when the rule is reusable.
- Required accessibility checks: semantic headings, table headers, labels, focus-visible styles, non-color status labels, and responsive fallback.
- Required handoff: record the exact rule added and how to verify it.

## Output format

```markdown
## Material 3 UI Check

- Component pattern:
- Existing tokens/components reused:
- Material guidance checked:
- Responsive behavior:
- Accessibility:
- Validator/test:
- Remaining visual risk:
```
