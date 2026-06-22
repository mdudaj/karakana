---
name: research-platform
description: Use this skill when working on software platforms that implement a research prototype, evaluation workflow, experiment design, data collection, or evidence generation for a dissertation or research project.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - pytest
requires_approval_for:
  - evaluation_protocol_change
  - participant_data_change
  - curriculum_source_change
  - automated_curriculum_review_change
  - whatsapp_message_template_change
  - model_provider_change
  - production_config_change
  - remote_push
activation:
  keywords:
    - research platform
    - prototype
    - evaluation workflow
    - experiment
    - evidence generation
    - participant data
  required_files: []
  optional_tools:
    - grep
category: research
scope: bundled
status: experimental
visibility: public
bucket: research
---
# Research Platform

## Purpose

Guide work on research software platforms that implement prototypes, evaluation workflows, experiment support, data collection, and evidence generation.

## When to use this skill

Use for software that supports a dissertation or research project through implementation, evaluation, logging, export, reproducibility, or participant-facing workflows.

## When not to use this skill

Do not use this skill for dissertation chapter writing, literature review editing, citation cleanup, or submission formatting. Use `research-writing` for manuscript and methodology text.

## Core concepts

- Every feature should map to a research objective or evaluation activity.
- Prototype scope should stay bounded by dissertation evidence needs.
- Evaluation workflows must preserve reproducibility and traceability.
- Participant-sensitive data must not be stored in Git or exposed in artifacts.
- Result exports should make evidence reviewable without requiring production deployment.
- Research platforms are instruments: preserve objective, workflow, evidence, provenance, and replay links.
- Prefer schema-backed evidence artifacts for curriculum, workflow, evaluation, export, and repository-safety records.
- Configurable workflows should separate governed definitions, runtime capture, evidence projection, and reconstruction.
- Deterministic curriculum extraction is the source of truth when official curriculum sources are involved.
- Optional LLM enrichment and automated review are assistive only and must not overwrite deterministic facts.
- Human review remains the final acceptance gate for promoted curriculum topics or evaluation decisions.

## Standard workflow

1. Identify the research objective the platform work supports.
2. Identify the evaluation activity the work enables.
3. Identify the evidence the platform should generate.
4. Check whether the feature is necessary for dissertation evaluation or overbuilt.
5. Review privacy, ethics, data retention, and reproducibility risks.
6. Define tests or eval checks for the user flow, data capture, and exports.

## MSc STEM platform guidance

Use this guidance for `stemgen-platform` and similar research instruments for curriculum-aligned STEM media generation.

- Start from an objective-to-feature-to-evidence matrix before adding implementation slices.
- Keep configurable workflow design behind repo-owned definitions, immutable published versions, compiled execution manifests, and explicit publication/review gates.
- Borrow the LIMS-style designer/runner separation: designers author governed definitions; runners execute published versions and capture evidence.
- Treat the workflow engine as layered: governed definition, workflow/runtime, runtime capture, evidence projection, and audit/reconstruction.
- Do not generate arbitrary executable workflow code from database records. Use controlled expressions, configured transitions, and stable framework adapters.
- For TIE curriculum intake, maintain a source registry, snapshot manifest, checksum artifact, extraction manifest, normalized items, candidate topic dataset, automated review artifact, and human selection decisions.
- Official curriculum sources remain Tier 1. Contextual or research sources may enrich interpretation but must not override Tier 1 facts.
- Rule-based topic screening should identify animation-friendly concepts such as process, sequence, change over time, cause/effect, spatial relation, abstraction, transformation, or system interaction.
- Verbalized-sampling-inspired automated review should request distributions of plausible judgments, rationales, and uncertainty flags, not one best answer.
- Automated review output must be stored separately from deterministic curriculum facts and must never auto-accept topics.
- Human topic selection must check source reference validity, deterministic extraction, animation rationale, and any automated review before accepting a topic.
- Expert review rubrics should preserve structured scores, comments, evaluator profile context, artifact links, and export readiness.
- WhatsApp may be a secondary evaluator communication channel for invitations, links, reminders, acknowledgements, and short support messages; the web platform remains canonical.
- Evidence exports should include analysis tables, structured provenance JSON, artifact bundles, and reporting summaries.
- Replay should distinguish deterministic replay expectations from external AI generation runs that may only be explainable, not bit-for-bit reproducible.
- Project repository commits and pushes require explicit opt-in, branch checks, clean patch review/gates, no secrets, no main/master push, and no force push.
- Do not implement a workflow artifact before its schema exists, unless the implementation task explicitly creates the schema first.
- Validate example fixtures before implementation begins.
- Treat schema changes as research-contract changes that require matching documentation and validation updates.
- Flag overengineering when a feature does not support a research objective, evaluation activity, evidence artifact, or reproducibility requirement.

## Safety rules

- Do not ingest `.env`, secrets, participant data, or generated evaluation data unless explicitly selected and redacted.
- Treat changes to evaluation protocol, data collection, model providers, prompts, exports, and participant workflows as high risk.
- Do not deploy, publish, or push research platform changes without explicit human action.
- Keep generated evidence reproducible and clearly linked to the evaluation activity.
- Do not allow LLM output to overwrite official curriculum facts or deterministic extraction outputs.
- Do not allow automated review to select or promote curriculum topics without human acceptance.
- Do not require WhatsApp credentials or send live WhatsApp messages during planning/documentation milestones.

## Required checks

- Which research objective does this support?
- Which evaluation activity does this enable?
- What evidence will this produce?
- Is this needed for the dissertation, or is it overengineering?
- What data or privacy risk is introduced?
- What test, eval, or manual review proves the workflow is ready?
- Is deterministic source-of-truth data separated from optional enrichment/review output?
- Is the human gate explicit and auditable?
- Is the implementation slice smaller than the full research platform?
- Does the artifact have a schema and example fixture?
- Has schema validation been run?
- Is any commit or push path explicit, gated, and auditable?

## Output format

Return a concise assessment with research objective alignment, evaluation readiness, evidence output, risks, tests, and next actions.

## Examples

- Review whether a prototype feature supports a stated research objective and evaluation activity.
- Check that an evaluation export produces reviewable evidence without exposing participant-sensitive data.
- Split a platform backlog into dissertation-required work and non-essential product polish.

## Quick Reference

- Map features to objectives, activities, and evidence.
- Prefer evaluation-ready slices over broad product features.
- Preserve reproducibility and privacy.
- Use `research-writing` for manuscript text and `research-platform` for implementation/evaluation support.

## Pitfalls

- Building polished product features that do not support the dissertation evaluation.
- Treating prototype logs or exports as safe to commit.
- Changing evaluation protocol without review.
- Losing the link between platform behavior and research evidence.
- Designing configurable workflows that execute editable drafts instead of published versions.
- Treating LLM review as curriculum authority.
- Making WhatsApp the canonical evaluation record.
- Combining workflow engine, curriculum extraction, generation, review, export, and messaging into one implementation issue.

## Verification

- Review a feature list against research objectives.
- Review evaluation setup for reproducibility and privacy.
- Check result export paths and logs for sensitive data risks.
- Check tests cover the prototype workflow and evidence generation path.
- Validate workflow definitions, manifests, candidate topic datasets, review distributions, topic decisions, evidence projections, exports, and push-safety checks before implementation slices are considered ready.
- Validate schema files and example fixtures before implementing producers or consumers of the evidence artifacts.
