---
name: power-platform-cli-admin
description: Use this skill for Microsoft Power Platform CLI administration, PAC authentication, service principal setup, Dataverse application users, environment role assignment, private Power Pages site access diagnostics, self-elevation, and troubleshooting Power Platform/Dataverse permission errors.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - web_fetch
  - shell
requires_approval_for:
  - tenant_admin_role_change
  - dataverse_role_change
  - application_user_creation
  - service_principal_registration
  - environment_creation_or_delete
  - production_import_or_publish
activation:
  keywords:
    - pac auth
    - pac admin
    - Power Platform CLI
    - Dataverse application user
    - service principal
    - self-elevate
    - prvCreateUser
    - Microsoft.BusinessAppPlatform
    - Power Platform admin
    - pac pages
    - Power Pages
    - site visibility
    - Grant site access
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
---
# Power Platform CLI Admin

## Purpose

Guide safe Microsoft Power Platform CLI administration for service principals, Dataverse application users, environment roles, and permission troubleshooting.

## When to use this skill

Use when planning, executing, reviewing, or troubleshooting:

- `pac auth create` with device code, client secret, workload identity, tenant, cloud, or environment options.
- `pac admin self-elevate`, `assign-user`, `application register`, `list`, or `create-service-principal`.
- Dataverse schema setup through PAC solution commands plus Dataverse Web API metadata calls.
- Dataverse application user creation and role assignment.
- Errors involving `prvCreateUser`, `systemuser`, `Microsoft.BusinessAppPlatform`, admin APIs, or service-principal access.
- Power Platform Build Tools or GitHub Actions service-principal setup.
- Private Power Pages site access diagnostics, including Site visibility grants, environment-variable backed private-site allow-lists, and Dataverse `aaduser` lookup checks.

## When not to use this skill

Do not use for canvas app UX, SharePoint/Microsoft Lists data modeling, or Power Fx form architecture unless the task involves PAC CLI administration. Use `power-platform-canvas-apps` for canvas app delivery.

## Quick Reference

- Treat Entra authentication, Power Platform tenant admin application registration, and Dataverse environment roles as separate permission layers.
- A successful `pac auth create` only proves sign-in worked; it does not prove the identity has Dataverse or admin API privileges.
- For a human admin missing Dataverse privileges, run `pac admin self-elevate --environment <env>` before creating users or assigning roles.
- For an existing app registration, use `pac admin application register --application-id <client-id>` to register it with Power Platform admin APIs.
- Add the app as a Dataverse application user with `pac admin assign-user --application-user`.
- PAC handles auth, solution lifecycle, solution export/import/check, and configuration data import/export; deterministic table/column/relationship creation should use Dataverse Web API metadata operations with `MSCRM.SolutionUniqueName`.
- PAC `pages` commands can list, download, upload, clone, and upload compiled code-site content for existing Power Pages sites. In PAC 2.8.1, `pac pages download-code-site` requires `--webSiteId`; `--siteName` is not accepted for that command.
- `pac pages clone` clones existing website content from a path; do not treat it as a blank Power Pages site creation command.
- First Power Pages site provisioning is normally done in Power Pages maker portal unless the installed, documented PAC CLI exposes a supported create command for that tenant/version.
- Private Power Pages site access is a separate gate from portal Contact/Web Role/Table Permission records. For development/non-production sites, first verify the user is granted Site visibility access, then test invitation redemption and `adx_externalidentity` creation.
- Power Pages stores private-site shared users in a Dataverse environment variable as Entra object IDs. Automation must resolve the organization user through an approved server-side path such as Dataverse `aaduser` or Microsoft Graph before appending the ID; do not append raw email addresses.
- Do not recreate a tenant until admin ownership, self-elevation, tenant app registration, and environment app-user assignment have all been checked.
- Do not print client secrets, access tokens, `.env` values, authorization headers, or tenant credentials.

## Core concepts

Power Platform CLI service-principal setup commonly spans four layers:

1. **Entra tenant role**: the human setup account needs direct Global Administrator, Power Platform Administrator, or Dynamics 365 Administrator privileges when performing tenant or environment administration.
2. **Dataverse environment role**: the human setup account needs a Dataverse role with privileges such as `prvCreateUser` on `systemuser`; `pac admin self-elevate` can grant System Administrator when the human has a qualifying tenant admin role.
3. **Power Platform admin application registration**: the Entra app must be registered with Power Platform for admin API access. The service principal cannot register itself.
4. **Dataverse application user**: the app must exist as an application user in the target environment and have an appropriate Dataverse security role.

## Standard workflow

1. Confirm the tenant, cloud, and environment URL are from the same tenant and target environment.
2. Authenticate as a human admin:

   ```bash
   pac auth create --deviceCode --tenant "$POWER_PLATFORM_TENANT_ID"
   ```

3. If user or role assignment fails with missing Dataverse privileges, self-elevate:

   ```bash
   pac admin self-elevate --environment "$POWER_PLATFORM_ENVIRONMENT_URL"
   ```

4. Register an existing Entra app with Power Platform admin APIs:

   ```bash
   pac admin application register --application-id "$POWER_PLATFORM_CLIENT_ID"
   ```

5. Add or update the Dataverse application user:

   ```bash
   pac admin assign-user \
     --environment "$POWER_PLATFORM_ENVIRONMENT_URL" \
     --user "$POWER_PLATFORM_CLIENT_ID" \
     --role "System Administrator" \
     --application-user
   ```

6. Test service-principal authentication:

   ```bash
   pac auth create \
     --name "$PAC_AUTH_NAME" \
     --applicationId "$POWER_PLATFORM_CLIENT_ID" \
     --clientSecret "$POWER_PLATFORM_CLIENT_SECRET" \
     --tenant "$POWER_PLATFORM_TENANT_ID" \
     --cloud "$POWER_PLATFORM_CLOUD" \
     --environment "$POWER_PLATFORM_ENVIRONMENT_URL"
   ```

7. Run the target operation, such as listing environments or exporting a solution, before wiring CI/CD.

## Dataverse schema setup workflow

Use this workflow when setting up custom Dataverse tables from reviewed schema artifacts:

1. Authenticate and verify the target environment:

   ```bash
   pac auth who
   pac solution list --environment "$POWER_PLATFORM_ENVIRONMENT_URL"
   ```

2. Initialize or select the unmanaged dev solution. PAC supports solution project lifecycle commands such as `pac solution init`, `list`, `export`, `import`, `check`, and `add-solution-component`.
3. Dry-run the schema plan from local artifacts. The plan must show tables, columns, relationships, choices, seed data, and whether any operation writes to Dataverse.
4. Create tables, columns, choices, and relationships through Dataverse Web API metadata endpoints, not ad hoc maker-portal clicks, when deterministic setup is required.
5. Include the `MSCRM.SolutionUniqueName` header on Web API metadata create requests so components are added to the intended unmanaged solution.
6. Publish customizations only after the schema plan and target environment are reviewed.
7. Use `pac data import` only for small configuration/seed data. Microsoft documents PAC data commands as configuration-data oriented and not suitable for large volumes.
8. Export the resulting unmanaged solution for review before any managed/test/prod deployment path.

## Power Pages readiness workflow

Use this workflow before deploying a Power Pages hosted SPA or configuring table permissions:

1. Confirm active auth and target environment:

   ```bash
   pac auth list
   pac env who
   pac admin list
   ```

2. List sites in the active environment:

   ```bash
   pac pages list
   ```

3. If no site appears but one was created in maker portal, check `pac admin list` for a `PowerPagesDeveloper-*` or trial environment and create a new auth profile against that environment URL.

4. Download the site source with the website ID:

   ```bash
   pac pages download-code-site \
     --environment "<environment-url>" \
     --webSiteId "<website-id>" \
     --path ./powerpages \
     --overwrite
   ```

5. Upload compiled code-site output only after explicit approval:

   ```bash
   pac pages upload-code-site \
     --rootPath "<source-root>" \
     --compiledPath "<compiled-output>" \
     --siteName "<site-name>"
   ```

6. Ensure Dataverse schema, seed data, Power Pages Web API site settings, and table permissions are configured in the same environment as the Power Pages site.
7. For private developer/non-production sites, verify Site visibility access for non-admin testers before diagnosing invitation, web-role, table-permission, or assignment failures.

## Private Power Pages site access workflow

Use this workflow when a non-admin tester receives "You don't have access" on a private site:

1. Confirm the site visibility banner/state in Power Pages Studio.
2. If the site is private, check whether the user appears in Security > Site visibility > People who can access the site.
3. Resolve the user's CRDB/Microsoft Entra identity. Prefer the organization UPN/mail that appears in Dataverse `aaduser`; do not rely only on the email typed in a TACATDP Contact.
4. If automating, have a server-side admin flow append the resolved Entra object ID to the Power Pages shared-users environment variable only after explicit approval.
5. Only then send/retry the Power Pages invitation and verify activation through Dataverse: invitation no longer `New`, `adx_externalidentity` exists, expected web role is present, and assignment is active.

## Troubleshooting

- **`missing prvCreateUser privilege` on `systemuser`**: the human account is connected but lacks Dataverse user-create privileges. Run `pac admin self-elevate --environment <env>` from a directly assigned Global Administrator, Power Platform Administrator, or Dynamics 365 Administrator account, then retry `assign-user`.
- **Service principal authenticated, then `does not have permission to access ... Microsoft.BusinessAppPlatform/scopes/admin/environments`**: the app can sign in but is not authorized for Power Platform admin APIs. Register it with `pac admin application register --application-id <client-id>` from a human admin context.
- **Application user exists but operations still fail**: verify the app user is active, in the intended environment/business unit, and has the required Dataverse security role.
- **Role changes made only in Entra do not fix Dataverse errors**: Entra admin roles and Dataverse security roles are different layers.
- **Enterprise applications do not appear when adding app users**: use the app registration application ID; Dataverse application users are based on Entra app registrations.

## Pitfalls

- Treating a successful `pac auth create` as proof that admin API and Dataverse privileges are configured.
- Assigning Entra roles but forgetting Dataverse self-elevation.
- Creating an app registration but not registering it with Power Platform admin APIs.
- Adding a Dataverse application user in the wrong environment or business unit.
- Retrying with stale PAC auth profiles after changing tenant or environment variables.
- Recreating tenants or environments before checking the separate permission layers.
- Running `pac pages list` against the default environment after Power Pages created a separate `PowerPagesDeveloper-*` environment.
- Assuming `pac pages download-code-site --siteName` works across PAC versions; check `pac pages download-code-site` usage and prefer `--webSiteId` when required.
- Deploying Dataverse schema to one environment while the Power Pages site is hosted in another environment.
- Diagnosing private-site "You don't have access" as a TACATDP assignment issue before checking Site visibility grants.
- Updating Power Pages private-site access from browser code. Treat it as privileged site configuration and keep it in maker/admin UI or an approved server-side onboarding processor.

## Safety rules

- Get explicit user approval before changing tenant admin roles, registering admin applications, creating application users, assigning Dataverse roles, creating/deleting environments, importing solutions, or publishing apps.
- Never expose secrets or token-bearing command output.
- Prefer least privilege for normal operations, but recognize that bootstrap commands often require temporary System Administrator or tenant-admin privileges.
- Keep tenant/environment identifiers explicit in commands; do not rely on stale default auth profiles for risky operations.
- Do not run production import, publish, delete, reset, copy, backup restore, or DLP changes unless the user explicitly approved the exact target.

## Required checks

- Is the signed-in human account in the intended tenant?
- Is the human admin role directly assigned, not only inherited through a group?
- Has the human account self-elevated into the target Dataverse environment when needed?
- Is the service principal registered with Power Platform admin APIs?
- Is the app added as an application user in the target Dataverse environment?
- Does the application user have the role required by the operation?
- For private Power Pages sites, is the tester explicitly granted Site visibility access or a System Administrator/site maker who already has access?
- If automating private-site access, can the process resolve email/UPN to a real Entra object ID without exposing secrets or relying on a stale account pattern?
- Are all secrets referenced only through environment variables or secure stores?

## Verification

- `pac admin list`
- `pac admin application list`
- `pac admin list-service-principal --max 100`
- `pac pages list`
- `pac env who`
- `pac auth create ...` using the service principal credentials
- Target operation smoke test, such as solution list/export or environment list, depending on the workflow
- `karakana skill validate skills/power-platform-cli-admin`
- `karakana eval run --skill power-platform-cli-admin`

## Output format

```markdown
## Power Platform CLI Admin Check

- Tenant/account:
- Environment:
- Human admin status:
- Dataverse self-elevation:
- Power Platform app registration:
- Application user status:
- Security role assignment:
- Commands to run:
- Verification:
- Remaining risks:
```

## Examples

- A user signs in successfully with `pac auth create --deviceCode`, but `assign-user --application-user` fails with `missing prvCreateUser`: self-elevate first, then retry the assignment.
- A service principal authenticates successfully, then fails on `Microsoft.BusinessAppPlatform/scopes/admin/environments`: register the Entra application with Power Platform admin APIs from a human admin context.
- A service principal is added to the environment but cannot export a solution: verify the app user is active and has a Dataverse role with the needed solution privileges.
