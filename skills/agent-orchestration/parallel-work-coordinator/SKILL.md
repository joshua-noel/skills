---
name: parallel-work-coordinator
description: Run independent work streams concurrently while preventing context drift, duplicated effort, and write conflicts. Use when several fragments have no blocking dependencies.
license: MIT
metadata:
  category: agent-orchestration
  origin: custom-synthesis
  revision: "1.1.0"
---

# Parallel Work Coordinator

## Trigger

- Research, review, implementation, and documentation can overlap.
- Latency can be reduced safely through parallelism.

## Inputs

- Task graph
- Ownership matrix
- Shared artifact map
- Merge strategy

## Procedure

1. Group tasks by dependency wave.
2. Identify shared files, assumptions, schemas, and terminology.
3. Create read-only snapshots or isolated branches/worktrees for conflicting writes.
4. Define checkpoints for assumptions that affect multiple streams.
5. Broadcast only material changes to dependent agents.
6. Cancel or re-scope streams invalidated by new evidence.
7. Hand all completed outputs to result integration with provenance.

## Output contract

- Execution-wave plan
- Conflict-avoidance rules
- Checkpoint log
- Completed artifacts with provenance

## Quality gates

- Only truly independent tasks run together.
- Shared assumptions are versioned.
- No concurrent uncoordinated writes to the same source of truth.
- Parallelism never bypasses validation.

## Handoffs and dependencies

- `dependency-aware-scheduler`
- `result-integrator`
- `escalation-and-recovery`

## Boundaries

- Do not parallelize tightly coupled design decisions.
- Do not conceal divergent conclusions; preserve them for adjudication.
