# ADR 0002: Make OKF a First-Class Karakana Knowledge Substrate

Date: 2026-06-22

## Status

Proposed

## Context

Karakana already keeps durable project memory, skills, handoffs, requirements, ADRs, evals, and self-improvement evidence. The current structure is useful for Codex sessions, but it remains Karakana-specific and does not expose a consistent portable knowledge graph across the harness and the projects it develops.

Google Cloud's Open Knowledge Format article and the OKF reference repository describe a file-native way to package knowledge as Markdown concepts with YAML frontmatter, links, indexes, and logs. The useful pattern for Karakana is not a dependency on Google Cloud infrastructure; it is the ability to represent curated knowledge as typed, versioned, linkable concepts that humans and agents can both inspect.

The user direction is that OKF should be first-class for the self-evolving harness, the Karakana knowledge base, and developed projects.

## Decision

Karakana will treat OKF-compatible concepts as a first-class durable knowledge representation.

Karakana will add a local OKF profile before implementing exporters, loaders, or graph traversal. The profile will define required frontmatter, allowed concept types, relationship conventions, lifecycle states, promotion rules from runtime artifacts, validation behavior, and safety constraints.

Karakana runtime artifacts under `.karakana/` remain append-only evidence. Promotion from runtime evidence to durable OKF concepts must be explicit, reviewable, and testable.

## Scope

The first implementation milestone must deliver:

- A Karakana OKF profile document.
- A deterministic OKF validator for repository and project bundles.
- A minimal Karakana OKF knowledge base for core harness concepts.
- A minimal `msc-platform` OKF bundle that references, but does not duplicate, source artifacts.
- Context-loading support that can select relevant OKF concepts by type, tag, project, status, and relationship.
- Tests or evals that prevent malformed concept frontmatter, broken required fields, unsafe promotion, and context overloading.

## Non-Goals

- Do not replace existing `ubongo/`, skills, handoffs, requirements, ADRs, or evals in the first milestone.
- Do not require a network service, hosted catalog, vector database, or Google Cloud dependency.
- Do not bulk ingest all runtime artifacts.
- Do not silently rewrite project memory.
- Do not promote `.karakana/` runtime logs into durable concepts without review.
- Do not use OKF to bypass existing safety, approval, model, or patch gates.

## Consequences

- Karakana knowledge will become portable across agents and tools that can read Markdown and YAML frontmatter.
- Handoffs can reference stable concept IDs instead of only file paths.
- Cross-project learning can operate on typed concept graphs rather than copying project-specific memory.
- Self-improvement proposals can be linked to the concepts they change.
- Project development can become more agentic-native by making requirements, schemas, UI contracts, workflows, and evidence artifacts discoverable as linked concepts.
- Validation and promotion rules become necessary to avoid turning OKF into another uncurated artifact dump.

## Verification

- `karakana okf validate` validates Karakana and project OKF bundles.
- `karakana skill validate-all` remains green after any skill or profile changes.
- Focused pytest/eval coverage verifies parser, validator, promotion, export, and context-selection behavior.
- Handoffs record changed concept IDs and exact next actions.

## References

- Google Cloud article: `https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing`
- OKF reference repository: `https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf`
