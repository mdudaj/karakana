# Skill vs Tool Policy

Karakana uses skills for reusable workflow guidance and tools for deterministic execution.

## Prefer a Skill When

- Instructions plus existing tools are enough.
- The task is mostly workflow guidance.
- The task involves repeated reasoning patterns.
- The task is project or domain convention heavy.
- Human judgment is needed before taking action.

## Create a Tool When

- Deterministic execution is required.
- Authentication or API handling is required.
- Binary or streaming data is involved.
- Precise parsing or transformation is required.
- Safety gates must be enforced programmatically.

## Operating Principle

Skills describe workflows.
Tools execute tightly scoped operations.
High-risk tools require safety gates.

## Examples

- Viewflow workflow review -> skill
- Viewflow frontend form review -> skill
- Viewflow process-state debugging checklist -> skill
- GePG callback idempotency checklist -> skill
- Posting GitHub comments -> tool
- Running tests -> tool
- Parsing GitHub event JSON -> tool
- Inspecting Viewflow process states in DB -> future tool

## Viewflow Guidance

Use `viewflow-framework` for workflow, frontend, process-state, task-transition, approval, assignment, and workflow-permission tasks.
Combine it with `django-debugging` for general Django errors.
Combine it with `gepg-billing` when billing workflows use Viewflow.
Combine it with `invenio-framework` when repository or project workflows use Viewflow.

## Governance

- Skills live under `skills/<name>/SKILL.md`.
- Tools live under `karakana/tools/` or a narrower package when ownership is clearer.
- Skills may recommend tools, but tools must enforce their own safety checks.
- Tool changes that touch authentication, GitHub writes, production systems, billing, migrations, or destructive operations require tests and human review.
