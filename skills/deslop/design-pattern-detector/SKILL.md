---
name: design-pattern-detector
description: Detect repeated AI-default visual, structural, interaction, and copy patterns before they harden into a design. Use when a mockup, screenshot, design system, or ui implementation needs an anti-slop audit.
license: MIT
metadata:
  category: deslop
  origin: custom-synthesis
  revision: "1.1.0"
---

# Design Pattern Detector

## Trigger

- Several generated pages look like color swaps of one template.
- An interface skill requests a pre-ship gate.

## Inputs

- Screenshots or code
- Page purpose and genre
- Design tokens/components
- Reference constraints

## Procedure

1. Audit macrostructure, navigation, hero, section cadence, component repetition, typography, palette, spacing, motion, imagery, and copy.
2. Count repeated shapes and alignments rather than relying only on aesthetic intuition.
3. Flag template tells: same-radius cards everywhere, icon-square feature tiles, gradient text, excessive badges, sticky generic nav, centered headline/body/CTA stacks, undifferentiated sections, and ornamental backgrounds.
4. Distinguish product constraints from generated defaults.
5. Rank findings by how strongly they erase identity or harm use.
6. Recommend structural alternatives, not cosmetic swaps.
7. Record patterns worth preserving because they are purposeful.

## Output contract

- Ranked pattern audit
- Structural replacement directions
- Pass/fail gate for interface delivery

## Quality gates

- Findings are observable and specific.
- Recommendations preserve product comprehension.
- A single legitimate component pattern is not mislabeled as slop.
- Structural sameness is addressed before palette changes.

## Handoffs and dependencies

- `ui-deslop`
- `hallmark-upstream/repository/skills/hallmark`
- `interface-and-experience/ux-audit`

## Boundaries

- Do not confuse minimalism with lack of design.
- Do not ban common patterns that solve a real user task.
- Do not clone a reference to create uniqueness.
