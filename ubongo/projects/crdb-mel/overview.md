# Sustainable Finance MEL Platform Overview

Sustainable Finance MEL Platform is a Microsoft Power Platform project for converting a long XLSForm/ODK-style data collection workflow into Microsoft-managed services for Monitoring, Evaluation, and Learning.

The project was previously tracked as TACATDP. Use Sustainable Finance MEL Platform for the current product/system name, documentation pack, project memory, and future product vision. Keep TACATDP where it refers to the original programme, source XLSForm labels, deployed Power Platform artifact names, proof-of-concept use case, or historical implementation evidence.

As of the 2026-08-01 CRDB SFU context review, Sustainable Finance MEL Platform should be treated as a reusable Integrated Digital MEL platform for Sustainable Finance Unit programmes/projects. TACATDP monitoring is the proof-of-concept implementation, but future-ready design should preserve seams for programmes/projects, beneficiaries, facilities, operational processes, resources, financial and institutional records, climate rationale, field evidence, indicator results, ESS/risk, geo insights, operational efficiency, and reporting templates.

The current delivery path is Dataverse-first with Power Pages as the preferred ODK-style field UX host. The Canvas app remains useful as a proof-of-concept and possible internal admin/monitoring surface, but the long-term field runner should be a Power Pages hosted Vue SPA using ODK Web Forms / `@getodk/xforms-engine`, saving to Dataverse through the Power Pages Web API `/_api`.

The long-term app vision is a reusable platform, not only a TACATDP monitoring app, but full multi-project implementation is a larger research track. The near-term implementation should deliver the TACATDP proof of concept while preserving seams for project, form, form version, XForm XML, assignment, submission, submission version, attachment, review state, dataset/entity, normalized answer projection, beneficiary identity, configurable monitored entities, KPI visualisation, and controlled vocabulary concepts. Microsoft Lists/SharePoint artifacts remain as fallback and source-decomposition evidence.

## Current Delivery Intent

- Build implementation only after skills, memory, workspace context, and OKF artifacts are registered.
- Every TACATDP research, brainstorming, documentation, schema, PAC, Dataverse, or Canvas implementation step must be grounded in inspected evidence: TACATDP repository artifacts, current exported Canvas source/package metadata, Dataverse schema files, PAC/runtime output, official Microsoft documentation for unstable Power Platform behavior, and the relevant Karakana skills.
- Delivery docs must include implementation instructions for the next agent: files/artifacts to inspect, Microsoft references to check, commands to run, expected outputs, known failure signatures, and Studio/App Checker gates where applicable.
- Repeated Power Platform failures must be encoded in `power-platform-*` skills and TACATDP validators/package scans before a new artifact is considered ready.
- Phase 3 is the active direction; backend work now has review-only multi-project Dataverse schema artifacts under `schemas/dataverse/` in the TACATDP repository. Do not create Dataverse tables until those artifacts are reviewed and approved.
- While Dataverse schema is being prepared, use placeholder data-source bindings and document the real Dataverse tables to substitute later.
- Use the `power-pages-odk-webforms` skill for Power Pages, ODK Web Forms, Power Pages Web API, offline draft, and ODK Central-inspired schema work.
- Use the `power-platform-canvas-apps` skill only for Canvas proof/admin UX, Power Fx, Canvas packaging, and Canvas-specific Dataverse binding.
- Use the `power-platform-cli-admin` skill for PAC auth, Power Pages environment checks, Dataverse schema writes, app users, and permission/bootstrap work.
- Prefer Power Platform solution-ready Dataverse schema artifacts over manual creation of TACATDP-only tables.
- Treat the fixed Canvas source as transitional proof. The long-term project-platform field UX should be a Power Pages hosted ODK Web Forms runtime that loads XForm XML/form-version records from Dataverse, stores drafts locally when offline support is in scope, and writes submissions/versioned payloads/attachments back to Dataverse through `/_api`.
- The Power Pages site currently confirmed by PAC is `TACATDP Monitoring Tool` in `PowerPagesDeveloper-070926-125720` at `https://orga3cf4b37.crm4.dynamics.com/`. Any Dataverse schema used by the Power Pages SPA must be deployed to the same environment as the site.
- Do not let the full multi-project renderer/platform vision block the TACATDP prototype; document shortcuts and revisit them before platform generalization.
- Do not mirror TACATDP M&E workbook sheets directly as application routes or Dataverse tables. Treat client Excel/DOCX inputs as evidence for domain concepts, indicators, workflows, and reporting outputs, then translate them through professional product/system design.
- Keep the Canvas App implementation simple and reviewable; Git can help source-control Canvas App changes after the app is created, but solution packaging is the durable path for Dataverse tables, relationships, choices, flows, and app components.

## Active Dataverse Artifacts

- `docs/powerpages-odk-webforms/`
- `ubongo/projects/crdb-mel/django-viewflow-pivot-research.md`
- `ubongo/projects/crdb-mel/ent-meal-bootstrap-plan.md`
- `schemas/dataverse/odk-central-inspired-mvp-schema.json`
- `schemas/dataverse/odk-central-inspired-mvp-schema.md`
- `schemas/dataverse/platform-tables.json`
- `schemas/dataverse/platform-columns.csv`
- `schemas/dataverse/platform-relationships.csv`
- `schemas/dataverse/platform-alternate-keys.csv`
- `schemas/dataverse/tacatdp-field-definitions.csv`
- `schemas/dataverse/tacatdp-vocabulary-terms.csv`
- `schemas/dataverse/tacatdp-village-reference.csv`
- `schemas/dataverse/import-order.md`
- `schemas/dataverse/form-renderer-contract.json`
- `docs/multi-project-monitoring/form-renderer-ux.md`
- `docs/app-vision.md`
- `docs/tacatdp-prototype-slice-1/`

These artifacts are review inputs unless an explicit environment-write approval is given. The ODK Central-inspired schema is the preferred path for the Power Pages ODK Web Forms MVP; the earlier metadata/question/answer renderer artifacts remain useful for Canvas proof work and analytics projections.

## Active Phase

Phase 3 should pivot to TACATDP Power Pages ODK Web Forms Slice 1: one Power Pages hosted Vue shell, one published XForm-backed form version, one user assignment, authenticated `/_api` read, local draft save/restore, online submit to Dataverse, and one attachment record. Use `docs/powerpages-odk-webforms/` as the implementation scope. Keep `docs/tacatdp-prototype-slice-1/` and `docs/canvas-renderer-mvp/` as Canvas proof history.

## Active UX Requirements

- The managed shell owns route identity. The side navigation and sticky top bar provide the current route title, global route actions, and navigation state; page content must not repeat the same route title in a second large banner.
- Content pages start with the current work surface: dashboard operational status, project list, selected-project context, user/access table, or system activity tabs. Use compact section headings inside those surfaces; reserve large object headers only for a selected business object such as a project.
- Top-level administration and project routes must use shared route chrome/action slots rather than page-local `top-action-bar` hero sections. If a route needs actions such as Back, Refresh, or Add user, place them in the shell action lane or a compact content toolbar.
- Use one field per row by default on data-entry screens.
- Use visible labels above inputs; never rely on placeholders as the only label.
- Put helper text and error text directly below the field.
- Use consistent spacing, section hierarchy, and wizard-style navigation for long forms.
- Preserve accessible focus order, touch targets, validation summaries, and save/error states.
- Prefer ODK Web Forms / XForms engine behavior for required, relevant, constraints, calculations, repeats, media, and geopoint semantics instead of rebuilding those semantics in Power Fx.
- Offline behavior must be explicit: browser local draft storage and a sync queue are not provided merely by enabling Power Pages PWA installability.
- Before changing UX, document expected behavior and data scope: shared versus current-user data, loaded record limit/pagination, search fields, action semantics, and empty/loading/error states. For the current Monitoring Tool proof, Saved records are shared submitted records readable by authenticated Power Pages table permissions; Add new remains scoped to the signed-in user's form assignments.

## Power Pages Invitation Lesson

- Private site visibility is an upstream Power Pages access gate. For developer or non-production sites, Microsoft may force the site to remain private and disable the public/private visibility controls; that does not mean TACATDP roles are broken. Before testing a non-admin invitee, add the organization user under Power Pages Studio > Security > Site visibility > Grant site access. Only after that should the invitee redeem the invitation and sign in. This Mshirika lesson applies to CRDB until the site is moved to approved public/production visibility.
- For TACATDP Power Pages onboarding, do not treat a generated invitation URL or a user reaching Microsoft sign-in as proof of access activation. The proof is Dataverse state: the invitation is no longer `New`, the Contact has an `adx_externalidentity` row, and the Contact/session has the expected Power Pages web role and active `mp_formassignment`.
- If a user enters an invitation code, is routed to Microsoft sign-in, and then lands on Access Denied with the invitation still `New` and no `adx_externalidentity`, redemption did not complete. Do not recycle the same link as the fix; inspect authentication/registration site settings, the actual redemption route, open-registration behavior, identity-provider mapping, and web-role/contact linkage.
- CRDB has shown that Contact login flags and active assignments can exist without an external identity binding. For collectors, verify contact, external identity, invitation status, web role, and assignment together before diagnosing email format or assignment scope.

## Power Pages Dataverse Write Lesson

- For Power Pages Web API writes to Dataverse Choice columns, send numeric option values, not display-label strings. CRDB returned `400` / `9004010D` / CDS code `0x80048d19` when the portal attempted to create `mp_accessauditlog` rows with text values such as `RemoveAssignment`, `Requested`, or `Assignment` for Choice columns.
- Before diagnosing assignment deactivation or email correction as a table-permission problem, verify whether the audit row was created. If no `mp_accessauditlog` row exists for the attempted action, inspect audit payload Choice values first.
- Use CRDB-generated modelbuilder artifacts and flow payloads as stronger evidence than planned schema prose. The onboarding processor correctly used numeric values such as `mp_action=100000002`, `mp_resultstatus=100000000`, and `mp_scopetype=100000003`.

## Review Questions

- Which exact TACATDP artifacts, Microsoft docs, exported packages, runtime errors, or validators prove the implementation approach?
- Which implementation instructions will let the next agent reproduce the work without relying on chat history?
- Which validator, eval, or package scan prevents a known failure from reappearing?
- Does the implementation preserve XLSForm required rules, skip logic, constraints, choice values, labels, and calculations?
- Does the data model keep TACATDP as a project configuration rather than hard-coding TACATDP as the platform schema?
- Are repeat groups and multi-select answers normalized as group instances and child answer rows?
- Are controlled variables implemented through governed vocabulary schemes and terms rather than hard-coded choices?
- Are Dataverse filters delegation-safe for large reference tables?
- Are skipped fields enforced through visible-only app validation rather than unsafe required backend columns?
- Are repeated or multi-select answers modeled as child rows where reporting requires one row per item?
- Can the user create/review generated Dataverse schema artifacts before environment writes?
- Are placeholder data sources isolated enough to swap for real Dataverse tables later?
