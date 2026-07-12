---
name: text-humanizer
description: Rewrite AI-shaped prose into precise, natural, context-aware human writing while preserving verified meaning. Use when text feels generic, inflated, promotional, repetitive, overly symmetrical, or mechanically polished.
license: MIT
metadata:
  category: deslop
  origin: custom-synthesis
  revision: "1.1.0"
---

# Text Humanizer

## Trigger

- A generated document, email, interface, or report needs a human voice.
- The user asks to humanize or remove AI tells.

## Inputs

- Draft text
- Audience and purpose
- Voice samples where available
- Facts and mandatory wording

## Procedure

1. Preserve facts, commitments, citations, and domain terms before editing style.
2. Infer voice from provided samples: sentence length, directness, vocabulary, humor, formality, and punctuation.
3. Remove significance inflation, vague attribution, promotional claims, empty signposting, superficial “-ing” analysis, and canned conclusions.
4. Break rule-of-three rhythms, false contrasts, synonym cycling, and repetitive paragraph templates.
5. Replace evasive copulas, passive or subjectless fragments, and vague abstractions with named actors and actions.
6. Reduce em-dashes, bold clutter, title-case headings, emoji, inline-header lists, and fake quotes where they are tells rather than intentional voice.
7. Vary cadence naturally and allow concise unevenness where appropriate.
8. Run a second pass specifically for remaining AI tells and factual drift.

## Output contract

- Humanized text
- Optional brief note of material factual ambiguities preserved for review

## Quality gates

- No new fact or promise appears.
- The text sounds like one consistent person, not a style checklist.
- Specific nouns and verbs replace inflated abstraction.
- Formatting serves reading rather than decoration.

## Handoffs and dependencies

- `voice-and-tone`
- `artifact-delint`
- `documentation/*`
- `interface-and-experience/*`

## Boundaries

- Do not erase a genuine authorial quirk merely because it is unusual.
- Do not make technical text casual at the cost of precision.
- Do not fabricate personal anecdotes.
