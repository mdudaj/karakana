# NHRILS Decisions

## 2026-08-04 - Use Invenio-App-ILS as vendor upstream

Decision: Keep `inveniosoftware/invenio-app-ils` as the vendor `upstream` remote and use `nimr-tz/nhrils` as the NIMR project `origin`.

Rationale: The project starts from Invenio-App-ILS but NIMR needs a durable fork/customization repository under the organization.

Implications:

- Pull vendor changes intentionally from `upstream`.
- Push NIMR customization branches to `origin`.
- Review NIMR fork history before any branch reset, force push, or customization.

Current setup:

- Local `master` tracks `origin/master` at `97dca62f`.
- Local `upstream-master` preserves the fetched Invenio upstream head at `fd71946a`.
- Do not merge `upstream/master` into `master` until the NHRILS rollout plan and user-provided docs are reviewed.
