---
name: design-system
description: Create or evolve a design system that encodes product decisions, accessibility, and composable behavior without turning every UI into the same generic template. Use when multiple products or teams need shared tokens/components.
license: MIT
metadata:
  category: interface-and-experience
  origin: custom-synthesis
  revision: "1.1.0"
---

# Design System

## Trigger

- UI inconsistency or duplicated components is costly.
- A component library needs governance and documentation.

## Inputs

- Product families and use cases
- Existing inventory
- Brand/accessibility standards
- Technology constraints

## Procedure

1. Audit existing patterns and cluster by semantic purpose, not visual similarity alone.
2. Define tokens in layers: primitives, semantic roles, component aliases, and modes.
3. Build components around stable behavior and composition points.
4. Document anatomy, variants, states, accessibility, content rules, and escape hatches.
5. Use governance and contribution criteria based on repeated need.
6. Keep product-specific compositions outside the core library when they would flatten identity.
7. Add visual, interaction, accessibility, and contract tests.
8. Run mandatory deslop gates on both the system and representative assembled pages.

## Output contract

- Token architecture
- Component library/spec
- Usage and contribution documentation
- Test and deslop evidence

## Quality gates

- Components are composable without prop explosions.
- Tokens express meaning rather than hard-coded appearance.
- Accessibility is built in.
- All mandatory deslop gates pass on representative use.

## Handoffs and dependencies

- `deslop/ui-deslop (mandatory)`
- `deslop/design-pattern-detector (mandatory)`
- `deslop/artifact-delint (mandatory)`
- `deslop/text-humanizer when interface copy is produced`
- `hallmark-upstream/repository/skills/hallmark`

## Mandatory deslop disposition

Fail delivery and return the failed gate report whenever `deslop/ui-deslop`, `deslop/design-pattern-detector`, or `deslop/artifact-delint` does not pass. Revise the work before it can be declared complete.

## Boundaries

- Do not add a component for a one-off design.
- Do not centralize product-specific content patterns prematurely.
- Do not let system consistency erase brand or task-specific hierarchy.
