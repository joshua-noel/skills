---
name: architecture-decision-record
description: Capture a consequential architecture decision, its context, options, trade-offs, and follow-up in a durable ADR. Use when a technical choice has meaningful long-term or cross-team impact.
license: MIT
metadata:
  category: documentation
  origin: custom-synthesis
  revision: "1.1.0"
---

# Architecture Decision Record

## Trigger

- A prior decision needs supersession or clarification.
- Trade-offs must be reviewable later.

## Inputs

- Decision context
- Drivers and constraints
- Options considered
- Evidence and stakeholders

## Procedure

1. Name the decision as an active outcome.
2. State the context and decision drivers without rewriting project history.
3. List viable options and why each was or was not selected.
4. Record the decision, status, date, scope, and owners.
5. Describe positive, negative, and neutral consequences.
6. Include rollout, reversal, monitoring, and review triggers.
7. Link related ADRs and source evidence.
8. Mark supersession explicitly rather than editing history invisibly.

## Output contract

- Numbered ADR in project format
- Decision and consequence summary
- Follow-up actions and review triggers

## Quality gates

- The chosen option follows from stated drivers.
- Rejected options are represented fairly.
- Consequences include operational and migration cost.
- The ADR is concise enough to be read during future change.

## Handoffs and dependencies

- `system-design/architecture-design`
- `operations/release-coordinator`
- `deslop/text-humanizer`

## Boundaries

- Do not use an ADR for trivial implementation details.
- Do not backdate or erase replaced decisions.
- Do not claim consensus that did not exist.
