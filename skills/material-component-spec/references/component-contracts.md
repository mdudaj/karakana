# Component Contracts

Use this reference when turning a UI pattern into a reusable component.

## Minimum component contract

Every reusable component should define:

- purpose/job;
- examples and non-examples;
- anatomy/slots;
- variants;
- states;
- token mapping;
- accessibility requirements;
- responsive/density behavior;
- framework mapping;
- acceptance criteria and tests.

## Anatomy template

```text
Root
  Leading region: icon/avatar/status/selection marker
  Body region: title/value, supporting text, metadata
  State region: badge/chip/progress/error
  Action region: primary/secondary/trailing actions
  Helper region: help text, validation, recovery
```

Only include regions the component actually needs. Empty decorative regions
create visual noise.

## Variant rules

Good variants express meaning:

- primary / secondary / tertiary;
- neutral / info / warning / error / success;
- compact / comfortable;
- read-only / editable;
- single / multi;
- elevated / filled / outlined when that maps to Material semantics.

Bad variants express arbitrary styling:

- blue-card-large;
- left-margin-fix;
- dashboard-special;
- screenshot-version-two.

## State checklist

Always consider:

- enabled;
- hover;
- focused;
- pressed;
- disabled.

Consider when applicable:

- selected;
- dragged;
- loading;
- empty;
- filtered-empty;
- no-results;
- validation-error;
- system-error;
- warning;
- success;
- readonly;
- permission-denied;
- stale;
- conflict;
- offline;
- queued.

If a state cannot occur, state why in the component spec.

## Token mapping

Map repeated values to project tokens:

| Decision | Token class |
| --- | --- |
| color | primitive/semantic/component color |
| typography | type role, size, weight, line height |
| spacing | gap, padding, stack, inset |
| size | min height, icon size, target size |
| radius | surface/control radius |
| elevation | shadow/elevation layer |
| motion | duration, easing, reduced motion |
| density | compact/comfortable scale |

Do not invent literal hex/px values in page code when the value should survive
across components.

## Viewflow mapping

For Viewflow/Django projects:

- page layout belongs in reusable templates/partials;
- form controls should be defined in Python form/layout/widget configuration;
- ordinary fields should render through the canonical Viewflow form renderer;
- custom widgets need a reusable adapter and states;
- server-side permissions/querysets remain authoritative.

## Acceptance criteria examples

- The component renders all required slots.
- Variant classes/tokens are bounded to the approved set.
- Icon size and container alignment match the spec.
- One active tab indicator exists when using tabs.
- Active filter chips can be removed and clear-all works.
- Disabled action has a reason when user action is expected.
- Keyboard focus order matches visual/task order.
- Loading/error/empty states do not remove essential context.
