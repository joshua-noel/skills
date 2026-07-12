---
name: web-evidence-synthesis
description: Collect, compare, and synthesize web evidence into a decision-ready answer with calibrated confidence. Use when a request needs market, policy, ecosystem, company, or current public information.
license: MIT
metadata:
  category: research
  origin: custom-synthesis
  revision: "1.1.0"
---

# Web Evidence Synthesis

## Trigger

- Sources disagree or cover different facets.
- A recommendation needs evidence rather than anecdotes.

## Inputs

- Research plan
- Search results and source text
- Evaluation criteria
- Date/geographic scope

## Procedure

1. Gather diverse, relevant sources with priority to primary and recognized authoritative publishers.
2. Record publication date and event/effective date separately.
3. Extract claims into an evidence table with source, scope, and limitations.
4. Corroborate load-bearing facts and investigate disagreements.
5. Assess incentives, methodology, sample, and recency.
6. Synthesize by subquestion and criterion rather than source-by-source summaries.
7. State confidence and what would change the conclusion.
8. Cite every material web-derived claim.

## Output contract

- Evidence table
- Synthesis with inline citations
- Conflicts and confidence notes
- Decision implications

## Quality gates

- No citation laundering through low-quality summaries.
- Recent claims use current sources.
- Minority or conflicting evidence is represented fairly.
- Recommendations follow from stated criteria.

## Handoffs and dependencies

- `source-verification`
- `documentation/project-documentation`
- `deslop/text-humanizer`

## Boundaries

- Do not fabricate citations or inaccessible evidence.
- Do not present correlation as causation.
- Do not bury uncertainty in footnotes.
