# Enterprise MEAL Architecture

Enterprise MEAL is a configurable platform with TACATDP as the first programme configuration.

## Baseline stack

- Django for backend application services.
- django-viewflow for application shell and workflow automation.
- PostgreSQL for transactional data.
- Redis for cache and Celery broker/result backend in development.
- Celery for asynchronous work such as imports, form conversion, projections, notification preparation, and report generation.
- Microsoft Entra ID as the target enterprise identity provider.
- Microsoft Graph for future notification and Microsoft ecosystem integration where CRDB grants permission.

## Domain principle

Configure programmes; do not hard-code TACATDP.

Core concepts:

- Portfolio item: programme, scheme, product, initiative, or operational workstream.
- Results framework: configurable outcomes, outputs, activities, assumptions, and indicators.
- Indicator registry: definitions, units, formulas, data sources, disaggregation, verification, targets, and reporting frequency.
- Party registry: beneficiaries, groups, organizations, partners, and internal units.
- Intervention registry: finance products, practices, technologies, guarantees, insurance links, and operational actions.
- Observation and evidence: submitted data, attachments, GPS, audit trail, verification status, and indicator computation lineage.

## Form-runtime boundary

The field-data subsystem must support XLSForm/XForm-style forms. The first implementation should expose an adapter seam that can later support pyxform conversion, web runtime rendering, offline-capable collection, and import from KoboToolbox/ODK-style exports.

Do not make dashboard calculations depend directly on raw spreadsheet uploads. Import into governed entities, validate, then project indicators.

## Microsoft boundary

The first scaffold uses local auth only. Microsoft integration is planned behind an adapter layer:

- Entra OIDC sign-in.
- Entra groups/application roles to platform roles.
- Graph-backed email notifications or approved mailbox integration.
- Power BI embedding or workspace publishing if approved.

No Microsoft tenant secrets or credentials should be stored in source control.
