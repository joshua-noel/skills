---
name: request-fragmenter
description: Convert a compound prompt into atomic work fragments that can be assigned, verified, and recombined without losing intent. Use when a prompt contains multiple deliverables, domains, files, audiences, or phases.
license: MIT
metadata:
  category: prompt-decomposer
  origin: custom-synthesis
  revision: "1.1.0"
---

# Request Fragmenter

## Trigger

- The request mixes research, design, implementation, review, and packaging.
- A downstream orchestrator needs a dependency-ready task graph.

## Inputs

- Original request verbatim
- Conversation context and attachments
- Known constraints, deadlines, tools, and target environment

## Procedure

1. Preserve the original request as the source of truth.
2. Extract explicit deliverables, actions, objects, audiences, formats, and success conditions.
3. Separate compound clauses into independently completable fragments.
4. Mark shared context once and reference it rather than duplicating it.
5. Identify implied work only when it is necessary to satisfy an explicit deliverable; label it inferred.
6. Record dependencies, possible parallel groups, and recombination points.
7. Assign each fragment a stable ID and a one-sentence completion test.

## Output contract

- A fragment table with ID, request span, intent, deliverable, inputs, constraints, dependencies, and completion test
- An unresolved-ambiguity register that distinguishes blocking from non-blocking questions
- A coverage map proving every material request span is represented

## Quality gates

- No fragment silently expands scope.
- Every explicit noun-object and requested output is covered.
- Fragments are small enough to assign but not so small that coordination dominates.
- Quoted constraints remain exact.

## Handoffs and dependencies

- `constraint-mapper`
- `acceptance-criteria-extractor`
- `skill-routing-plan`
- `agent-orchestration/work-delegator`

## Boundaries

- Do not solve the fragments.
- Do not choose implementation details unless the prompt already fixes them.
- Do not discard contradictory instructions; surface them.
