---
name: acceptance-criteria-extractor
description: Turn request fragments and constraints into observable, testable completion criteria. Use when a deliverable is subjective or underspecified.
license: MIT
metadata:
  category: prompt-decomposer
  origin: custom-synthesis
  revision: "1.1.0"
---

# Acceptance Criteria Extractor

## Trigger

- An agent needs a definition of done before implementation.
- Multiple outputs must be validated consistently.

## Inputs

- Fragments
- Constraint matrix
- Target format and runtime
- Relevant quality standards

## Procedure

1. For each fragment, define the observable outcome rather than the activity.
2. Use Given/When/Then only where behavior benefits from it; otherwise use direct checks.
3. Include positive, negative, edge, integration, and packaging criteria as applicable.
4. Separate must-pass criteria from desirable enhancements.
5. Tie each criterion to an evidence type: test, file inspection, command output, screenshot, citation, or human review.
6. Add a final end-to-end criterion for the integrated deliverable.

## Output contract

- Acceptance-criteria register with IDs traceable to fragment IDs
- Validation evidence plan
- Definition of done for the complete request

## Quality gates

- Criteria are binary or objectively reviewable.
- No criterion tests an implementation detail unless required.
- Every hard constraint appears in at least one criterion.
- The integrated artifact can be validated without reading hidden reasoning.

## Handoffs and dependencies

- `skill-routing-plan`
- `agent-orchestration/result-integrator`
- `operations/deployment-readiness`

## Boundaries

- Do not confuse “implemented” with “works.”
- Do not use vague criteria such as “high quality,” “robust,” or “user friendly” without measurable indicators.
