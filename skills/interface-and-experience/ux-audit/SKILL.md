---
name: ux-audit
description: Evaluate an end-to-end experience against user goals, comprehension, efficiency, accessibility, trust, and distinctiveness, then prioritize evidence-based improvements. Use when an existing product flow needs critique.
license: MIT
metadata:
  category: interface-and-experience
  origin: custom-synthesis
  revision: "1.1.0"
---

# Ux Audit

## Trigger

- Conversion, completion, support, or satisfaction is poor.
- A redesign requires a baseline diagnosis.

## Inputs

- Product/flow access
- User goals and audience
- Analytics/research/support evidence
- Technical and policy constraints

## Procedure

1. Define critical journeys and success measures.
2. Walk the experience with realistic content, permissions, errors, latency, and narrow screens.
3. Assess orientation, information scent, hierarchy, control clarity, feedback, recovery, trust, and cognitive load.
4. Compare observed behavior with analytics, support themes, and research where available.
5. Separate usability defects from preference and visual sameness.
6. Run accessibility and all mandatory deslop audits.
7. Rank findings by user impact, frequency, confidence, and effort/reversibility.
8. Recommend experiments or changes with measurable outcomes.

## Output contract

- Ranked UX findings
- Journey evidence
- Prioritized remediation/experiment plan
- Accessibility and deslop gate reports

## Quality gates

- Findings connect to a user goal and evidence.
- No fake certainty where user research is absent.
- Critical recovery paths are included.
- All mandatory deslop gates pass before final redesign approval.

## Handoffs and dependencies

- `deslop/ui-deslop (mandatory)`
- `deslop/design-pattern-detector (mandatory)`
- `deslop/artifact-delint (mandatory)`
- `deslop/text-humanizer when interface copy is produced`
- `hallmark-upstream/repository/skills/hallmark`
- `accessibility-review`
- `research/research-planner when user evidence is missing`

## Mandatory deslop disposition

Fail delivery and return the failed gate report whenever `deslop/ui-deslop`, `deslop/design-pattern-detector`, or `deslop/artifact-delint` does not pass. Revise the work before it can be declared complete.

## Boundaries

- Do not present taste as user evidence.
- Do not optimize conversion through deception or dark patterns.
- Do not approve a redesign that failed mandatory deslop or accessibility gates.
