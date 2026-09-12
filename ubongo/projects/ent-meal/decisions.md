# Enterprise MEAL Decisions

## 2026-08-24 — Platform name and repo

Decision: use `Enterprise MEAL` as the platform name and `ent-meal` as the repository name.

Rationale: the product is intended for Monitoring, Evaluation, Accountability, and Learning across SFU programmes and operations, not only the TACATDP proof of concept.

## 2026-08-24 — Django/Viewflow platform direction

Decision: use Django plus django-viewflow for the long-term application shell and workflow automation.

Rationale: CRDB indicated willingness to provide a new Docker-capable environment, and the platform requires configurable workflows, role-aware operations, and a conventional enterprise web application architecture.

## 2026-08-24 — PostgreSQL/Redis/Celery baseline

Decision: PostgreSQL, Redis, and Celery form the baseline development infrastructure.

Rationale: the platform needs transactional persistence, spatial and analytical extension path, asynchronous imports/projections, and workflow-adjacent background work.

## 2026-08-24 — XLSForm/XForm seam

Decision: treat form collection as a first-class subsystem with an XLSForm/XForm adapter seam.

Rationale: the TACATDP baseline came from KoboToolbox-style collection, and CRDB needs a long-term path for governed, versioned, field-capable forms without locking Enterprise MEAL to one external collection product.

## 2026-09-03 — Browser form runtime target

Decision: the Enterprise MEAL form runtime must preserve the working Power Pages form-runner behavior already proven in the TACATDP prototype, then improve it using XLSForm/XForm-informed long-form rendering patterns.

Rationale: runtime collection is not a simplified custom form renderer. It must render the active published form version, support long forms through sections/pages, save every browser submission into the same canonical `FormSubmission` store used by imports, preserve raw and normalized payloads, and route submitted evidence into verification before indicator projection. TACATDP is the first enabled configuration, but the runtime must remain configurable for future programmes, schemes, departments, and operational activities.
