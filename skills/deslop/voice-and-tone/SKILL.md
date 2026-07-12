---
name: voice-and-tone
description: Define and enforce a usable voice system grounded in audience, context, and real examples rather than generic brand adjectives. Use when a project needs consistent product, documentation, support, or marketing voice.
license: MIT
metadata:
  category: deslop
  origin: custom-synthesis
  revision: "1.1.0"
---

# Voice And Tone

## Trigger

- Several writers or agents produce inconsistent copy.
- A “friendly/professional” brief is too vague to guide decisions.

## Inputs

- Audience and context
- Existing high-quality samples
- Brand/product values
- Content types and risk levels

## Procedure

1. Collect representative “sounds right” and “sounds wrong” samples.
2. Describe voice through observable continua: directness, warmth, technicality, confidence, humor, sentence length, and vocabulary.
3. Define stable voice traits separately from context-dependent tone.
4. Create do/don’t examples for key surfaces such as UI, errors, docs, support, and incidents.
5. Specify terminology, contractions, punctuation, capitalization, and inclusivity rules only where they matter.
6. Test the system on difficult messages: error, delay, denial, security warning, and success.
7. Use text-humanizer to apply the system without robotic consistency.

## Output contract

- Voice and tone guide
- Surface-specific examples
- Terminology and editorial rules
- Review checklist

## Quality gates

- Guidance is behavioral, not a list of adjectives.
- Examples cover high-stakes and negative contexts.
- Voice does not obscure accountability.
- Consistency leaves room for natural cadence.

## Handoffs and dependencies

- `text-humanizer`
- `interface-and-experience/interaction-design`
- `documentation/project-documentation`

## Boundaries

- Do not invent a brand personality unsupported by context.
- Do not use humor in safety, security, or loss situations without explicit fit.
- Do not turn the guide into a restrictive grammar manual.
