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

On 2026-08-11, the latest dashboard layout refinement was deployed to Mshirika first for review:

- Environment: `PowerPagesDeveloper-070926-125720`
- Environment URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`
- PAC user: `john.mduda@mshirikacorp.onmicrosoft.com`
- Source branch/commit: `prototype-next-delivery` / `a8d0d16`
- Package marker: `tacatdp-dashboard-20260811-006`
- Entry assets: `/assets/index-CpeETUAV.mjs` and `/assets/index-hj0iKXuy.css`

The upload used the clean fresh Enhanced-model package overlay pattern, replacing only the two Home copy fragments and the new Home-referenced entry web files. Upload succeeded in `218.21 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-006`, and the downloaded `index-CpeETUAV.mjs` bundle passed `node --check`.

The Program Impact Goal background image refinement was then deployed to Mshirika:

- Source branch/commit: `prototype-next-delivery` / `ae28a31`
- Package marker: `tacatdp-dashboard-20260811-007`
- Entry assets: `/assets/index-D1aDNeLa.mjs` and `/assets/index-BnSf0Bae.css`
- Background asset: `/assets/program-impact-farmer-U4dPWmM1.png`

The upload used the same clean fresh Enhanced-model package overlay pattern, replacing the two Home copy fragments, the new entry JS/CSS web files, and the farmer PNG web file. Upload succeeded in `249.72 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-007`, the farmer PNG exists in deployed web files, and the downloaded `index-D1aDNeLa.mjs` bundle passed `node --check`.

The follow-up image-fit refinement was deployed to Mshirika after changing the Program Impact Goal artwork from a cropped background to a contained image:

- Source branch/commit: `prototype-next-delivery` / `74e1ed6`
- Package marker: `tacatdp-dashboard-20260811-008`
- Entry assets: `/assets/index-D77AjqZ4.mjs` and `/assets/index-CaiBw9Lr.css`
- Background asset: `/assets/program-impact-farmer-U4dPWmM1.png`

The upload used the same clean fresh Enhanced-model package overlay pattern, replacing the two Home copy fragments, the new entry JS/CSS web files, and the farmer PNG web file. Upload succeeded in `246.99 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-008`, the farmer PNG exists in deployed web files, and the downloaded `index-D77AjqZ4.mjs` bundle passed `node --check`.

The CRDB blank-page issue was then repaired by redeploying the same `008` package to CRDB using a fresh CRDB Enhanced-model download as the upload base:

- Environment: `TACATDP-CRDB-Dev`
- Environment URL: `https://org5eb0379b.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`
- PAC profile/user: `tacatdp-crdb` / `dmuroba@CRDBBANK.CO.TZ`
- Source branch/commit: `prototype-next-delivery` / `74e1ed6`
- Package marker: `tacatdp-dashboard-20260811-008`
- Entry assets: `/assets/index-D77AjqZ4.mjs` and `/assets/index-CaiBw9Lr.css`
- Background asset: `/assets/program-impact-farmer-U4dPWmM1.png`

Direct upload of the older local upload folder failed with the known PAC `Expected 'SequenceStart', got 'MappingStart'` package-format issue. Uploading a fresh CRDB export succeeded, confirming the fresh-download package was compatible. A new overlay package was then created from the fresh export, with only the current SPA web files and Home copy fragments overlaid. The CRDB fix upload succeeded in `249.23 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-008`, `index-D77AjqZ4.mjs` passes `node --check`, and all imported chunks exist in live CRDB web files, including `charts-BPLJPjyX.mjs`, `components-L5WOVj4e.mjs`, `core-BTH3Gimn.mjs`, `main-D33weQsb.mjs`, `vendor-datepicker-JwSW3Esp.mjs`, and `vue-datepicker-Ber1572m.mjs`. PAC reported managed `powerpagecomponent` delete warnings during upload; the CLI stated those stale-record delete failures did not stop the upload.

The Program Impact Goal farmer-image background refinement was then deployed to Mshirika for preview:

- Source branch/commit: `prototype-next-delivery` / `3efe80a`
- Package marker: `tacatdp-dashboard-20260811-009`
- Entry assets: `/assets/index-CYleeA6X.mjs` and `/assets/index-PQZUFUpJ.css`
- Background asset: `/assets/program-impact-farmer-U4dPWmM1.png`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the new SPA entry JS/CSS, the farmer PNG, and the two Home copy fragments. Upload succeeded in `211.34 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-009`, `index-CYleeA6X.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live Mshirika web files.

After Mshirika preview approval, the same Program Impact Goal farmer-image background refinement was deployed to CRDB:

- Source branch/commit: `prototype-next-delivery` / `3efe80a`
- Package marker: `tacatdp-dashboard-20260811-009`
- Entry assets: `/assets/index-CYleeA6X.mjs` and `/assets/index-PQZUFUpJ.css`
- Background asset: `/assets/program-impact-farmer-U4dPWmM1.png`
- PAC profile/user: `tacatdp-crdb` / `dmuroba@CRDBBANK.CO.TZ`

The CRDB upload used a fresh CRDB Enhanced-model download as the base and overlaid only the new SPA entry JS/CSS, the farmer PNG, and the two Home copy fragments. Upload succeeded in `246.26 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-009`, `index-CYleeA6X.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live CRDB web files. This verification explicitly checked the assets that previously caused the CRDB blank page.

The Disbursement Trend label-spacing refinement was deployed to Mshirika for preview:

- Source branch/commit: `prototype-next-delivery` / `ed9cd7d`
- Package marker: `tacatdp-dashboard-20260811-010`
- Entry assets: `/assets/index-CJWwOy6W.mjs` and `/assets/index-C9y6VjKL.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the new SPA entry JS/CSS, the farmer PNG, and the two Home copy fragments. Upload succeeded in `220.86 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-010`, `index-CJWwOy6W.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live Mshirika web files.

The compact-unit Disbursement Trend revision was then deployed to Mshirika:

- Source branch/commit: `prototype-next-delivery` / `c6155b4`
- Package marker: `tacatdp-dashboard-20260811-011`
- Entry assets: `/assets/index-mklvB7ql.mjs` and `/assets/index-C9y6VjKL.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the new SPA entry JS/CSS, the farmer PNG, and the two Home copy fragments. Upload succeeded in `240.73 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-011`, `index-mklvB7ql.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live Mshirika web files.

The Disbursement Trend edge-label clearance fix was then deployed to Mshirika:

- Source branch/commit: `prototype-next-delivery` / `d4271ce`
- Package marker: `tacatdp-dashboard-20260811-012`
- Entry assets: `/assets/index-DO1bCuTP.mjs` and `/assets/index-C9y6VjKL.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the new SPA entry JS/CSS, the farmer PNG, and the two Home copy fragments. Upload succeeded in `209.91 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-012`, `index-DO1bCuTP.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live Mshirika web files.

After Mshirika preview, the Disbursement Trend edge-label clearance fix was deployed to CRDB:

- Source branch/commit: `prototype-next-delivery` / `d4271ce`
- Package marker: `tacatdp-dashboard-20260811-012`
- Entry assets: `/assets/index-DO1bCuTP.mjs` and `/assets/index-C9y6VjKL.css`
- PAC profile/user: `tacatdp-crdb` / `dmuroba@CRDBBANK.CO.TZ`

The upload used a fresh CRDB Enhanced-model download as the base and overlaid only the new SPA entry JS/CSS, the farmer PNG, and the two Home copy fragments. Upload succeeded in `246.88 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-012`, `index-DO1bCuTP.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live CRDB web files. This verification explicitly checked the chunk set that previously caused the CRDB blank page.

The Material beneficiaries route prototype was deployed to Mshirika:

- Source branch/commit: `prototype-next-delivery` / `353238f` plus staging-script fix commit
- Package marker: `tacatdp-dashboard-20260811-013`
- Entry assets: `/assets/index-fYl4hH1T.mjs` and `/assets/index-B4t5D1m2.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`

The first upload attempt failed before changing the site because `stage-powerpages-spa-build.py` had deleted the fresh PAC download and replaced it with the repository `.powerpages-site` tree, reintroducing stale/older YAML records and causing PAC `2.9.3` to fail with `Expected 'SequenceStart', got 'MappingStart'` plus null-primary-key errors such as `adx_weblinksetid`. The script was corrected to require a fresh upload package and overlay only the two Home copy fragments plus current SPA web files and metadata. The corrected upload succeeded in `231.72 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-013`, `index-fYl4hH1T.mjs` passes `node --check`, the farmer PNG exists, and all imported chunks exist in live Mshirika web files.

The reusable Material card accent rail abstraction was deployed to Mshirika for visual review:

- Source branch/commits: `prototype-next-delivery` / source slice `6669008`, deployment artifact `1a287c0`
- Package marker: `tacatdp-dashboard-20260811-014`
- Entry assets: `/assets/index-ov02QyPH.mjs` and `/assets/index-DNgW64y7.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`
- Target environment: `PowerPagesDeveloper-070926-125720`
- Target URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the current SPA web files plus the two Home copy fragments. Upload succeeded in `216.03 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-014`, `index-ov02QyPH.mjs` passes `node --check`, and all 32 Vite `dist/assets` files exist in the downloaded Power Pages `web-files` package. `npm run test:material` and `npm run build:mshirika-runtime` passed before upload. The build still reports the known upstream `@getodk/web-forms` direct-`eval` and large-chunk warnings.

The metric-only accent rail correction was deployed to Mshirika:

- Source branch/commits: `prototype-next-delivery` / source slice `1feba3d`, deployment artifact `da74573`
- Package marker: `tacatdp-dashboard-20260811-015`
- Entry assets: `/assets/index-tYULaFNG.mjs` and `/assets/index-DAC01KWF.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`
- Target environment: `PowerPagesDeveloper-070926-125720`
- Target URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the current SPA web files plus the two Home copy fragments. Upload succeeded in `210.97 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-015`, `index-tYULaFNG.mjs` passes `node --check`, and all 32 Vite `dist/assets` files exist in the downloaded Power Pages `web-files` package. `npm run test:material` and `npm run build:mshirika-runtime` passed before upload. The build still reports the known upstream `@getodk/web-forms` direct-`eval` and large-chunk warnings.

The remaining decorative route-card rail cleanup was deployed to Mshirika:

- Source branch/commits: `prototype-next-delivery` / source slice `5c291e8`, deployment artifact `87c5669`
- Package marker: `tacatdp-dashboard-20260811-016`
- Entry assets: `/assets/index-CxlvaPDY.mjs` and `/assets/index-Cdswfmo9.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`
- Target environment: `PowerPagesDeveloper-070926-125720`
- Target URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The source slice removed decorative brand/accent left rails from route-level and content-card surfaces including route headers, project/form/data cards, user cards, drawers, pagination, connection panels, and command/detail panels. The metric-card rails remain, and semantic state rails remain for warning/error/success/focus states. `scripts/validate-route-card-accent-scope.mjs` was added to `npm run test:material` to enforce this distinction.

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the current SPA web files plus the two Home copy fragments. Upload succeeded in `214.77 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-016`, `index-CxlvaPDY.mjs` passes `node --check`, and all 32 Vite `dist/assets` files exist in the downloaded Power Pages `web-files` package. `npm run test:material` and `npm run build:mshirika-runtime` passed before upload. The build still reports the known upstream `@getodk/web-forms` direct-`eval` and large-chunk warnings.

The project-list rail exception correction was deployed to Mshirika:

- Source branch/commits: `prototype-next-delivery` / source slice `2e1f544`, deployment artifact `e0e56a7`
- Package marker: `tacatdp-dashboard-20260811-017`
- Entry assets: `/assets/index-DDzmzwy7.mjs` and `/assets/index-BmUeU1mv.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`
- Target environment: `PowerPagesDeveloper-070926-125720`
- Target URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The source slice restored the left shade for `.project-card` project-list cards only. Users route and project-detail metric strips continue to shade only the first metric card via `metric-card--accent`; form/data cards and other content surfaces remain plain. `scripts/validate-route-card-accent-scope.mjs` was updated to allow the project-list exception while continuing to block decorative rails on form/data cards and other route surfaces.

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the current SPA web files plus the two Home copy fragments. Upload succeeded in `229.83 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-017`, `index-DDzmzwy7.mjs` passes `node --check`, and all 32 Vite `dist/assets` files exist in the downloaded Power Pages `web-files` package. `npm run test:material` and `npm run build:mshirika-runtime` passed before upload. The build still reports the known upstream `@getodk/web-forms` direct-`eval` and large-chunk warnings.

The all-metric-card rail correction was deployed to Mshirika:

- Source branch/commits: `prototype-next-delivery` / source slice `6caee89`, deployment artifact `13cd405`
- Package marker: `tacatdp-dashboard-20260811-018`
- Entry assets: `/assets/index-CQZYRfsF.mjs` and `/assets/index-CS6nPAt1.css`
- PAC profile/user: `mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`
- Target environment: `PowerPagesDeveloper-070926-125720`
- Target URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The source slice corrected the previous interpretation error where only the first metric card in Users and Project Detail received the rail. The rail now belongs to the shared `.metric-card` primitive, so every metric card in Users, Project Detail, Reporting, System Activity, and Activation metric strips receives the metric rail. Non-metric content cards remain plain, and the temporary project-list card shade remains allowed.

The upload used a fresh Mshirika Enhanced-model download as the base and overlaid only the current SPA web files plus the two Home copy fragments. Upload succeeded in `235.68 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-018`, `index-CQZYRfsF.mjs` passes `node --check`, and all 32 Vite `dist/assets` files exist in the downloaded Power Pages `web-files` package. `npm run test:material` and `npm run build:mshirika-runtime` passed before upload. The build still reports the known upstream `@getodk/web-forms` direct-`eval` and large-chunk warnings.

The accepted all-metric-card rail correction was deployed to CRDB:

- Source branch/commits: `prototype-next-delivery` / source slice `6caee89`
- Package marker: `tacatdp-dashboard-20260811-018`
- Entry assets: `/assets/index-CQZYRfsF.mjs` and `/assets/index-CS6nPAt1.css`
- PAC profile/user: `tacatdp-crdb` / `dmuroba@CRDBBANK.CO.TZ`
- Target environment: `TACATDP-CRDB-Dev`
- Target URL: `https://org5eb0379b.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The upload used a fresh CRDB Enhanced-model download as the base and overlaid the accepted marker `018` SPA build plus the two Home copy fragments. Upload succeeded in `275.29 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-018`, and the downloaded `index-CQZYRfsF.mjs` bundle passed `node --check`. A stricter deployed-asset check verified all 32 Vite assets by Power Pages `adx_partialurl` and content hash rather than exported local filename, because PAC exports duplicate CRDB web-file records with local suffixes when multiple records share the same partial URL. The check found duplicate partial URLs for the three ODK locale chunks (`strings_es-C8xkQaZj-KYNBMnTd.mjs`, `strings_fr-C0vLmCzP-Bi34LuTN.mjs`, and `strings_id-BE0G3I_d-B0dO9nQF.mjs`), but at least one deployed web-file record for each expected browser URL has the exact current binary. PAC reported managed `powerpagecomponent` delete warnings during upload; the CLI stated those stale-record delete failures did not stop the upload.

The Beneficiaries page label cleanup was deployed to Mshirika:

- Source branch/commits: `prototype-next-delivery` / source slice `07c8eda`, deployment artifact `93cc501`
- Package marker: `tacatdp-dashboard-20260811-019`
- Entry assets: `/assets/index-Zg2kTrjA.mjs` and `/assets/index-CIPM5vqe.css`
- PAC profile/user: `tacatdp-mshirika` / `john.mduda@mshirikacorp.onmicrosoft.com`
- Target environment: `PowerPagesDeveloper-070926-125720`
- Target URL: `https://orga3cf4b37.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The source slice removed the visible `Material list surface` eyebrow from the Beneficiaries records surface. The upload used a fresh Mshirika Enhanced-model download as the base and overlaid marker `019` SPA assets plus the two Home copy fragments. Upload succeeded in `248.94 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-019`, `index-Zg2kTrjA.mjs` passes `node --check`, and all 32 Vite assets exist by Power Pages `adx_partialurl` and content hash with no duplicate partial URLs observed. `npm run test:material` and `npm run build:mshirika-runtime` passed before upload. The build still reports the known upstream `@getodk/web-forms` direct-`eval` and large-chunk warnings.

The Beneficiaries page label cleanup was deployed to CRDB:

- Source branch/commits: `prototype-next-delivery` / source slice `07c8eda`, deployment artifact `93cc501`
- Package marker: `tacatdp-dashboard-20260811-019`
- Entry assets: `/assets/index-Zg2kTrjA.mjs` and `/assets/index-CIPM5vqe.css`
- PAC profile/user: `tacatdp-crdb` / `dmuroba@CRDBBANK.CO.TZ`
- Target environment: `TACATDP-CRDB-Dev`
- Target URL: `https://org5eb0379b.crm4.dynamics.com/`
- Website: `TACATDP Monitoring Tool`
- Website ID: `fccc0cc6-7f5e-4885-aeb8-2272e68130a3`

The upload used a fresh CRDB Enhanced-model download as the base and overlaid marker `019` SPA assets plus the two Home copy fragments. Upload succeeded in `267.42 secs`. Post-upload PAC download confirmed both deployed Home fragments reference `tacatdp-dashboard-20260811-019`, `index-Zg2kTrjA.mjs` passes `node --check`, and all 32 Vite assets exist by Power Pages `adx_partialurl` and content hash. The stricter partial-URL/content-hash check again found duplicate CRDB records for the three ODK locale chunks (`strings_es-C8xkQaZj-KYNBMnTd.mjs`, `strings_fr-C0vLmCzP-Bi34LuTN.mjs`, and `strings_id-BE0G3I_d-B0dO9nQF.mjs`), with 8 records for each partial URL, but at least one deployed web-file record for each expected browser URL has the exact current binary. PAC reported managed `powerpagecomponent` delete warnings during upload; the CLI stated those stale-record delete failures did not stop the upload.

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
