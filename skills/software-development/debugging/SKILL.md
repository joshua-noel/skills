---
name: debugging
description: Find and fix the causal defect behind a reproducible failure, then prevent recurrence. Use when a test, build, deployment, integration, or runtime behavior is failing.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Debugging

## Trigger

- Symptoms are intermittent or poorly localized.
- A previous fix treated symptoms rather than cause.

## Inputs

- Exact error and logs
- Reproduction steps
- Relevant code and recent changes
- Runtime/environment details

## Procedure

1. Reproduce the failure or establish the closest observable proxy.
2. Minimize the failing case while preserving the symptom.
3. Separate facts from hypotheses and list competing causes.
4. Instrument the boundaries where state changes; avoid random edits.
5. Use a binary search through data flow, control flow, commits, or configuration.
6. Confirm the root cause by predicting and observing a changed outcome.
7. Apply the narrowest fix at the correct abstraction layer.
8. Add a regression test and run adjacent tests.
9. Remove temporary instrumentation or gate it appropriately.

## Output contract

- Root-cause statement
- Minimal fix
- Regression test
- Reproduction and validation evidence

## Quality gates

- The fix explains all material symptoms.
- A test fails before and passes after the fix where feasible.
- No catch-all fallback hides the defect.
- The root cause is distinguished from the triggering input.

## Handoffs and dependencies

- `implementation`
- `test-driven-change`
- `performance-optimization`
- `operations/incident-operations`

## Boundaries

- Do not guess based only on the final stack-frame line.
- Do not swallow exceptions.
- Do not broaden permissions or disable controls as a fix.
