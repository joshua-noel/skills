---
name: code-quality-gate
description: Run a deterministic anti-slop quality pass over generated or heavily edited code and convert findings into real fixes. Use when code was ai-generated or rapidly prototyped.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Code Quality Gate

## Trigger

- A change contains suspicious fallbacks, duplication, TODOs, or oversized functions.
- CI needs a quality threshold.

## Inputs

- Changed files
- Language linters/type checkers/tests
- Project rules
- Optional ais-lop scanner output

## Procedure

1. Run parser/compiler, formatter check, linter, type checker, tests, and project-specific static analysis.
2. Scan for narrative comments, swallowed exceptions, hidden fallbacks, unsafe casts, hallucinated imports, duplicated helpers, dead code, stubs, and oversized functions.
3. Auto-fix only mechanical findings with deterministic tools.
4. Review semantic findings in context and remove the cause rather than suppressing the rule.
5. Re-run all gates after edits.
6. Produce a baseline or threshold only when legacy debt prevents zero findings; do not let new debt pass.
7. Record justified suppressions next to the narrowest scope.

## Output contract

- Cleaned code
- Gate report by tool and severity
- Explicit, minimal suppressions
- CI-ready command set

## Quality gates

- No hidden fallback converts failure into apparent success.
- No unresolved import or unsafe cast is left without reason.
- Generated commentary explains why, not what syntax does.
- New code does not worsen the baseline.

## Handoffs and dependencies

- `deslop/code-deslop`
- `code-review`
- `security/secure-code-review`
- `operations/ci-cd`

## Boundaries

- Do not delete necessary domain comments merely because they are verbose.
- Do not game scores by disabling rules.
- Do not treat static analysis as a substitute for tests.
