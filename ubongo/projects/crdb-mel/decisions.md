# Sustainable Finance MEL Platform Decisions

Sustainable Finance MEL Platform is the current product identity. Existing `TACATDP_*` artifact names are retained where they refer to generated schemas, deployed list/table names, source form labels, or historical programme context.

## Historical Microsoft Lists fallback

Microsoft Lists/SharePoint was used during early brainstorming and fallback planning. Do not present Microsoft Lists or Canvas as the active prototype architecture unless the current repository artifacts prove the work has moved back to that path.

The active prototype direction is Power Pages with a Vue SPA, ODK Web Forms runtime, and Dataverse-backed assignments, submissions, reporting projections, and access-management tables.

## Importable list templates

Generated Excel/CSV templates are preferred for creating Microsoft Lists where possible. This reduces manual list and column creation.

## Skill-first implementation

Implementation should not start until the relevant Karakana skill, project memory, workspace registration, and OKF concepts are present and validated.

## Phase 3 with placeholder data sources

Phase 3 may continue with explicit prototype shortcuts while environment permissions are incomplete. Keep shortcuts isolated and document their replacement path. For the current Power Pages prototype, beneficiary KPI and map panels may derive insights from `mp_submissionreportrow.mp_rootanswersjson` until a governed beneficiary master table is approved.

## Portal visualisation libraries

For the prototype portal dashboard, use Apache ECharts through `vue-echarts` for KPI charts and the Tanzania regional choropleth map. The map should use a local Tanzania ADM1 GeoJSON asset rather than external tile services.

The previous Leaflet marker-map slice is superseded. Do not reintroduce Leaflet for this dashboard unless a later map requirement specifically needs pan/zoom tiles or marker-heavy geospatial exploration.

Use MapLibre GL JS only as a future-product option when the platform needs vector tiles, WebGL rendering, or heavier geospatial layers.

## Dashboard route separation

The default Dashboard route is a high-fidelity TACATDP visualization route for the single-project prototype. Operational workbench components should live under Workspace/Data Submissions so visualization is not mixed with form operations.

The left drawer may keep Administration and `Organizations` visible for product shape. In the current prototype, `Organizations` is a future-ready placeholder for responsible organizations such as implementation partners, CRDB units/branches, cooperatives, AMCOS/SACCOS, and similar institutional actors.

## One-field-per-row form layout

Data-entry screens should default to one field per row with visible labels, helper/error text near the input, consistent spacing, and accessible focus order.

## App-layer validation for skip logic

Power Fx should enforce requiredness and constraints according to visibility/relevance. SharePoint columns that can be skipped should not be marked required.
