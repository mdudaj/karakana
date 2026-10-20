# ILMS Known Issues

## Internal address in recovery email

On 2026-10-16 an email contained `http://ilms:8080/.../restore.action`.
The proxy called DHIS using its internal service URL without public-origin
headers. `system.base_url` was correct but was not consulted by this DHIS
2.33 code path. A successful API response or SMTP log did not reveal it.
The correction is deployed through eGA MR !9 and pipeline #52191. The real-email
regression test passes in the isolated bench. Evidence is tracked in
`docs/ilms-development-bench-2026-10-16.md`; do not reopen the original cause
without checking current code, image pins and request headers.

## Legacy runtime and identity data

DHIS 2.33 and Java 8 require version-specific endpoint and password behavior;
do not assume current DHIS APIs apply. Existing accounts can share an email,
so email-only lookup must require exactly one match. Username recovery remains
available for those accounts.

The legacy native page uses the wording "Restore account". This terminology
does not mean the account has been deleted. Any terminology change requires
separate UX scope and verification.
