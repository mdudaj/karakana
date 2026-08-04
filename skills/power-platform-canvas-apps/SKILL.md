---
name: power-platform-canvas-apps
description: Use this skill for Microsoft Power Apps canvas app architecture, Dataverse metadata-driven form renderers, Microsoft Lists/SharePoint connector data design, Power Fx validation/skip logic, packaging, responsive UX, and Fluent/Material-inspired form design.
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
    - Dataverse
    - metadata renderer
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

- Treat Dataverse and Microsoft Lists as different connector/data-model choices; use Dataverse tables and solutions when the app is a platform runtime.
- If the target UX is ODK Collect/Web Forms parity and the selected host is Power Pages, switch to `power-pages-odk-webforms`; do not keep extending Canvas as the primary field form runtime.
- For Dataverse metadata renderers, load form definitions from tables such as `Forms`, `FormVersions`, `Sections`, `Questions`, `Choices`, `ValidationRules`, and `FormAssignments`; store captures in `Submissions`, `SubmissionAnswers`, and `SubmissionFiles`.
- Keep assignment/history queries delegable. Filter Dataverse on simple equality/comparison predicates and avoid local filtering for tables that can grow.
- Do not call string functions such as `Lower()` on Dataverse columns inside assignment/history filters. Normalize values when writing/seeding, then compare `UserEmail = gblUserEmail`.
- Do not use Power Fx `Choices()` for dynamic form options stored as rows; query the metadata `Choices` table directly.
- If a Dataverse table is named `Choices`, verify Studio has actually bound it as a data source before referencing it. If the package does not contain that data source, remove choice loading from the import package and add the table in Studio first.
- Use `User().Email` carefully: it returns the current user UPN. Preserve a `UserEmail` fallback assignment key and use Dataverse `systemuser` lookups when available.
- Avoid generic custom Dataverse display names such as `Status` for Canvas-bound columns. Every Dataverse table already has built-in state/status fields, and imported Canvas source can fail to bind a custom `Status` choice consistently.
- If a generic custom Dataverse `Status` choice is required by schema and Studio cannot bind it in Canvas formulas, do not reintroduce `Status` patches into generated Canvas YAML. Relax the required level for the MVP or rename the column to a domain-specific name such as `SubmissionStatus`, then regenerate from Studio-normalized source.
- Use sectioned, wizard-like canvas app flows for long survey forms; default to one field per row on data-entry screens.
- In authenticated monitoring/data-collection apps, show the signed-in user in a consistent top header on every screen. Do not bury identity inside assignment-state or error messages.
- Assigned-form lists/cards must display both the human form name and the form version. A version-only button is not enough for field users or reviewers.
- For phone-responsive Canvas apps, follow Microsoft display guidance: disable Scale to fit, Lock aspect ratio, and Lock orientation. In packed artifacts, verify `DocumentLayoutScaleToFit`, `DocumentLayoutMaintainAspectRatio`, and `DocumentLayoutLockOrientation` are `false`.
- Preserve XLSForm semantics where in scope: `required`, `relevant`, `constraint`, choice values, labels, and calculations.
- Use Power Fx validation before navigation and submission; data-source required columns are unsafe for fields hidden by skip logic.
- Prefer modern controls and Fluent UI patterns in Power Apps; borrow Material Design principles for form structure, validation, progress, and accessibility.
- Treat layout, spacing, labels, helper text, error text, touch targets, and focus order as implementation requirements, not post-build polish.
- Set `AccessibleLabel` on controls that support it, especially buttons, galleries, and inputs. For labels/headings and tab order, follow Microsoft accessibility guidance in Studio, but do not emit unsupported properties into `*.pa.yaml`.
- Use Power Platform CLI/package workflows for source-controlled canvas apps and validate imports in Power Apps Studio.
- In importable/generated formulas, initialize collections with `ClearCollect` before clearing/removing rows. `Clear` only operates on existing collections and can fail App Checker if the generated app has not created the collection yet.
- Avoid `Filter(Table, false)` as an empty-table initializer in importable formulas. Studio can warn that the predicate is a literal and does not reference the input table. After a local collection is populated, use `FirstN(collection, 0)` for an empty table with the same shape.
- Avoid one-shot `ClearCollect` staging of whole Dataverse tables for large or growing tables. Prefer delegable `Filter`/`LookUp` bindings directly in galleries and formulas, and collect only staged local UI state.
- For Source Code `*.pa.yaml`, validate against the Microsoft PA YAML schema. Custom canvas component instances use `Control: CanvasComponent` plus `ComponentName`; `Control: Component` is invalid in Source Code schema.
- Prefer unversioned first-party controls such as `Control: Button` in generated `*.pa.yaml` unless the source was round-tripped from Studio with a known-good version. If Studio reports PA2106 and downgrades a control version, remove the explicit `@version`.
- Keep generated Button properties minimal for import packages: `AccessibleLabel`, `Text`, `OnSelect`, `DisplayMode`, `X`, `Y`, `Width`, and `Height` are the safe first pass. Do not style generated Button YAML with `Fill`, `Color`, `HoverFill`, `PressedFill`, `HoverColor`, `PressedColor`, `BorderThickness`, or `Align` unless Studio has round-tripped that exact control/version.
- Do not assume schema-valid generated `*.pa.yaml` is importable. Microsoft documents source files as read-only/review/source-control artifacts in normal app loading; external editing is supported through Power Platform Git Integration, and `pac canvas pack/unpack` is preview/deprecated. `.msapr` is a pack reference archive, not the primary Studio import target; pack it into `.msapp`, and understand whether `packed.json` sets `LoadFromYaml` before relying on YAML changes. Keep generated blueprints outside live `Src/` until Studio or supported tooling normalizes them.
- When a package is built from a Studio `.msapr` scaffold, stale table references can survive in `References/DataSources.json`, `References/QualifiedValues.json`, and `Properties.json` even after formulas stop using those tables. Prefer removing unused data sources in Studio; if generating a package, prune only exact unused table families and then inspect parsed package metadata.

## Purpose

Guide delivery of Microsoft Power Apps canvas applications that use Dataverse or Microsoft Lists/SharePoint data sources, especially metadata-driven survey/form runtimes and large workflows converted from XLSForm/ODK-style specifications. For Power Pages hosted ODK Web Forms work, use `power-pages-odk-webforms`.

## When to use this skill

Use when planning, designing, implementing, reviewing, or validating:

- Power Apps canvas app architecture.
- Dataverse metadata-driven renderer architecture.
- Dataverse schema usage for forms, assignments, submissions, answers, and files.
- Microsoft Lists/SharePoint connector schema design.
- Power Fx validation, skip logic, formulas, and save orchestration.
- XLSForm-to-Power Apps transformations.
- Canvas app source export/import, Power Platform CLI packing, or app import readiness.
- Responsive, accessible form UX using Power Apps modern controls, Fluent UI, or Material-inspired form patterns.

## When not to use this skill

Do not use for model-driven apps, Dynamics customizations, Dataverse administration unrelated to a canvas app, SharePoint administration unrelated to a canvas app, or Power Pages hosted ODK Web Forms delivery. Use `power-platform-cli-admin` for PAC/admin/schema bootstrap work and `power-pages-odk-webforms` for Power Pages/ODK runtime delivery.

## Core concepts

- **Delegation first**: Large data must be filtered on the server. Power Apps nondelegable formulas can return incomplete results after the first 500/2,000 records.
- **Dataverse metadata runtime**: A generic Canvas app can render a form from Dataverse metadata instead of generating one app/screen per form. Keep metadata tables small enough for the selected form, but keep assignment/history/submission queries delegable.
- **Generic answer model**: For a Dataverse runtime, prefer `Submissions` plus typed `SubmissionAnswers` fields (`ValueText`, `ValueNumber`, `ValueDecimal`, `ValueDate`, `ValueBoolean`, `ValueJson`) for the first slice. Use `SubmissionFiles` for attachments.
- **Dynamic choices are rows**: Query the form metadata `Choices` table for select-one/select-many options. Avoid Power Fx `Choices()` unless using Dataverse choice/lookup metadata intentionally.
- **Identity matching is explicit**: `User().Email` is the signed-in UPN. Match assignments by Dataverse `systemuser` lookup where available and by a normalized `UserEmail` fallback.
- **Simple filter keys**: Store reference keys in simple indexed columns (`Text`, `Number`, `DateTime`) when Power Apps needs to filter large data sources.
- **Choice/status naming is fragile**: A custom Dataverse choice column displayed as `Status` can sit beside built-in `statecode`/`statuscode`. Prefer names such as `SubmissionStatus`, `AssignmentStatus`, or `LifecycleStatus`. If an existing custom `Status` column does not bind in Studio, remove it from first-slice formulas or rename the column rather than repeatedly guessing a remapped display name.
- **Complex columns are UX conveniences, not default data architecture**: Choice, Lookup, Person, and Managed Metadata fields can be useful, but they complicate delegation and Power Fx formulas.
- **Skip logic belongs in the app layer**: A skipped field must not block navigation or save. Do not make skip-eligible data-source columns required.
- **Long forms need architecture**: Split by section, persist drafts, validate section-by-section, and show progress.
- **Reference data is data**: Large choice lists and cascading geography should be importable/reference lists, not copied into controls.
- **Fluent host, Material discipline**: Power Apps lives in Microsoft 365 and should use Fluent/modern controls where possible; Material Design principles still help with one-column form structure, labels, helper/error text, touch targets, progress, and navigation clarity.
- **One field per row by default**: For survey/data-entry screens, especially tablet and phone layouts, stack fields vertically with label, input, helper/error text, and reserved validation space before the next field.
- **Spacing is a tokenized rule**: Use consistent container padding and gaps instead of page-local nudges. Start from 16-24 px horizontal padding, 16 px between field rows, 4-8 px between an input and helper/error text, and larger section breaks when the app has no stronger project token.

## Standard workflow

1. Inventory the form/data source: field types, required rules, relevance rules, constraints, calculations, choice lists, large reference sets, attachments/media, and geolocation.
2. Choose the runtime data architecture:
   - Dataverse metadata renderer for platform forms, assignments, submissions, answers, and files, or
   - Microsoft Lists/SharePoint lists for simpler list-backed apps.
3. For Dataverse metadata renderers, define the renderer contract before building controls: assigned forms, history, runner shell, field renderer, attachment capture, and status transitions.
4. Classify data storage:
   - form/version/section/question metadata,
   - `FormAssignments` for assigned forms,
   - dynamic choices,
   - validation rules,
   - submissions and typed answer rows,
   - file rows,
   - repeated/line-item child rows when in scope,
   - reference data,
   - computed values.
5. For Microsoft Lists, design typed columns and indexed simple filter keys.
6. Define Power Apps screens/sections before building controls.
7. Define the form layout contract before building screens:
   - one field per row unless a paired-field exception is explicitly justified,
   - visible label above each input,
   - helper text and validation text directly below the input,
   - reserved error/helper space to avoid layout jumps,
   - consistent section and field spacing,
   - touch-safe control heights and tap targets,
   - top-to-bottom focus and tab order.
8. Define reusable components: app shell, section header, progress indicator, form section/card, validation summary, field row, reference ComboBox, save/submit command bar.
9. Translate XLSForm/form metadata logic into Power Fx conventions:
   - `Visible` for relevance,
   - validation expressions for constraints,
   - section completion formulas,
   - save eligibility formulas,
   - formulas or named formulas for repeated logic.
10. Plan save orchestration with explicit `Patch`, `IfError`, `Errors`, returned-record handling, and user-visible failure states. For Dataverse metadata renderers, save parent `Submissions` first, then upsert answer/file child rows.
11. Keep Dataverse lookup comparisons simple in first-slice formulas: prefer `FormVersion = gblFormVersion`, `Section = gblCurrentSection`, `Submission = gblSubmission`, and `Question = pending.Question`; avoid deep chains such as `Question.Section.FormVersion.FormVersion = ...` until Studio confirms the expanded field shape.
12. Validate generated `*.pa.yaml` against Source Code schema rules before packing:
   - keep active source under `Src/`, with component definition files under `Src/Component/`,
   - use `Control: CanvasComponent` for custom component instances,
   - include `ComponentName` only with `CanvasComponent` or `CodeComponent`,
   - quote Power Fx scalar values that include YAML-sensitive characters such as colons, braces, and multiline formulas,
   - avoid duplicate control names across component definitions,
   - do not add App Checker properties to a control/version unless the active Source Code schema accepts that property for that exact control.
13. Treat generated screens/components as scaffolds unless they were created in Power Apps Studio, checked in through Git Integration, or round-tripped through verified Power Platform tooling. Do not promote generated YAML directly into importable `Src/` as the primary delivery path.
14. For `.msapr` source folders, pack to `.msapp` before Studio import. Use `--disable-load-from-yaml` for baseline recovery packs when YAML should be ignored; omit it only when intentionally validating Studio loading from normalized YAML.
15. Validate with App Checker, Monitor, Power Apps Studio import/open, targeted happy-path and invalid-path tests, delegation warning review, and screen-by-screen UX review.

## Dataverse metadata renderer guidance

Use this guidance when the app is a generic runtime over Dataverse metadata:

- Start with an assigned-forms screen filtered by active assignments for the signed-in user. Do not build a marketing/landing page before the working collector flow.
- The assigned-forms screen should separate app identity, signed-in user identity, assignment state, and selectable form rows/cards. Keep status copy user-neutral, and put `User().Email`/`gblUserEmail` in the shared header.
- Each assigned form row/card must include the parent form display name and version code, for example `Form.Name - VersionCode`, so users can distinguish published versions.
- For assignment filters, use normalized text equality such as `UserEmail = gblUserEmail`. Avoid `Lower(UserEmail)` because column-side string functions can trigger delegation warnings.
- Load only the selected form version's sections, questions, choices, validation rules, and current submission answers into local collections. Do not load all submissions or all forms at app start.
- If App Checker reports incomplete rows from collection loading, bind small selected metadata directly with filtered gallery/formula expressions before reintroducing caching. The first slice should not copy all `Sections`, `Questions`, `Submissions`, or `SubmissionAnswers` into local collections.
- Keep dynamic field rendering simple: one gallery/list of questions, with control visibility selected by question type. For the first slice, support text, integer, decimal, date, select one, select many, attachment, and GPS only.
- For select one/select many, filter the metadata `Choices` table by current question and order by display order. Store select-one in `ValueText`; store select-many as JSON in `ValueJson` until analytics require a normalized child table.
- Required validation should read `ValidationRules` and visible/current answer state before submit. Do not rely only on Dataverse required columns for dynamic fields.
- Save Draft should patch `Submissions` first and store the returned record; then upsert answer rows. Submit should validate, save current answers, then patch status to `Submitted` and set submitted timestamp.
- Patch only typed answer fields that the current renderer actually stages. Do not emit `ValueDate: pending.ValueDate` until a date control creates a Date-typed `ValueDate` field in the staged answer collection.
- Edit-until-locked should be display-mode driven from `Submissions.Status`: Draft/Submitted editable, Locked read-only.
- If Studio reports incompatible or unrecognized custom `Status` choice references after import, do not keep patching the same display name. For the MVP, remove that choice from formulas and use another stable field such as `SubmittedAt`; for the durable design, rename the Dataverse column to a domain-specific display name and regenerate the app source.
- A Dataverse runtime error such as `mp_status is required` should be fixed at the Dataverse/schema layer when the Canvas binding for generic `Status` is already known fragile. Do not satisfy it by adding `Status: 'Status (...)'.Draft` back into generated package source.
- The Attachments control has form-context constraints. Use a small Dataverse Edit form bound to `SubmissionFiles` for the attachment row instead of trying to make a transformed dynamic table behave like an attachment source.
- GPS capture should happen on a button/action, using `Location` only when needed, then storing a compact JSON object with latitude, longitude, accuracy, and captured timestamp.
- The documented Power Fx `Location` signal exposes `Latitude`, `Longitude`, and `Altitude`; do not emit `Location.Accuracy` unless Studio/docs for the target environment confirm it exists.
- Use App Checker and Monitor to inspect delegation warnings, connector errors, and slow formulas before declaring the renderer scalable.

## Design guidance

- Use modern Power Apps controls when stable for the needed behavior.
- Use a responsive container hierarchy: app shell, header, navigation/progress, content container, section surfaces, footer/command bar.
- Use a consistent app shell header: screen title/action row first, signed-in user line second, then content. Avoid changing header semantics per screen.
- Before calling a phone experience ready, inspect the package/display settings as well as control formulas. A tablet canvas with scale-to-fit enabled can look correct in Studio while forcing a tablet-sized experience on phones.
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
- Follow Microsoft keyboard guidance in Studio: labels/images/shapes/icons should have `TabIndex = -1` unless interactive; interactive buttons, galleries, and inputs should have logical focus behavior and an accessible name. In generated Source Code YAML, only serialize `TabIndex`, `AccessibleLabel`, or `Role` where the target control version imports successfully.
- Keep primary navigation and save actions in predictable positions, such as a persistent footer/command bar or the bottom of each section, and show unsaved/saving/error state visibly.

## Safety rules

- Do not run scripts that write to live Dataverse, SharePoint, or Microsoft Lists without explicit user approval and an explicit dev/test/prod target.
- Do not publish/import apps into production environments without explicit approval.
- Do not store credentials, tokens, connection strings, or tenant secrets in app source, scripts, or examples.
- Do not use destructive list operations by default; scripts should create or update additively unless explicitly approved.
- Do not hide authorization or permission assumptions in UI navigation; SharePoint permissions and app connections must enforce access.

## Required checks

- Are all large reference, assignment, history, and submission filters delegable?
- For Dataverse renderers, are metadata tables, assignment tables, submissions, typed answer rows, and file rows clearly separated?
- Are all skip-eligible fields not required at the data-source column level?
- Are multi-select and repeated data modeled for reporting?
- Are value and label storage decisions explicit for choices?
- Are dynamic form choices queried from data rows rather than hard-coded or misusing `Choices()`?
- Are Power Fx formulas centralized enough to avoid copy/paste drift?
- Does save orchestration surface parent, answer, file, and child-list failures?
- Are the target devices and screen sizes accounted for?
- Does every data-entry screen have a declared form row pattern, spacing rule, and section hierarchy before implementation starts?
- Are fields one-per-row by default, with any two-column exceptions documented and tested on target widths?
- Are labels, helper text, error text, required indicators, focus states, and validation summaries visible and accessible?
- Are accessibility labels, error states, progress states, and keyboard/touch interactions considered?

## Pitfalls

- Building one giant generated form for hundreds of fields.
- Compressing fields into dense two-column layouts because the XLSForm has many variables.
- Treating spacing, labels, helper text, and error placement as maker-portal cleanup instead of a reusable screen contract.
- Pulling all reference, assignment, submission, or metadata data into collections and filtering locally.
- Assuming unused data sources disappear from a packed app when source formulas stop referencing them. Studio package reference metadata may need cleanup separately, and substring matching can confuse a table named `Forms` with Dataverse form metadata such as `FormVersions (Forms)`.
- Using Power Fx `Choices()` for form metadata options that are stored as Dataverse rows.
- Assuming `User().Email` always matches Dataverse `internalemailaddress` without a fallback assignment field.
- Calling `Lower(UserEmail)` or other string functions on a Dataverse column inside a delegable `Filter`.
- Creating Canvas-bound custom Dataverse choice columns with generic names such as `Status`, then expecting them to bind reliably beside built-in table status/state fields.
- Comparing deep lookup-id chains from generated assumptions instead of direct lookup records.
- Referencing a metadata table named `Choices` in generated source before confirming the imported app actually includes that data source.
- Using `Coalesce` across mixed answer value types such as text, number, date, and JSON; for required validation, check whether an answer record exists or use type-specific validation branches.
- Calling `Clear(collection)` in generated/imported formulas before the collection has been initialized. Prefer `ClearCollect` plus `RemoveIf(collection, true)` for staged local collections.
- Using literal predicates such as `Filter(colQuestions, false)` to create empty collections in generated/imported source. Prefer `FirstN(colQuestions, 0)` after `colQuestions` exists, or initialize with a typed staged-record table.
- Mutating a data source or collection inside `ForAll` for import/package scaffolds; Microsoft recommends inverting `ForAll(x, Collect(y, ...))` to `Collect(y, ForAll(x, ...))` where possible, and App Checker can warn about excessive re-evaluation.
- Leaving unused data sources in a Studio-imported app. Source YAML may not own data-source references; remove unused connectors/tables from the Studio Data pane after import rather than editing `References/DataSources.json` by hand.
- Patching typed answer fields from untyped or nonexistent staged-record properties, such as `pending.ValueDate` before a date input has established that column as Date.
- Patching boolean answer fields before Studio confirms whether the imported Dataverse field binds as Boolean or an option-set-like value.
- Trying to use the Attachments control outside its supported form context.
- Using SharePoint Choice/Lookup columns for large/cascading filters without testing delegation.
- Making SharePoint columns required when they can be hidden by skip logic.
- Storing multi-select values as comma-separated text when analytics require one row per selected option.
- Hand-editing exported canvas YAML heavily without validating against the active Source Code `*.pa.yaml` schema and then through Power Apps Studio.
- Treating App Checker recommendations as universally valid source YAML properties. For example, current imports have rejected `AccessibleLabel`, `TabIndex`, and `Role` on `Label@2.5.1`, and `TabIndex` on `Button@2.2.0`; apply those fixes in Studio or by using schema-supported control properties instead.
- Styling generated `Button@2.2.0` controls to mimic labels. In the current import path, Studio may downgrade Button to `0.0.45` and then reject properties such as `Fill`, `Color`, `HoverFill`, `PressedFill`, `HoverColor`, and `PressedColor`.
- Emitting retired/preview component syntax such as `Control: Component`; Source Code schema requires `Control: CanvasComponent` with `ComponentName`.
- Treating schema validation as proof that a manually generated Canvas source tree will import/open. Runtime import can still fail if the packed app is not produced by a supported source-control or Studio round-trip.
- Treating Material Design visual examples as a requirement to imitate Google styling inside a Microsoft 365/Fluent app.

## Verification

- `karakana skill validate skills/power-platform-canvas-apps`
- `karakana skill validate-all`
- `karakana eval run --skill power-platform-canvas-apps`
- For project work: regenerate schema/mapping artifacts, validate scripts compile, validate generated Source Code `*.pa.yaml` against Microsoft schema constraints, review Power Apps delegation warnings, open/import app in Power Apps Studio, run App Checker/Monitor, and run happy-path/invalid-path manual scenarios.

## Output format

```markdown
## Power Platform Canvas App Check

- Data source and scale:
- Delegation-sensitive areas:
- Dataverse/List schema architecture:
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
- Dataverse metadata renderer: show assigned forms, load the selected form version metadata, render questions dynamically, patch `Submissions` first, then upsert typed `SubmissionAnswers` and `SubmissionFiles`.
- TACATDP-style field screen: use a vertical container with 16-24 px page padding, a section header, one field-row component per question, visible label above input, helper/error text below input, and Next/Back/Save actions in a consistent command area.
