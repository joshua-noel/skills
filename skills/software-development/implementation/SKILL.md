---
name: implementation
description: Implement the smallest complete software change that satisfies the specification and fits the existing codebase. Use when a validated design or ticket is ready to code.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Implementation

## Trigger

- A missing feature, integration, script, or behavior must be built.
- A prototype must be hardened into maintainable implementation.

## Inputs

- Repository and local conventions
- Acceptance criteria
- Architecture/API contracts
- Test and runtime environment

## Procedure

1. Read the nearest code, tests, configuration, and contributor guidance before editing.
2. Trace the current execution path and identify the narrowest change surface.
3. Apply the Ponytail ladder: avoid building when configuration, existing code, platform primitives, standard libraries, or installed dependencies already solve the need.
4. Implement a vertical slice that is runnable and observable.
5. Handle validation, errors, cleanup, logging, accessibility, and security at the same layer as the change.
6. Add or update tests that prove behavior and regression safety.
7. Run focused checks, then the relevant broader suite.
8. Summarize changed behavior and evidence.

## Output contract

- Production-ready code and tests
- Migration/configuration notes when required
- Executed validation evidence

## Quality gates

- No speculative abstraction.
- No unrelated cleanup mixed into the change.
- Errors are actionable and do not leak secrets.
- Public behavior matches contracts and acceptance criteria.
- The simplest sufficient dependency path was chosen.

## Handoffs and dependencies

- `test-driven-change`
- `code-review`
- `security/secure-code-review`
- `documentation/*`
- `ponytail-upstream/ponytail`

## Boundaries

- Do not bypass tests or validation to make checks pass.
- Do not add a dependency without comparing native and existing options.
- Do not silently change public contracts.
