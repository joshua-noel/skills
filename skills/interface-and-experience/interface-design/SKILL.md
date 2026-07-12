---
name: interface-design
description: Design a visually intentional, responsive interface that makes hierarchy and action obvious while conforming to mandatory deslop gates. Use when a new page, application surface, dashboard, landing page, or component family needs design.
license: MIT
metadata:
  category: interface-and-experience
  origin: custom-synthesis
  revision: "1.1.0"
---

# Interface Design

## Trigger

- An existing interface needs visual redesign.
- A brief requires implementation-ready UI direction.

## Inputs

- User jobs and content
- Brand and product constraints
- Platform/component stack
- Accessibility and responsive requirements

## Procedure

1. Start with content, hierarchy, and the primary user path.
2. Choose a genre and macrostructure appropriate to the brief rather than defaulting to a centered SaaS page.
3. Define display/body/label typography roles, spacing scale, palette, surfaces, borders, radii, shadows, and states.
4. Design at narrow and wide widths concurrently.
5. Use real product evidence and content-shaped components.
6. Specify states: loading, empty, error, success, disabled, permission-limited, and overflow.
7. Apply Hallmark where compatible, then run all mandatory deslop dependencies.
8. Fail delivery and revise when any mandatory deslop gate fails.

## Output contract

- Responsive interface specification or implementation
- Token and component decisions
- State coverage
- Deslop gate report

## Quality gates

- Primary action and hierarchy are readable in seconds.
- No fabricated proof or content.
- Keyboard, contrast, target size, zoom, and reduced-motion requirements pass.
- All mandatory deslop gates pass.

## Handoffs and dependencies

- `deslop/ui-deslop (mandatory)`
- `deslop/design-pattern-detector (mandatory)`
- `deslop/artifact-delint (mandatory)`
- `deslop/text-humanizer when interface copy is produced`
- `hallmark-upstream/repository/skills/hallmark`

## Boundaries

- Do not decorate before information architecture is sound.
- Do not clone references.
- Do not ship if a mandatory deslop dependency is unavailable or failed; report the block.
