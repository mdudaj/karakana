# TACATDP Deployment

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
