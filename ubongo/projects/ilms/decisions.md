# ILMS Decisions

- 2026-10-16: Preserve the eGA source, NIMR runtime/overlay, and GitOps ownership
  boundaries. Do not vendor private eGA source into the public harness.
- 2026-10-16: Add an isolated bench to the runtime repository and register
  ILMS separately from LIMS/NHRILS in Karakana.
- 2026-10-16: Configure a public origin for DHIS-generated links. Derive its
  Host, X-Forwarded-Proto and X-Forwarded-Port headers server-side; ignore
  caller-supplied alternatives for that upstream request.
- 2026-10-16: Validate actual captured email, native form, redemption and
  subsequent login before calling account recovery verified.
- 2026-10-16: Keep new skills experimental. Deterministic skill evals verify
  prompt context, not model compliance or the running application.
