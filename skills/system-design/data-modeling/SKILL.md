---
name: data-modeling
description: Design data structures, storage boundaries, lifecycle, integrity, and access patterns for correctness and evolution. Use when persistent data or analytics storage needs design.
license: MIT
metadata:
  category: system-design
  origin: custom-synthesis
  revision: "1.1.0"
---

# Data Modeling

## Trigger

- A schema must scale or migrate.
- Consistency and retention requirements are unclear.

## Inputs

- Domain model
- Read/write/query patterns
- Volume and growth
- Consistency, privacy, retention, and recovery needs

## Procedure

1. Identify authoritative sources and ownership for each datum.
2. Model keys, relationships, constraints, temporal history, and lifecycle.
3. Choose storage based on access and integrity requirements rather than trend.
4. Define transactions, consistency boundaries, isolation expectations, and conflict handling.
5. Design indexes from measured query patterns and write costs.
6. Specify retention, deletion, archival, encryption, backup, and restore.
7. Plan online migrations, compatibility windows, and rollback.
8. Create representative datasets and integrity tests.

## Output contract

- Logical/physical data model
- Access-pattern table
- Integrity and lifecycle rules
- Migration and recovery plan

## Quality gates

- No critical invariant relies only on application convention.
- PII classification and deletion path are explicit.
- Indexes have a query justification.
- Migration is reversible or has a tested forward recovery.

## Handoffs and dependencies

- `security/threat-modeling`
- `scalability-and-reliability`
- `operations/deployment-readiness`

## Boundaries

- Do not denormalize without a measured access need.
- Do not use eventual consistency without describing user-visible effects.
- Do not store derived data without reconciliation rules.
