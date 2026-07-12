---
name: code-deslop
description: Remove AI-generated code artifacts that obscure intent, hide failure, duplicate logic, or pretend incomplete work is complete. Use when code contains narrative comments, catch-all fallbacks, unsafe casts, hallucinated imports, duplicate helpers, stubs, or oversized generated functions.
license: MIT
metadata:
  category: deslop
  origin: custom-synthesis
  revision: "1.1.0"
---

# Code Deslop

## Trigger

- A prototype is moving toward production.
- Static analysis reports AI-slop patterns.

## Inputs

- Changed code
- Tests and type/lint output
- Repository conventions
- Intended behavior

## Procedure

1. Compile/parse first to expose nonexistent APIs and imports.
2. Remove comments that narrate syntax; keep domain rationale and non-obvious constraints.
3. Replace swallowed exceptions and hidden fallbacks with explicit error policy.
4. Eliminate unsafe casts by fixing types and validation at boundaries.
5. Consolidate duplicated helpers only when semantics truly match.
6. Delete dead code and completed TODO scaffolding; convert remaining work into explicit tracked gaps.
7. Split oversized functions by responsibility, not arbitrary line count.
8. Re-run tests, lints, types, and semantic review.

## Output contract

- Cleaned code
- Resolved finding list
- Explicit remaining debt with owner/context

## Quality gates

- No behavior disappears during cleanup.
- No suppression hides a reachable defect.
- Comments explain why.
- Error behavior is visible to callers and operators.

## Handoffs and dependencies

- `software-development/code-quality-gate`
- `software-development/refactoring`
- `artifact-delint`

## Boundaries

- Do not remove necessary validation or compatibility handling.
- Do not refactor unrelated code.
- Do not convert explicit errors into silent defaults.
