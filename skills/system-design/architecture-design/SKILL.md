---
name: architecture-design
description: Design a software architecture whose boundaries, responsibilities, data flow, and trade-offs are clear enough to implement and evolve. Use when a new system or major capability needs planning.
license: MIT
metadata:
  category: system-design
  origin: custom-synthesis
  revision: "1.1.0"
---

# Architecture Design

## Trigger

- An existing system needs re-partitioning.
- Multiple technologies or services must be evaluated.

## Inputs

- Business goals and quality attributes
- Constraints and expected scale
- Current landscape
- Team and operational capabilities

## Procedure

1. Clarify actors, core journeys, invariants, and failure consequences.
2. Prioritize quality attributes with concrete scenarios.
3. Define system context, major components, ownership, and contracts.
4. Prefer deep modules and stable interfaces over many shallow layers.
5. Trace critical data/control flows and failure recovery.
6. Evaluate at least two viable options and record trade-offs.
7. Design observability, security, rollout, migration, and operability from the start.
8. Mark assumptions and validation experiments.

## Output contract

- Architecture narrative and diagrams
- Component responsibility table
- Key flows and failure modes
- Trade-off/decision log
- Implementation slices

## Quality gates

- Every component has one clear reason to exist.
- Cross-boundary calls have explicit contracts and ownership.
- Quality attributes are testable.
- The design is no more distributed than requirements demand.

## Handoffs and dependencies

- `api-and-contract-design`
- `domain-modeling`
- `data-modeling`
- `scalability-and-reliability`
- `documentation/design-document`

## Boundaries

- Do not choose technology before framing the problem.
- Do not use microservices as a default.
- Do not hide unresolved decisions behind generic boxes.
