---
name: escalation-and-recovery
description: Recover from blocked, failed, low-confidence, or contradictory work without losing completed value. Use when an agent cannot access a dependency or tool.
license: MIT
metadata:
  category: agent-orchestration
  origin: custom-synthesis
  revision: "1.1.0"
---

# Escalation And Recovery

## Trigger

- Validation fails repeatedly.
- Sources conflict or a specialist returns low confidence.
- A delegated task exceeds its boundaries.

## Inputs

- Failure evidence
- Task graph
- Completed outputs
- Fallback skills and tools

## Procedure

1. Classify the failure: input, access, capability, dependency, implementation, validation, or policy.
2. Preserve reproducible evidence and the last known-good artifact.
3. Retry only when a changed condition makes success plausible.
4. Reduce scope to the smallest failing unit.
5. Reassign to a more suitable skill or use a bounded fallback.
6. Invalidate downstream work only where dependency impact exists.
7. Return a partial but usable result with explicit gaps when recovery is not possible.

## Output contract

- Recovery decision
- Revised task graph
- Preserved artifacts
- Failure and limitation record

## Quality gates

- No blind retry loops.
- Recovery does not weaken hard constraints.
- Partial results are clearly labeled and still validated.
- Security or policy blocks are never bypassed.

## Handoffs and dependencies

- `work-delegator`
- `dependency-aware-scheduler`
- `result-integrator`

## Boundaries

- Do not ask the user to repeat known information.
- Do not invent success after an unavailable check.
- Do not discard useful completed work.
