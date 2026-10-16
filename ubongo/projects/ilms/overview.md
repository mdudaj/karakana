# ILMS Overview

ILMS is NIMR's eGA-developed integrated library system at
`https://ilms.apps.nimr.or.tz`. It uses an Angular frontend, an Express
registration/account proxy, and DHIS 2.33 on Java 8/Tomcat with PostgreSQL.
It is distinct from the Django laboratory LIMS and Invenio NHRILS projects.

## Repository map

- Workspace project root: `../apps/nimr-ilms`, remote `nimr-tz/nimr-ilms`.
  Owns runtime image, NIMR overlay, development bench, and project instructions.
- eGA source: `../apps/ega-ilmis`, remote
  `https://external.ega.go.tz/fredrick.abisai/nimr-ilmis.git`, project 1017,
  protected deployment branch `nimr`. Owns Angular and `server/` Express code.
- GitOps: `../platform-gitops`, remote `nimr-tz/platform-gitops`,
  path `clusters/msmt-02/research/ilms/manifests`.
- Harness: workspace `nimr`, skillpack `ilms`, memory `ubongo/projects/ilms`.

## Inspect first

Read the project root's `AGENTS.md`, `KARAKANA.md`, `dev/bench/README.md`,
and `automation/ega/README.md`. For account work inspect the eGA checkout's
`server/src/config.ts`, `dhis2Client.ts`, `routes/account.ts`,
`server/test/account-flow.test.js`, and Angular account components.

Use `karakana handoff load --project ilms --skillpack ilms` at task entry.
Skillpacks provide context; executable tests establish actual behavior.
