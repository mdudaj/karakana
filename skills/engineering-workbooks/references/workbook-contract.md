# Local export and proposed-feedback workflow

Use [P02](../../../docs/skills/engineering-artifact-catalogue/P02.md) for exact
supported CLI/API/limits; use the maintained content contract and blank template.
Do not create another exporter, copy a proprietary spreadsheet skill or alter
native engine schemas. The optional workbooks extra installs openpyxl; validation
and binding proposals use base dependencies.

For an instantiated source inside a declared root, run:

```bash
python -m karakana.tools.engineering_artifacts --root . validate \
  --source source.md --namespace example
python -m karakana.tools.engineering_artifacts --root . export \
  --source source.md --namespace example --audience business \
  --baseline-revision reviewed-source-revision \
  --output review/business-v1.xlsx --snapshot review/business-v1.json
python -m karakana.tools.engineering_artifacts --root . feedback \
  --baseline review/business-v1.xlsx --snapshot review/business-v1.json \
  --returned review/business-v1-annotated.xlsx --output review/feedback-v1.json
```

Repeat --source or --returned as needed. All paths resolve inside --root; links
in Markdown resolve relative to that document. Validate known authority and resolved
native bindings. Use new filenames: existing/aliased outputs reject. Preserve the
original XLSX/JSON pair and every returned annotated file unchanged. Source hashes
and caller-supplied baseline revision do not prove a clean or approved Git tree.

Feedback is a three-way proposed report against original baseline, current source
and returned workbooks. Report stale/missing/invalid source, changed rows/fields,
comments/formulas, altered headers/identities and conflicts. Conflicts require
source review; there is no apply operation. Workbook agreement cannot update approvals.
Macros/external calculation links reject; formulas are never evaluated. Unsupported
formatting/chart edits stay in the preserved input and are not semantic feedback.

Native binding bootstrap/reconciliation uses P02 `bindings`; proposals do not mark
new/changed associations resolved. Exact source drift requires reviewed refresh.
Basis: original P02 implementation and PLAN S35–S37/L02; no borrowed skill text.
