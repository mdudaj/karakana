# Enterprise MEAL Known Issues

## Bootstrap-only shell

The current shell renders placeholder module pages. Domain models, workflow processes, imports, Microsoft sign-in, and dashboards are not implemented yet.

## Local auth only

The first slice intentionally uses Django local authentication. Microsoft Entra OIDC mapping is a planned slice after CRDB confirms app registration and group/role mapping.

## Form runtime compatibility constraints

The repository now has a browser-based XLSForm/XForm runtime path: uploaded or seeded XLSForms are compiled with pyxform, published as `FormVersion` records, assigned through `FormAssignment`, rendered in the browser, and submitted into canonical `FormSubmission` evidence.

Known constraints:

- External CSV itemsets such as `jr://file-csv/wards.csv` and `jr://file-csv/villages.csv` must be stored with the published `FormVersion.itemsets`; a compiled XForm alone is not enough for runtime rendering.
- Assigned form runtime resource endpoints must be accessible to the assigned collector, not only data-collection managers. Management screens remain role-gated separately.
- The TACATDP workbook expression `substr(once(uuid()),1,8)` caused ODK Web Forms initialization to fail with a generic “Unknown error” dialog. Enterprise MEAL rewrites that exact expression to `uuid(8)` during XLSForm publish/seed as an auditable browser-runtime compatibility transform.
- Do not broadly strip calculations. Any future XForm compatibility rewrite must be narrow, documented in publish warnings/notes, and covered by browser or service-level regression tests.
