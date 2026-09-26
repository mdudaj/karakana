# Concern-driven design views

Choose views from the people and concerns affected: product/user behavior, component
responsibility, interfaces/data flow, runtime/failure behavior, deployment/operations
or security/quality. Do not produce every possible diagram as a checklist exercise.

For each view name stakeholder/concern, viewpoint/scope, relevant elements/interfaces,
scenario and quality constraint. Explain the boundary, dependencies and assumptions.
State what the view intentionally omits and where the full authoritative source lives.
A single diagram rarely answers all stakeholder concerns.

Use scenario walkthroughs to connect views: inputs/actor -> responsible elements ->
state/data transitions -> observable result -> failure/recovery/feedback. Check that
names, states, ownership and dependencies agree across views and requirements.
Record unresolved contradictions rather than smoothing them into a coherent picture.

Prefer repository-native diagram source, schema or an established design tool. Link
path/version and explain the diagram; generated screenshots are views, not another
master. Do not fetch, execute or change linked resources merely because they are
listed. Use system-design-thinking when the underlying choice is still unresolved.

Design descriptions retain rationale in Markdown; Design Views tables carry concise
concern/scenario/constraint links. A workbook excerpt always points to the complete
source and states omissions. Basis: [research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md),
S02/S05/S17/S18; public summaries only, no claim of normative compliance.
