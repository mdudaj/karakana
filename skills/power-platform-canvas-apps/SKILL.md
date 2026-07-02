---
name: power-platform-canvas-apps
description: Use this skill for Microsoft Power Apps canvas app architecture, Microsoft Lists/SharePoint connector data design, Power Fx validation/skip logic, packaging, responsive UX, and Fluent/Material-inspired form design.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - web_fetch
  - python
  - run_tests
requires_approval_for:
  - production_sharepoint_write
  - permission_change
  - app_import_or_publish
  - destructive_list_change
activation:
  keywords:
    - Power Apps
    - Power Platform
    - Microsoft Lists
    - SharePoint connector
    - canvas app
    - Power Fx
    - Fluent UI
    - XLSForm
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
---
# Power Platform Canvas Apps

## Quick Reference

- Treat Microsoft Lists as SharePoint lists; design for SharePoint connector delegation from the start.
- Prefer simple indexed text/number/date columns for filters. Avoid relying on complex Choice/Lookup subfields for large-list filtering.
- Use reference lists for large or cascading choices; do not hard-code large choice arrays in formulas.
- Use sectioned, wizard-like canvas app flows for long survey forms; default to one field per row on data-entry screens.
- Preserve XLSForm semantics: `required`, `relevant`, `constraint`, choice values, labels, and calculations.
- Use Power Fx validation before navigation and submission; SharePoint required columns are unsafe for fields hidden by skip logic.
- Prefer modern controls and Fluent UI patterns in Power Apps; borrow Material Design principles for form structure, validation, progress, and accessibility.
- Treat layout, spacing, labels, helper text, error text, touch targets, and focus order as implementation requirements, not post-build polish.
- Use Power Platform CLI/package workflows for source-controlled canvas apps and validate imports in Power Apps Studio.

## Purpose

Guide delivery of Microsoft Power Apps canvas applications that use Microsoft Lists/SharePoint data sources, especially large survey or form workflows converted from XLSForm/ODK-style specifications.

## When to use this skill

Use when planning, designing, implementing, reviewing, or validating:

- Power Apps canvas app architecture.
- Microsoft Lists/SharePoint connector schema design.
- Power Fx validation, skip logic, formulas, and save orchestration.
- XLSForm-to-Power Apps transformations.
- Canvas app source export/import, Power Platform CLI packing, or app import readiness.
- Responsive, accessible form UX using Power Apps modern controls, Fluent UI, or Material-inspired form patterns.

## When not to use this skill

Do not use for model-driven apps, Dataverse-only architecture, Dynamics customizations, or SharePoint administration unrelated to a canvas app unless the task explicitly connects back to Power Apps delivery.

## Core concepts

- **Delegation first**: Large data must be filtered on the server. Power Apps nondelegable formulas can return incomplete results after the first 500/2,000 records.
- **Simple filter keys**: Store reference keys in simple indexed columns (`Text`, `Number`, `DateTime`) when Power Apps needs to filter large lists.
- **Complex columns are UX conveniences, not default data architecture**: Choice, Lookup, Person, and Managed Metadata fields can be useful, but they complicate delegation and Power Fx formulas.
- **Skip logic belongs in the app layer**: A skipped field must not block navigation or save. Do not make skip-eligible SharePoint columns required.
- **Long forms need architecture**: Split by section, persist drafts, validate section-by-section, and show progress.
- **Reference data is data**: Large choice lists and cascading geography should be importable/reference lists, not copied into controls.
- **Fluent host, Material discipline**: Power Apps lives in Microsoft 365 and should use Fluent/modern controls where possible; Material Design principles still help with one-column form structure, labels, helper/error text, touch targets, progress, and navigation clarity.
- **One field per row by default**: For survey/data-entry screens, especially tablet and phone layouts, stack fields vertically with label, input, helper/error text, and reserved validation space before the next field.
- **Spacing is a tokenized rule**: Use consistent container padding and gaps instead of page-local nudges. Start from 16-24 px horizontal padding, 16 px between field rows, 4-8 px between an input and helper/error text, and larger section breaks when the app has no stronger project token.

## Standard workflow

1. Inventory the form/data source: field types, required rules, relevance rules, constraints, calculations, choice lists, large reference sets, attachments/media, and geolocation.
2. Classify data storage:
   - scalar parent/section fields,
   - multi-select child rows,
   - repeated/line-item child rows,
   - reference data,
   - computed values.
3. Design Microsoft Lists with typed columns and indexed simple filter keys.
4. Define Power Apps screens/sections before building controls.
5. Define the form layout contract before building screens:
   - one field per row unless a paired-field exception is explicitly justified,
   - visible label above each input,
   - helper text and validation text directly below the input,
   - reserved error/helper space to avoid layout jumps,
   - consistent section and field spacing,
   - touch-safe control heights and tap targets,
   - top-to-bottom focus and tab order.
6. Define reusable components: app shell, section header, progress indicator, form section/card, validation summary, field row, reference ComboBox, save/submit command bar.
7. Translate XLSForm logic into Power Fx conventions:
   - `Visible` for relevance,
   - validation expressions for constraints,
   - section completion formulas,
   - save eligibility formulas,
   - formulas or named formulas for repeated logic.
8. Plan save orchestration for parent, section, and child lists, with explicit `IfError`/`Errors` handling and user-visible failure states.
9. Validate with App Checker, Monitor, Power Apps Studio import/open, targeted happy-path and invalid-path tests, delegation warning review, and screen-by-screen UX review.

## Design guidance

- Use modern Power Apps controls when stable for the needed behavior.
- Use a responsive container hierarchy: app shell, header, navigation/progress, content container, section surfaces, footer/command bar.
- Use vertical containers with a clear `Gap` for form rows; avoid manually positioning every control when responsive containers can express the layout.
- Default each data-entry row to `Label -> Input -> helper/error text`. Keep the label visible above the input and keep the error close to the field it explains.
- Use one field per row for ordinary survey inputs. Allow two fields per row only for tightly coupled short values, such as start/end dates, when the target device width supports it and accessibility remains clear.
- Use 16-24 px horizontal content padding and at least 16 px between stacked field rows unless project tokens define a different density.
- Reserve a helper/error text area under each field or field component so validation messages do not push the rest of the form around.
- Keep form labels visible; do not rely on placeholder text as the only label.
- Put helper text and error messages near the field.
- Use section cards or section headers with larger vertical spacing than field rows so a long form remains scannable.
- Use determinate progress for known sections, for example "Section 4 of 12".
- Use disabled primary actions only when paired with visible reasons; otherwise show validation summary on action.
- Use tabs only for peer content inside a section; use stepper/wizard navigation for a survey flow.
- Use clear focus order, visible focus states, accessible labels, and touch targets large enough for field devices.
- Keep primary navigation and save actions in predictable positions, such as a persistent footer/command bar or the bottom of each section, and show unsaved/saving/error state visibly.

## Safety rules

- Do not run scripts that write to live SharePoint/Microsoft Lists without explicit user approval and a target site URL.
- Do not publish/import apps into production environments without explicit approval.
- Do not store credentials, tokens, connection strings, or tenant secrets in app source, scripts, or examples.
- Do not use destructive list operations by default; scripts should create or update additively unless explicitly approved.
- Do not hide authorization or permission assumptions in UI navigation; SharePoint permissions and app connections must enforce access.

## Required checks

- Are all large reference filters delegable?
- Are all skip-eligible fields not required at the SharePoint column level?
- Are multi-select and repeated data modeled for reporting?
- Are value and label storage decisions explicit for choices?
- Are Power Fx formulas centralized enough to avoid copy/paste drift?
- Does save orchestration surface parent, section, and child-list failures?
- Are the target devices and screen sizes accounted for?
- Does every data-entry screen have a declared form row pattern, spacing rule, and section hierarchy before implementation starts?
- Are fields one-per-row by default, with any two-column exceptions documented and tested on target widths?
- Are labels, helper text, error text, required indicators, focus states, and validation summaries visible and accessible?
- Are accessibility labels, error states, progress states, and keyboard/touch interactions considered?

## Pitfalls

- Building one giant generated form for hundreds of fields.
- Compressing fields into dense two-column layouts because the XLSForm has many variables.
- Treating spacing, labels, helper text, and error placement as maker-portal cleanup instead of a reusable screen contract.
- Pulling all reference data into collections and filtering locally.
- Using SharePoint Choice/Lookup columns for large/cascading filters without testing delegation.
- Making SharePoint columns required when they can be hidden by skip logic.
- Storing multi-select values as comma-separated text when analytics require one row per selected option.
- Hand-editing exported canvas YAML heavily without validating through Power Apps Studio.
- Treating Material Design visual examples as a requirement to imitate Google styling inside a Microsoft 365/Fluent app.

## Verification

- `karakana skill validate skills/power-platform-canvas-apps`
- `karakana skill validate-all`
- `karakana eval run --skill power-platform-canvas-apps`
- For project work: regenerate schema/mapping artifacts, validate scripts compile, review Power Apps delegation warnings, open/import app in Power Apps Studio, and run happy-path/invalid-path manual scenarios.

## Output format

```markdown
## Power Platform Canvas App Check

- Data source and scale:
- Delegation-sensitive areas:
- List/schema architecture:
- Screen/section architecture:
- Reusable components:
- Validation and skip logic:
- Save orchestration:
- Fluent/Material UX decisions:
- Verification:
- Remaining risks:
```

## Examples

- XLSForm with 60,000+ villages: create reference lists with indexed parent keys and filter by selected region/district/ward.
- Survey field with `relevant`: drive card `Visible`; validate only when visible; clear or ignore hidden value according to the data policy.
- `select_multiple`: store one row per selected choice in a child answers list for analytics-ready reporting.
- Repeated cost stages: normalize to a line-item list instead of generating `vc1_*` through `vc18_*` scalar columns.
- TACATDP-style field screen: use a vertical container with 16-24 px page padding, a section header, one field-row component per question, visible label above input, helper/error text below input, and Next/Back/Save actions in a consistent command area.
