---
name: research-planner
description: Turn a question into a bounded evidence plan with subquestions, source strategy, freshness needs, and synthesis criteria. Use when a request requires external facts, current information, comparison, or deep investigation.
license: MIT
metadata:
  category: research
  origin: custom-synthesis
  revision: "1.1.0"
---

# Research Planner

## Trigger

- Research scope is broad or ambiguous.
- Several source types must be combined.

## Inputs

- Research question and intended decision
- Geographic/time scope
- Quality and citation requirements
- Known sources

## Procedure

1. Define the decision the research must support.
2. Break the question into factual, comparative, causal, implementation, and risk subquestions.
3. Set inclusion/exclusion criteria and freshness threshold.
4. Map each subquestion to primary sources first, then high-quality secondary corroboration.
5. Plan search terms, aliases, repositories, standards, and document versions.
6. Define stop conditions: saturation, source agreement, or decision sufficiency.
7. Create an evidence table before synthesis.

## Output contract

- Research plan
- Subquestion/source matrix
- Evidence schema
- Stop and confidence criteria

## Quality gates

- The plan can distinguish absence of evidence from evidence of absence.
- Current claims have a freshness strategy.
- Primary sources carry the most weight.
- The plan is bounded enough to complete.

## Handoffs and dependencies

- `documentation-research`
- `web-evidence-synthesis`
- `source-verification`
- `repository-analysis`

## Boundaries

- Do not search broadly without a decision question.
- Do not predetermine the conclusion.
- Do not use citation count as a proxy for source quality.
