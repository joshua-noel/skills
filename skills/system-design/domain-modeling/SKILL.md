---
name: domain-modeling
description: Model domain concepts, language, states, invariants, and boundaries so software reflects the problem rather than accidental storage or UI structure. Use when business rules are complex or inconsistent.
license: MIT
metadata:
  category: system-design
  origin: custom-synthesis
  revision: "1.1.0"
---

# Domain Modeling

## Trigger

- Several teams use the same words differently.
- A system has an anemic or overly generic model.

## Inputs

- Domain narratives and examples
- Subject-matter expert language
- Current data/process model
- Known edge cases

## Procedure

1. Collect concrete scenarios, counterexamples, and lifecycle events.
2. Build a glossary and resolve overloaded terms.
3. Identify entities, values, aggregates, policies, commands, events, and invariants only where useful.
4. Define bounded contexts by language and change cadence, not organization chart alone.
5. Model state transitions and invalid transitions explicitly.
6. Test the model against difficult examples and temporal rules.
7. Keep persistence and transport concerns outside the core model where practical.
8. Document unresolved domain questions.

## Output contract

- Ubiquitous-language glossary
- Domain model and state diagrams
- Invariant list
- Context map
- Example-driven model tests

## Quality gates

- The same term has one meaning within a context.
- Invariants have an enforcement owner.
- Invalid states are difficult or impossible to represent.
- The model explains real exceptions, not only happy paths.

## Handoffs and dependencies

- `data-modeling`
- `api-and-contract-design`
- `documentation/design-document`

## Boundaries

- Do not force every noun into a class.
- Do not create abstractions before concrete scenarios.
- Do not treat current database shape as domain truth.
