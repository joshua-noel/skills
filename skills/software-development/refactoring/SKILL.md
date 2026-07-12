---
name: refactoring
description: Improve internal structure while preserving externally observable behavior and reducing future change cost. Use when code is difficult to understand, test, or extend.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Refactoring

## Trigger

- Duplication or coupling causes repeated defects.
- A feature requires preparatory restructuring.

## Inputs

- Characterization tests
- Change history and pain points
- Architecture boundaries
- Static analysis findings

## Procedure

1. State the maintainability problem and desired structural property.
2. Characterize current behavior before moving logic.
3. Choose a sequence of reversible, behavior-preserving transformations.
4. Move toward deep modules, explicit contracts, cohesive naming, and one source of truth.
5. Remove obsolete helpers only after all callers are migrated.
6. Keep semantic changes in separate commits or patches.
7. Run focused tests after each structural step and broader tests at the end.
8. Measure complexity only as supporting evidence, not the goal.

## Output contract

- Refactored code
- Behavior-preservation evidence
- Updated architecture notes where boundaries changed

## Quality gates

- Public behavior is unchanged unless separately specified.
- Abstraction reduces cognitive load rather than relocating it.
- No duplicate compatibility paths remain accidentally.
- Tests describe behavior, not old structure.

## Handoffs and dependencies

- `implementation`
- `test-driven-change`
- `codebase architecture review`
- `code-quality-gate`

## Boundaries

- Do not create generic utility layers without multiple concrete uses.
- Do not mix mass formatting with logic moves.
- Do not preserve dead code “just in case.”
