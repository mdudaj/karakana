# WeasyPrint Professional PDF Notes

Use these notes when styling submission or client-facing PDFs with WeasyPrint.

## Primary WeasyPrint capabilities

- `HTML.write_pdf()` writes rendered HTML to a PDF target. Use `base_url` when rendering from strings so relative assets resolve correctly.
- `@page` defines page size, margins, headers, footers, and page counters.
- Page margin boxes such as `@top-left` and `@bottom-right` are the stable way to add simple running headers and page numbers.
- CSS generated content supports named strings. Use this for active document titles in running headers.
- WeasyPrint automatically generates PDF bookmarks from headings unless CSS changes bookmark behavior.
- HTML metadata such as `<title>`, `<meta name="author">`, `<meta name="description">`, and `<html lang="en">` is used for PDF metadata.
- PDF/UA and PDF/A variants exist, but validity is not guaranteed just by enabling the option. Use correct semantic HTML and validate externally if compliance is required.

Sources checked:

- WeasyPrint API Reference 69.0: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html
- WeasyPrint Common Use Cases 69.0: https://doc.courtbouillon.org/weasyprint/stable/common_use_cases.html
- WeasyPrint samples page: https://weasyprint.org/#samples
- Official report sample PDF: https://github.com/CourtBouillon/weasyprint-samples/raw/main/report/report.pdf
- Official report sample source: https://github.com/CourtBouillon/weasyprint-samples/tree/main/report

## Professional document rules

- Do not expose generator implementation details in client PDFs.
- Do not print source filenames unless the user explicitly asks.
- Do not label a document as “client pack” inside the visible page header unless that is part of the intended cover/title.
- Separate running headers from content with subtle color and whitespace. Avoid header rules when they look inconsistent across pages.
- Keep headings numbered for human review, but avoid repeated full system names in every section title.
- Avoid dense walls of text. Use readable line height, controlled paragraph spacing, and consistent heading rhythm.
- Tables need visible but light borders, shaded header rows, repeated table headers, and break handling.
- Always inspect the first rendered page visually after changing print CSS.

## Lessons from the official report sample

The official report sample is a useful reference for sophisticated WeasyPrint layout. Adopt its patterns selectively; do not copy the design wholesale into client submission documents.

### Patterns to reuse

- Use CSS variables for core colors when the style grows beyond a few declarations.
- Use custom fonts with `@font-face` only when the font files are versioned with the document source or already available in the target environment.
- Use separate `@page` margin boxes for running header text and page counters. Add rules only when the design calls for them.
- Use `string-set` for document-aware running titles.
- Use named pages for special layouts such as a cover, contents page, or divider page.
- Use `target-text()` and `target-counter()` to build an automatic table of contents when the document requires a ToC.
- Use `break-before` for major sections so PDF sections start predictably.
- Use light rules, restrained accent color, and whitespace instead of heavy borders.

### Patterns to avoid unless explicitly requested

- Do not add blank pages through `break-before: right` or `break-after: left` for ordinary client packs. Those rules are suitable for print-book spreads, but they make a digital submission look broken.
- Do not add a cover page if the user asked the client document to start at the executive summary.
- Do not add a generated ToC when the user asked the client version to start with `1. Executive Summary`.
- Do not use decorative page-number badges if the user has asked for the running header text to be the main header element.
- Do not use multi-column body text for requirements, architecture, testing, or admin guidance. Multi-column text is attractive in a brochure but reduces scannability for technical review.
- Do not introduce sample colors directly. Use project/client-appropriate colors.

### Current CRDB MEL choice

For the Sustainable Finance MEL Platform client pack:

- Keep the running header as a zero-padded title, for example `01 Executive Summary`.
- Keep the visible page heading as `1. Executive Summary`.
- Keep page numbers in the footer.
- Keep the client PDF starting at the executive summary.
- Use a text-only zero-padded running title in the left margin box. Do not add a header rule for the current client pack.
- Keep tables full-width and single-column for review clarity.

## Recommended CSS features

- `@page { size: A4; margin: ... }`
- `@top-left { content: string(doc-title); ... }`
- `@bottom-right { content: "Page " counter(page) " of " counter(pages); }`
- `.doc-section { break-before: page; string-set: doc-title attr(data-running-title); }`
- `h1, h2, h3 { break-after: avoid; }`
- `p { orphans: 3; widows: 3; }`
- `thead { display: table-header-group; }`
- `tr { break-inside: avoid; }`

## Verification checklist

- `file <pdf>` reports a PDF.
- `pdftotext -f 1 -l 1 <pdf> -` shows expected header and heading text.
- `pdftoppm -f 1 -l 1 -png -r 120 <pdf> /tmp/preview` produces an image for visual inspection.
- Review the first page for:
  - correct running header;
  - text-only running header without an underline or rule;
  - correct page heading;
  - no filename or internal pack label;
  - readable text size and spacing.
