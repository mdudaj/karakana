# Engineering Standards

Document durable engineering standards that apply across Karakana-managed projects, including testing expectations, code review expectations, and maintainability conventions.

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

Karakana-managed product interfaces should not expose implementation-process language such as "readiness", "artifact gate", "protocol", "harness", or similar delivery vocabulary in the primary user experience unless the project explicitly defines an administrator diagnostic surface for it.

For operational users, express the same meaning with user-facing terms such as status, checks, configuration, health, setup, access, or next action. Keep delivery readiness, scope readiness, and implementation gates in documentation, handoff notes, validators, or admin diagnostics rather than dashboards, primary navigation, quick-action panels, or normal route headers.
