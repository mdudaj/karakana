#!/usr/bin/env python3
"""Render Markdown submission packs to professional PDFs with WeasyPrint."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt
from weasyprint import HTML


RUNNING_TITLES = {
    "README.md": "Submission pack",
    "00-documentation-plan.md": "00 Documentation Plan",
    "01-executive-summary.md": "01 Executive Summary",
    "02-prototype-scope.md": "02 Prototype Scope",
    "03-requirements-specification.md": "03 Requirements Specification",
    "04-current-architecture.md": "04 Current Architecture",
    "05-user-manual.md": "05 User Manual",
    "06-testing-validation-report.md": "06 Testing and Validation Report",
    "07-deployment-admin-guide.md": "07 Deployment and Administration Guide",
    "08-known-limitations.md": "08 Known Limitations",
    "09-future-product-vision.md": "09 Future Product Vision",
    "10-implementation-roadmap.md": "10 Implementation Roadmap",
    "11-traceability-matrix.md": "11 Traceability Matrix",
}

FULL_ORDER = [
    "README.md",
    "00-documentation-plan.md",
    "01-executive-summary.md",
    "02-prototype-scope.md",
    "03-requirements-specification.md",
    "04-current-architecture.md",
    "05-user-manual.md",
    "06-testing-validation-report.md",
    "07-deployment-admin-guide.md",
    "08-known-limitations.md",
    "09-future-product-vision.md",
    "10-implementation-roadmap.md",
    "11-traceability-matrix.md",
]

CLIENT_ORDER = [
    "01-executive-summary.md",
    "02-prototype-scope.md",
    "03-requirements-specification.md",
    "04-current-architecture.md",
    "05-user-manual.md",
    "06-testing-validation-report.md",
    "07-deployment-admin-guide.md",
    "08-known-limitations.md",
    "09-future-product-vision.md",
]


CSS = """
@page {
  size: A4;
  margin: 22mm 16mm 20mm 16mm;
  @top-left {
    content: string(doc-title);
    font-size: 10pt;
    color: #6b7280;
    border-bottom: 0.35pt solid #c9ced6;
    padding-bottom: 0.9mm;
    width: 178mm;
    vertical-align: bottom;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-size: 8pt;
    color: #6b7280;
  }
}

* { box-sizing: border-box; }

html {
  color: #1f1f1f;
  font-family: "Segoe UI", Arial, sans-serif;
  font-size: 11.5pt;
  line-height: 1.48;
}

body {
  margin: 0;
}

.doc-section {
  break-before: page;
  padding-top: 3.5mm;
  string-set: doc-title attr(data-running-title);
}

.doc-section:first-of-type {
  break-before: auto;
}

h1 {
  color: #0f4761;
  font-size: 23pt;
  font-weight: 700;
  letter-spacing: -0.015em;
  line-height: 1.16;
  margin: 0 0 8mm 0;
}

h2 {
  color: #0f4761;
  font-size: 15.5pt;
  font-weight: 700;
  line-height: 1.22;
  margin: 8mm 0 3.5mm 0;
}

h3 {
  color: #0f4761;
  font-size: 12.7pt;
  font-weight: 700;
  line-height: 1.22;
  margin: 6mm 0 2.5mm 0;
}

h1, h2, h3 {
  break-after: avoid;
}

p {
  margin: 0 0 3.7mm 0;
  orphans: 3;
  widows: 3;
}

ul, ol {
  margin: 0 0 4mm 0;
  padding-left: 6mm;
}

li {
  margin-bottom: 1.7mm;
}

table {
  border-collapse: collapse;
  font-size: 9.6pt;
  line-height: 1.34;
  margin: 4mm 0 6mm 0;
  width: 100%;
}

thead {
  display: table-header-group;
}

tr {
  break-inside: avoid;
}

th, td {
  border: 0.5pt solid #c9ced6;
  padding: 2.1mm;
  vertical-align: top;
}

th {
  background: #edf5f8;
  color: #0f4761;
  font-weight: 700;
}

tbody tr:nth-child(even) td {
  background: #fafafa;
}

code {
  background: #f4f4f4;
  border-radius: 2pt;
  font-family: "Cascadia Mono", "Consolas", monospace;
  font-size: 9.6pt;
  padding: 0.4mm 0.9mm;
}

pre {
  background: #f4f4f4;
  border-left: 2.5pt solid #c9ced6;
  font-family: "Cascadia Mono", "Consolas", monospace;
  font-size: 9.6pt;
  line-height: 1.35;
  margin: 4mm 0 5mm 0;
  overflow-wrap: anywhere;
  padding: 3mm;
  white-space: pre-wrap;
}

a {
  color: #0f6cbd;
  text-decoration: none;
}

blockquote {
  border-left: 3px solid #b6d7e8;
  color: #444;
  margin: 4mm 0;
  padding-left: 4mm;
}

hr {
  border: 0;
  border-top: 0.5pt solid #d9d9d9;
  margin: 8mm 0;
}
"""


def render_pack(source_dir: Path, order: list[str], output: Path, title: str) -> None:
    markdown = MarkdownIt("commonmark", {"html": False}).enable("table")
    sections = []

    for name in order:
        path = source_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Missing submission file: {path}")

        running_title = RUNNING_TITLES.get(name, path.stem)
        body = markdown.render(path.read_text(encoding="utf-8"))
        sections.append(
            f'<section class="doc-section" data-running-title="{escape(running_title)}">'
            f"{body}"
            "</section>"
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(title)}</title>
  <meta name="author" content="CRDB Sustainable Finance Unit">
  <meta name="generator" content="Karakana pdf-submission-renderer">
  <meta name="description" content="{escape(title)}">
  <style>{CSS}</style>
</head>
<body>
  {"".join(sections)}
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(source_dir)).write_pdf(str(output))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render professional Markdown submission packs with WeasyPrint."
    )
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--client-output", required=True, type=Path)
    parser.add_argument("--internal-output", required=True, type=Path)
    args = parser.parse_args()

    render_pack(
        args.source_dir,
        CLIENT_ORDER,
        args.client_output,
        "Sustainable Finance MEL Platform Client Submission Pack",
    )
    render_pack(
        args.source_dir,
        FULL_ORDER,
        args.internal_output,
        "Sustainable Finance MEL Platform Internal Submission Pack",
    )
    print(args.client_output)
    print(args.internal_output)


if __name__ == "__main__":
    main()
