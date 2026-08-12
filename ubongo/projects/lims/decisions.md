# LIMS Decisions

## Phase 1 is single-lab

Decision: Implement a useful single-lab LIMS first.

Implications:

- Do not introduce tenant tables, tenant routing, entitlements, billing, or
  deployment stamps in phase 1.
- Keep stable extension seams for future Mtafiti integration.
- Keep lab identity explicit even when there is only one operating lab.

## Specimen is the canonical internal term

Decision: Use `specimen` for product and model language.

Implications:

- Avoid `sample` as internal model terminology except when mapping external
  source fields such as `source_sample_id`.
- Accession is the generic custody entry point for DBS, urine, whole blood,
  plasma, serum, DNA, aliquots, and other controlled local specimen types.

## Operation engine is the governed execution boundary

Decision: Regulated capture should pass through operation definition/version,
workflow node, runner, runtime submission evidence, ingest decision, and typed
domain projection.

Implications:

- Do not add direct governed capture to domain forms or templates.
- Published operation versions are immutable.
- Domain records such as `SpecimenAccession`, `QcDecision`, `StorageUpdate`,
  and downstream results are projection outputs from accepted evidence.

## Viewflow-backed runner with custom LIMS UX

Decision: Use Viewflow for process/task lifecycle, but do not expose default
generic Viewflow task UX as the final LIMS operator experience.

Implications:

- Worklists, specimen/batch cockpits, workflow path strips, runtime runner
  pages, and reconstruction views are LIMS-owned surfaces built on Viewflow/MDC
  primitives.
- React is the target browser renderer for the operation runner; Django and
  Viewflow remain authoritative for validation, evidence, workflow completion,
  projection, audit, and reconstruction.

## User creation is invitation-based

Decision: Normal product user creation goes through LIMS-native invitations
created by a Laboratory Manager.

Implications:

- No open self-registration.
- Invite tokens are stored as digests and expire.
- Invited users set their own password from a one-time invite link.
- Controlled roles are backed by Django groups.
- The last active Laboratory Manager cannot be deactivated or demoted.

## User emails use configured SMTP without tracked secrets

Decision: User invitation, resend, role-change, deactivation, and reactivation
notifications send through Django's configured email backend.

Implications:

- Gmail SMTP can be used through environment variables or deployment secrets.
- Real app passwords must never be committed, printed, or stored in durable
  docs.
- If email delivery fails after an account action succeeds, the manager sees a
  visible warning and the account action remains recoverable.
- Tests should use Django's in-memory email backend and must not send real
  external email.
