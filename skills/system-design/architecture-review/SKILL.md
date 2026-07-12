---
name: architecture-review
description: Audit a proposed or existing architecture for clarity, fitness, coupling, failure behavior, and evolutionary cost. Use when an architecture document or system needs an independent review.
license: MIT
metadata:
  category: system-design
  origin: custom-synthesis
  revision: "1.1.0"
---

# Architecture Review

## Trigger

- A major decision is approaching approval.
- Incidents or delivery friction suggest structural issues.

## Inputs

- Architecture artifacts and code map
- Quality attributes and constraints
- Operational evidence
- Decision history

## Procedure

1. Reconstruct the actual architecture from evidence, not only diagrams.
2. Evaluate problem fit, boundaries, data ownership, contracts, coupling, security, operability, and change paths.
3. Trace one normal and one failure journey end to end.
4. Identify accidental distribution, duplicate sources of truth, shallow layers, and hidden synchronous dependencies.
5. Compare stated quality goals with measurable mechanisms.
6. Rank risks by probability, impact, and reversibility.
7. Propose incremental remedies before wholesale rewrites.
8. Record strengths that must be preserved.

## Output contract

- Ranked architecture findings
- Risk heatmap
- Incremental remediation roadmap
- Decision recommendation

## Quality gates

- Findings cite concrete components or flows.
- Recommendations fit team and migration constraints.
- A rewrite is justified only against incremental options.
- Unknowns are labeled and assigned validation work.

## Handoffs and dependencies

- `documentation/architecture-decision-record`
- `software-development/refactoring`
- `operations/release-coordinator`

## Boundaries

- Do not review diagrams in isolation from runtime behavior.
- Do not prescribe fashionable patterns without causal benefit.
- Do not understate migration risk.
