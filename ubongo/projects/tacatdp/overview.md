# TACATDP Overview

TACATDP is a Power Apps canvas app project for converting a long XLSForm-style data collection workflow into a Microsoft Power Platform application.

The current delivery path uses Microsoft Lists/SharePoint as the data layer because Dataverse privileges are not available. The app should reuse imported main variables, choices, and administrative reference lists such as zones, regions, districts, and wards.

## Current Delivery Intent

- Build implementation only after skills, memory, workspace context, and OKF artifacts are registered.
- Phase 3 is the active direction; Milestone 1 and Milestone 2 remain on hold until the Windows/Power Apps environment is ready.
- While waiting for Windows environment readiness, use placeholder data-source bindings and document the real Microsoft Lists/SharePoint sources to substitute later.
- Use the `power-platform-canvas-apps` skill for architecture, UX, Microsoft Lists schema design, Power Fx validation, and deployment planning.
- Prefer importable Microsoft Lists templates and generated artifacts over manual creation of hundreds of columns.
- Keep the Canvas App implementation simple and reviewable; Git can help source-control Canvas App changes after the app is created, but it is not a complete Git-only deployment path for the whole app and Lists backend.

## Active Phase

Phase 3 should focus on UI/component structure, navigation, validation patterns, and placeholder data-source seams. Do not block screen work on final SharePoint connection names. Keep a clear mapping from placeholder names to intended Microsoft Lists so the placeholders can be replaced after the Windows/Power Apps environment is ready.

## Active UX Requirements

- Use one field per row by default on data-entry screens.
- Use visible labels above inputs; never rely on placeholders as the only label.
- Put helper text and error text directly below the field.
- Use consistent spacing, section hierarchy, and wizard-style navigation for long forms.
- Preserve accessible focus order, touch targets, validation summaries, and save/error states.

## Review Questions

- Does the implementation preserve XLSForm required rules, skip logic, constraints, choice values, labels, and calculations?
- Are Microsoft Lists filters delegation-safe for large reference lists?
- Are skipped fields not required at the SharePoint column level?
- Are repeated or multi-select answers modeled as child rows where reporting requires one row per item?
- Can the user import generated list templates and continue building in Power Apps without Dataverse privileges?
- Are placeholder data sources isolated enough to swap for real SharePoint/Microsoft Lists connections later?
