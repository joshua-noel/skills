---
name: dependency-aware-scheduler
description: Transform routed work into an executable dependency graph with critical path, checkpoints, and safe concurrency. Use when a request has prerequisites, phases, or cross-artifact dependencies.
license: MIT
metadata:
  category: agent-orchestration
  origin: custom-synthesis
  revision: "1.1.0"
---

# Dependency Aware Scheduler

## Trigger

- An orchestrator needs to know what can start now.
- A failed task may block or invalidate other work.

## Inputs

- Fragments and dependencies
- Delegation briefs
- Expected artifacts
- Resource/tool limits

## Procedure

1. Normalize dependencies as data, evidence, decision, artifact, or environment edges.
2. Detect cycles and break them by extracting a decision or interface contract.
3. Topologically order execution waves.
4. Mark critical-path tasks and optional enhancements.
5. Place validation checkpoints before expensive downstream work.
6. Define re-run scope for each failure class.
7. Update the graph when assumptions or outputs change.

## Output contract

- Acyclic task graph
- Execution waves and critical path
- Checkpoint and re-run policy

## Quality gates

- All dependencies have named producers and consumers.
- Cycles are resolved, not ignored.
- Optional work cannot block required delivery.
- Expensive work is preceded by cheap validity checks.

## Handoffs and dependencies

- `parallel-work-coordinator`
- `escalation-and-recovery`
- `operations/release-coordinator`

## Boundaries

- Do not fabricate time estimates.
- Do not infer tool availability without checking.
- Do not schedule around hidden assumptions.
