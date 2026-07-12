---
name: test-driven-change
description: Use red–green–refactor to deliver behavior in small vertical slices with trustworthy tests. Use when behavior is clear enough to specify with examples.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Test Driven Change

## Trigger

- A regression needs a durable guard.
- A risky refactor needs characterization tests.

## Inputs

- Behavioral acceptance criteria
- Existing test conventions
- Public interfaces and fixtures

## Procedure

1. Choose the smallest observable behavior slice.
2. Write a test that fails for the intended reason.
3. Make the minimal production change required to pass.
4. Refactor only while the suite is green.
5. Repeat across normal, boundary, invalid, and integration paths.
6. Prefer tests at the lowest level that proves the contract, with selective end-to-end coverage.
7. Keep tests deterministic, isolated, readable, and representative.
8. Run mutation or negative checks mentally or mechanically to ensure the test can detect the defect.

## Output contract

- Tests and implementation commits/slices
- Coverage of acceptance criteria
- Executed test evidence

## Quality gates

- No test-only production branch.
- Mocks do not replace the behavior under test.
- Assertions verify outcomes, not incidental calls, unless interaction is the contract.
- Flaky timing and network dependencies are controlled.

## Handoffs and dependencies

- `implementation`
- `debugging`
- `refactoring`
- `operations/ci-cd`

## Boundaries

- Do not write tests after the implementation and call it TDD.
- Do not weaken assertions to get green.
- Do not overfit tests to private structure.
