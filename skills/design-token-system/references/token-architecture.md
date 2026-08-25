# Token Architecture

Use this reference when defining, auditing, or migrating design tokens.

## Layer model

```text
Primitive tokens
  Raw scales and palette values.
  Example: blue.600, spacing.4, radius.md, duration.fast

Semantic tokens
  Product meaning and accessibility pairs.
  Example: color.action.primary.container, color.text.primary,
  color.surface.container-low, focus.ring.default

Component tokens
  Component anatomy/state bindings.
  Example: kpi-card.accent.warning, filter-chip.selected.container,
  form-field.error.supporting-text
```

Do not bind components directly to primitive tokens unless the project has
explicitly chosen a very small token system. Semantic tokens protect components
from brand/theme changes.

## Naming guidance

Prefer:

- `color.text.primary`
- `color.surface.container`
- `color.status.warning.container`
- `space.stack.md`
- `size.icon.lg`
- `focus.ring.default`
- `component.kpi-card.icon-container.size`

Avoid:

- `blue-card`
- `dashboard-yellow`
- `margin-fix`
- `pretty-shadow`
- `new-ui-color`

## Token categories

Minimum practical categories:

- color;
- typography;
- spacing;
- sizing;
- radius;
- elevation/shadow;
- focus;
- motion;
- breakpoints;
- density;
- z-index/layers where needed.

## Contrast gates

Check semantic pairs:

- text on surface;
- secondary text on surface;
- action text on action container;
- error/warning/success text on their containers;
- focus ring against adjacent surfaces;
- disabled content if it communicates important state;
- chip/badge/status foreground on container.

Automated contrast checks do not prove the visual design is usable, but failing
contrast should block the token change unless there is a documented exception.

## Component-token checklist

For each reusable component:

- map root surface/background;
- map border/elevation/radius;
- map typography roles;
- map padding/gap/stack;
- map icon sizes and containers;
- map state colors;
- map focus treatment;
- map disabled/readonly treatment;
- map responsive/density adjustments.

## Migration checklist

- Identify every use of old token/literal.
- Decide whether to replace, alias, or deprecate.
- Avoid changing token meaning silently.
- Update component specs and docs.
- Run hardcode scans and focused visual checks.
- Record affected pages/components.

## Framework outputs

Choose output by project:

- CSS custom properties for server-rendered apps and Viewflow templates;
- Tailwind config or utilities for Tailwind projects;
- JS/TS theme objects for component frameworks;
- JSON design-token files for cross-tool exchange;
- documentation tables for human review.

For Viewflow projects, tokens should flow into the project CSS/component layer
and be consumed by reusable templates/widgets, not scattered into task-specific
templates.
