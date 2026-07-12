---
name: incident-operations
description: Coordinate incident detection, containment, diagnosis, recovery, communication, and learning with clear roles and evidence. Use when a production service or security control is degraded.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Incident Operations

## Trigger

- Customer impact is active or likely.
- An alert requires structured triage.

## Inputs

- Alert and impact evidence
- Service ownership/runbooks
- Recent changes
- Observability and communication channels

## Procedure

1. Declare severity based on impact and uncertainty.
2. Assign incident command, operations, communications, and scribe roles appropriate to scale.
3. Stabilize: stop harmful changes, reduce load/exposure, and preserve evidence.
4. Build a timestamped fact log and separate hypotheses.
5. Use controlled experiments and one change at a time where possible.
6. Communicate impact, mitigation, and next update without speculation.
7. Verify recovery from customer and system perspectives.
8. Schedule a blameless review with concrete corrective actions and owners.

## Output contract

- Incident log
- Containment/recovery actions
- Stakeholder updates
- Post-incident action set

## Quality gates

- Customer impact drives priority.
- Facts and hypotheses are separated.
- Recovery is verified, not inferred from one green metric.
- Actions address contributing system conditions, not individual blame.

## Handoffs and dependencies

- `software-development/debugging`
- `security/zero-day-triage`
- `documentation/runbook-authoring`

## Boundaries

- Do not improvise destructive commands without safeguards.
- Do not share sensitive forensic details broadly.
- Do not delay containment solely to perfect diagnosis.
