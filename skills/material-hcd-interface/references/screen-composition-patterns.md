# Screen Composition Patterns

Use this reference when turning critique into implementation instructions.

## Page anatomy

Prefer a consistent page stack:

```text
Shell/header context
Page title + route-scoped actions
Primary status/attention surface
Primary work surface
Supporting metrics or context
Secondary actions/details
```

Do not repeat shell-owned context as a large content hero. If context must be
submitted with a form, render it as compact attached metadata.

## Action placement

| Scope | Placement | Examples |
| --- | --- | --- |
| Global/session | shell/header | account, notifications, global search |
| Route/page | page header action lane | refresh, export, create item |
| Section | section header/action rail | view all, add related item |
| Row/object | row trailing action | open, claim, review |
| Risky/irreversible | confirmation flow | deactivate, revoke, delete, override |

Do not place a dependent action before the object it depends on exists unless it
is a setup call-to-action that creates the missing prerequisite.

## Cards

Use cards for grouped meaning, not for every rectangle.

Good card anatomy:

```text
icon or visual anchor
primary value/title
supporting text
status/metadata
action region
```

Sibling cards should share anatomy. If KPI cards use icon circles, make the
icon visible enough to be intentional, align the text stack, and use restrained
semantic accent only where the state has meaning.

## Chips and badges

Use chips when the item is itself a compact control or token:

- active filters;
- removable selections;
- suggestions;
- compact status controls.

Use badges when the item is a small count/status attached to another component:

- unread count on notification icon;
- row count on a tab;
- warning count attached to a navigation item.

Do not replace an active filter chip with a badge if the user needs to remove it
directly.

## Tabs

Tabs are for sibling views under one context. Requirements:

- one active tab only;
- active indicator visually attached to active tab;
- each tab changes the same route/object’s content mode;
- tab row separated from filters or result surfaces by the project page stack;
- tab labels describe user concepts, not implementation state names.

If two tabs return the same result set, remove one.

## Filters

Filters should refine results, not dominate the screen.

Recommended pattern:

```text
Search input
More filters
Active filter chips
Results
```

Use a drawer/side sheet/dialog only when the filter set is too large for the
default toolbar. Keep primary search visible. Apply select changes immediately
when the cost is low and user intent is clear. Show active filters as removable
chips and provide a clear-all action when more than one filter may be active.

## Empty states

A useful empty state answers:

1. what state the user is in;
2. why it happened;
3. what can happen next;
4. which action is available for this user.

Avoid generic `No data`. Avoid showing actions the user cannot perform. Avoid
nested bordered boxes for an empty state inside another card unless the nested
container carries separate meaning.

## Forms

Recommended form anatomy:

```text
Header: task + destination/back + page actions
Context: compact attached metadata
Field groups: framework-rendered fields
Validation: field and form-level errors
Actions: cancel/back + primary submit
```

Rules:

- visible label for every control;
- related fields grouped;
- required/optional meaning clear;
- help text belongs near the field;
- dependent fields appear only when relevant;
- action labels use user outcomes, not implementation verbs.

## Operational/lab environments

For time-sensitive operational systems:

- prioritize exception/attention states;
- make the next safe action obvious;
- expose actor, context, and record identity where wrong-object action is a
  risk;
- keep dense work surfaces scannable;
- reduce decorative clutter;
- show stale-data/update time when decisions depend on freshness;
- keep manual fallback and error recovery visible when automation can fail.

## Review checklist

- Can the user identify the current page and object in under a few seconds?
- Can the user tell what needs attention?
- Can the user tell what they can act on now?
- Are advanced/rare controls one layer down, not removed?
- Are labels/values structurally separated?
- Are icons large enough to be intentional and paired with text where meaning
  matters?
- Are empty/loading/error/success states defined?
- Are permissions enforced outside the UI?
- Is the change made through a reusable token/component/partial where it can
  recur?
