# UI Style Organization Contract

Use this reference before non-trivial UI/UX work. The goal is to prevent
page-local styling and repeated inconsistency across projects.

## Required project-level style contract

Before implementing or reviewing a UI slice, confirm the project has reusable
guidance or components for these areas:

| Area | Required contract |
|---|---|
| Page identity | One shared pattern for page icon, title, subtitle, optional context metadata, and page-level action lane. |
| Layout stack | Shared spacing between major sections; sibling sections must not touch. |
| Action lanes | Page actions, section actions, row actions, destructive actions, and back/return actions have distinct positions. |
| Filters/search | Search, More filters, selected filter chips, clear-all, filtered-empty, and autosubmit/submit behavior are defined. |
| Rows/cards | Reusable anatomy for icon/status, primary text, secondary text, metadata, status, and action region. |
| Empty states | Standard contextual empty and filtered-empty treatments with role-aware actions. |
| States | Loading, error, stale, disabled, permission, success, and no-results states are handled or explicitly not applicable. |
| Responsive behavior | Compact/medium/expanded behavior is defined for headers, actions, filters, and dense rows. |

If the project lacks this contract, create or update it before implementing the
page. Do not continue with page-local styling unless the user explicitly asks
for a throwaway prototype.

## Page identity rule

Every route-level page should use a shared page identity pattern:

```text
[icon]  Title                                      [page actions]
        Subtitle / task purpose
        Optional low-emphasis context metadata
```

Rules:

- the icon is intentional and sized/aligned by the design system;
- the title is the strongest text in the content area;
- the subtitle explains the user task, not implementation details;
- page actions sit in the header action lane, not mixed into content;
- child pages use the same identity pattern plus the shared back/return action;
- section headers use a weaker pattern and must not visually compete with the
  page identity.

## Implementation order

1. Find the project’s existing page identity/header component or template.
2. If it exists, use it. Do not invent a local header.
3. If it is missing or ambiguous, create a reusable component/class first.
4. Convert the target page to that component.
5. Add a focused render assertion or browser check for the durable rule.

## Review checks

- Does the page identity match sibling pages?
- Are icon size, title size, subtitle color, and spacing consistent?
- Are page actions separated from row/section actions?
- Are filters visually below page identity and secondary to results?
- Does the layout still work on compact screens?
- Did the implementation add a reusable rule instead of one-off CSS?
