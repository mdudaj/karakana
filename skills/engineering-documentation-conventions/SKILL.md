---
name: engineering-documentation-conventions
description: Select and tailor engineering documentation resources and apply shared language, reference and source-authority conventions during requested document authoring or review.
version: 0.1.0
risk_level: medium
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
    - engineering documentation
    - documentation conventions
    - requirements template
    - system design template
  required_files: []
  optional_tools:
    - python
    - pytest
allowed_tools:
  - read_file
  - grep
  - code_search
  - python
  - run_tests
requires_approval_for:
  - source_approval_change
  - remote_publish
---
# engineering-documentation-conventions

## Purpose

Choose the right content resources and keep engineering documents relevant to
their readers while preserving project sources and evidence.

## When to use this skill

Use for requested engineering document authoring/review or document-template
selection. Combine it with the owning documentation skill in the
[document map](references/document-map.md); read only the resources needed for
the selected type.

## When not to use this skill

Use domain skills for unresolved product design or implementation. Use the
appropriate document-format skill for Word, PDF or spreadsheet rendering. An
ordinary chat answer does not need an engineering document pack.

## Quick Reference

Preserve the request type: an inquiry returns information, a review returns
findings, a plan returns proposed work. Draft/revise only when requested or
already authorised. Accepted review decisions carry forward; record later
revisions and their impact rather than silently replacing them.

Before drafting identify document type, audience, purpose, scope, authoritative
sources, applicable product/release and output format. Follow explicit task
instructions and project conventions, then tailor the mapped resources.

## Core concepts

- A clean template supplies a content outline; its separate guide explains use.
  A worked example illustrates completed content and is not a project baseline.
- Content conventions and visual presentation are separate. Select sections for
  actual reader needs; small changes can reference existing governing views.
- Markdown can own documentation; native engine fields, schemas and diagram
  sources retain their declared authority. Avoid competing editable masters.
- Source links and optional catalogue entries are discovery aids. The current
  loader does not recursively read them or automatically enforce these rules.

## Standard workflow

1. Inspect the current source and agreed intent; identify the requested type in
   the [document map](references/document-map.md). Use the owning skill and read
   its relevant guide before copying a template.
2. Keep necessary context, technical content and verification references. Add
   conditional sections when applicable and omit empty, irrelevant sections.
   Retain the reason for any material omission in the working record.
3. Write direct, neutral statements with consistent domain terms. Describe
   observable product behavior and scoped measures. Keep unknown thresholds,
   dependencies and assumptions explicit; do not invent dates or agreement.
4. Include title, revision, actual date and product/release applicability where
   relevant. Add a short Standards and references section identifying exact
   editions and how they are used. Distinguish mandatory project obligations
   from guidance; use tailored/informed-by wording where supported.
5. Keep template instructions, meeting arrangements and document-review logistics
   in authoring/review records. Product approval workflows, audit requirements
   and operating authority remain valid technical content. Avoid automatic
   “Draft for review” labels and repeated approval disclaimers in issued content.
6. Check source links, coverage, internal consistency and unresolved facts.
   Separate acceptance criteria, planned tests and actual test results. Keep
   proposed decisions distinct from accepted ones and forecasts from observations.
7. Use the existing project lifecycle and the
   [source/export contract](../../docs/engineering-artifacts.md). New narrative
   assets are not supported P02 structured-export inputs. Preserve existing
   exact-table sources and exports; an explicit adapter/projection is later work.

## Safety rules

Document work grants no new permission for live model calls, publication,
deployment, source approval changes or automatic workbook-feedback import.
Preserve scoped approval evidence and redact sensitive values before sharing.
Public standards summaries support the stated guidance, not a clause-level
conformity or certification claim.

## Required checks

Check resource/type fit, declared authority, required and applicable content,
stable IDs and references, evidence limits and changed-decision history. Read
the actual completed artifact; a template link or structural pass is insufficient.

## Output format

The requested engineering artifact or review, with appropriate source references,
applicability, unresolved facts and verification limits. For ordinary review,
present a self-contained summary in conversation with links for optional detail.

## Examples

- A requirements review uses engineering-requirements and its guide; it does not
  generate product implementation tasks merely because templates are available.
- A design for a small interface change can reference the existing deployment
  view and describe only affected contracts, scenarios and quality concerns.
- A user guide uses the existing release-documentation guidance. Its dedicated
  clean template pack is not supplied by this slice; see the document map.

## Pitfalls

Do not equate source-text instruction evals with model behavior, factual truth or
recipient acceptance. A successful legacy parser result does not establish that
an arbitrary narrative source was fully parsed. Avoid a universal document that
copies every library table into every task.

## Verification

Validate skill metadata and links, run the coordinator's deterministic evals and
affected discovery/source-compatibility tests. Review actual example content
against the accepted outline; visual exports need their own rendering checks.
No automatic activation, parser repair or completion enforcement is added here.
