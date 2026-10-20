# ILMS Deployment

Production namespace is `ilms`; Argo application is `msmt-02-ilms`.
Read current live image pins and Argo revisions before reporting deployment
state. Memory records are historical evidence, not current cluster status.

On 2026-10-16 eGA MR !9, pipeline #52191 and GitOps commit `247972af` delivered
the public-origin fix as `ega-16cbb003-nimr13`. Both deployments were observed
healthy. The runtime is now `dhis2-2.33.0-31`; its filesystem layers match the
previous tested `-30` artifact. The bench pins the runtime by digest.

eGA project 1017 has GitLab CI on protected `nimr` commits. It downloads an
immutable NIMR overlay, tests the proxy, compiles Angular in a Node job,
packages/pushes both images to GHCR, then updates both GitOps image pins.
Argo syncs the GitOps commit. The eGA `shared-runner` Docker runner blocks
rootless BuildKit user namespaces; Angular/esbuild also crashed inside Kaniko,
so Angular builds outside image packaging. Inspect current CI before changing
this approach. The old GitHub poll is manual-only to avoid competing promotion.

Application mail uses eGA SMTP from the NIMR network. GitLab pipeline-status
mail uses the GitLab integration; GitHub workflow mail uses Gmail. Do not
copy mail credentials between those execution environments without testing.

## Local bench

From `../apps/nimr-ilms`:

```bash
scripts/ilms-devbench prepare --source ../ega-ilmis
scripts/ilms-devbench up
scripts/ilms-devbench test
scripts/ilms-devbench browser-test
scripts/ilms-devbench status
scripts/ilms-devbench down
```

The app is `https://localhost:18443`, captured mail is
`http://127.0.0.1:18025`, and the test report is under ignored `.devbench/`.
The bench uses synthetic metadata and a fresh local database. SMTP settings
are seeded through DHIS system settings, not `mail.*` in `dhis.conf`.
