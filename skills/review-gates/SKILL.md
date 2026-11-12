---
name: review-gates
description: Rules for reviewing and merging. Use when a change touches auth, personal data, deletion or migration, money, admin scripts or credentials; before merging any pull request; when starting a review loop; or before approving a spec, audit, design or multi-session plan.
---

# Review gates

A gate is a check that must pass before work moves on. The aim: what ships is exactly what was reviewed.

## Code: when a change needs a security review

Any change touching authentication or authorization, personal data, deleting or migrating data, money, admin scripts, credentials, elevated rights, or untrusted input. Other changes follow the project's normal review.

1. **Fresh reviewer.** A new agent that did not write or fix the code. Give it the diff, the goal and the threat surface, not your conclusions.
2. **Review the exact head.** Record the reviewed SHA. A later push, rebase or squash means the review no longer covers the head.
3. **Never merge on red,** and never merge an unreviewed head: required checks are green and the head SHA equals the reviewed SHA, both read from the live source.
4. **Merge only when authorized:** the user's OK or a standing authorization that covers this change. A passing review is not authorization.
5. **Post the review** on the pull request. Each finding has a severity (`blocker`, `major`, `minor`), the file and line, the harm, the evidence, and the smallest fix. A worry without evidence is a question, not a finding.
6. **Fixes are new commits** and get re-checked. Never fix your own findings silently.
7. **Narrow re-check.** Give the reviewer only the new commits and its earlier findings. It answers per finding: closed, open or worse, then scans the new diff. Go back to a full review only if the fix changed the design or the trust boundary.
8. If the change adds a dependency or copies third-party text, check its licence first.

## Documents: fresh-eyes ("goldfish") review

Before approving a spec, audit, design or multi-session plan, have an agent with no history read only the document and the paths it cites. Long context anchors the author; a cold reader finds what the page does not say. (Idea credit: see `THIRD_PARTY_NOTICES.md`.)

1. Spawn a fresh `reviewer`. If you cannot create a fresh context, say so; do not role-play one.
2. Give it the document type, who will act on it, and these questions. Do not give it your opinion.
   - **Clarity:** could someone with no context act on this? Which terms or steps are undefined?
   - **Consistency:** do any parts, names or numbers contradict each other?
   - **Evidence:** which claims have no source? Is the design judged against the stated problem and outside evidence, with the author's own past projects as examples only?
   - **Reality:** is each named file, command, number and API true now?
   - **Gaps and scope:** what decision, risk or owner is missing? What was not asked for?
   - **Safety:** any secrets, private data or dangerous instructions?
3. Ask for findings that quote the line, say what is wrong and what fixes it, not rewrites. Fix the right ones, reject the wrong ones with a reason; confidence is not evidence.
4. Re-check narrowly, as in code review.

## Stopping rules

Set these before round one and write them down.

- A round limit: normally the first review plus two re-checks; high-risk changes may take three.
- Stop when a round finds no blocker or major finding.
- If the limit is reached with blockers open, take the problem to the user with a recommendation. Do not start another round "to be sure". Findings that repeat in new words mean stop.

A review does not replace tests or the user's judgement.
