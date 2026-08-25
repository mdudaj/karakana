---
name: design-token-system
description: Use this skill when creating, revising, auditing, or mapping design tokens for colors, typography, spacing, sizing, radius, elevation, motion, density, themes, contrast-safe semantic roles, component tokens, and framework output.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - design tokens
    - token system
    - primitive tokens
    - semantic tokens
    - component tokens
    - color tokens
    - typography tokens
    - spacing tokens
    - density tokens
    - theme tokens
    - dark mode
    - contrast
    - DTCG
  required_files: []
  optional_tools:
    - grep
    - pytest
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - frontend_design_system_change
  - accessibility_pattern_change
  - token_contract_change
  - brand_identity_change
---
# Design Token System

## Purpose

Guide agents to create, revise, audit, and map design tokens as durable
cross-interface decisions rather than scattered colors, spacing, type sizes, or
CSS literals.

Use this skill when project UI consistency depends on a token contract:
primitive values, semantic roles, component tokens, theme modes, density,
contrast, framework output, and change governance.

## When to use this skill

Use for:

- defining or auditing color, typography, spacing, sizing, radius, elevation,
  shadow, motion, breakpoint, z-index, and density tokens;
- mapping Material 3 roles into project tokens;
- introducing light/dark/high-contrast themes;
- replacing hardcoded UI values with reusable token references;
- defining component token contracts for reusable components;
- checking token aliases, contrast, naming, deprecation, and migration impact.

## When not to use this skill

Do not use for one-off visual tweaks that should not become reusable decisions.
Do not replace brand identity or product visual direction without explicit
approval. For component anatomy use `material-component-spec`; for screen
hierarchy use `material-hcd-interface`; for accessibility gates use
`accessibility-wcag-audit`; for visual critique use `visual-design-review`;
for design-system governance use `design-system-governance`.

## Quick Reference

- Use a layered token model: primitive → semantic → component.
- Primitive tokens store raw values; semantic tokens express product meaning;
  component tokens bind meaning to component anatomy/states.
- Prefer aliases/references over duplicated literals.
- Token names should describe role and intent, not current color appearance.
- Validate contrast for semantic foreground/background pairs, not only raw
  palette colors.
- Include interaction states: hover, focus, pressed, selected, disabled,
  warning, error, success, loading, and readonly where relevant.
- Keep theme and density variants systematic. Do not tune one component in
  isolation.
- Document migration impact before changing token meanings.
- Token changes require visual/accessibility verification across representative
  components/pages.
- Use `visual-design-review` when token changes are proposed from screenshot
  critique or perceived visual imbalance.

## Core concepts

- **Primitive token**: raw brand or scale value such as a palette color, spacing
  step, font size, radius, or duration.
- **Semantic token**: intent-based alias such as `color.text.primary`,
  `color.surface.container`, `space.stack.md`, or `focus.ring.default`.
- **Component token**: component-specific alias such as
  `kpi-card.icon-container.size` or `filter-chip.selected.container`.
- **Theme mode**: token values for light, dark, high-contrast, or brand modes.
- **Density mode**: compact/comfortable sizing and spacing decisions for work
  environments.
- **Contrast pair**: foreground/background token combination that must pass the
  project accessibility target.
- **Token migration**: controlled replacement/deprecation of token names or
  meanings across code and documentation.

## Evidence-backed basis

Read `references/token-architecture.md` before non-trivial token work.

Key source directions:

- The W3C Design Tokens Community Group exists to standardize how products and
  tools share stylistic design-system pieces at scale.
- The DTCG format treats design tokens as named information with values,
  optional type, descriptions, groups, aliases/references, and extension points.
- Public UX/UI agent skill systems use layered token models and gates for
  contrast, alias resolution, hardcoded values, theming, and component specs.
- Material 3 exposes role-based color, type, shape, motion, and state concepts
  that should map into project semantic/component tokens rather than copied as
  page-local literals.

## Standard workflow

1. **Classify token work.** New system, audit, migration, theme, component
   tokens, hardcode cleanup, or framework mapping.
2. **Inspect current source.** Check token files, CSS variables, theme files,
   templates/components, hardcoded values, and design-system docs.
3. **Define token layers.** Primitive values, semantic roles, and component
   aliases. Do not skip semantic tokens.
4. **Map meaning.** Name tokens by purpose: surface, text, border, focus,
   action, state, density, spacing, or component slot.
5. **Define state/theme variants.** Light/dark/high contrast, hover/focus/
   pressed/disabled/selected/error/warning/success, and compact/comfortable
   density where applicable.
6. **Check accessibility.** Verify contrast pairs, focus visibility, disabled
   legibility, color-independent state signals, and reduced motion.
7. **Plan migration.** Replace literals safely, deprecate old tokens, update
   docs, and avoid silent meaning changes.
8. **Map outputs.** CSS variables, Viewflow templates/classes, Tailwind config,
   JS/TS theme objects, native platform tokens, or docs as applicable.
9. **Verify.** Validate token syntax, alias resolution, hardcode cleanup,
   representative components, and browser/screenshot checks where available.

## Required checks

- Are primitive, semantic, and component layers present?
- Are token names intent-based rather than appearance-based?
- Are aliases/references valid and non-cyclic?
- Are semantic foreground/background contrast pairs defined and checked?
- Are state tokens defined for focus, hover, pressed, selected, disabled,
  warning, error, and success where applicable?
- Are component tokens tied to named anatomy/slots from `material-component-spec`?
- Are theme/density variants systematic?
- Are hardcoded values removed or justified?
- Are deprecated tokens documented with replacement paths?
- Are changed tokens verified on representative pages/components?
- Does the change avoid unauthorized brand identity changes?

## Safety rules

- Do not change brand identity, accessibility contrast targets, or global token
  meanings without explicit approval.
- Do not copy another design system’s proprietary brand palette or token names
  as the project identity.
- Do not use color-only semantics for states.
- Do not bypass contrast checks for disabled, warning, error, or focus states.
- Do not replace semantic tokens with raw primitive values in components.
- Do not silently reuse a token name for a different meaning.

## Output format

```markdown
## Design Token System Plan

- Token task:
- Current token sources:
- Proposed layers:
- Semantic roles:
- Component tokens:
- Theme/density variants:
- Accessibility/contrast gates:
- Migration impact:
- Framework/Viewflow output:
- Verification:
- Remaining risk:
```

## Examples

- KPI card: primitive palette values map to semantic workload tones, then to
  component tokens for accent stripe, icon container, icon size, value type,
  label type, and supporting-text color.
- Filter chips: semantic selected/neutral/action roles map to chip container,
  label, icon, focus, hover, disabled, and remove-action tokens.
- Viewflow form: field spacing, helper/error colors, focus ring, label type,
  control height, and validation state tokens map to the canonical renderer.

## Pitfalls

- Naming tokens after colors instead of intent.
- Jumping from primitives directly to component literals.
- Checking contrast only on the brand palette.
- Creating component tokens without component anatomy.
- Changing token meaning without migration notes.
- Solving density with page-local margins.
- Treating dark mode as inverted light mode.

## Verification

- `karakana skill validate skills/design-token-system`
- `karakana eval run --case skills/design-token-system/evals/design-token-system.yml`
- `karakana skill validate-all`
- For projects: validate token files, scan hardcoded literals, check contrast
  pairs, and visually inspect representative components/pages.
