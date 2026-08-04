---
name: power-pages-odk-webforms
description: Use this skill for Microsoft Power Pages hosted SPA delivery with ODK Web Forms/XForms, Dataverse through the Power Pages Web API, offline draft planning, private-site access checks, invitation activation, and ODK Central-inspired schema design.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - web_fetch
  - shell
  - python
  - run_tests
requires_approval_for:
  - power_pages_upload
  - dataverse_schema_write
  - table_permission_change
  - site_setting_change
  - authentication_change
  - package_install
activation:
  keywords:
    - Power Pages
    - pac pages
    - upload-code-site
    - ODK Web Forms
    - xforms-engine
    - Power Pages Web API
    - Portals Web API
    - ODK Central
    - offline draft
    - site visibility
    - invitation activation
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
---
# Power Pages ODK Web Forms

## Quick Reference

- Use this skill when building a Microsoft-managed ODK-style field app with Power Pages, Vue, ODK Web Forms, Dataverse, and the Power Pages Web API.
- Inside Power Pages, prefer `/_api/...` over raw Dataverse Web API when the app relies on Power Pages authentication, web roles, table permissions, and CSRF protections.
- Treat the form definition as XForms-first. Store canonical XForm XML on the form version, not only decomposed question metadata.
- Mirror the useful ODK Central boundaries: `Projects`, `Forms`, `FormVersions`, `FormAttachments`, `FormAssignments`, `Submissions`, `SubmissionVersions`, and `SubmissionAttachments`.
- Use `SubmissionAnswers` only as an optional analytics/reporting projection. Do not make it the source of truth for the ODK Web Forms runtime.
- Use ODK `instanceId` as a stable submission identity and store submission payload versions separately from the submission header.
- Keep attachments separate from submission headers and versions. Store filename, media type, file/blob reference, and captured/uploaded timestamps.
- Model review separately from collection lifecycle. Collection lifecycle can be `Draft`, `Submitted`, `Locked`; ODK-style review can be `Received`, `Edited`, `HasIssues`, `Rejected`, `Approved`.
- For offline MVP, use browser-local IndexedDB drafts and an explicit sync queue. Power Pages PWA offline support should not be treated as offline write/sync support unless Microsoft docs for the target date confirm it.
- For private developer or non-production sites, grant the CRDB/Microsoft Entra user access under Power Pages Site visibility before testing invitation redemption. This private-site allow-list is separate from Contact, Web Role, Table Permission, Invitation, and TACATDP assignment records.
- Download source with the command matching the artifact type. Use `pac pages download` / `pac pages upload` for Power Pages metadata source, and use `pac pages download-code-site` / `pac pages upload-code-site` for compiled custom front-end code-site artifacts. Check the installed PAC help before upload because argument shapes differ by command and CLI version.
- Keep Power Pages source under a dedicated package, for example `powerpages/tacatdp-monitoring-tool/` plus a sibling SPA package such as `powerpages/webforms-spa/`.
- For user-facing field work, treat the host as an operational monitoring shell, not a diagnostic proof page. The shell owns authentication state, project/form work queue, loading, top action bars, history, status, and debug panels; ODK Web Forms owns question rendering and validation.

## Purpose

Guide delivery of an ODK-like mobile field experience inside Microsoft-managed services:

- Power Pages as the authenticated hosting surface.
- Vue SPA as the field app shell.
- ODK Web Forms and `@getodk/xforms-engine` as the form runtime.
- Dataverse as the system of record.
- Power Pages Web API as the browser-to-Dataverse access layer.

## When to use this skill

Use when planning, implementing, reviewing, or validating:

- Power Pages site source downloads/uploads.
- `pac pages download-code-site` or `pac pages upload-code-site`.
- Power Pages Web API settings for Dataverse tables.
- Power Pages table permissions and web roles for a Dataverse-backed SPA.
- Private-site visibility grants, invitation activation, and external identity diagnostics for development/test users.
- Vue/ODK Web Forms integration hosted in Power Pages.
- ODK Central-inspired Dataverse schema design.
- Offline draft and sync queue design for Power Pages hosted apps.

## When not to use this skill

Do not use this skill for Canvas-only apps, PAC service-principal bootstrap, or generic Dataverse table administration. Use `power-platform-canvas-apps` for Canvas work and `power-platform-cli-admin` for PAC/admin/bootstrap work.

## Evidence to inspect first

- Current project architecture docs and ADRs.
- Downloaded Power Pages site source under the project `powerpages/` package.
- Current Dataverse schema artifacts and deployment scripts.
- Current `pac auth list`, `pac env who`, and `pac pages list` output.
- Project UX/design-system artifacts before frontend changes, especially Monitoring Tool UX contracts, brand assets, token/component files, and comparable mature project design-system docs.
- Official Microsoft docs for Power Pages Web API, table permissions, PWA/offline support, and PAC Pages CLI.
- Official Microsoft docs for Power Pages built-in file controls and file columns before claiming binary attachment support.
- Official ODK docs for Central API, form management, submission management, entities/datasets, and Web Forms.
- ODK Web Forms and Central Frontend package/repository state for the target date.

## Core concepts

- **Power Pages host**: the site provides Microsoft-managed hosting, authentication, web roles, table permissions, and `/_api`.
- **ODK runtime**: ODK Web Forms / XForms engine owns form rendering and XForms computation semantics.
- **XForms-first storage**: canonical XForm XML and submitted instance XML/JSON are source-of-truth payloads.
- **Versioned submissions**: a `Submission` is the header; `SubmissionVersions` records payload versions and current state.
- **Explicit offline**: browser local drafts and sync queues are implemented app features, not automatic Power Pages behavior.

## Architecture Rules

- The Power Pages SPA must not bypass Power Pages security when the requirement is Power Pages authentication plus table permissions. Use the Portals Web API path `/_api`.
- Configure Power Pages Web API site settings per table and field before browser code calls `/_api`.
- Configure table permissions/web roles before exposing a table through the site.
- Treat direct Dataverse table-permission rows and relationship rows as necessary but not sufficient. After table-permission or web-role changes, verify the Power Pages browser runtime with an authenticated `/_api` request; if the runtime returns `EntityPermissionReadIsMissing`, open/save the table permission and `Authenticated Users` association through Power Pages `Edit site > Security > Table permissions`.
- Treat private-site access as a separate prerequisite. A user can have Contact, Invitation, Web Role, and `mp_formassignment` rows and still be blocked if the Power Pages site is private and the user was not granted Site visibility access. If the site is private, verify Site visibility access before diagnosing activation or assignment.
- Browser code must request and send the Power Pages CSRF token for mutating `/_api` calls.
- Do not put client secrets, Dataverse app credentials, or bearer tokens in the SPA.
- Treat Dataverse file columns as a special case. Microsoft documents Dataverse file upload with single-request binary `PATCH` for files under 128 MB and block-upload actions for larger files, while Power Pages documents the portals Web API as a CRUD subset, JSON-oriented, and not supporting actions/functions. If a Power Pages SPA needs attachment binaries, first create the metadata record through `/_api`, then prove any file-column binary route in the hosted browser and report exact failures; do not assume ordinary JSON create stores the binary.
- Treat built-in Power Pages file controls as Dataverse form controls, not ODK runtime controls. Basic forms can attach files to notes or Azure Blob Storage when configured and permitted, but the control renders at the Dataverse form level. File-column upload in built-in forms requires an existing record; do not assume Insert-mode upload covers an ODK submission create flow.
- Treat Power Pages PWA installability as separate from offline writes. Build offline drafts/sync explicitly with IndexedDB.
- Keep ODK engine concerns separate from storage concerns: XForms engine renders/validates/finalizes; Dataverse stores form versions, submission versions, and attachments.
- Keep host UX concerns separate from ODK runtime concerns: host CSS may define shell spacing, top bars, loading panels, status banners, and ODK boundary spacing; it must not broadly restyle ODK controls with generic selectors.
- Keep XForm XML and submitted instance XML/JSON payloads intact so later ODK/OpenRosa/OData-style integrations remain possible.
- Lookup binds in browser `/_api` creates require association permissions on both sides. For TACATDP submission create, `mp_submission` needs create/append and `mp_formversion` must remain read-only but grant `Append To`; otherwise Power Pages returns `90040106 TablePermissionAppendToIsMissingDuringAssociationChange`.

## ODK Central-Inspired Dataverse Model

Use this as the default minimum model for Power Pages ODK Web Forms work:

- `Projects`: top-level collection of forms, assignments, and submissions.
- `Forms`: form/instrument identity with `XmlFormId`, display name, and lifecycle state.
- `FormVersions`: versioned canonical XForm XML with `Version`, `Hash`, `PublishedAt`, and `WebFormsEnabled`.
- `FormAttachments`: media/data files referenced by a form version.
- `FormAssignments`: which Power Pages/Dataverse user or email can fill a form version.
- `Submissions`: submission header with `InstanceId`, submitter, lifecycle, review state, and timestamps.
- `SubmissionVersions`: immutable/current payload versions containing instance XML and optional JSON projection.
- `SubmissionAttachments`: uploaded media/file records associated with a submission version.

Defer until required:

- `Datasets`, `Entities`, and `EntityVersions` for longitudinal records.
- `SubmissionAnswers` projection for analytics.
- OpenRosa-compatible endpoints.
- Full XLSForm compiler and authoring UI.

## Standard workflow

1. Confirm target environment and site:

   ```bash
   pac auth list
   pac env who
   pac pages list
   ```

2. Download current site source:

   ```bash
   pac pages download-code-site \
     --environment "<environment-url>" \
     --webSiteId "<website-id>" \
     --path ./powerpages \
     --overwrite
   ```

   For uploadable metadata source in PAC versions where `pac pages upload` requires `adx_*` fields, use:

   ```bash
   pac pages download \
     --environment "<environment-url>" \
     --webSiteId "<website-id>" \
     --path ./powerpages-upload \
     --overwrite \
     --modelVersion Enhanced
   ```

3. Create or update architecture artifacts before schema writes:
   - requirements,
   - ADR,
   - schema definition,
   - deployment runbook,
   - verification checklist.

4. Review the ODK Central-inspired schema and run a dry-run plan.
5. Deploy Dataverse schema only after explicit approval and target confirmation.
6. Configure Power Pages table permissions and Web API site settings only after explicit approval.
7. Add the SPA under a dedicated package such as `powerpages/webforms-spa/`.
8. Verify `/_api` prerequisites with an automated hosted-state smoke verifier before integrating ODK Web Forms. Manual browser navigation can be optional observation, but should not be the delivery gate.
9. Verify local draft save/restore before implementing submit.
10. Verify submit creates `Submissions`, `SubmissionVersions`, and `SubmissionAttachments` records in the same Dataverse environment as the Power Pages site.
11. Before sharing an MVP, replace proof-page diagnostics with a task-oriented shell: Microsoft/Power Pages login route, CRDB-branded app shell, project/form work queue, reusable loading panel, top action bar, history entry point, concise status banner, and a collapsible debug panel.

## Pitfalls

- Calling raw Dataverse Web API from a Power Pages SPA while expecting Power Pages web roles and table permissions to apply.
- Treating Power Pages PWA support as proof of offline draft/submit support.
- Designing only decomposed question/answer metadata and losing canonical XForm XML or instance XML.
- Mixing collection lifecycle (`Draft`, `Submitted`, `Locked`) with review state (`HasIssues`, `Rejected`, `Approved`) in one generic `Status` column.
- Creating Power Pages tables in the default environment while the Power Pages site lives in a developer/trial environment.
- Uploading a code site before verifying downloaded source structure and target site ID.
- Using `pac pages upload-code-site` for ordinary downloaded Power Pages metadata pages. In PAC CLI 2.8.1, metadata upload uses `pac pages upload --path ... --modelVersion Enhanced`; `upload-code-site` expects `--rootPath` and `--compiledPath` for compiled front-end code.
- Trusting exported JavaScript after a page upload/download round trip without a syntax check. Validate browser scripts with a local checker such as `node --check` before and after upload.
- Trusting automated Dataverse metadata verification as the only Power Pages permission gate. In TACATDP on 2026-07-10, `mspp_entitypermission`, `mspp_entitypermission_webroleset`, `powerpagecomponent_powerpagecomponent`, contact, external identity, and Liquid `user.roles` were all correct, but browser `/_api` still returned `EntityPermissionReadIsMissing` until the affected table permissions were saved in the Power Pages Security workspace.
- Installing ODK packages without documenting package versions, license, and maintenance state.
- Assuming an archived ODK Web Forms repository means the packages are obsolete; check Central Frontend and npm package state for the current date.
- Treating dependency-origin Vite/Rolldown warnings as TACATDP source defects without evidence. `@getodk/web-forms` may build successfully while warning about direct `eval` usage and large chunks in its distributed bundle; record this as an upstream package risk and revisit CSP/chunking before production hardening.
- Removing `.js` from Dataverse organization-wide blocked attachment extensions just to make `pac pages upload-code-site` work. First check the PAC log for `AttachmentBlocked`; prefer emitting browser module chunks as `.mjs` when the site can load ES modules and the environment blocks `.js`.
- Trusting `pac pages upload-code-site --siteName` when multiple site records can share the same name. In TACATDP on 2026-07-10, this created a duplicate `powerpagesite` with the same name and left the public URL serving the old Home page. For a known public site, download/upload the enhanced model package by explicit `--webSiteId` and verify the Home page record ids in Dataverse.
- Rendering `OdkWebForm` without installing `webFormsPlugin` in the Vue app bootstrap. Register the plugin with `createApp(App).use(webFormsPlugin).mount(...)` so ODK reset styles and PrimeVue configuration are available before the component renders.
- Seeding XForms with repeated body controls bound to the same node. ODK Web Forms rejects duplicate body refs, for example repeated `<group ref="/data">` wrappers fail with `Multiple body elements for reference: /data`. Use unbound section groups for presentation, bind only individual questions/repeats to unique instance nodes, and add source plus hosted verifier checks for duplicate body refs.
- Styling ODK controls from the host shell. ODK Web Forms imports Roboto, PrimeFlex, ODK global styles, component styles, and a PrimeVue theme through the package entrypoint/plugin. Host CSS must be scoped to host shell classes, must not target generic `button`, `input`, `label`, `select`, or `textarea` under the renderer, and should mount the form in a dedicated boundary such as `odk-runtime-host`.
- Treating a visible jump back to the top after ODK Send as proof of browser reload. In the TACATDP 2026-07-11 bundle inspection, ODK Web Forms/PrimeVue rendered the Send control as `type="button"`, so the first checks are: loaded build marker, ODK runtime click diagnostic, ODK submit-event diagnostic, Dataverse row count, and visible ODK validation errors. Power Pages server-side cache can also serve stale uploaded web files; clear cache through `/_services/about` or Power Pages preview before retesting a newly uploaded bundle.
- Treating metadata tables as universally read-only after submit is added. If a submission record binds to a metadata record, the referenced metadata table may need `Append To` while still denying create/write/delete. Use the exact Power Pages error code to decide; `90040106` indicates missing `Append To` for an association.
- Continuing to bind a lookup from browser `/_api` after verified Power Pages table permissions still return `90040106`. For MVP delivery, prefer an explicit documented compromise: persist canonical XML plus form-version identity in immutable submission-version JSON, avoid the failing lookup bind in the browser, and revisit server-side association or child table permissions after the vertical slice works.
- Assuming `SubmissionAttachments` binary storage is done because a metadata row exists. A Dataverse file column is virtual storage (`mp_file` in TACATDP) and binary upload needs a separate file-column request. Power Pages may reject non-JSON file requests even when record CRUD works; keep a browser-visible binary upload count/warning until hosted verification proves the route.
- Leaving runtime proof diagnostics in the primary user flow after the vertical slice works. Build markers, click diagnostics, ODK event diagnostics, and Dataverse write traces belong in a collapsed debug panel or development-only view before the MVP is shared.
- Letting the host shell force a tablet-style layout on phones. The work queue and form runner must have phone-width breakpoints verified in browser, and the ODK runtime should get the full form area under the top action bar.
- Applying CRDB colors as page-local CSS. Add project tokens from the CRDB logo/assets and consume those tokens through shared shell components.
- Treating a private developer/non-production Power Pages site as if invitation redemption alone grants access. Private site visibility is an upstream Microsoft gate: non-admin test users must be granted site access in Power Pages Studio before redemption/sign-in can complete. Disabled public/private visibility controls usually indicate developer-site or tenant governance restrictions, not a TACATDP role or assignment bug.
- Making the ODK `loaded` event the only path that clears a blocking "Loading form" overlay. If the runtime host mounts but the event is delayed or missed, the user can be trapped behind a spinner while the form is present. Keep a mount fallback, visible status, and refresh guidance.

## Safety rules

- Get explicit approval before Power Pages code upload, Dataverse schema writes, table permission changes, site setting changes, authentication changes, or package installation.
- Never put client secrets, Dataverse app credentials, bearer tokens, or tenant secrets in Power Pages source or SPA code.
- Keep target environment and website ID explicit before upload or schema write.
- Prefer additive schema operations. Do not delete or overwrite portal/site metadata unless the user approved that exact target.
- Treat public site visibility as a deployment risk; verify visibility before upload.

## Required checks

- Does `pac env who` show the same environment as the Power Pages site?
- Does `pac pages list` show the expected website ID?
- Are Dataverse schema, seed data, table permissions, and Web API settings in the same environment as the site?
- Is browser code using `/_api` when relying on Power Pages auth/table permissions?
- Are canonical XForm XML and submitted instance XML/JSON preserved?
- Is offline behavior explicitly implemented and tested rather than assumed from PWA support?
- Are ODK package versions, licenses, and maintenance state documented before install?

## Verification

- `karakana skill validate skills/power-pages-odk-webforms`
- `karakana eval run --skill power-pages-odk-webforms`
- `pac env who`
- `pac pages list`
- Dry-run Dataverse schema plan for the Power Pages environment.
- Automated hosted-state smoke test for Power Pages page records, Web API settings, table permissions, web-role links, EntitySetName values, assignment seed, form version, and form metadata.
- Required browser runtime smoke test of authenticated `/_api` read after permission or web-role changes. The page should show the expected Liquid contact, expected web role such as `Authenticated Users`, and a successful `/_api` read. If the error body includes `innererror.type = EntityPermissionReadIsMissing`, re-save the failing table permission and role association in Power Pages Security workspace, then restart and retest.
- Private-site onboarding smoke test: for developer/non-production sites, confirm the tester appears in Site visibility > People who can access the site before sending or redeeming an invitation; after redemption, confirm the invitation is no longer `New` and an `adx_externalidentity` exists.
- Browser smoke test of local IndexedDB draft save/restore.
- Browser smoke test of submission create with CSRF token.
- Browser smoke test of attachment metadata row creation and file-column binary upload result. Verify `mp_submissionattachments` row count and, only if the browser reports success, verify the Dataverse file column content.
- Browser visual smoke test for the Monitoring Tool shell at phone and desktop widths: authenticated work queue, form-card version display, CRDB loading panel, top action bar, isolated ODK runtime spacing, and hidden/collapsed diagnostics.

## Output format

```markdown
## Power Pages ODK Web Forms Check

- Target environment:
- Website:
- Source package:
- Dataverse schema:
- Power Pages Web API settings:
- Table permissions:
- ODK packages:
- Offline draft plan:
- Commands:
- Verification:
- Remaining risks:
```

## Examples

- If `pac pages list` shows no sites but maker portal created one, run `pac admin list` and authenticate to the `PowerPagesDeveloper-*` environment URL.
- If a Power Pages SPA must use table permissions, call `/_api/mp_forms` with CSRF handling rather than raw Dataverse Web API.
- If analytics need answer rows, generate `SubmissionAnswers` as a projection after storing `SubmissionVersions.XFormSubmissionXml`.
