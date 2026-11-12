---
name: eval-driven
description: Test-first method for anything where a model or prompt makes decisions. Use before changing a prompt, model, rule set, classifier, judge or agent behaviour, and when the user asks whether a change "made it better".
---

# Eval-driven development

Software with a model in the loop does not fail the same way twice, so a change that looks better in one example can be worse overall. This skill makes "better" measurable before you change anything.

Credit: the practice follows the LangChain article "What is eval-driven development" (<https://www.langchain.com/blog/what-is-eval-driven-development>) and the verification-first operating model in Meta's engineering post on Forum (<https://engineering.fb.com/2026/10/15/ml-applications/how-meta-built-forum-ai-native-engineering/>). This is an independent summary in our own words; no text is copied. See `THIRD_PARTY_NOTICES.md`.

## Steps, in order

1. **Write the spec as pass/fail.** Say what "good" means as statements that can be checked: what the system must do, what it must not do, and what must keep working. If you cannot phrase it as pass/fail, it is not ready to build.
2. **Build the dataset.** Collect real examples first: past inputs, past failures, edge cases. Add synthetic ones only for gaps, and label them. Keep each example's expected result or a rule for judging it. Aim for tens to hundreds, not thousands.
3. **Hold some back.** Split off a **held-out set** now, before any tuning, and do not look at it while you iterate. It is the only guard against fitting the examples you stared at.
4. **Write the evaluator before the change.**
   - Prefer code checks (exact match, schema, a rule, a test).
   - Use a model as judge only where code cannot decide, and check the judge against human labels on a sample first. An unchecked judge is a guess.
5. **Baseline.** Run the current system through the evaluator and save the per-example results. This is the number every later run is compared against.
6. **Change one thing.** Prompt, model or rule. Not several.
7. **Compare per example, not only the average.** Report which examples went from fail to pass and which went from pass to fail. A higher average with new regressions in important cases is not a win.
8. **Run the held-out set once** at the end. If it disagrees with the working set, you overfit; revert or widen the data.
9. **Keep the evals.** Run them in CI or on a schedule. Every production failure becomes a new example.

## What to report to the user

| Item | Content |
| --- | --- |
| Spec | The pass/fail statements |
| Data | How many examples, where from, how many held out |
| Evaluator | Code or judge; if judge, how it was checked |
| Before / after | Pass counts, plus the list of regressions and fixes |
| Held-out result | One number, run once |
| Limits | What the set does not cover |

## When it is overkill

A deterministic function with ordinary unit tests does not need this. It is for outputs that vary: prompts, models, agents, ranking, classification, automated approvals, anything graded by judgement.

## Related

The same discipline applies to claims about your own tooling: "this setup makes agents build better" needs a with-and-without comparison on the same tasks, not an anecdote. A result from one project is an example, not proof.
