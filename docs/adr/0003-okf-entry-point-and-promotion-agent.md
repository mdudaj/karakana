# ADR 0003: Use OKF as Agent Workflow Entry Point and Add Promotion Agent

Date: 2026-06-22

## Status

Proposed

## Context

ADR 0002 made OKF a first-class Karakana knowledge substrate. The initial implementation added local OKF parsing, validation, bounded concept selection, curated concept bundles, promotion-record validation, and handoff fields for loaded and changed concept IDs.

The next gap is operational. Agents still start primarily from handoff files and bespoke inspect-first paths. OKF concepts should become the systematic entry point for agentic workflows, and Karakana needs an explicit role that promotes durable artifacts into OKF based on rules.

## Decision

Karakana will add an OKF workflow entry point and an OKF promotion agent role.

Session start and handoff loading should first select relevant OKF concepts for the project and task. Agents should then inspect the source artifacts referenced by those concepts. Handoffs must record loaded and changed concept IDs.

Karakana will also add an `okf-promotion-agent` skill and CLI workflow that scans eligible runtime and durable artifacts, proposes OKF concept changes, validates promotion records, and requires review before promotion. Promotion must be rule-based and must never silently bulk-promote runtime artifacts.

## Promotion Rules

Promotable by default:

- Accepted ADRs.
- Ready requirements and user stories.
- Stable design-system rules.
- Schema and evidence contracts.
- Safety rules and model-routing decisions.
- Verified implementation lessons that recur.
- Handoffs that contain stable next-action or decision knowledge.

Not promotable by default:

- Raw traces.
- Noisy logs.
- Failed experiments.
- Temporary notes.
- Runtime artifacts with secrets or blocked paths.
- Project-specific memory proposed for another project without explicit crosslink metadata.

## Consequences

- Agent workflows will become concept-first rather than path-first.
- OKF promotion becomes a reviewable workflow rather than a manual copy operation.
- The harness can evolve by curating stable knowledge while keeping runtime evidence append-only.
- More tests and evals are required to prevent unsafe promotion, context overload, and cross-project contamination.

## Verification

- Session start tests show OKF concepts are selected before source files.
- Promotion-agent tests show eligible artifacts become proposals, not committed concepts.
- Unsafe artifacts are rejected or warned.
- Handoff output includes loaded and changed concept IDs.
- `karakana okf validate --strict` remains green.
