---
name: result-integrator
description: Merge specialist outputs into one coherent deliverable while preserving correctness, traceability, and user intent. Use when several agents return files, findings, or recommendations.
license: MIT
metadata:
  category: agent-orchestration
  origin: custom-synthesis
  revision: "1.1.0"
---

# Result Integrator

## Trigger

- Conflicting outputs must be reconciled.
- The final package needs cross-cutting validation.

## Inputs

- Agent outputs
- Acceptance criteria
- Constraint matrix
- Artifact and provenance map

## Procedure

1. Verify each output against its return contract before merging.
2. Normalize names, terminology, paths, formats, and versions.
3. Resolve contradictions by evidence and source precedence; record unresolved risk.
4. Integrate at defined interfaces rather than editing unrelated internals.
5. Run cross-artifact tests and deslop/security gates where applicable.
6. Build a coverage ledger from request fragment to final evidence.
7. Produce a concise final handoff with known limitations.

## Output contract

- Integrated artifacts
- Coverage and provenance ledger
- Conflict resolutions
- Validation report

## Quality gates

- Every fragment is represented or explicitly marked incomplete.
- No source attribution is lost.
- The combined result passes end-to-end criteria.
- Known limitations are concrete, not euphemistic.

## Handoffs and dependencies

- `documentation/project-documentation`
- `operations/deployment-readiness`
- `deslop/artifact-delint`

## Boundaries

- Do not average incompatible recommendations.
- Do not silently rewrite specialist conclusions.
- Do not claim validation that was not run.
