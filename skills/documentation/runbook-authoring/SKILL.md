---
name: runbook-authoring
description: Write an executable operational runbook for recurring procedures, alerts, incidents, recovery, and verification. Use when operators need a repeatable procedure.
license: MIT
metadata:
  category: documentation
  origin: custom-synthesis
  revision: "1.1.0"
---

# Runbook Authoring

## Trigger

- An incident exposed undocumented recovery steps.
- A deployment or maintenance task carries risk.

## Inputs

- Trigger and scope
- Required access/tools
- Commands and expected outputs
- Rollback/escalation contacts

## Procedure

1. State when to use the runbook and when not to.
2. List prerequisites, permissions, safety checks, and impact.
3. Write numbered actions with exact commands, parameters, expected outputs, and decision branches.
4. Place verification after each consequential step.
5. Include abort conditions, rollback, recovery, and escalation.
6. Separate environment-specific values into variables or secure references.
7. Test in the closest safe environment and record last verification.
8. Add owner and review cadence.

## Output contract

- Operational runbook
- Verification and rollback steps
- Troubleshooting branches
- Ownership/freshness metadata

## Quality gates

- A qualified operator can execute without tribal knowledge.
- Destructive actions are conspicuous and guarded.
- Secrets are referenced, not embedded.
- Rollback is realistic and tested where feasible.

## Handoffs and dependencies

- `operations/incident-operations`
- `operations/deployment-readiness`
- `security/secrets-and-supply-chain`

## Boundaries

- Do not write “check logs” without naming where and what to look for.
- Do not hide irreversible steps in prose.
- Do not promise rollback where data changes make it impossible.
