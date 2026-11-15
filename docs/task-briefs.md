# Task briefs that work on first encounter

A task brief should let a developer explain the work and its relevance without
prior chat history or opening links. Start with product → feature/capability →
this task, then give technical scope, acceptance and execution instructions.
A feature ID, acronym, component name or list of mechanisms alone is insufficient.
This applies when writing a task or next-task brief; preserve inquiry, review,
research and implementation request types and their existing authority.

## Compact opening

Use the [blank task brief](../templates/protocols/task-brief.md), tailoring its
length to the task. A short paragraph and compact labeled lines are sufficient.
Explain:

- Project/product purpose and relevant subsystem, expanding local acronyms.
- Related feature/capability in plain language, with an ID/link if available.
- Who or which workflow is affected and what problem creates the work.
- Why this task matters now: gap, dependency, risk or learning decision.
- Current state and prerequisites, with accepted/proposed and actual/planned clear.
- Intended outcome and immediate contribution to the feature; identify later work.
- Bounded scope, request type and existing authority.
- Governing evidence, revision/status and first references to inspect.

Follow with observable acceptance, required work/decisions, non-goals, risks,
verification, deliverables and exact next action. References support the opening;
they do not replace its explanation. Reuse governing artifacts rather than copying
their histories. Mark missing facts unconfirmed with an evidence/decision owner
and next action. Never manufacture users, business benefit, priorities, dates,
parent feature or approval. Mechanical work may need only a few sentences.

## First-encounter review

Read only the opening. Can a new developer state what product this serves, the
related feature, who benefits, the current gap, why now, what this task changes
and what is actually authorized? If not, revise it before presenting it as a
complete brief. Human review establishes relevance and factual applicability;
heading/field coverage cannot establish those qualities.

## Worked example

Fictional SurveyHub example; these statements are illustrative, not project facts.

SurveyHub helps research teams prepare study forms before data collection. This
task belongs to **form preparation → reliable background compilation**. A technical
maintainer currently starts compilation synchronously; a stopped process has no
durable attempt to inspect or recover. The next task defines durable job ownership
so failures can be recovered without accepting a stale result. It builds on an
already accepted inactive-artifact registry; data collection is later work.

Scope is requirements/design only. Produce job/attempt/outbox contracts and state
transitions, acceptance examples for duplicate dispatch, worker death and late
results, and the first bounded implementation slice. Implementing jobs, selecting
production operations or activating forms requires the corresponding authority.
Evidence for a real brief would name the current source, accepted feature/requirement
and verified baseline; this fictional example cannot supply that authority.

Compare “Add outbox, leases and fencing”: mechanisms alone leave product purpose,
feature relevance, current behavior and developer responsibility unexplained.

## Generated Codex tasks

Existing Codex task metadata optionally accepts `brief_context`:

```json
{
  "project_purpose": "SurveyHub prepares study forms for research teams.",
  "related_feature": "Form preparation: reliable background compilation (FORM-08).",
  "beneficiary": "Technical maintainers preparing forms for study teams.",
  "task_relevance": "Interrupted synchronous work cannot be durably inspected or recovered.",
  "current_state": "Inactive artifact registry accepted; durable job design pending.",
  "intended_outcome": "A bounded job design and first implementation slice.",
  "scope_and_authority": "Research/design requested; implementation and activation remain separate.",
  "references": ["Unconfirmed — provide real requirement, design and source revision locators."]
}
```

For an action-to-Codex handoff, author this map in `action.metadata.brief_context`.
It is carried to `codex-task.json` and rendered before task details/model metadata.
There is no inferred extraction from IDs or bundle summaries. Missing, invalid or
placeholder fields render unconfirmed and `needs_context`; complete field coverage
renders `complete`. These are structural context statuses only, not task readiness,
factual validation, acceptance or permission. Unknown fields require reconciliation.
References are displayed, never automatically read or followed. Existing redaction
is applied to this optional context in JSON and Markdown. Legacy JSON still loads.

The plain Markdown template is an authoring aid, not a new P02 export or M2 input
profile. Existing document-task check/readiness and execution gates are unchanged.
Shared conditional prompt guidance also covers planning/document preparation;
there is no automatic live model execution or conversion of reviews into tasks.

## Method references and limits

The introduction follows [arc42 goals/stakeholders](https://docs.arc42.org/section-1/)
and [C4 system context](https://c4model.com/diagrams/system-context), tailored to a
short task. [Shape Up pitches](https://basecamp.com/shapeup/1.5-chapter-06) motivate
concrete problem/boundary explanations; [GitHub task guidance](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results)
supports scoped acceptance and relevant files. Checked15 November2026. This is a
synthesis of documentation practices, not a performance study or conformance claim.
