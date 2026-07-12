---
name: api-and-contract-design
description: Design stable, evolvable service and module contracts with explicit semantics, errors, compatibility, and observability. Use when services, modules, events, commands, or external consumers need an interface.
license: MIT
metadata:
  category: system-design
  origin: custom-synthesis
  revision: "1.1.0"
---

# Api And Contract Design

## Trigger

- An API must be versioned or migrated.
- Integration ambiguity is causing defects.

## Inputs

- Use cases and consumers
- Domain model
- Security model
- Latency/consistency requirements

## Procedure

1. Start from consumer jobs and domain verbs.
2. Define resources/messages, identifiers, states, and invariants.
3. Specify request/response or event schemas with required, optional, nullable, and default semantics.
4. Design idempotency, pagination, concurrency control, retries, timeouts, and ordering where relevant.
5. Create a stable error taxonomy with machine-readable codes and safe messages.
6. Define authentication, authorization, rate limits, and audit fields.
7. Plan backward-compatible evolution and deprecation.
8. Provide representative examples and contract tests.

## Output contract

- Contract specification
- Error and compatibility policy
- Example interactions
- Contract test plan

## Quality gates

- No ambiguous null/default behavior.
- No transport detail leaks domain internals unnecessarily.
- Retries cannot duplicate non-idempotent work without protection.
- Breaking changes have a migration path.

## Handoffs and dependencies

- `domain-modeling`
- `security/threat-modeling`
- `documentation/api-documentation`
- `software-development/implementation`

## Boundaries

- Do not mirror database tables directly unless that is truly the contract.
- Do not return raw internal exceptions.
- Do not add version numbers without an evolution strategy.
