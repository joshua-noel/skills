---
name: motion-design
description: Design purposeful, interruptible, performant motion that communicates causality and spatial change without becoming decorative sludge. Use when transitions, gestures, loading, layout change, or microinteractions need motion.
license: MIT
metadata:
  category: interface-and-experience
  origin: custom-synthesis
  revision: "1.1.0"
---

# Motion Design

## Trigger

- Existing animations feel sluggish, generic, or disorienting.
- A UI needs motion audit or improvement.

## Inputs

- Interaction flows
- Platform/runtime
- Performance constraints
- Reduced-motion requirement

## Procedure

1. Define the communication purpose of each animation; remove motion with no purpose.
2. Audit frequency so repeated interactions remain fast.
3. Choose duration and easing based on distance, size, and interruption; favor responsive ease-out for entrances and direct manipulation.
4. Maintain physical continuity and origin/destination relationships.
5. Make animations interruptible and state-driven rather than queued.
6. Animate compositor-friendly properties when possible and profile real devices.
7. Provide reduced-motion alternatives that preserve meaning.
8. Review cohesion across the product, then run mandatory deslop gates to remove fashionable but generic motion.

## Output contract

- Motion specification or implementation
- Timing/easing/state table
- Performance and reduced-motion evidence
- Deslop gate report

## Quality gates

- Motion explains change or feedback.
- Frequent actions are not delayed.
- Interrupted interactions settle correctly.
- All mandatory deslop gates pass.

## Handoffs and dependencies

- `deslop/ui-deslop (mandatory)`
- `deslop/design-pattern-detector (mandatory)`
- `deslop/artifact-delint (mandatory)`
- `deslop/text-humanizer when interface copy is produced`
- `hallmark-upstream/repository/skills/hallmark`
- `Emil Kowalski-inspired animation audit dimensions`

## Mandatory deslop disposition

Fail delivery and return the failed gate report whenever `deslop/ui-deslop`, `deslop/design-pattern-detector`, or `deslop/artifact-delint` does not pass. Revise the work before it can be declared complete.

## Boundaries

- Do not animate every state change.
- Do not use spring motion without physical/brand fit.
- Do not ship motion without reduced-motion behavior or passed deslop gates.
