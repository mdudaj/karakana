# Synthetic governing requirement views

## Requirement records

| ID | Requirement | Rationale / source | Acceptance criteria |
| --- | --- | --- | --- |
| REQ-01 | The checker shall preserve selected source bytes. | Authors own canonical content. | AC-01 |

## Quality records

| ID | Requirement / constraint | Conditions and measure | Verification reference |
| --- | --- | --- | --- |
| REQ-02 | The checker shall refuse output over an existing file. | Existing output bytes stay identical after refusal. | AC-02 |

## Criteria

| Criterion ID | Requirement ID | Conditions / event | Expected outcome | Verification method |
| --- | --- | --- | --- | --- |
| AC-01 | REQ-01 | A synthetic source is checked | Original source bytes are identical | Compare hashes before and after checking |
| AC-02 | REQ-02 | An existing output path is selected | Output is refused and existing bytes are identical | Exercise the CLI against a temporary root |
