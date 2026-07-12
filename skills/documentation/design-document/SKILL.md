---
name: design-document
description: Convert a system or feature design into an implementation-ready document with context, decisions, interfaces, risks, and validation. Use when a design needs review before implementation.
license: MIT
metadata:
  category: documentation
  origin: custom-synthesis
  revision: "1.1.0"
---

# Design Document

## Trigger

- Research and architecture outputs must be consolidated.
- A multi-step change requires shared technical alignment.

## Inputs

- Problem statement
- Requirements and constraints
- Proposed design
- Alternatives and evidence

## Procedure

1. Open with problem, users, goals, non-goals, and success measures.
2. Describe current state and constraints only as needed to understand the change.
3. Present the proposed architecture, flows, data, interfaces, and failure handling.
4. Explain security, privacy, accessibility, observability, migration, rollout, rollback, and testing.
5. Compare alternatives and trade-offs.
6. List risks, unknowns, experiments, and decisions required.
7. Break implementation into independently verifiable slices.
8. Run terminology and deslop passes.

## Output contract

- Reviewable design document
- Diagrams and contracts
- Risk/unknown register
- Implementation and validation plan

## Quality gates

- A reviewer can challenge assumptions and interfaces.
- Non-goals prevent scope creep.
- Failure paths receive equal treatment to happy paths.
- Implementation slices map to acceptance criteria.

## Handoffs and dependencies

- `system-design/*`
- `research/*`
- `deslop/text-humanizer`
- `operations/release-coordinator`

## Boundaries

- Do not use polished prose to conceal undecided mechanics.
- Do not include decorative diagrams.
- Do not claim future performance without a validation plan.
