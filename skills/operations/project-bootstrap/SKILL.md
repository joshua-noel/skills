---
name: project-bootstrap
description: Create a coherent project skeleton with conventions, tooling, quality gates, documentation, and secure defaults matched to the chosen stack. Use when a new software project or package is starting.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Project Bootstrap

## Trigger

- A prototype needs production-grade structure.
- A multi-skill workspace must be initialized.

## Inputs

- Project purpose and stack
- Runtime/tool versions
- Deployment target
- Team conventions and license

## Procedure

1. Select the smallest stack that satisfies requirements.
2. Create conventional source, test, docs, scripts, config, and infrastructure boundaries.
3. Add dependency lockfiles and version/tool managers.
4. Configure formatting, linting, type checking, tests, security scanning, and build commands.
5. Create README, contributing, license, environment example, ignore rules, and ownership metadata.
6. Use secure defaults and no real secrets.
7. Add a smoke test and one-command local verification.
8. Validate from a clean checkout.

## Output contract

- Runnable project tree
- Quality/verification commands
- Starter documentation
- Bootstrap validation report

## Quality gates

- Clean checkout reaches first success.
- No generated secrets or machine-specific paths.
- Tool versions are reproducible.
- The skeleton contains no speculative layers.

## Handoffs and dependencies

- `repository-setup`
- `environment-setup`
- `ci-cd`
- `software-development/dependency-minimizer`

## Boundaries

- Do not scaffold features not requested.
- Do not choose a framework solely for popularity.
- Do not commit credentials.
