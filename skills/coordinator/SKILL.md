---
name: coordinator
description: Running a long session that spawns many agents. Use when you coordinate more than a couple of subagents, work overnight or across restarts, share a machine with heavy jobs, or must stop at a usage limit and resume later.
---

# Coordinator

A coordinator keeps a large piece of work moving without exceeding the machine, the budget or its own memory. The practice is generic. **Numbers and tools that belong to one machine live in the user's local overlay, not here.**

## Machine specifics come from the overlay

Before spawning anything, look for the user's local overlay: extra skills (for example one named `machine-practice`) or text after the house principles at the end of the managed instructions. It holds the real values for the limits below. Use them. If there are none, use the suggested defaults here and tell the user which ones you chose. Never invent machine facts and never write them back into this repository.

| Limit | Suggested default if the overlay is silent | What to do |
| --- | --- | --- |
| Agent cap | 4 running at once | Queue the rest. Every agent is recorded in the ledger. |
| Heavy resource slot | 1 holder | Browser runs, full test suites, builds and big downloads wait for the slot. One holder at a time. |
| Load gate | Normal only | Check machine load first. Start heavy work only when load is normal. If it is high, wait; do not skip the job. |
| Usage limit | Stop at 95% of the plan window | Warn at 85%, stop cleanly at 95%. |
| Agent context | Retire at about 60% | Hand off, then replace the agent. |

## Ledger

Keep one shared record of every agent you start: name, task, start time, status, files it owns, PR or output path. The coordinator reads it before starting a new agent and updates it when one finishes. If the ledger and reality disagree, trust reality, then fix the ledger. Never stop a process because the ledger holds its pid without checking name and command line first.

## Ownership

- Give each agent its own files and its own branch or directory. Two agents never edit one file.
- One integration owner merges. Agents report; they do not merge.
- Spawn only what has work. Do not pad, and do not spawn then idle. Independent slices go out together in one batch.
- Give each agent the full task. Agents start blank; they do not share your conversation.

## Usage limits

Read the usage meter whenever an agent finishes or messages. Then:

- **Below the warning level:** keep going and start the next ready work as slots free.
- **At the warning level (about 85%):** every agent commits locally and writes a progress note after every step (push only where the user has authorized it); start nothing new that cannot finish.
- **At the stop level (about 95%):** every agent writes a progress note and stops cleanly. You write the resume plan. After the window resets, resume from the notes.

## Progress notes

A note lets a new agent, or you after a restart, continue without the old transcript. Each note holds: goal, what is done (with evidence), what is in progress, what is next, the branch or files, and any decision still waiting for the user. Write one at every stop, at every handoff and before any known restart. Keep them in files, not only in chat.

## Restarts

After any restart of the session, the machine or a tool:

1. Re-read the ledger and the latest progress notes.
2. **Re-arm every background watcher** (CI watchers, usage watchers, file watchers, scheduled checks). Watchers do not survive restarts; assume they are gone and check, never assume they are running.
3. Check each running agent's real state from its output, not from what you remember.

## Retiring agents

Watch each long-lived agent's context use. At about 60%, ask it for a progress note, start a fresh agent from that note, and retire the old one. A bloated agent gets slower, more expensive and less accurate.

## Live sources

Before reporting status, read the live source: current CI, current branch head, the current state of the tracker or board. Not your last message about it, and not a cache. Mark anything you could not read `[INFERENCE]`.

## Reporting to the user

Use `skill://user-comms`: done, running, waiting on you, next. Gather every decision that needs sign-off into one document with a recommendation for each, and write it last, after the agents finish, so it is complete.
