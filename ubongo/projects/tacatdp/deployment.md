# TACATDP Deployment

## Current Deployment Path

Milestone 1 and Milestone 2 are on hold until the Windows/Power Apps environment is ready. During Phase 3, use placeholder data-source bindings and maintain a replacement map for the real SharePoint/Microsoft Lists sources.

1. Import or create Microsoft Lists from generated templates.
2. Confirm reference/admin lists exist for choices, zones, regions, districts, wards, and other imported lookup data.
3. Create the Canvas App in Power Apps Studio.
4. Add SharePoint data sources for submissions, repeats, choices, and admin lists.
5. Build screens/components using the `power-platform-canvas-apps` skill guidance.
6. Validate delegation warnings, App Checker results, save behavior, and UX behavior on target devices.
7. Connect the Canvas App to Git only after the app exists and the environment supports the Power Apps Git workflow.

## Important Constraints

- There is no simple Git-only path that creates the complete Canvas App and all Microsoft Lists from repository artifacts.
- Placeholder data sources must remain clearly named and documented; do not treat them as production SharePoint connections.
- Do not publish/import apps into production without explicit approval.
- Do not run scripts that write to live SharePoint/Microsoft Lists without explicit approval and a target site URL.
- Do not store tenant credentials, tokens, connection strings, or `.env` content in artifacts.

## Verification

- Placeholder-to-real data-source mapping exists and names the intended Microsoft Lists replacements.
- Microsoft Lists import templates open and create the expected columns.
- Power Apps data sources connect to the intended SharePoint site and lists.
- Delegation warnings are reviewed for reference filters.
- Required, skip, constraint, repeat, and multi-select behavior is tested manually.
- Screen layout is reviewed for one-field-per-row, spacing, labels, helper/error text, focus order, and accessible touch targets.
