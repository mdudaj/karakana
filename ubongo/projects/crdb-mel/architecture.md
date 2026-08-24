# Sustainable Finance MEL Platform Architecture

Sustainable Finance MEL Platform is the current project identity. TACATDP remains the historical programme/form context and is still used by several existing schema, list, form, and deployment artifacts.

## Platform

- Frontend/application: Power Pages hosted Vue SPA for the current prototype.
- Form runtime: ODK Web Forms / XForms engine for XLSForm-compatible baseline collection.
- Data layer: Dataverse tables exposed to the portal through Power Pages Web API and table permissions.
- Source form model: XLSForm-style survey with required rules, relevance/skip logic, constraints, choices, calculations, and repeats.
- Deployment support: source-controlled Power Pages package, Vite SPA build assets, Dataverse schema/seed scripts, PAC runbooks, and validation scripts.

## 2026-08-24 Architecture Pivot Under Review

- Current CRDB Power Pages delivery is paused at a known permission blocker: browser XML upload fails because the effective portal administrator role lacks `Create` permission on `mp_formversion`.
- New CRDB information indicates the bank may provide a new Docker-capable environment. Treat this as a potential architecture pivot, not yet a completed decision.
- If approved, the next product architecture should move from Power Pages as the main application runtime to a configurable SFU MEL platform built around Django, PostgreSQL, Redis, Celery, Viewflow, and related Python/Django ecosystem libraries.
- The future platform should remain Microsoft-integrated where CRDB policy requires it, but the core application model should support multi-project, multi-programme, and operational MEL use cases through configuration rather than TACATDP-specific hard-coding.
- Before creating the new repository, run a research and planning slice covering architecture, Microsoft tenant integration, authentication/SSO, deployment topology, data model, workflow engine, background jobs, reporting, and migration path from the current Power Pages prototype.

## Data Architecture

- Baseline submissions are stored in Dataverse submission/version/attachment records.
- Reporting projections provide root submission rows, repeat rows, and answer rows for portal reporting and export.
- The earlier mixed beneficiary KPI/map panel is superseded by a dedicated TACATDP dashboard route that uses structured demonstration data until governed live KPI projections are approved.
- Future accepted-product architecture should introduce centrally governed beneficiary master data, programme/project membership, configurable indicators, and stronger data governance.
- Multi-select and repeat data should use child rows when analytics or reporting need one row per selected/repeated item.
- Large or cascading choices should use governed reference data with indexed parent keys rather than hard-coded app collections.
- Skip-eligible fields should not be required backend columns unless the visibility/relevance rule is represented server-side.

## Portal UX Architecture

- The managed shell owns route identity, side navigation, sticky top bar, and footer.
- The default Dashboard route is the dedicated TACATDP visualization dashboard for the current proof of concept.
- Operational workbench content belongs under the Workspace/Data Submission route, not mixed into the visualization dashboard.
- Use Apache ECharts through `vue-echarts` for prototype KPI charts and the Tanzania ADM1 choropleth map.
- The Tanzania map uses a local geoBoundaries ADM1 GeoJSON asset to avoid external tile dependencies in Power Pages.
- Lazy-load chart libraries after the shell renders.
- Keep the Administration drawer area visible. `Organizations` is a future-ready placeholder for implementation partners, CRDB units/branches, cooperatives, AMCOS/SACCOS, and other responsible institutions; it is not a core TACATDP-only prototype workflow yet.

## Integration Notes

- Keep TACATDP where deployed forms, source XLSForm labels, Dataverse logical names, package paths, and historical artifacts still use that name.
- Use Sustainable Finance MEL Platform for product-facing documentation and future vision.
- Do not deploy Power Pages packages or write Dataverse schema/data without explicit approval.
