# Sustainable Finance MEL Platform Deployment

Sustainable Finance MEL Platform is the current product identity. TACATDP remains valid where it refers to the original programme, deployed Power Pages site labels, existing managed-solution artifacts, table/list names, or source form terminology.

## Current Deployment Path

The active delivery path is Power Pages plus Dataverse, packaged as a Power Platform solution with environment-specific configuration. The older Canvas/Microsoft Lists path remains historical fallback context only.

1. Import the latest governed TACATDP managed solution into the target Dataverse environment.
2. Import or verify seed/configuration data for projects, forms, form versions, assignments, web roles, table permissions, Web API site settings, and onboarding configuration.
3. Verify the Power Pages site points to the same Dataverse environment as the solution.
4. For developer or non-production sites that remain private, grant every non-admin tester access under Power Pages Studio > Security > Site visibility before sending/retrying invitations.
5. Send or manually share the Power Pages invitation link/code only after private-site access is confirmed.
6. Verify activation in Dataverse: the invitation is no longer `New`, the Contact has an `adx_externalidentity`, the expected web role is available in the portal session, and the TACATDP assignment is active.
7. Purge Power Pages cache/restart the site after site settings, table permissions, web role associations, or Web API settings change.
8. Test the authenticated portal flows: dashboard, project visibility, collect, submit/edit, data tab, exports/Power BI surfaces, user management, and onboarding diagnostics.

## PAC 2.9.3 Power Pages package format

On 2026-08-09, Mshirika upload with PAC `2.9.3+ga17df1d` succeeded only after using a fresh PAC download as the upload base. The repository package had older per-entity YAML files that PAC rejected with `Expected 'SequenceStart', got 'MappingStart'`, and `website.yml` needed PAC-required `adx_websiteid` and `adx_name` keys.

For Power Pages uploads with this PAC version:

1. Confirm the Mshirika profile is active: `john.mduda@mshirikacorp.onmicrosoft.com` against `https://orga3cf4b37.crm4.dynamics.com/`.
2. Download a fresh package from the target website.
3. Overlay only the built SPA assets and the existing fresh-package Home copy files. Do not copy the whole repository `web-pages/home` folder into a fresh package, because repository and fresh-download content-page folder conventions can differ and can introduce duplicate or primary-key-missing webpage records.
4. Upload the fresh-format package with `pac pages upload --modelVersion Enhanced --forceUploadAll`.
5. Download again and verify both Home fragments reference the expected cache marker.

## Latest Mshirika deployment

On 2026-08-10, the TACATDP ECharts dashboard prototype was deployed to Mshirika and then revised/deployed again after dashboard layout feedback:

- Environment: `PowerPagesDeveloper-070926-125720`
- Environment URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`
- PAC user: `john.mduda@mshirikacorp.onmicrosoft.com`
- Source branch/commit: `prototype-next-delivery` / `cb11d48`
- Package marker: `tacatdp-dashboard-20260810-002`
- Entry assets: `/assets/index-D18L6wsc.mjs` and `/assets/index-BFYDxzL8.css`

Deployment used the fresh PAC download and overlay workaround. The latest revision upload succeeded in `212.88 secs`. Post-upload PAC download confirmed both Home fragments reference the dashboard marker, and the downloaded entry bundle passed `node --check`.

The latest revision moved dashboard header text to the shell header, restored the CRDB logo in the sidenav brand, compacted/scroll-enabled the sidenav, moved status/copyright text to the shell footer, and rebuilt the final-row dashboard cards with code-native SVG icons/illustration.

On 2026-08-11, the Loan Portfolio by Type legend fix was committed and deployed to Mshirika:

- Source branch/commit: `prototype-next-delivery` / `417d613`
- Package marker: `tacatdp-dashboard-20260811-002`
- Entry assets: `/assets/index-_YAHDKxX.mjs` and `/assets/index-B7MyrjMt.css`
- PAC user: `john.mduda@mshirikacorp.onmicrosoft.com`

The first upload attempts failed before deployment: direct upload hit the older YAML `Expected 'SequenceStart', got 'MappingStart'` package-format issue, and a broad Home-folder overlay on a fresh package introduced duplicate/missing-primary-key webpage records. The successful upload used a clean fresh Enhanced-model download, replaced only:

- `web-pages/home/Home.webpage.copy.html`
- `web-pages/home/content-pages/Home.en-US.webpage.copy.html`
- the five Home-referenced web files and their `.webfile.yml` files

The corrected upload succeeded in `206.22 secs`. Post-upload PAC download confirmed the deployed Home fragments reference `tacatdp-dashboard-20260811-002`, and the downloaded `index-_YAHDKxX.mjs` bundle passed `node --check`.

On 2026-08-11, CRDB device-code authentication was recreated successfully with the delegated Denis Muroba profile:

- PAC profile: `tacatdp-crdb`
- PAC user: `dmuroba@CRDBBANK.CO.TZ`
- Environment: `TACATDP-CRDB-Dev`
- Environment URL: `https://org5eb0379b.crm4.dynamics.com/`
- Environment ID: `42a3b1e6-8eea-e74a-ae11-3edc41e62d57`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The dashboard chart spacing revision was then deployed directly to CRDB:

- Source branch/commit: `prototype-next-delivery` / `d3d4f21`
- Package marker: `tacatdp-dashboard-20260811-004`
- Entry assets: `/assets/index-BKbav0i7.mjs` and `/assets/index-onZrj1qI.css`

The CRDB upload used the same clean fresh Enhanced-model package overlay pattern and succeeded in `236.56 secs`. Post-upload PAC download confirmed the deployed Home fragments reference `tacatdp-dashboard-20260811-004`, and the downloaded `index-BKbav0i7.mjs` bundle passed `node --check`.

The Mshirika-reviewed dashboard legend layout refinement was then deployed to CRDB:

- Source branch/commit: `prototype-next-delivery` / `576805f`
- Package marker: `tacatdp-dashboard-20260811-005`
- Entry assets: `/assets/index-BslHF5sX.mjs` and `/assets/index-Ch-JYMmt.css`

The CRDB upload used the same clean fresh Enhanced-model package overlay pattern and succeeded in `213.90 secs`. Post-upload PAC download confirmed the deployed Home fragments reference `tacatdp-dashboard-20260811-005`, and the downloaded `index-BslHF5sX.mjs` bundle passed `node --check`.

## Important Constraints

- There is no simple Git-only path that creates the complete Canvas App and all Microsoft Lists from repository artifacts.
- Placeholder data sources must remain clearly named and documented; do not treat them as production SharePoint connections.
- Do not publish/import apps into production without explicit approval.
- Do not run scripts that write to live SharePoint/Microsoft Lists without explicit approval and a target site URL.
- Do not store tenant credentials, tokens, connection strings, or `.env` content in artifacts.
- Do not treat private-site access as the same thing as TACATDP authorization. Private-site access is a Microsoft Power Pages visibility gate; TACATDP authorization is enforced later through Contact, Web Role, Table Permission, and assignment records.
- Do not automate private-site grants from browser JavaScript. If automation is approved, use a server-side onboarding processor that resolves a CRDB/Microsoft Entra user to an object ID and updates the Power Pages shared-users configuration.

## User Guide Requirements

Future administrator/user guides must include a clear onboarding checklist:

1. Confirm whether the site is private or public.
2. If private, grant the user site access in Power Pages Site visibility or through the approved server-side onboarding processor.
3. Create/reuse the Power Pages Contact.
4. Create or resend the invitation.
5. Share the manual link/code if mailbox delivery is not configured.
6. Ask the user to redeem with the CRDB Microsoft account.
7. Confirm activation diagnostics show external identity, web role, and assignment readiness before marking the user active.

## Verification

- Placeholder-to-real data-source mapping exists and names the intended Microsoft Lists replacements.
- Microsoft Lists import templates open and create the expected columns.
- Power Apps data sources connect to the intended SharePoint site and lists.
- Delegation warnings are reviewed for reference filters.
- Required, skip, constraint, repeat, and multi-select behavior is tested manually.
- Screen layout is reviewed for one-field-per-row, spacing, labels, helper/error text, focus order, and accessible touch targets.
- Private-site test users appear in Power Pages Site visibility > People who can access the site before invitation redemption testing.
- Activation diagnostics confirm invitation redemption, external identity creation, web-role availability, and active assignment.
