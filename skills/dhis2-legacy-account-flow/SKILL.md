---
name: dhis2-legacy-account-flow
description: Diagnose and verify DHIS 2.33 login, recovery and invitation integrations, including public email links behind reverse proxies.
version: 0.1.0
risk_level: high
category: domain
scope: bundled
status: experimental
visibility: public
bucket: domain
activation:
  keywords: [DHIS account recovery, DHIS invitation, ILMS password reset]
  optional_tools: [docker, node, curl]
allowed_tools: [read_file, grep, code_search, run_tests]
requires_approval_for: [authentication_change, permission_change, production_config_change, deployment]
---
# DHIS 2.33 Account Flows

## Purpose

Trace identity, token and email behavior through the actual legacy DHIS runtime.

## When to use this skill

Use for DHIS 2.33 account creation, email/username login, password recovery,
admin invitations, native security-page routing, and incorrect links in mail.

## When not to use this skill

Do not apply its version-specific API details to newer DHIS versions without
checking their source. Laboratory LIMS and Invenio NHRILS are separate projects.

## Quick Reference

- DHIS 2.33 recovery: POST `/api/account/recovery`, form field `username`.
- Reset: POST `/api/account/restore`, fields `username`, `token`, `password`.
- Invitation: POST `/api/users/invite`; acceptance uses `/api/account` with
  `inviteUsername` and `inviteToken`, not the recovery redemption endpoint.
- Verify the mail body and token redemption; SMTP acceptance alone is incomplete.

## Core concepts

DHIS owns credentials and tokens. Preserve its validation and expiration rules.
The 2.33 recovery controller passes the incoming request context to the mailer.
Its context helper uses the request server name and X-Forwarded-Proto plus
X-Forwarded-Port. X-Forwarded-Host alone does not fix the request server name;
`system.base_url` does not control this link. Keep an internal API address and
a configured public origin distinct. Set trusted Host and forwarding headers
from that configuration, never from caller-supplied headers.

## Standard workflow

1. Read project memory, the deployed version, proxy route, ingress, and exact
   version's DHIS controller/context/mail code. Map each request and URL owner.
2. Reproduce with synthetic accounts and captured mail. Inspect the full URL's
   scheme, hostname, port, path, username and token without logging the token.
3. Test the native form, password update and subsequent login. A generic 202
   can intentionally conceal unknown accounts and upstream failures.
4. Check unknown and shared email addresses, invalid credentials, expired token
   and reused token. Resolve email only when exactly one account matches.
5. Keep admin invitation distinct from self-registration. Check import status
   and created count as well as HTTP status; DHIS can report import failure in
   a successful HTTP response. Respect the 2.33 password maximum of 40 characters.
6. Deliver changes in their owning repositories with current user authorization,
   then verify the built image, GitOps revision, rollout and public endpoint.

## Safety rules

Use a local synthetic database and a mail sink for redemption/expiry tests.
Never print tokens, passwords or authorization headers. Do not alter production
user passwords for a smoke test. Skills do not expand the user's authorization.

## Required checks

Captured email has the expected public HTTPS origin; no internal service host
or port appears. The native form opens; the new password authenticates; the old
password, expired token and reused token are rejected. Client host/protocol
headers cannot poison the generated link. Check invitation acceptance separately.

## Pitfalls

Mock-only success misses rendered email defects. `dhis.conf` mail entries are
not the 2.33 system-settings mail configuration. Its email configuration check
requires nonempty SMTP username/password, including for a local sink. Its email
validator rejects `.invalid`; use reserved `example.org` addresses in the isolated
sink. Patch compilation must preserve
controller parameter names where this Spring version relies on them.

## Verification

For NIMR ILMS, run `scripts/ilms-devbench test` in the runtime/overlay project
and `npm test` in the eGA source's `server/` directory. For account UI changes
run `scripts/ilms-devbench browser-test` to check the proxy request and visible
confirmation on desktop/mobile. Report separately what
was verified locally, merged, deployed, SMTP-accepted and received in an inbox.

## Examples

An email containing `http://ilms:8080` despite a correct configured public URL
requires tracing the incoming recovery request host and forwarded scheme/port,
then capturing a new real email in the bench and redeeming its link.

## Output format

Return the request/link path, evidence for the cause, owning repository, focused
fix, executed checks, deployment state and any unverified delivery step.

## References

- https://github.com/dhis2/dhis2-core/blob/2.33.0/dhis-2/dhis-web/dhis-web-api/src/main/java/org/hisp/dhis/webapi/controller/AccountController.java
- https://github.com/dhis2/dhis2-core/blob/2.33.0/dhis-2/dhis-web/dhis-web-api/src/main/java/org/hisp/dhis/webapi/utils/ContextUtils.java
