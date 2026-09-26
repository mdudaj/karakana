# Synthetic pilot brief: offline checklist reader

This is an original resolved intent seed for a documentation pilot, not stakeholder
research, a named project, a production requirement or a software implementation.
The author chooses these fictional scenario constraints solely to exercise guidance.
No real user, owner, agreed priority, commitment date or product test is supplied.

A reader opens a local UTF-8 checklist catalogue and locates items with an exact,
case-sensitive category filter. Items have stable IDs, title and category. Empty
matches must show an explicit empty state. Bad input must show a meaningful error
and no partial list. Reading must leave the input file unchanged. No network,
login, collaborative editing, saving, telemetry or deployment is in scope.

A proposed file format is recorded in catalogue.schema.json and illustrated by
catalogue.json. This fixture defines a contract candidate, not an accepted product
interface. There is no prototype; behavior, keyboard/screen-reader results,
performance thresholds, support ownership and recovery evidence are absent.

Direction is selected for this scenario: first settle input/error behavior, then
verify the reader task in a selected environment. Now/Next/Later are learning
horizons, not delivery dates. The version convention is a numbered pilot iteration,
not SemVer. Draft release scope may be communicated; delivered product notes cannot
be written without real delivered evidence. Local documentation/export observations
must be labelled separately from product facts.

Feedback exercise: clarify whether the category filter ignores whitespace. Scenario
scope resolves this as exact matching, including whitespace. Preserve record IDs;
review one amendment in Markdown, retain the prior source and annotated exports,
and create a new derived view. Do not import an agreement cell as approval.
