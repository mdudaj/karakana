# Stories, criteria and verification

Use a story to describe actor, goal and benefit in a bounded user scenario. Keep
conversation/scope, dependencies and acceptance records visible; a sentence alone
cannot define all behavior. INVEST is a useful discussion heuristic, not proof that
all dependencies can be eliminated. Do not force stories on every maintenance task.

Give each criterion a persistent ID and a resolvable source requirement/story.
Record context, event and observable outcome; use Given/When/Then if helpful, not
as a mandatory syntax. Cover meaningful normal, failure and permission boundaries,
quality/accessibility constraints and examples needed to settle ambiguity. Record
measurement/threshold, verification method and owner; never manufacture agreement.

Keep three things separate:

- Criterion: what outcome must be observable, and under what conditions.
- Test case/UAT script: preconditions, steps, expected result and method/source.
- Test run: actual revision/environment/time/executor/result and evidence.

Use Not run, Blocked, Skipped, Fail or Pass accurately. A skipped or unexecuted case
is not a pass. Pass/Fail needs a real scoped observation; test success does not equal
business acceptance. Acceptance/review records identify the reviewer/role, source
revision, decision, time and evidence under the existing project process.

Example criterion: after a reviewer opens a derived record, its stable source ID and
full-source link remain visible. Whether the link resolves must be checked in the
actual recipient environment; a written expected outcome is not that observation.

For export use Stories/Acceptance/Test Cases/Test Runs and typed Links as applicable.
The native engine's identical criterion text in different owners does not merge
identity. Basis: [research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md),
S10–S13/S19; these are tailored local practices, not extra Scrum requirements.
