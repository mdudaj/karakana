# LIMS Known Issues

- `ubongo/projects/lims` was missing until 2026-08-12 even though
  `workspaces/nimr.yml` and `skillpacks/lims.yml` already referenced it.
- Direct SQLite test fallback fails during migration because
  `apps/specimens/migrations/0012_alter_operationalevent_event_type_and_more.py`
  uses PostgreSQL-specific `DROP TABLE ... CASCADE` SQL.
- `lims-reconstruction-package-001` is intentionally deferred behind MVP
  operational readiness.
- Bulk downstream step submission and non-DBS downstream profile packs are
  follow-up slices.
- A Gmail app password was pasted in chat during the email setup discussion on
  2026-08-12. Treat it as exposed and rotate it before production or shared
  testing use.
