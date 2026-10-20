# ILMS Architecture

The public HTTPS origin routes Angular assets to the frontend, `/public/`
account endpoints to Express, and `/api/` plus DHIS security pages to DHIS.
DHIS owns credentials, recovery/invitation tokens, and mail generation.
Express resolves a unique email address to a DHIS username without selecting
among accounts sharing an email. Login resolution authenticates the password.

The internal DHIS API origin and public link origin have different purposes.
`DHIS2_BASE_URL` can use `http://ilms:8080/api/`; `PUBLIC_BASE_URL` is the
public HTTPS origin. In DHIS 2.33 the recovery controller constructs email
links from the request host plus forwarded protocol/port, independently of
`system.base_url`. Set trusted headers from the configured public origin.

The development bench runs the pinned production DHIS image, PostgreSQL 15,
Express, Angular, Mailpit and a TLS gateway on an internal Docker network.
Only the gateway and Mailpit UI are published, on loopback. Generated source
copies, certificates, reports and synthetic data remain local.
