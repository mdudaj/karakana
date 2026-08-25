# Viewflow Widget Patterns

Use this reference when implementing or reviewing Viewflow/Django controls.

## Source-backed Viewflow patterns

Viewflow forms separate Python form/layout logic from HTML rendering. The
practical rule for agents is:

```text
Python: fields, order, layout, widgets, validation, queryset scope
Template: canonical Viewflow/Material rendering
CSS: reusable design-system styling
JavaScript: only reusable behavior that Viewflow/widget support does not cover
```

Do not make templates responsible for deciding which fields exist or how domain
querysets are scoped.

## Control decision table

| Data/task | Preferred control | Notes |
| --- | --- | --- |
| Short text | Text field | Visible label, help, validation |
| Long text | Textarea | Use only when free text is necessary |
| Number/measurement | Numeric field | Unit visible near field or in label/help |
| Date | Date picker/calendar + typed input | Preserve keyboard path |
| Date/time/timestamp | Date/time control + format/timezone help | Store unambiguous value |
| Short fixed choice | Select/radio/chips | Choose by density and risk |
| Boolean confirmation | Checkbox/switch only when meaning is explicit | Avoid vague yes/no labels |
| Large FK lookup | `AjaxModelSelect` | Scope queryset; no huge option list |
| Large M2M lookup | `AjaxMultipleModelSelect` | Scope queryset; show selected tokens |
| Repeated rows | Formset/inline | Add/remove/error states needed |
| File/evidence | File input/dropzone adapter | Type/size/status feedback |

## AJAX select requirements

For `AjaxModelSelect` and `AjaxMultipleModelSelect`:

- use model lookup fields that match how users search;
- scope suggestions to active lab/study/tenant/workflow permissions;
- limit result count;
- return stable display labels and IDs;
- cover no-results, loading, selected, cleared, and error states;
- reject submitted IDs outside the allowed queryset;
- test both suggestion endpoint and final form submission.

When using `FormAjaxCompleteMixin`, verify the OPTIONS autocomplete request path
does not expose fields that the current user cannot use.

## Date and timestamp requirements

For calendar/date/time controls:

- match the stored field type: date, time, datetime, or duration;
- preserve manual keyboard entry;
- show accepted format in help text when not obvious;
- show timezone when recording operational timestamps;
- validate min/max values when the workflow requires them;
- avoid defaulting to now unless that matches the physical event;
- distinguish occurred-at from recorded-at where audit matters.

## Dynamic workflow forms

Generated workflow forms need stricter rules than static CRUD forms:

- metadata must map to an allowed widget type;
- labels/help/options must be escaped by default;
- required fields must be explicit;
- field order must follow task sequence, not raw metadata order;
- workflow state must be checked at render and submit;
- submitted values must be stored with enough context for audit.

## Browser verification checklist

- Form renders with visible labels and expected groups.
- Keyboard can reach every control in order.
- AJAX select opens, searches, selects, clears, and handles no results.
- Date/timestamp control accepts picker selection and typed entry.
- Validation errors are shown next to fields and summarized when useful.
- Permission-denied data is not suggested and cannot be submitted.
- Dynamic workflow form preserves values after validation failure.
