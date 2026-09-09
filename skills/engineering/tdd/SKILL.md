---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
license: MIT
metadata:
  category: engineering
  origin: "mattpocock/skills"
  revision: "original-snapshot"
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Prefer stable public seams. A narrower internal seam is acceptable when it detects a real failure that a practical public test cannot observe.

**Test at deliberate public seams.** Before writing each test, name the interface under test in the working notes or plan and choose the highest stable seam that observes the requested behavior. You cannot test everything, so keep the validation surface on critical paths and complex logic instead of every edge case. Proceed within the user's authorized scope; notify the workflow coordinator when a new seam or a newly discovered regression test materially changes the agreed validation surface.

Ask: "What public interface exposes this behavior, and which seam gives the strongest signal?"

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), consult `$codebase-design` for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage, and locality terms, and it is a reference to consult rather than an automatic dispatch.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactor while tests stay green.** Make small behavior-preserving improvements during implementation. Return broader cleanup needs to the coordinator. The code-review skill reports findings and does not perform refactoring.
