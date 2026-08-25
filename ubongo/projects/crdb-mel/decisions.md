# Sustainable Finance MEL Platform Decisions

Sustainable Finance MEL Platform is the current product identity. Existing `TACATDP_*` artifact names are retained where they refer to generated schemas, deployed list/table names, source form labels, or historical programme context.

## Historical Microsoft Lists fallback

Microsoft Lists/SharePoint was used during early brainstorming and fallback planning. Do not present Microsoft Lists or Canvas as the active prototype architecture unless the current repository artifacts prove the work has moved back to that path.

The active prototype direction is Power Pages with a Vue SPA, ODK Web Forms runtime, and Dataverse-backed assignments, submissions, reporting projections, and access-management tables.

## 2026-08-24 CRDB Docker-capable environment option

CRDB may provide a new environment that allows Docker. Pause assumptions that the long-term SFU MEL platform must run primarily inside Power Pages/Dataverse.

The current Power Pages prototype remains useful for demonstration and for preserving baseline-import lessons, but the next architecture planning slice should evaluate a new repository for a configurable SFU MEL platform using Django, PostgreSQL, Redis, Celery, Viewflow, and related Python/Django ecosystem libraries. The target product should support multiple projects, programmes, and operational MEL workflows for the SFU department.

This is not approval to abandon the existing Power Pages demonstration. Continue to treat CRDB Power Pages updates as a demonstration-maintenance path until the Docker-capable environment and new architecture are formally confirmed.

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

Dashboard chart refinements must be based on the relevant official ECharts examples/docs before implementation. For line charts, preserve explicit grid gutters, `grid.containLabel`, axis-label margins, point-label `position`/`distance`, and overlap protection where labels are visible. Add or update a repeatable visual-spacing guard when a chart layout issue is fixed so the same overlap does not return silently.

Use compact numeric axis labels as the default dashboard convention. Do not repeat units such as `B`, `%`, `TZS`, or `tCO₂e` on every axis tick when the unit can be shown once in the chart title, subtitle, axis name, legend, or nearby caption. This keeps dense cards readable and avoids label collisions. Visual guards should enforce this convention for compact dashboard charts.

For compact category line charts with visible point labels, keep `xAxis.boundaryGap` enabled by default. Disabling it places the first/last point directly on the chart edge or y-axis gutter, which can make the first point label collide with y-axis tick labels even when `grid.containLabel` is enabled.

## Dashboard route separation

The default Dashboard route is a high-fidelity TACATDP visualization route for the single-project prototype. Operational workbench components should live under Workspace/Data Submissions so visualization is not mixed with form operations.

The left drawer may keep Administration and `Organizations` visible for product shape. In the current prototype, `Organizations` is a future-ready placeholder for responsible organizations such as implementation partners, CRDB units/branches, cooperatives, AMCOS/SACCOS, and similar institutional actors.

## Dashboard card background imagery

Cards that need full-surface illustration or photographic artwork should use a reusable card background layer or background slot behind the card header/content. Do not place the image as ordinary card content with `object-fit: contain`, because it leaves unused space and makes the artwork look detached. Use an absolutely positioned background layer with `inset: 0`, `overflow: hidden`, `object-fit: cover`, and an explicit `object-position` chosen for the asset. Keep text content in a higher z-index layer and use a readable contrast treatment when the background sits behind copy.

## Metric card accent rail

Use the subtle 4 px left accent rail only on KPI/metric summary cards, not on every elevated content card. On the dashboard, the rail belongs on the first-row KPI cards through `KpiCard`; analytic/content cards rendered by `DashboardCard` remain plain elevated surfaces. On route pages such as Beneficiaries, the rail belongs on the metric summary row only; hero, filter, table, list, and other content cards should use plain `SurfaceCard`.

The rail must stay in shared metric-card primitives or explicit opt-in metric modes, not page-local borders. Pages may choose a semantic tone such as green, blue, amber, purple, red, or neutral for metric cards, but they should not redefine the rail anatomy. Validators should check both sides of the rule: metric cards keep the accent token and pseudo-element, while generic content cards do not shade themselves by default.

Use `scripts/validate-route-card-accent-scope.mjs` as the guard against decorative route-card rails. It should allow metric-card rails, active navigation, semantic warning/error/success status treatments, ODK focus/error indicators, and the project-list card shade while that temporary exception is desired. It should reject brand/accent left rails on route headers, user cards, form/data cards, drawers, pagination, connection panels, and similar content surfaces.

Important clarification: "Metric-card rail" means every card that uses the shared `.metric-card` primitive gets the metric rail. Do not interpret the rule as "only the first metric card in a strip." Users route, Project Detail summary, Reporting summary, System Activity summary, and Activation summary metric rows should show the rail on each metric card while non-metric content cards remain plain.

## One-field-per-row form layout

Data-entry screens should default to one field per row with visible labels, helper/error text near the input, consistent spacing, and accessible focus order.

## App-layer validation for skip logic

Power Fx should enforce requiredness and constraints according to visibility/relevance. SharePoint columns that can be skipped should not be marked required.
