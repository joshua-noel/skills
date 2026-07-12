---
name: scalability-and-reliability
description: Design capacity, resilience, graceful degradation, and recovery around concrete load and failure scenarios. Use when a system must handle growth, bursts, regional failure, or strict availability targets.
license: MIT
metadata:
  category: system-design
  origin: custom-synthesis
  revision: "1.1.0"
---

# Scalability And Reliability

## Trigger

- Reliability incidents expose unclear limits.
- A design needs SLO-driven review.

## Inputs

- Traffic and data forecasts
- Critical journeys
- SLOs/RTO/RPO
- Dependency limits and failure history

## Procedure

1. Define service-level indicators and realistic objectives per journey.
2. Model steady, peak, burst, and pathological load.
3. Find bottlenecks and finite resources across the full path.
4. Select partitioning, caching, queuing, batching, backpressure, and admission control only where needed.
5. Design timeouts, retries with jitter, circuit breaking, idempotency, and bulkheads coherently.
6. Specify degradation modes and customer-visible behavior.
7. Plan backup, failover, restore, and disaster exercises.
8. Create load, chaos, and recovery validation plans.

## Output contract

- Capacity model
- Reliability architecture
- Failure-mode table
- SLO and validation plan

## Quality gates

- Retry budgets do not amplify outages.
- Queues have bounds and poison-message handling.
- Failover is tested, not assumed.
- SLOs map to user journeys and alerting.

## Handoffs and dependencies

- `performance-optimization`
- `operations/incident-operations`
- `operations/deployment-readiness`
- `security/threat-modeling`

## Boundaries

- Do not promise “infinite scale.”
- Do not add distributed components without identifying the bottleneck they solve.
- Do not confuse redundancy with recoverability.
