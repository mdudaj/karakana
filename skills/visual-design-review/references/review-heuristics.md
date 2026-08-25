# Visual Review Heuristics

Use this reference when reviewing screenshots or rendered UI.

## Review order

1. User job and primary decision.
2. Overall visual hierarchy.
3. Grouping and spacing.
4. Component anatomy and consistency.
5. Typography and density.
6. Color and semantic meaning.
7. Interaction states.
8. Accessibility risk.
9. Reusable implementation path.

## Severity model

| Severity | Meaning | Example |
| --- | --- | --- |
| P0 | Blocks task or creates serious safety/access risk | Critical action hidden, keyboard trap |
| P1 | High error risk or major task friction | Similar destructive/safe actions, unreadable state |
| P2 | Slows scanning or weakens confidence | Cramped KPI cards, unclear grouping |
| P3 | Polish/maintainability issue | Minor icon alignment drift |

Prioritize by impact and frequency, not by what is easiest to see.

## Hierarchy checks

- What does the eye see first?
- Is that the correct first thing for the user’s task?
- Are primary actions stronger than filters and metadata?
- Are warnings dominant only when there is an actual warning?
- Are disabled/unavailable capabilities moved deeper unless they explain a
  setup prerequisite?

## Grouping checks

- Related items are near each other.
- Similar items have similar visual treatment.
- Separate groups have enough spacing.
- Bordered regions are used only when they add meaning.
- Nested surfaces do not create false hierarchy.

## Component checks

- Repeated components share anatomy.
- Icons have a clear job and sufficient size.
- Text hierarchy separates value/title/supporting text.
- Actions are placed by scope.
- States are visible and consistent.
- Dense records use lists/tables rather than card walls.

## Typography and density checks

- Type roles match content purpose.
- Important values/titles are dominant.
- Supporting text is readable but lower emphasis.
- Line height and spacing avoid cramped stacks.
- Density matches the work context and input modality.

## Color checks

- Primary color is reserved for primary action/selection.
- Semantic colors map to meaning: warning, error, success, info.
- Whole surfaces are not tinted when a stripe/icon/chip would be enough.
- Contrast is checked through `accessibility-wcag-audit`.
- Repeated values are tokenized through `design-token-system`.

## Implementation routing

| Finding | Route |
| --- | --- |
| Wrong screen priority | `material-hcd-interface` |
| Repeated component anatomy issue | `material-component-spec` |
| Repeated color/spacing/type issue | `design-token-system` |
| Missing loading/error/empty state | `interaction-state-design` |
| Labels/focus/contrast/keyboard risk | `accessibility-wcag-audit` |
| Viewflow template/widget issue | `viewflow-material-ui` or `viewflow-form-controls` |

## Review output discipline

Each finding should include:

- observed issue;
- why it matters;
- recommended change;
- reusable implementation route;
- verification check.
