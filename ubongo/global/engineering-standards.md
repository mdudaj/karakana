# Engineering Standards

Durable engineering standards for Karakana-managed projects.

## Task Lifecycle

Apply `docs/engineering-process.md` from the Karakana harness: classify the request
and authority, establish acceptance, reuse or research/design, plan, implement,
verify and validate, review, release only when authorized, then hand off.
Tailor depth to risk; do not require a new PRD/ADR for a mechanical fix or repeat
current approved research. Reopen affected decisions when scope/evidence changes.

Prerequisite and completion artifact checks are distinct. File presence is not
proof of semantic quality, test success or approval. Inspect actual results,
including skipped checks and unresolved findings. A self-review is not independent
review, and merged is not deployed or accepted. Keep project/revision/environment
provenance explicit; test fixtures must not populate real handoff stores.

## Engineering Documentation Skills

Use the [shared catalogue](../../skills/README.md) and
[content contract](../../docs/engineering-artifacts.md) from the Karakana harness.
Select the applicable experimental skill for requested authoring or review:

- `engineering-requirements`: PRDs, requirements, stories, criteria and traceability.
- `engineering-design-records`: ADRs, design views and contract/quality descriptions.
- `engineering-delivery-planning`: outcome roadmaps, milestones and task plans.
- `engineering-release-documentation`: release plans, notes and adoption/handover.
- `engineering-workbooks`: audience Excel exports and proposed-feedback reports.

Markdown is primary; Excel is a derived audience view. Preserve native engine and
machine-source authority, stable IDs and scoped evidence; global templates remain
generic and blank. Catalogue availability does not authorize drafting: inquiry,
research and planning retain their requested output. Optional skills are choices,
not automatically loaded bodies; select one explicitly with `--skill` when using
Karakana planning. Existing elicitation, lifecycle and approval rules still govern.

## Evidence-Grounded Delivery

All Karakana-managed work must be grounded in inspected evidence rather than unverified assumptions.

This applies to research, brainstorming, architecture, documentation, implementation, debugging, packaging, deployment planning, and review. Before changing behavior or issuing implementation guidance, inspect the most authoritative available sources for the task:

- project instructions and durable memory;
- relevant skills and their verification sections;
- repository source, schemas, migrations, exported artifacts, package metadata, or generated files;
- official vendor/framework documentation for unstable APIs, CLIs, schemas, permissions, or product behavior;
- runtime output, import errors, logs, tests, evals, and validation commands.

For non-trivial work, the delivery artifact or working notes must state:

- the evidence checked;
- the governing skill, project instruction, ADR, requirement, or doc;
- the implementation steps the agent should follow;
- the verification commands or external gates required;
- known assumptions, missing evidence, and residual risks.

When a failure reveals a reusable rule, encode it into the right durable layer: global memory for cross-project behavior, project memory for project-specific constraints, a skill for repeatable workflows, documentation for human delivery, and tests/evals/validators for regressions.

Do not present guesses as established facts. If evidence is unavailable, label the statement as an assumption and prefer a reversible, minimal change with explicit verification.

## UX Feedback for Mutating Workflows

Unless a project explicitly specifies a different interaction model, Karakana-managed UI work must provide clear user feedback after every mutating action.

For create, update, delete, submit, invite, assign, import, export, publish, deploy, payment, approval, and permission workflows:

- show a visible success, failure, or pending/interrupted state after the action;
- keep the result visible long enough for the user to read, verify, dismiss, or continue;
- do not silently redirect, reload, close a dialog, or return to a list without an outcome message;
- include the affected entity or user, timestamp, and next action when practical;
- preserve feedback across an unexpected reload when the action is asynchronous or externally integrated;
- expose actionable failure text rather than only logging to the console.

For high-risk systems such as banking, healthcare, billing, permissions, or production deployment, feedback must be page-level or otherwise persistent, not only a transient toast.

## Product UI Wording

Karakana-managed product interfaces should not expose implementation-process language such as "readiness", "artifact gate", "protocol", "harness", "fixture", "seed", "projection", "migration", "purge", or similar delivery/backend vocabulary in the primary user experience unless the project explicitly defines an administrator diagnostic surface for it.

For operational users, express the same meaning with user-facing terms such as status, checks, configuration, health, setup, access, or next action. Keep delivery readiness, scope readiness, and implementation gates in documentation, handoff notes, validators, or admin diagnostics rather than dashboards, primary navigation, quick-action panels, or normal route headers.

Before user-facing UI copy is delivered, route labels, status text, warnings, help text, empty states, and instructions through the `ux-writing` skill or an equivalent project copy contract. Copy that explains policy or system status must state the current user-visible state and consequence in plain language.

## Research-Backed UI/UX Delivery

Before delivering user-facing UI/UX work, Karakana-managed projects must ground
the interface decision in human-centered design evidence.

Default order:

1. Use existing project design-system guidance, product UX specifications,
   component contracts, and relevant Karakana UX skills.
2. If the feature, component, work environment, or interaction pattern is not
   already covered, research current authoritative guidance before planning or
   implementation.
3. Record the relevant HCD/design evidence in the requirements, specification,
   delivery notes, or trace.
4. Translate the finding into reusable components, tokens, copy rules, state
   patterns, accessibility checks, or browser verification when the issue is
   likely to repeat.

Suitable evidence includes official framework/design-system documentation,
accessibility standards, product-specific research, domain workflow evidence,
observed screenshots, user feedback, and comparable project design contracts.

Do not treat ad hoc visual preference as enough for delivery. If evidence is
missing, state the assumption and keep the change reversible and narrowly
scoped.
