---
name: deployment-readiness
description: Decide whether a change is safe to deploy by verifying artifact, configuration, migration, observability, security, capacity, and rollback evidence. Use when a release candidate is approaching deployment.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Deployment Readiness

## Trigger

- A high-risk configuration or migration will change production.
- A go/no-go review is needed.

## Inputs

- Release artifact and provenance
- Test/security results
- Migration/rollout plan
- Dashboards, alerts, and rollback

## Procedure

1. Verify exact artifact identity and environment configuration.
2. Confirm tests, security gates, compatibility, and change approvals.
3. Review database/data migrations for locks, duration, compatibility, backup, and recovery.
4. Validate feature flags, staged rollout, capacity, dependency readiness, and support coverage.
5. Confirm dashboards, logs, traces, alerts, and success/failure thresholds.
6. Rehearse or inspect rollback and forward-fix options.
7. Set go/no-go criteria and named decision owners.
8. Record post-deploy verification and observation window.

## Output contract

- Readiness checklist with evidence
- Go/no-go recommendation
- Rollout, verification, and rollback plan

## Quality gates

- No unchecked item is treated as implicitly passed.
- Rollback limitations are explicit.
- Observability exists before exposure.
- The artifact is immutable and traceable.

## Handoffs and dependencies

- `release-coordinator`
- `incident-operations`
- `documentation/runbook-authoring`
- `security/*`

## Boundaries

- Do not approve based on schedule pressure.
- Do not call a rollback safe without data compatibility analysis.
- Do not hide failed checks in prose.
