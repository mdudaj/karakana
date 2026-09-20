# Adaptive component contract

Use for responsive shell, queue, metric-card or navigation-disclosure changes.

## Diagnose before styling

- Inspect the computed cascade and ancestor sizing. A generic `span` rule can
  override an icon's flex/grid alignment even when its font size is correct.
  Separate icon anatomy from body-text selectors; measure the glyph region as
  well as the outer tonal container.
- Zero document overflow does not prove that controls fit: clipping ancestors
  and intrinsic grid tracks can conceal overflow. Inspect actual controls,
  clipping/scroll ancestors and horizontal scroll offsets. Prefer appropriate
  `minmax(0, 1fr)` tracks and `min-width: 0` on shrinking items over hiding overflow.
- Use container width where shell/sidebar space changes the usable area.
  For fixed small metric sets, consider balanced rows rather than an orphaned
  card; choose thresholds from content needs. Do not impose one card count,
  palette, breakpoint or density across projects.
- A bounded row is not necessarily readable: an intrinsic action column can
  starve identity/metadata columns without overflowing. Wrap actions into their
  own row when needed and verify meaningful text width with populated records.
- Reduce decoration and repeated explanations before hiding operational context.
  If actions are lab, study, account or project scoped, retain a concise visible
  scope indicator and a clear route to the full selector. Test missing and long
  labels as well as normal values. Never change scope implicitly to fit a screen.

## Navigation behavior

Choose semantics from interaction, not the visual name “menu”. Ordinary account
links can use a disclosure with native Tab order, an expanded state and a control
relationship. Escape closes it and returns focus to the trigger; leaving the
region closes without stealing focus from the new target. If using ARIA menu
roles, implement that pattern's full keyboard/selection contract instead.
For persistent-document navigation, check reconnect, revisit and cache behavior.

## Verification

Use `design-qa-playwright` for control-level reflow, open/closed disclosure,
keyboard focus, populated/empty queues and rendered alignment. An existing
page-width smoke test is not evidence that a reported visual bug is fixed.
Prefer a regression which fails on the old behavior before changing baselines.

Sources reviewed 2026-09-20:
- [W3C reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html): narrow
  layouts must retain functionality; genuinely two-dimensional content has
  exceptions, ordinary forms and action rows do not inherit those exceptions.
- [WAI disclosure navigation](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/):
  native links, expanded state, Tab, Escape and focus restoration.

These sources inform behavior. Project design tokens and framework-native
components continue to govern visual identity and implementation.
