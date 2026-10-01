---
status: evidence_blocked
question: "What navigation and accessibility evidence can be obtained for the frozen executive workbook in the available office application, and which target-application checks remain open?"
evidence:
  - source: "exports/executive-v0.1.xlsx, exports/executive-v0.1.json, and executive-reader-baseline.md"
    finding: "The immutable pair and all seven source hashes match the frozen receipt; the workbook was inspected without saving it."
  - source: "LibreOffice Calc 26.2.5.2 620(Build:2), isolated headless UNO load and A3 PDF render, 2026-10-01"
    finding: "Calc loaded 11 sheets in expected order and rendered 21 A3 pages. Readiness page 5 was visually inspected; pages 5–6 retained text blockers, source filenames and planned release state."
  - source: "openpyxl inspection of exports/executive-v0.1.xlsx, 2026-10-01"
    finding: "All sheets have unique names, one named table with a header row, D5 freeze panes, wrapped populated body cells and no merged or hidden rows/columns; 40 file links resolve beside the workbook and 11 internal links target Read Me."
  - source: "Microsoft Excel accessibility guidance and LibreOffice accessibility/Calc documentation, checked 2026-10-01"
    finding: "These sources identify structured tables, descriptive names, keyboard and assistive review as relevant checks; documentation of a capability does not establish that this workbook passed it."
requirements:
  - decision: "Keep the executive pilot's application evidence separate from structural inspection, rendered-page review, native Excel checks and independent reader acceptance."
    acceptance: "Record exact application/version, frozen hashes, checks performed, observed results, unperformed checks and refresh triggers without an accessibility or audience-usefulness pass claim."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
design:
  - choice: "Inspect the pinned XLSX read-only through an isolated LibreOffice process, audit its file structure, render a disposable PDF, and preserve the original pair."
    rationale: "This yields reproducible local evidence without changing the pilot baseline or disturbing the user's desktop; Excel and assistive behavior need a later test environment."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
artifact_choices:
  - kind: requirements
    disposition: reused
    path: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
    rationale: "The approved bounded pilot already defines the navigation and application-observation criteria."
  - kind: design
    disposition: reused
    path: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
    rationale: "The staged baseline-first method applies without a workbook, exporter or architecture change."
  - kind: test
    disposition: updated
    path: "docs/skills/engineering-artifact-catalogue/pilots/executive-reader-accessibility.md"
    rationale: "This receipt records direct tool observations and exact coverage limits."
  - kind: schema
    disposition: not_applicable
    rationale: "No profile, contract or source schema was changed."
authority:
  state: approved
  evidence: "The user directed execution of the next B2 local review task on 2026-10-01; this does not authorize reader outreach, live model calls or a remote write."
pending_decisions:
  - owner: "Karakana maintainer and an operator with the intended Excel/assistive environment"
    question: "Can the exact frozen workbook be checked with native Excel Accessibility Checker, keyboard traversal, source-link activation and a screen reader in the intended desktop/version?"
    next_action: "Open a verified copy with the seven linked sources in the intended desktop; record application/build, checker findings, keyboard path, spoken labels/order, link results and screenshots or private notes."
next_action: "Complete native Excel and assistive navigation evidence for this pinned baseline in the intended desktop; retain the separate coordinator gate before independent-reader sessions."
---

# Executive workbook navigation and accessibility observation

**Observed 2026-10-01. Outcome: partial local evidence; native Excel and assistive checks remain open.** This B2 receipt extends the [frozen baseline receipt](executive-reader-baseline.md) and [pilot method](../../../research/2026-10-01-engineering-workbooks-audience-pilot.md). The input is `exports/executive-v0.1.xlsx`, SHA-256 `6f58fdfb31ce6dd8222518095e3cd27f1786fdb403190fba111b1105e808327c`, paired with JSON SHA-256 `766bff7af53196c04e85ee753d4ba9905f8d3243128ff6f2ac73a2a808f9ae83`. All seven source hashes were recalculated and matched the baseline receipt. No source, XLSX or JSON was modified.

## Method and observed results

The application was **LibreOffice Calc 26.2.5.2 620(Build:2)** on Linux. An isolated headless LibreOffice profile opened the tracked XLSX read-only through UNO. A separate isolated profile rendered the workbook to a disposable PDF. `openpyxl 3.1.5` inspected OOXML structure and link targets; this is file inspection, not a GUI interaction. The disposable PDF and inspection scripts were kept outside the repository.

| Check | Observation | Boundary |
| --- | --- | --- |
| Application load and sequence | Calc loaded 11 sheets in order: Read Me, Control, Source Manifest, Readiness and Blockers, Artifact Register, Sources, Links, Roadmap, Milestones, Risks and Decisions, Release Plan. First-sheet cell text and table headers were readable through UNO. | Headless load proves import and text availability through UNO, not keyboard or screen-reader use. |
| Names and tables | All 11 names are unique and descriptive. Each sheet has one named Excel table starting at row 4, with `headerRowCount=1`; no merged cells or hidden rows/columns were found. | OOXML inspection; Calc's table/filter controls were not exercised interactively. |
| Frozen identity and wrapping | Every sheet records `D5` freeze panes. All 534 populated body cells have wrap enabled and explicit body row heights of at least 34 points. | OOXML layout settings; interactive scroll behavior and every row's on-screen legibility remain untested. |
| Provenance and omissions | Control states profile/contract `0.1`, `pilot-0.1-unaccepted`, structural validation only and the detailed sections omitted from this executive view. Source Manifest remains present. | Text inspected in file; no independent reader interpreted it. |
| Status as text | Readiness and Blockers retains `Not run`, `Blocked`, `draft`, `open`, `planned` and `unconfirmed` in cell text. Page 5 visibly shows test and risk blockers beside source filenames; page 6 text extraction includes the planned release and unconfirmed support/recovery. | This checks text visibility in the rendered view, not color contrast or spoken status. |
| Links | The XLSX contains 40 relative file links whose targets exist in the adjacent seven-source folder, plus 11 internal `Return to Read Me` links. | Target existence was checked; clickable behavior, keyboard activation and destination focus were not tested. |
| Print rendering | Calc produced 21 A3 pages. Page 5 was visually inspected and showed headers, row text and source labels without obvious clipping; pages 5–6 text extraction retained the readiness/release language. | A dense 21-page printout is not a concise presentation and is not an accessible PDF certification; only page 5 received visual review in this B2 run. |

The original workbook's existing labels and table structure broadly match [Microsoft's Excel accessibility guidance](https://support.microsoft.com/en-us/accessibility/excel/accessibility-best-practices-with-excel-spreadsheets). [LibreOffice's accessibility guide](https://help.libreoffice.org/latest/en-US/text/shared/guide/accessibility.html) and [Calc keyboard guide](https://help.libreoffice.org/latest/en-US/text/scalc/04/01020000.html) describe application capabilities. Neither source establishes this workbook's accessibility in the intended reader workflow.

## Unperformed checks and implications

- **Native Microsoft Excel desktop and its Accessibility Checker:** Excel was unavailable in this environment. No checker result, Excel import/round-trip finding or version-specific compatibility claim exists.
- **Interactive keyboard navigation:** the isolated headless Calc load has no focusable UI. Sheet switching, table movement, frozen-column behavior while scrolling, link activation and return focus were not exercised.
- **Screen reader and spoken order:** Orca is installed, but no isolated interactive desktop or recorded Orca session was used. Header announcement, status meaning, source-link labels and reading order remain untested. No WCAG conformance claim is made.
- **All-page visual and contrast audit:** one readiness page was visually inspected; the other 20 pages and on-screen zoom/contrast states were not reviewed in this B2 run.
- **Independent intended-reader understanding:** no reader session or audience acceptance has occurred. The separate coordinator/recruitment gate in the pilot method still applies.

For the next environment check, use a verified copy of this exact pair with only the seven source files and the neutral handout in the [facilitator receipt](executive-reader-baseline.md). Record Excel build/OS, Accessibility Checker output, a keyboard-only path from Read Me to a blocker and its source and back, and a screen-reader path that announces sheet/table headers, status text and link destination. Capture failures and unperformed steps. Do not edit or resave the frozen baseline. Review the affected findings if the seven sources, profile/contract/exporter, workbook guidance or office application version changes.

## Verification summary

The frozen pair and seven source hashes matched the baseline receipt. LibreOffice UNO read-only load succeeded for all 11 sheets; the isolated PDF conversion produced 21 A3 pages; page 5 was visually inspected and pages 5–6 were text-extracted. The OOXML audit found 11 named tables, 11 `D5` freeze panes, 51 links with 40 existing file targets, no merged/hidden rows or columns and wrapped populated body cells. These checks support only the observations above. Native Excel, keyboard, assistive and recipient results are pending; no exporter or workbook behavior changed.
