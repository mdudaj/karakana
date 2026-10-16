# ILMS Open Issues

- Public-link correction is deployed and the account/browser bench tests pass.
  Inspect the delivery record and latest handoff before selecting follow-up work.
- Production service credentials previously embedded in an old frontend bundle
  need a coordinated rotation and service-account scope review. The bench and
  harness must not contain those values.
- OPAC remains a distinct eGA project (1023) with a separate automation rollout.
  ILMIS CI success does not establish OPAC CI readiness.
- Broader circulation, counts and soft-copy issues need their own acceptance
  criteria and synthetic fixtures before changes are attempted.
