---
name: environment-setup
description: Make local, test, and shared environments reproducible, diagnosable, and safe to reset. Use when developers or agents cannot reproduce the runtime.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Environment Setup

## Trigger

- Multiple tools/services need coordinated startup.
- Environment drift causes failures.

## Inputs

- Runtime and service dependencies
- OS/container constraints
- Configuration/secrets sources
- Seed data needs

## Procedure

1. Pin supported runtime/tool versions.
2. Choose native, container, devcontainer, or virtualized setup based on project needs.
3. Separate public configuration examples from secret injection.
4. Automate dependency install, service startup, migrations, seed, health checks, and teardown.
5. Use deterministic fixtures and idempotent setup.
6. Provide diagnostics for ports, credentials, versions, and service readiness.
7. Test on a clean environment.
8. Document reset and data-loss boundaries.

## Output contract

- Environment definitions and scripts
- Configuration schema/example
- Health and diagnostic commands
- Clean setup evidence

## Quality gates

- No secret is embedded in images or examples.
- Setup is idempotent.
- Health checks test readiness, not only process existence.
- Reset behavior is explicit.

## Handoffs and dependencies

- `project-bootstrap`
- `ci-cd`
- `documentation/runbook-authoring`

## Boundaries

- Do not claim cross-platform support without testing.
- Do not hide manual steps outside documentation.
- Do not use production data as local seed data.
