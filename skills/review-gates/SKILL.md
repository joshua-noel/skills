---
name: review-gates
description: Rules for reviewing and merging risky changes. Use when a change touches auth, personal data, deletion or migration, money, admin scripts or credentials; before merging any pull request; when starting or ending a review loop; or when asked for a security review.
---

# Review gates

A gate is a check that must pass before work moves on. The aim is that what ships is exactly what was reviewed.

## When a change needs a security review

Any change that touches one of these:

- authentication, authorization, sessions
- personal or sensitive data
- deleting or migrating data
- money, payments, entitlements
- admin scripts, credentials, secrets handling
- anything that runs with elevated rights or accepts untrusted input

Everything else follows the project's normal review.

## Rules

1. **Fresh reviewer.** The reviewer is a new agent that did not write or fix the code and has none of the author's history. Give it the diff, the goal, and the threat surface, not your conclusions.
2. **Review the exact head.** Record the commit SHA you reviewed. If anyone pushes, rebases or squashes afterwards, the review no longer covers the head.
3. **Never merge on red.** Required checks must be green on the head you are merging, read from the live source, not from memory.
4. **Never merge an unreviewed head.** Merge only when the head SHA equals the reviewed SHA. A new commit needs a narrow re-check (below).
5. **Merge only when authorized.** Authorization is the user's OK, or a standing authorization they gave that covers this change. A passing review is not authorization.
6. **Post the review** on the pull request, so it outlives the session.
7. **Do not fix your own findings silently.** Fixes are new commits, and they get re-checked.

## Review file format

Write the review as one file or pull request comment. Keep this shape so reviews are comparable and scannable:

```
Review of <pull request or change>
Head reviewed: <full SHA>
Scope: <files or areas read> / <what was not read>
Verdict: APPROVE | CHANGES REQUESTED | BLOCKED

Findings
- [severity] <one-line title>
  Where: <file:line>
  Why it matters: <the harm, in one sentence>
  Evidence: <command, input or code path that shows it>
  Fix: <smallest change that closes it>

Checked and fine
- <the things you looked at that were correct, so the author does not re-check them>

Not checked
- <anything out of scope or not possible to check>
```

Severities: `blocker` (must fix before merge), `major` (fix before merge unless the user accepts the risk), `minor` (may follow later). Every finding needs evidence; a worry without evidence is a question, not a finding.

## Narrow re-checks

After fixes, do not repeat the full review. Give the reviewer the new commits only, plus the list of earlier findings. The reviewer answers, per finding: closed, open, or made worse; then looks at the new diff for fresh problems. Record the new head SHA.

Go back to a full review only if the fix changed the design, the trust boundary or more than the finding's area.

## Stopping rules

Set these before the first round, write them down, and keep to them:

- A **round limit**: usually two rounds after the first review for a normal change, three for a high-risk one.
- A **convergence rule**: stop when a round produces no blocker or major finding.
- A **non-convergence rule**: if round limit is reached with blockers open, stop and take the problem to the user with a recommendation. Do not start another round to "be sure".
- Findings that repeat the same point in new words are a sign to stop, not to continue.

## Audits and plans

Reviews of specs, audits and multi-session plans use `skill://goldfish-review`. Do the same before approval, with the same stop rules.
