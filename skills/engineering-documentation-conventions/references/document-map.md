# Engineering document resource map

Map version: 0.1. Content resources are selected by the requested artifact and
reader need. Explicit project instructions and declared source authority govern.

| Document type | Owning skill and resources | Available content pack |
| --- | --- | --- |
| Requirements specification | [engineering-requirements](../../engineering-requirements/SKILL.md); [authoring guide](../../engineering-requirements/references/requirements-template-guide.md) | [Clean template](../../engineering-requirements/assets/requirements-template.md) and [synthetic example](../../engineering-requirements/assets/requirements-example.md) |
| System design | [engineering-design-records](../../engineering-design-records/SKILL.md); [authoring guide](../../engineering-design-records/references/system-design-template-guide.md) | [Clean template](../../engineering-design-records/assets/system-design-template.md) and [matching synthetic example](../../engineering-design-records/assets/system-design-example.md) |
| Architecture decision record | [engineering-design-records ADR guidance](../../engineering-design-records/references/adr.md) | Existing decision guidance and [structured example](../../engineering-design-records/examples/design.md); separate clean ADR pack not added here |
| Implementation plan / milestones / roadmap | [engineering-delivery-planning](../../engineering-delivery-planning/SKILL.md) and its selected references | Existing guidance and examples; dedicated clean packs remain later work |
| Release notes / release plan | [engineering-release-documentation](../../engineering-release-documentation/SKILL.md) and its selected references | Existing guidance and examples; dedicated clean packs remain later work |
| User guide | [adoption and handover guidance](../../engineering-release-documentation/references/adoption-and-handover.md) | Existing guidance; dedicated clean pack remains later work |
| UAT pack | [stories/acceptance guidance](../../engineering-requirements/references/stories-and-acceptance.md), with [engineering-workbooks](../../engineering-workbooks/SKILL.md) for requested workbook views | Existing case/run tables and export guidance; dedicated clean pack remains later work |
| Deployment / recovery runbook | [release-documentation guidance](../../engineering-release-documentation/SKILL.md), with [delivery planning](../../engineering-delivery-planning/SKILL.md) where needed | Existing guidance; dedicated clean pack remains later work |

Read only the selected guide, template and relevant example. References in this
map do not automatically load their contents. The coordinator is an experimental
optional catalogue choice, not a required skill or automatic task router.

The two new `assets/` packs are narrative authoring resources. Existing
`examples/` files use the [P02 structured source/export contract](../../../docs/skills/engineering-artifact-catalogue/P02.md).
Keep their exact metadata, tables and native bindings for supported exports.
Do not pass narrative assets to P02 and claim their content is validated/exported;
the narrative adapter, machine profiles and client projections are later slices.
