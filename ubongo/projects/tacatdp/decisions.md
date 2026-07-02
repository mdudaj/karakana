# TACATDP Decisions

## Microsoft Lists instead of Dataverse

Dataverse privileges are not available, so TACATDP should use Microsoft Lists/SharePoint as the current backend.

## Importable list templates

Generated Excel/CSV templates are preferred for creating Microsoft Lists where possible. This reduces manual list and column creation.

## Skill-first implementation

Implementation should not start until the relevant Karakana skill, project memory, workspace registration, and OKF concepts are present and validated.

## Phase 3 with placeholder data sources

Phase 3 may continue while Milestone 1 and Milestone 2 are on hold. Data-source connections should use placeholders until the Windows/Power Apps environment is ready, with an explicit mapping to the intended SharePoint/Microsoft Lists sources for later replacement.

## One-field-per-row form layout

Data-entry screens should default to one field per row with visible labels, helper/error text near the input, consistent spacing, and accessible focus order.

## App-layer validation for skip logic

Power Fx should enforce requiredness and constraints according to visibility/relevance. SharePoint columns that can be skipped should not be marked required.
