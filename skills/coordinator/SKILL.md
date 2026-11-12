---
name: coordinator
description: Running a long session that spawns many agents. Use when you coordinate more than a couple of subagents, work overnight or across restarts, share a machine with heavy jobs, must stop at a usage limit, or report status to the user.
---

# Coordinator

Keep a large piece of work moving without exceeding the machine, the budget or your own memory. This skill is generic. **Numbers that belong to one machine live in the user's own local practice** (for example a local skill named `machine-practice`, kept outside this repository). Use its values; if there is none, use the defaults below and say which you chose. Never write machine facts into this repository.

| Limit | Default | Rule |
| --- | --- | --- |
| Agent cap | 4 running | Queue the rest. Record every agent in one shared ledger (name, task, files, status, output). |
| Heavy slot | 1 holder | Browser runs, full test suites and builds wait for the slot. |
| Load gate | normal only | Start heavy work only when machine load is normal; wait, never skip. |
| Usage | warn 85%, stop 95% | Read the meter whenever an agent finishes. At 85% agents commit locally and write a note after every step (push only if authorized). At 95% everyone writes a note and stops; resume from the notes after the reset. |
| Agent context | retire at ~60% | Get a progress note, start a fresh agent from it, retire the old one. |

- **Progress note:** goal, done (with evidence), in progress, next, branch or files, decisions waiting on the user. Write it at every stop and handoff, in a file.
- **After any restart:** re-read the ledger and notes, re-arm every background watcher (CI, usage, files; they do not survive restarts), and check each agent's real state from its output.
- **Report to the user** in four lines, from live sources: **Done** (with evidence), **Running** (and when it ends), **Waiting on you** (each as a question with a recommendation), **Next**. Use local time; label UTC when quoting logs. Put sign-off decisions in one document, written last.
