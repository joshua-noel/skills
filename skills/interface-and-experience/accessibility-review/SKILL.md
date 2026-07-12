---
name: accessibility-review
description: Audit and remediate an interface for perceivability, operability, understandability, robustness, and inclusive use while retaining deliberate design. Use when a ui is being reviewed before release.
license: MIT
metadata:
  category: interface-and-experience
  origin: custom-synthesis
  revision: "1.1.0"
---

# Accessibility Review

## Trigger

- Accessibility defects are suspected.
- A redesign must meet WCAG-aligned requirements.

## Inputs

- Rendered interface and source
- Target platforms/browsers/AT
- Content and user journeys
- Applicable conformance target

## Procedure

1. Test semantic structure, landmarks, headings, names, roles, values, and reading order.
2. Operate complete journeys by keyboard and inspect focus visibility/order/traps.
3. Check contrast, non-color cues, zoom/reflow, text spacing, target sizes, and orientation.
4. Inspect forms, validation, errors, status messages, dialogs, live regions, and dynamic updates.
5. Test reduced motion and avoid vestibular triggers.
6. Use automated tooling as a floor, then manual and assistive-technology checks on critical journeys.
7. Remediate at shared component level when possible.
8. Run mandatory deslop gates after remediation to prevent generic accessibility overlays or visual regression.

## Output contract

- Prioritized accessibility findings
- Remediated implementation/spec
- Manual test evidence
- Deslop gate report

## Quality gates

- Critical journeys work without pointer or vision assumptions.
- Accessible names match visible intent.
- Focus is never lost silently.
- All mandatory deslop gates pass.

## Handoffs and dependencies

- `deslop/ui-deslop (mandatory)`
- `deslop/design-pattern-detector (mandatory)`
- `deslop/artifact-delint (mandatory)`
- `deslop/text-humanizer when interface copy is produced`
- `hallmark-upstream/repository/skills/hallmark`

## Mandatory deslop disposition

Fail delivery and return the failed gate report whenever `deslop/ui-deslop`, `deslop/design-pattern-detector`, or `deslop/artifact-delint` does not pass. Revise the work before it can be declared complete.

## Boundaries

- Do not claim full conformance from automated scans alone.
- Do not remove aesthetics unnecessarily when accessible alternatives exist.
- Do not use overlay widgets as a substitute for fixing the product.
