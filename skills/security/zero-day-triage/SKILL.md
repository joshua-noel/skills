---
name: zero-day-triage
description: Defensively triage newly disclosed or suspected zero-day risk and coordinate containment without speculative exploitation. Use when a credible new vulnerability may affect deployed systems.
license: MIT
metadata:
  category: security
  origin: custom-synthesis
  revision: "1.1.0"
---

# Zero Day Triage

## Trigger

- A vendor advisory is incomplete or no patch exists.
- Indicators suggest exploitation of an unknown weakness.

## Inputs

- Affected product inventory
- Current vendor/CERT advisories
- Logs and indicators
- Business criticality and exposure

## Procedure

1. Establish an incident lead and preserve source authenticity.
2. Verify affected products, versions, configurations, and internet reachability.
3. Separate confirmed facts, credible hypotheses, and rumor.
4. Apply temporary containment in order of reversibility: reduce exposure, disable vulnerable feature, tighten identity/network controls, isolate, then stop service if necessary.
5. Increase targeted logging and preserve forensic evidence without tipping off an active adversary unnecessarily.
6. Hunt only for published, defensible indicators and anomalous behavior.
7. Track vendor updates and test patches in a representative environment.
8. Communicate impact, decisions, and review intervals to stakeholders.

## Output contract

- Exposure matrix
- Containment and monitoring actions
- Evidence-preservation log
- Patch/recovery plan

## Quality gates

- Actions are based on verified applicability.
- Containment does not destroy evidence.
- No unvalidated signature creates excessive false positives without review.
- All exceptions and next-review times are owned.

## Handoffs and dependencies

- `operations/incident-operations`
- `dependency-cve-audit`
- `documentation/runbook-authoring`

## Boundaries

- Do not develop or share zero-day exploit chains.
- Do not probe systems without authorization.
- Do not state compromise is absent merely because known indicators are absent.
