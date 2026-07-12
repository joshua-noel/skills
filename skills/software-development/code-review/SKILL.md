---
name: code-review
description: Review a change against both engineering standards and the intended specification, prioritizing defects over preferences. Use when a patch, pull request, or generated implementation needs review.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Code Review

## Trigger

- A change is high-risk or touches public contracts.
- A user asks for correctness, maintainability, performance, or security feedback.

## Inputs

- Diff and surrounding code
- Specification/acceptance criteria
- Tests and CI results
- Repository standards

## Procedure

1. Understand the requested behavior before judging the diff.
2. Review on two axes: conformance to specification and conformance to engineering standards.
3. Trace changed inputs through outputs, failure paths, cleanup, and concurrency.
4. Look for missing behavior, regressions, hidden fallbacks, unsafe defaults, and compatibility breaks.
5. Validate tests can fail meaningfully and cover the risky paths.
6. Rank findings by user impact and confidence.
7. Give file/line evidence and a concrete fix direction.
8. Separate blocking findings from non-blocking suggestions.

## Output contract

- Ranked findings with severity, evidence, impact, and remediation
- Test gaps
- Residual risk and approval recommendation

## Quality gates

- No praise padding before critical findings.
- No style-only blocker unless a stated standard requires it.
- Every finding is actionable and tied to changed or affected code.
- Absence of findings is not claimed as proof of correctness.

## Handoffs and dependencies

- `security/secure-code-review`
- `performance-optimization`
- `code-quality-gate`
- `ponytail-upstream/ponytail-review`

## Boundaries

- Do not rewrite the whole solution during review.
- Do not flag hypothetical issues without a plausible execution path.
- Do not expose secrets found in code.
