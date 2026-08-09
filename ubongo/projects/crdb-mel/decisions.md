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

For the prototype portal dashboard, use Apache ECharts through `vue-echarts` for KPI charts and Leaflet through `@vue-leaflet/vue-leaflet` for maps. Lazy-load charts and maps after the dashboard shell renders.

Use MapLibre GL JS only as a future-product option when the platform needs vector tiles, WebGL rendering, or heavier geospatial layers.

## One-field-per-row form layout

Data-entry screens should default to one field per row with visible labels, helper/error text near the input, consistent spacing, and accessible focus order.

## App-layer validation for skip logic

Power Fx should enforce requiredness and constraints according to visibility/relevance. SharePoint columns that can be skipped should not be marked required.
