# Controlled synthetic documentation pilot

These are instantiated scenario copies, not the global blank template or a real
project release pack. Read [brief.md](brief.md), then [requirements.md](requirements.md),
[design.md](design.md), [plan.md](plan.md) and [release.md](release.md).
They use namespace `pilot-checklist` and keep draft/proposed/unconfirmed facts.
The fictional reader is not implemented. Product tests remain Not run/Blocked;
Release Notes deliberately has no delivered rows. No operational authority exists.

The documents exercise the four authoring skills; exports and returned-input review
exercise engineering-workbooks. This is guided author self-review with observable
tool/office outcomes, not an independent reviewer, live model benchmark, stakeholder
agreement or stable promotion. [P05](../P05.md) records acceptance and continuation.

## Sources and retained revisions

Markdown owns documentation. [catalogue.schema.json](catalogue.schema.json) owns
the candidate machine syntax; [catalogue.json](catalogue.json) illustrates input.
The complete export baseline includes the four documents, brief and both machine
files: seven hashes with explicit authority/revision. No native engine field is
overwritten, and no schema is replaced by a workbook summary.

Version 0.1 documents/exports are the immutable review baseline.
[requirements-v0.2.md](requirements-v0.2.md) is a separately retained reviewed
amendment: AC-01 and TC-01 clarify exact whitespace handling already present in the
brief. IDs persist; Change History explains the reason and author self-review.
This is the current source for the revised business view only. Do not combine both
requirement revisions in one export. Neither revision has stakeholder acceptance;
the revised content does not inherit approval. Workbook comments are proposed input.

## Audience sharing baseline

Retain the existing profile/contract version 0.1 for this bounded pilot. The table
records author-assessed suitability for review, not domain audience sign-off.

| Audience | Workbook | Sheets / rows | Useful review task |
| --- | --- | --- | --- |
| Business | [business v0.1](exports/business-v0.1.xlsx) | 15 / 66 | Inspect need, story/criteria, outcome and adoption gaps |
| Engineering | [engineering v0.1](exports/engineering-v0.1.xlsx) | 20 / 103 | Read ADR alternatives/consequences, views/contracts and bounded tasks |
| QA | [QA v0.1](exports/qa-v0.1.xlsx) | 14 / 65 | Connect criteria to defined cases and unobserved runs |
| Operations | [operations v0.1](exports/operations-v0.1.xlsx) | 12 / 58 | Inspect planned trial/recovery, support and release blockers |
| Executive | [executive v0.1](exports/executive-v0.1.xlsx) | 11 / 55 | Inspect forecast outcomes, dependencies and unavailable release evidence |
| Business amendment | [business v0.2](exports/business-v0.2.xlsx) | 15 / 66 | Review clarified criterion while retaining the original baseline |

Each XLSX has a matching same-name JSON immutable feedback baseline. Include this
whole pilot folder when sharing so relative full-source hyperlinks resolve. Start
with Read Me, Control and Readiness and Blockers; source status is not approval.
Control declares omitted detailed tables/narrative. The generated Source Manifest
is always present; an omission labelled Source Manifest means the authored registry
detail was projected into that generated manifest, not that hashes were omitted.
Engineering retains full narrative; other views link complete Markdown. The business
0.2 view omits Change History detail and links its complete source containing history.

These files are deliberately transparent review views, not concise presentation
slides. Inspect XLSX interactively and follow source links for full context. Wide
tables span horizontal print pages; the executive PDF exercise produced 21 A3 pages.
Feedback columns can appear on separate pages and long cells/narrative may require
opening the cell/source. A printed excerpt must not be described as the complete pack.
Native Excel desktop, Accessibility Checker, assistive and recipient usability
checks remain unperformed. LibreOffice transport is separate evidence.

## Reproduce and review

From the repository root, validate the original pack:

```bash
.venv/bin/python -m karakana.tools.engineering_artifacts \
  --root docs/skills/engineering-artifact-catalogue/pilots validate \
  --namespace pilot-checklist --source requirements.md --source design.md \
  --source plan.md --source release.md
.venv/bin/python -m pytest -q tests/test_engineering_artifact_pilots.py
```

For a new export, create a new output directory and use the P02 `export` recipe
with these four sources, an explicit audience and a caller-supplied baseline label.
Use new filenames; never replace an annotated workbook or either retained baseline.
For the amended view substitute requirements-v0.2.md only. A baseline label is not
proof of an approved or clean Git revision.

Reviewers may add Feedback values/comments or proposed value changes in a copy.
Retain headers and qualified identity columns. Preserve all returned files, compare
using the P02 `feedback` recipe against the exact original XLSX/JSON and current
canonical files, then inspect every stale/conflict/unknown-content finding. There
is no apply operation. Review any accepted amendment in Markdown, preserve history
and export a new pair. An agreement cell cannot supply source or release approval.

Actual office/feedback observations and author-quality rubric are in [QA.md](QA.md).
