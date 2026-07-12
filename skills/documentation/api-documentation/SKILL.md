---
name: api-documentation
description: Produce accurate, example-rich API documentation that explains semantics, authentication, errors, lifecycle, and compatibility. Use when an http/rpc/event/module api needs consumer documentation.
license: MIT
metadata:
  category: documentation
  origin: custom-synthesis
  revision: "1.1.0"
---

# Api Documentation

## Trigger

- A contract changed or generated reference lacks guidance.
- Integration defects result from ambiguous docs.

## Inputs

- Verified API contract
- Authentication model
- Examples/fixtures
- Version and error taxonomy

## Procedure

1. Define audience, base concepts, and first successful call.
2. Document authentication and authorization separately.
3. For each operation, state purpose, preconditions, parameters, schemas, defaults, idempotency, errors, and side effects.
4. Use realistic request/response examples that validate against schemas.
5. Explain pagination, rate limits, retries, webhooks/events, and consistency.
6. Document compatibility, versioning, and deprecation.
7. Add troubleshooting for common integration mistakes.
8. Cross-check generated reference with executable contract tests.

## Output contract

- API guide and reference
- Validated examples
- Error catalog
- Version/deprecation notes

## Quality gates

- Examples contain no real secrets or personal data.
- Schema and prose agree.
- Error recovery is actionable.
- Optional/nullable/default semantics are unambiguous.

## Handoffs and dependencies

- `system-design/api-and-contract-design`
- `security/secure-code-review`
- `deslop/text-humanizer`

## Boundaries

- Do not expose internal stack traces or confidential fields.
- Do not document implementation behavior as a permanent guarantee unless contracted.
- Do not substitute generated schemas for conceptual guidance.
