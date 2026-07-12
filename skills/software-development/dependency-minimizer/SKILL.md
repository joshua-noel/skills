---
name: dependency-minimizer
description: Choose the least costly dependency strategy using existing capabilities before adding new packages or services. Use when a solution proposes a new library, sdk, framework, service, or tool.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Dependency Minimizer

## Trigger

- Dependency sprawl, bundle size, licensing, or supply-chain exposure is a concern.
- A simple requirement may already be supported natively.

## Inputs

- Required capability
- Runtime/platform version
- Existing dependencies
- License/security/maintenance constraints

## Procedure

1. Apply the ladder in order: do not build, reuse repository code, use standard library, use platform-native feature, use installed dependency, use a small local implementation, then add one focused dependency.
2. Compare capability fit, API surface, transitive dependencies, maintenance, licensing, security history, portability, and removal cost.
3. Reject packages that merely save a few transparent lines while adding long-term risk.
4. Prototype the leading options only where uncertainty is material.
5. Record the decision and upgrade/removal plan.
6. Pin and verify integrity according to ecosystem practice.

## Output contract

- Dependency decision record
- Selected implementation path
- Risk and lifecycle notes

## Quality gates

- A new dependency has a concrete net benefit.
- No duplicate library for an existing capability.
- License compatibility is checked.
- Transitive and install-time behavior is understood.

## Handoffs and dependencies

- `ponytail-upstream/ponytail`
- `security/secrets-and-supply-chain`
- `system-design/architecture-design`

## Boundaries

- Do not equate fewer source lines with simpler systems.
- Do not reimplement mature security primitives.
- Do not choose an abandoned package for superficial convenience.
