# Sustainability Monitoring and Reporting Platform decisions

## 2026-09-27 — Apply the agreed public name

Decision: use **Sustainability Monitoring and Reporting Platform**, as already
recorded in the requirements baseline and platform overview v0.2. Use
**Sustainability Reporting** for compact navigation. This supersedes the original
August naming decision below; do not ask for naming approval again.

The earlier contract and project memory were stale. Read the approved requirements
and current overview before choosing user-facing terminology. The application
keeps `ent-meal`, `ent_meal`, `ENT_MEAL_*`, saved group names, role keys and deployment
identifiers for compatibility. Display role labels rather than saved group names.
Original distributed workbooks, reports, ADRs and delivery evidence remain unchanged.
Current clarification reviews are v0.4, with one Reviewer comment column.
Notifications use a send-only no-reply sender. The user confirmed that this
mailbox does not receive replies; do not request a reply-to or support mailbox.

References: `/home/jmduda/KodeX/ent-meal/docs/requirements/baseline/01-full-product-requirements-baseline.md`,
`/home/jmduda/KodeX/ent-meal/docs/overview/platform-overview-v0.2.json`, and
`/home/jmduda/KodeX/ent-meal/docs/ux/product-naming.md`.

## 2026-08-24 — Platform name and repo (superseded)

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
