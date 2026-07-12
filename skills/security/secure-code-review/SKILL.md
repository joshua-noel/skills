---
name: secure-code-review
description: Review code and configuration for exploitable trust, data, identity, injection, cryptographic, and failure-handling weaknesses. Use when security-sensitive code changed.
license: MIT
metadata:
  category: security
  origin: custom-synthesis
  revision: "1.1.0"
---

# Secure Code Review

## Trigger

- A release needs defensive review.
- A vulnerability report points to a code path.

## Inputs

- Diff and surrounding code
- Threat model
- Runtime/framework version
- Tests and configuration

## Procedure

1. Trace untrusted input through parsing, validation, authorization, storage, execution, and output.
2. Check authentication state, object-level and action-level authorization, tenant isolation, and privilege boundaries.
3. Review injection, deserialization, SSRF, file/path, template, command, and prompt/tool execution surfaces.
4. Review secret handling, crypto primitives, randomness, session/cookie/token behavior, and sensitive logging.
5. Check race conditions, replay/idempotency, resource exhaustion, and fail-open behavior.
6. Confirm framework protections are enabled and correctly scoped.
7. Recommend minimal remediations and security regression tests.
8. Redact sensitive proof details in broad reports.

## Output contract

- Ranked security findings
- Exploitability rationale at a safe level
- Remediation and regression-test guidance
- Residual risk

## Quality gates

- Every finding has a concrete trust-boundary path.
- Severity reflects impact and reachability.
- No false assurance from input validation alone.
- Fixes do not merely blacklist examples.

## Handoffs and dependencies

- `threat-modeling`
- `software-development/code-review`
- `dependency-cve-audit`

## Boundaries

- Do not provide operational weaponization, credential theft, persistence, or evasion instructions.
- Do not disclose live secrets.
- Do not recommend custom cryptography.
