# ILMS Development Bench Delivery

## Requirements and authority

The user approved execution on 2026-10-16 of the ILMS public recovery-link
correction, an isolated development bench, project registration in Karakana,
and reusable skills with evaluations. The prior PR/squash-merge and GitOps
delivery convention applies. No harness execution policy or model routing
implementation changes are required.

ILMS means the eGA Angular/Express frontend and DHIS 2.33 library system.
It is distinct from the Django laboratory LIMS and Invenio-based NHRILS.
The workspace entry must retain those boundaries.

## Evidence and decisions

- eGA project 1017, branch `nimr`, owns Angular and the registration proxy.
- `nimr-tz/nimr-ilms` owns the runtime image, NIMR overlays, and development bench.
- `nimr-tz/platform-gitops` owns production configuration and image pins.
- DHIS 2.33 `AccountController.recoverAccount` passes the incoming request's
  context path into `DefaultSecurityService.sendRestoreMessage`.
- `ContextUtils.getContextPath` reads the request server name and forwarded
  protocol/port; `system.base_url` does not control this email link.
- The proxy used `http://ilms:8080/api/` without public-origin headers. SMTP
  acceptance and a generic 202 did not verify the generated email body.

The proxy will use an explicit public origin for DHIS link-generating requests.
The bench will use the deployed DHIS image, PostgreSQL 15, synthetic metadata,
Mailpit, a local HTTPS gateway, the proxy, and the compiled Angular frontend.
It will have an internal Docker network and loopback-only published ports.
Production records and credentials are excluded.

## Implementation

1. Correct and test public-origin forwarding in eGA source; configure its
   public origin in GitOps before the image rollout.
2. Put repeatable bench setup and executable account-flow tests in the NIMR
   runtime/overlay repository. Record exact source/overlay revisions and dirtiness.
3. Register `ilms` at `../apps/nimr-ilms` in workspace `nimr`; map eGA source
   and GitOps as related repositories in project memory rather than duplicating
   source in the public harness.
4. Add `dhis2-legacy-account-flow` and `gitlab-gitops-delivery` skills, project
   skillpack and six project-memory documents. Reuse existing review, CI, and
   handoff skills. Add agent entry instructions in the project repository.

## Verification rationale

The executable bench tests must capture the real email body, validate its HTTPS
origin, open the native form, redeem the token, authenticate the new password,
reject the old password and reused/expired tokens, and complete an invitation.
Unknown and shared email addresses must not select an account. Caller-supplied
forwarding headers must not control the emailed URL.

Karakana validation checks skill metadata, memory, skillpack and workspace
references. Deterministic skill evals check that generated task context includes
the required constraints; they do not prove agent compliance or runtime behavior.
Run the repository's full tests before merge. Keep tokens, passwords, captured
mail and generated TLS keys outside tracked files.

## Verification results

- eGA MR !9 is squash-merged at `16cbb003a8c9bf9b53a1aa3a3475b988960755bf`.
  Both proxy regression tests pass, including fixed public-origin headers,
  malformed configuration and credential-safe startup warnings.
- GitOps PR #95 configured the public origin before rollout. eGA pipeline
  #52191 passed all jobs and promoted `ega-16cbb003-nimr13` through GitOps commit
  `247972afe076319c0689de7f2831e4f03161303d`. Argo and both image rollouts were
  observed Synced/Healthy. A fresh production recovery email was accepted by
  the eGA relay on 2026-10-16; recipient inbox receipt is not independently proven.
- Runtime/bench PR #30 is squash-merged at
  `2ed2e639916a29673905943eeebe45403b8ab5cc` and passed GitHub validation.
  Seven real account checks and desktop/mobile browser checks passed using the
  clean eGA source revision. Screenshots and secret-free reports are local in
  `../apps/nimr-ilms/.devbench/` after installation.
- The runtime workflow initially rebuilt the unchanged DHIS image because it
  classified all `scripts/` files as runtime inputs. The resulting `-31` image
  has identical filesystem layers to `-30`. Squash-merged runtime PR #31 narrows this scope,
  adds three regression tests, includes runtime patches in the build trigger,
  and aligns the bench with the latest immutable runtime artifact. GitHub main
  run #32 passed and correctly skipped both runtime build and GitOps promotion.
- Karakana: 728 repository tests passed; all 175 deterministic eval cases
  passed; skill, skillpack and ILMS memory validation passed. Workspace
  validation reports existing absent LIMS/MSc checkouts, unrelated to ILMS.
- Clean startup from newly created synthetic volumes passed at the permanent
  `../apps/nimr-ilms` checkout. Seven account checks and two browser checks
  passed without the exploratory setup commands used during development.
  The source checkout at `../apps/ega-ilmis` is clean at merged `16cbb003`.
  The final repeat also passed on clean overlay `fd0f7e4` and the digest-pinned
  `-31` runtime. Both source/overlay dirty flags are false in the local report.

## Delivery links

- [eGA source MR !9](https://external.ega.go.tz/fredrick.abisai/nimr-ilmis/-/merge_requests/9)
- [eGA pipeline #52191](https://external.ega.go.tz/fredrick.abisai/nimr-ilmis/-/pipelines/52191)
- [Public-origin GitOps PR #95](https://github.com/nimr-tz/platform-gitops/pull/95)
- [Development bench PR #30](https://github.com/nimr-tz/nimr-ilms/pull/30)
- [Runtime scope PR #31](https://github.com/nimr-tz/nimr-ilms/pull/31)

## Lessons encoded

The bench records several requirements that mocks did not expose: the initial
DHIS migration needs an increased PostgreSQL lock limit; the mail configuration
requires nonempty SMTP credentials; `.invalid` fixture emails are rejected;
recipients are BCC; and reusing deleted fixture identities can leave cached
principals pointing to old rows. Fresh per-run fixture identities avoid that
cache artifact. Test commands remove stale success reports and clean up users.

The new skills remain experimental. A passing deterministic prompt eval does
not establish that an agent followed it; the executable bench tests provide
the application evidence.

## References

- https://github.com/dhis2/dhis2-core/blob/2.33.0/dhis-2/dhis-web/dhis-web-api/src/main/java/org/hisp/dhis/webapi/controller/AccountController.java
- https://github.com/dhis2/dhis2-core/blob/2.33.0/dhis-2/dhis-web/dhis-web-api/src/main/java/org/hisp/dhis/webapi/utils/ContextUtils.java
- `skills/write-karakana-skill/SKILL.md`
- `docs/workspaces.md`
- `docs/skillpacks.md`
