---
name: goldfish-review
description: Fresh-context review of a spec, audit, design or multi-session plan. Use before approving any such document, when a long session may have anchored your own view, or when the user asks for a "fresh eyes", "goldfish" or "cold read" review.
---

# Goldfish review

Credit: the idea comes from the Elephant-Goldfish Model (EGM) by Google, <https://github.com/google/elephant-goldfish-model>, Apache-2.0. EGM pairs an "elephant" that remembers the whole project with "goldfish" reviewers that see only the document. This skill is a short, independent description of that practice for OMP; it uses none of EGM's text or code. See `THIRD_PARTY_NOTICES.md`.

## Why

An author, or any agent with a long history, reads what it meant, not what the page says. A reviewer that starts with nothing can only use the page. Whatever is unclear to it is unclear to the next reader, and whatever the page leaves out is missing for real.

## When

Use it before approving:

- a spec or design
- an audit or investigation report
- a multi-session plan or handoff
- a document someone else will act on without you

Do not use it for code review of a risky change. That is `skill://review-gates`.

## How

1. **Prepare the input.** Name the document and, if it makes claims about code or data, the paths needed to check them. Add nothing else: no conversation, no summary, no "what I meant".
2. **Spawn a fresh agent.** Use a `reviewer` (or `scout` for read-only checking). It must not have been part of the work. If you cannot create a fresh context, say so; do not simulate one by role-playing.
3. **Give a short brief.** Tell it the document type, who will act on it, and the questions below. Do not tell it your opinion of the document.
4. **Ask for findings, not rewrites.** Each finding quotes the line it concerns, says what is wrong, and says what would fix it.
5. **Read the findings yourself.** Fix the ones that are right. Reject the ones that are wrong, with a reason. Do not accept a finding because it is confident.
6. **Re-check narrowly.** Send the reviewer only the changed parts and its own findings. Do not restart from zero.
7. **Report to the user:** the document, the number of findings by severity, what you changed, and what you rejected and why.

## Questions to put to the reviewer

- **Clarity.** Could someone with no context act on this? Which terms, steps or references are not defined?
- **Consistency.** Do any two parts contradict each other? Do names, numbers and dates match throughout?
- **Evidence.** Which claims have no source, no command or no file behind them? Which are labelled as guesses and which should be?
- **Fit with reality.** For each named file, command, API or number: is it true now?
- **Gaps.** What decision, risk, owner or failure mode is missing?
- **Scope.** Is anything in the document that was not asked for, or anything asked for that is missing?
- **Safety.** Does it contain secrets, private data or instructions that would be dangerous to follow?

## Stopping

Set the limit first (principle: review loops need a stop). The default is one review, one narrow re-check, then stop. If blocker-level findings remain after that, take them to the user. A goldfish review does not replace tests, a security review or the user's judgement.
