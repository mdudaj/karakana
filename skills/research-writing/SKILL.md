---
name: research-writing
description: Use this skill for academic and concept-note writing, including proposal structure, literature review, methodology, objectives, significance, scope, risk analysis, and grant requirement analysis.
version: 0.1.0
risk_level: low
allowed_tools:
  - read_file
  - grep
  - code_search
requires_approval_for:
  - external_submission
  - publication_claim
activation:
  keywords:
    - research
    - proposal
    - literature review
    - methodology
  required_files: []
  optional_tools:
    - grep
category: research
scope: bundled
---
# Research Writing

## Purpose

Guide academic, concept-note, grant, and proposal writing.

## When to use this skill

Use for proposal structure, literature review, methodology, objectives, significance, scope, risk analysis, and grant or call requirement analysis.

## When not to use this skill

Do not use for code implementation, payment logic, CI repair, or infrastructure changes.

## Core concepts

- Claims should be specific, supported, and scoped.
- Methods should align with objectives and available data.
- Requirements from calls or funders should be tracked explicitly.

## Standard workflow

1. Identify audience, call requirements, and expected format.
2. Clarify research problem, objectives, and scope.
3. Structure methodology and expected outputs.
4. Review risks, limitations, and significance.
5. Keep citations and unsupported claims visible.

## Safety rules

- Do not invent citations or evidence.
- Do not make publication or submission claims without approval.
- Flag unsupported assumptions.

## Required checks

- Check alignment between title, objectives, methods, and outputs.
- Check call requirements.
- Check ethical, data, and feasibility risks.

## Output format

Return structured sections, assumptions, gaps, and recommended next edits.

## Examples

- Draft a concept note outline from a call for proposals.

## Quick Reference

- Align problem, objectives, methods, outputs, and significance.
- Keep unsupported claims and citation gaps visible.
- Track funder or call requirements explicitly.

## Pitfalls

- Do not invent citations or evidence.
- Do not overstate novelty, feasibility, or expected impact.
- Do not claim submission or publication without approval.

## Verification

- Check alignment between objectives, methods, and outputs.
- Check call requirements and formatting constraints.
- Flag ethical, data, feasibility, and evidence gaps.
- Review a methodology section for feasibility and alignment.
