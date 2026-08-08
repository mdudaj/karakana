---
name: pdf-submission-renderer
description: Render professional Markdown submission packs to clean client-facing PDFs with WeasyPrint. Use when Codex needs to create, revise, style, or regenerate proposal, prototype, submission, handover, client-sharing, or internal documentation PDFs from Markdown sources, especially when the output needs running headers, page numbers, tables, section breaks, PDF metadata, or repeatable styling.
version: 0.1.0
risk_level: low
allowed_tools:
  - read_file
  - grep
  - code_search
  - python
  - weasyprint
  - pdftotext
  - pdftoppm
requires_approval_for:
  - remote_push
  - overwriting_client_deliverable
activation:
  keywords:
    - PDF
    - WeasyPrint
    - submission
    - client-facing
    - document pack
    - professional document
    - running header
    - page numbers
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
---
# PDF Submission Renderer

## Quick Reference

- Use `scripts/render_submission_pdf.py` instead of one-off inline Python.
- Keep Markdown headings clean for page content, for example `# 1. Executive Summary`.
- Set running headers separately from page headings, for example `01 Executive Summary`.
- Use WeasyPrint `@page` margin boxes for headers, footers, and page numbers.
- Use a text-only running-header pattern unless the user explicitly asks for a rule or divider.
- Let `@page` margins define the top content start; do not add section-level top padding to simulate header spacing.
- Use section-level `string-set` for the active running header.
- Verify PDFs with text extraction and at least one rendered page image before delivery.
- Do not add implementation labels, filenames, or pack names to client-facing pages unless the user asks for them.

## Purpose

Create professional, repeatable PDF submission packs from Markdown without rediscovering WeasyPrint styling, page-header behavior, table rules, and verification steps on every delivery.

## When to use this skill

Use this skill when generating, revising, or reviewing client-facing or internal PDF submission packs from Markdown. Use it for WeasyPrint styling changes, running headers, page numbers, section breaks, table formatting, PDF metadata, and final visual checks.

## When not to use this skill

Do not use this skill for DOCX editing, slide decks, scanned PDFs, raster image generation, or PDFs that must preserve an existing manually designed template unless the user asks to recreate that template with HTML/CSS.

## Core concepts

- Markdown content and PDF running headers are separate concerns.
- Client-facing PDFs must not expose implementation details such as source filenames or pack labels.
- WeasyPrint page margin boxes are reliable for simple headers, footers, and counters.
- Named strings and section attributes let each document section control its own running header.
- Visual verification is required because PDF text extraction cannot prove spacing, line placement, or page balance.

## Standard workflow

1. Inspect the source Markdown and confirm the client-facing order.
2. If the user requests research-backed styling, read `references/weasyprint-professional-pdf.md`.
3. Generate PDFs with:

   ```bash
   python skills/pdf-submission-renderer/scripts/render_submission_pdf.py \
     --source-dir /path/to/docs/submission \
     --client-output Client-Pack.pdf \
     --internal-output Internal-Pack.pdf
   ```

4. Verify:

   ```bash
   pdftotext -f 1 -l 1 /path/to/Client-Pack.pdf -
   pdftoppm -f 1 -l 1 -png -r 120 /path/to/Client-Pack.pdf /tmp/client-preview
   ```

5. Confirm the first page shows:
   - zero-padded running header, for example `01 Executive Summary`;
   - page heading, for example `1. Executive Summary`;
   - no filename line;
   - no implementation label such as `Client submission pack`.

## Safety rules

- Do not rewrite stakeholder-facing claims while making style-only changes.
- Do not expose secrets, environment URLs with credentials, or internal-only comments in generated PDFs.
- Do not commit generated PDFs until the source Markdown and rendered first page have been checked.
- Ask before changing the document scope, adding a cover, adding logos, or introducing client branding not already approved.

## Required checks

- Did the source Markdown headings match the requested visible document titles?
- Did the running header match the requested header convention?
- Did the first page avoid filename, pack-label, or generator text?
- Did tables remain readable after typography changes?
- Did `pdftotext` and a rendered preview both confirm the output?

## Styling Rules

- Use A4 portrait unless the user asks otherwise.
- Keep the running header gray and visually separate from content.
- Prefer a clean text-only running header in `@top-left`; avoid header rules unless specifically requested.
- Use page numbers in the footer.
- Increase body text only when readability improves; avoid making tables unusable.
- Use table header repetition, avoid row splitting where possible, and keep table text slightly smaller than body text.
- Use `break-before: page` between documents.
- Keep header-to-content spacing consistent by using page margins, not `.doc-section` padding.
- Use `break-after: avoid` for headings and `orphans`/`widows` for paragraphs.
- Preserve source content. Styling changes should not rewrite technical claims.

## Pitfalls

- Header rules can render inconsistently across pages and look like content. Prefer text-only running headers for clean client packs.
- Section-level top padding creates inconsistent header/content spacing because it only applies at the start of a section, not continuation pages.
- Using `h1 { string-set: ... }` makes running headers match page headings; use section attributes when the two formats differ.
- Larger body text can make tables overflow or push a client pack into too many pages.
- `pdftotext` can confirm labels and order, but it cannot verify visual spacing.
- Generic skill validators may reject Karakana's extended skill frontmatter; use Karakana validators for repository skills.

## Verification

Run:

```bash
karakana skill validate skills/pdf-submission-renderer
karakana skillpack validate-all
karakana okf validate
```

For generated PDFs, run:

```bash
pdftotext -f 1 -l 1 <client.pdf> -
pdftoppm -f 1 -l 1 -png -r 120 <client.pdf> /tmp/client-preview
```

Inspect the generated preview image before delivery.

## Output format

When reporting delivery, include:

- generated PDF paths;
- validation commands and results;
- visual-check result;
- commit hash if pushed;
- any known warnings that are unrelated to the delivered PDF.

## Examples

Client-facing pack:

```bash
python skills/pdf-submission-renderer/scripts/render_submission_pdf.py \
  --source-dir /home/jmduda/KodeX/crdb-mel/docs/submission \
  --client-output /home/jmduda/KodeX/crdb-mel/docs/submission/Sustainable-Finance-MEL-Platform-Client-Submission-Pack.pdf \
  --internal-output /home/jmduda/KodeX/crdb-mel/docs/submission/Sustainable-Finance-MEL-Platform-Submission-Pack.pdf
```

## Resources

- `scripts/render_submission_pdf.py`: deterministic Markdown-to-PDF renderer for CRDB MEL-style submission packs.
- `references/weasyprint-professional-pdf.md`: researched WeasyPrint styling notes and guardrails.
