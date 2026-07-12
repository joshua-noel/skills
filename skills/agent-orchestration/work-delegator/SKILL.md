---
name: work-delegator
description: Assign each routed fragment to the most capable agent or skill with a bounded brief and explicit return contract. Use when a routing plan is ready for execution.
license: MIT
metadata:
  category: agent-orchestration
  origin: custom-synthesis
  revision: "1.1.0"
---

# Work Delegator

## Trigger

- A complex task requires specialist delegation.
- Ownership is unclear across agents.

## Inputs

- Routing plan
- Fragment context
- Acceptance criteria
- Agent capabilities and tool access

## Procedure

1. Confirm one accountable owner per fragment.
2. Package only the context needed by that owner while preserving exact constraints.
3. State what is in scope, out of scope, required evidence, and return format.
4. Grant the least tool and file access required.
5. Attach upstream dependencies and downstream consumers.
6. Avoid delegating trivial coordination work that is cheaper to execute directly.
7. Record assignment and expected integration point.

## Output contract

- Delegation briefs
- Ownership matrix
- Expected artifact/evidence paths

## Quality gates

- No orphaned fragment.
- No two owners can independently overwrite the same artifact without a merge plan.
- Delegated briefs preserve source constraints.
- Sensitive access follows least privilege.

## Handoffs and dependencies

- `dependency-aware-scheduler`
- `parallel-work-coordinator`
- `result-integrator`

## Boundaries

- Do not delegate final accountability.
- Do not expose unrelated private context.
- Do not split work merely to increase agent count.
