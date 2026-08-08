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

## Professional document rules

- Do not expose generator implementation details in client PDFs.
- Do not print source filenames unless the user explicitly asks.
- Do not label a document as “client pack” inside the visible page header unless that is part of the intended cover/title.
- Separate running headers from content with subtle color, whitespace, and a line close to the header text.
- Keep headings numbered for human review, but avoid repeated full system names in every section title.
- Avoid dense walls of text. Use readable line height, controlled paragraph spacing, and consistent heading rhythm.
- Tables need visible but light borders, shaded header rows, repeated table headers, and break handling.
- Always inspect the first rendered page visually after changing print CSS.

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
  - underline directly under the running header;
  - correct page heading;
  - no filename or internal pack label;
  - readable text size and spacing.
