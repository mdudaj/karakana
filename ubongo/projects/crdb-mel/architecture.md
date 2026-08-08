# Sustainable Finance MEL Platform Architecture

Sustainable Finance MEL Platform is the current project identity. TACATDP remains the historical programme/form context and is still used by several existing schema, list, form, and deployment artifacts.

## Platform

- Frontend/application: Microsoft Power Apps canvas app.
- Data layer: Microsoft Lists/SharePoint connector.
- Source form model: XLSForm-style survey with required rules, relevance/skip logic, constraints, choices, calculations, and repeats.
- Deployment support: generated artifacts, importable Microsoft Lists templates, and documentation for Power Apps Maker Portal steps.

## Data Architecture

- Main submission data should be stored in a parent submissions list.
- Repeated production cost data should be stored in a child list linked to the parent submission.
- Multi-select and repeat data should use child rows when analytics or reporting need one row per selected/repeated item.
- Large or cascading choices should use reference lists with indexed simple parent keys rather than hard-coded app collections.
- Skip-eligible fields should not be required SharePoint columns; Power Fx validation should enforce requiredness only when the field is visible/relevant.

## Canvas App Architecture

- Use sectioned, wizard-style screens rather than one giant generated form.
- Define reusable components before screen build: app shell, section header, progress indicator, form section/card, field row, reference ComboBox, validation summary, and command bar.
- Use vertical containers and responsive layout rules instead of manually positioning every field.
- Keep Power Fx formulas centralized enough to avoid copy/paste drift.

## Integration Notes

- Existing imported main variables, choices, and administrative lists should be reused as Power Apps data sources.
- Power Apps Git integration is useful after an app exists, but it does not replace list creation, SharePoint data source setup, or environment-specific app import/publish steps.
