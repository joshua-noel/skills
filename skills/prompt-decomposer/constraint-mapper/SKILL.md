---
name: constraint-mapper
description: Extract, normalize, rank, and attach constraints to the exact work fragments they govern. Use when a request contains technical, legal, stylistic, budget, time, compatibility, safety, or format constraints.
license: MIT
metadata:
  category: prompt-decomposer
  origin: custom-synthesis
  revision: "1.1.0"
---

# Constraint Mapper

## Trigger

- Requirements appear across conversation turns or attached material.
- Conflicting constraints need deterministic resolution.

## Inputs

- Prompt fragments
- Conversation history
- Environment/tool constraints
- Applicable policies and source licenses

## Procedure

1. Collect constraints using exact wording before paraphrasing.
2. Classify each as hard, soft, default, inferred, external, or prohibited.
3. Attach scope: global, category, fragment, deliverable, or file.
4. Order precedence: safety/policy, explicit latest user instruction, project constraints, then defaults.
5. Detect contradictions and propose the least-assumptive resolution.
6. Record verification method for each hard constraint.

## Output contract

- Constraint matrix with source, normalized rule, scope, precedence, conflict status, and verification method
- A concise list of defaults applied only where the prompt is silent

## Quality gates

- No hard constraint is converted into a preference.
- No inferred constraint is presented as user-stated.
- Every conflict has an explicit disposition.
- License and attribution requirements travel with copied material.

## Handoffs and dependencies

- `request-fragmenter`
- `acceptance-criteria-extractor`
- `security/*`
- `operations/release-coordinator`

## Boundaries

- Do not invent requirements to make planning easier.
- Do not override a high-precedence constraint with a conventional best practice.
