# Material HCD Interface Research Synthesis

This reference gives the evidence base for the `material-hcd-interface` skill.
Use it when planning or reviewing non-trivial user-facing UI/UX work.

## Sources checked

- Material Design 3: https://m3.material.io/
- Material cards: https://m3.material.io/components/cards/overview
- Material chips: https://m3.material.io/components/chips/overview
- Material tabs: https://m3.material.io/components/tabs/overview
- Material badges: https://m3.material.io/components/badges/overview
- Android adaptive Material layout guidance:
  https://developer.android.com/codelabs/adaptive-material-guidance
- Android layout and navigation patterns:
  https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns
- W3C WAI forms tutorial: https://www.w3.org/WAI/tutorials/forms/
- Nielsen Norman Group / progressive disclosure summaries and long-standing
  HCI guidance: show primary work first and defer advanced/rare functions.
- Public design-skill examples:
  - Nothing Design Skill:
    https://github.com/dominikmartn/nothing-design-skill
  - Material 3 Skill:
    https://github.com/hamen/material-3-skill

## Validated principles

### 1. User job before component choice

Material is a component system, not an information architecture by itself.
Start with the user’s job-to-be-done, work environment, urgency, permissions,
and common failure modes. Then choose components.

For operational software, the first screen question is usually:

> What needs attention, and what can I act on now?

Only after that should the screen expose metrics, search, filters, setup,
reference data, or lower-frequency operations.

### 2. Progressive disclosure must preserve the primary path

Advanced filters, rare actions, setup dependencies, and diagnostic detail should
not crowd the default view. They belong behind labeled controls such as
`More filters`, detail pages, side sheets, dialogs, or advanced sections.

The default surface must still let the user complete the normal primary task.
If the user must open an advanced panel for the main task, the disclosure is
wrong.

### 3. Material components have semantic jobs

- **Navigation drawer/rail/bar**: top-level destinations and major product
  areas.
- **Top app bar / shell header**: current route context, global search, global
  actions, account/session controls.
- **Tabs**: sibling views under one route/object, with one active state.
- **Cards**: grouped summaries, action tiles, dashboards, and related content.
- **Chips**: compact filters, suggestions, input tokens, or small status
  controls.
- **Badges**: small counts or attention markers attached to another component.
- **Data tables/lists**: dense rows requiring scanning, comparison, sorting, or
  row-level actions.
- **Dialogs/sheets**: temporary focused decisions, advanced filters, or
  short-lived configuration, not persistent primary workflow.

### 4. Adaptive layout is not simple scaling

Material adaptive guidance favors layout choices that respond to window classes
and ergonomics. Compact, medium, and expanded screens may use different
navigation and pane patterns. Do not merely shrink a desktop dashboard into a
phone viewport.

### 5. Visual hierarchy should be sparse

If every surface has a border, icon, high contrast, and strong color, no element
is dominant. Use a small number of contrast levels. Make primary information
larger or more central; make metadata smaller and lower contrast.

### 6. Forms require accessibility and low cognitive load

W3C WAI guidance emphasizes visible labels, grouping related controls,
instructions, and clear feedback. Ask only for fields needed to complete the
transaction. Avoid concatenated labels/values; use semantic structure.

### 7. Public design skills use durable rules plus references

The Nothing Design Skill packages a visual language as `SKILL.md` plus
references for tokens, components, and platform mapping. Material 3 skill
examples similarly separate navigation/component guidance into references.

Karakana should use the same pattern: concise activation and workflow in the
entrypoint, with evidence and component detail in references.

## Practical screen-order heuristics

### Operational dashboard

1. urgent attention
2. ready work
3. key operational metrics
4. quick starts
5. health/status summaries
6. drilldowns

Avoid turning the dashboard into a catalogue of all possible workflows.

### Worklist/task queue

1. workload summary
2. task mode/tab
3. search and active filters
4. actionable result rows
5. contextual empty state

Filters support work; they should not become the page’s dominant object.

### Form

1. page/task identity
2. attached context
3. grouped fields
4. validation/help
5. primary submit and secondary cancel/back

Supporting context should be lower emphasis than the form fields.

### Detail/review page

1. object identity and state
2. available next actions
3. critical warnings/holds
4. summary facts
5. tabs or sections for evidence, history, attachments, and related records

Do not put rarely used administrative actions above the object’s current state.
