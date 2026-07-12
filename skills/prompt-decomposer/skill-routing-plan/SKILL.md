---
name: skill-routing-plan
description: Map each work fragment to the smallest sufficient set of existing skills and expose routing gaps before execution. Use when a decomposed request must be matched to skills.
license: MIT
metadata:
  category: prompt-decomposer
  origin: custom-synthesis
  revision: "1.1.0"
---

# Skill Routing Plan

## Trigger

- Several skills overlap and routing needs a deterministic choice.
- The catalog may lack a required capability.

## Inputs

- Fragment table
- Constraint matrix
- Acceptance criteria
- Available skill catalog and metadata

## Procedure

1. Match primary intent to one owner skill.
2. Add supporting skills only for independent quality, safety, research, deslop, or operational gates.
3. Prefer a deep specialist over a broad category skill.
4. Distinguish sequential dependencies from parallel advisers.
5. Check each skill’s boundaries and required inputs.
6. Flag capability gaps and select a safe generalist fallback without pretending it is a specialist.
7. Emit a routing rationale short enough for an orchestrator to inspect.

## Output contract

- Routing plan: fragment → owner skill → supporting skills → dependencies → expected output
- Gap and conflict report
- Recommended execution waves

## Quality gates

- Every fragment has exactly one accountable owner.
- No circular dependency remains.
- Interface work includes mandatory deslop dependencies.
- Security-sensitive work includes a defensive security review.

## Handoffs and dependencies

- `agent-orchestration/work-delegator`
- `agent-orchestration/dependency-aware-scheduler`

## Boundaries

- Do not execute work.
- Do not route solely by keyword; use requested outcome and skill boundaries.
- Do not create a new skill when an existing one is sufficient.
