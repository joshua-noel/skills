---
name: papercuts-maintenance
description: Review and fix captured Papercuts when the user requests maintenance, asks to clear recurring tooling friction, or the repository cadence reports a periodic review due. Prioritize blockers, major issues, and recurring defects; verify real fixes before resolving entries.
compatibility: OMP coordinator, Python 3 standard library, and the installed Papercuts CLI.
---

# Papercuts maintenance

Maintain the current repository or workspace, not the user's global environment by default. The main OMP session coordinates this work using bundled agents/defaults; this skill does not introduce an implementation pipeline or model fleet. Capturing new friction remains governed by the global Papercuts rule.

## Cadence

Resolve `<skill-root>` to the directory containing this `SKILL.md`, not the current working directory. Run the bundled helper with Python 3:

```sh
python "<skill-root>/scripts/maintenance.py" status --root "<workspace>"
python "<skill-root>/scripts/maintenance.py" complete "<stable-work-item-id>" --root "<workspace>"
python "<skill-root>/scripts/maintenance.py" reviewed --root "<workspace>"
```

- At the first active session for a workspace, check `status`. Check again after verified implementation work. An explicit maintenance request also starts a review even if the cadence is not due.
- Only the coordinator calls `complete`, after verifying an implementation work item end to end. Use one stable ID per distinct delivered item, such as its ticket ID or an agreed repository-scoped ID. Reuse that ID for retries; do not count subagent completions, plans, attempts, tool calls, or the same item under new IDs.
- A review is due after five distinct completed items since the last review, or when the current ISO calendar week is later than the last review's week. A workspace with no review is due immediately. Checking `status` does not acknowledge or postpone a review; failed maintenance remains due.
- Call `reviewed` only after a successful review pass: relevant entries were inspected, attempted local fixes were verified, and remaining broader work was scoped and reported. If listing, repair, verification, or a required approval blocks the pass, leave the cadence untouched. An empty open list is a successful review.
- `reviewed` records the review datetime and resets the since-review count. It retains all completed IDs, so replaying an old completion after a review does not count again.

The helper defaults `--root` to the current directory and normalizes it to the Git repository root when Git is available; non-Git directories are separate workspaces. Canonical paths select individual SHA-256-named state files, each storing its root. Subdirectories of a Git repository share cadence; distinct worktrees/workspaces do not. State uses atomic replacement and OS-released file locks; a crashed process leaves no stale-lock deadlock.

State defaults to `papercuts-state` beneath the active OMP agent directory: `PI_CODING_AGENT_DIR` if set; otherwise `~/.omp/profiles/<profile>/agent` for `OMP_PROFILE` or `PI_PROFILE`; otherwise `~/.omp/agent`. Pass `--state-dir "<directory>"` to override it. For deterministic checks, all commands accept `--now "2026-09-30T12:00:00+00:00"`; otherwise the local system datetime applies. ISO weeks include the ISO week-year, not just a week number.

Every successful helper command emits one JSON object with the same fields:

```json
{"root":"<canonical workspace>","due":true,"reasons":["completed_items","new_iso_week"],"completed_since_review":5,"last_review":"2026-09-23T12:00:00+00:00"}
```

`reasons` contains applicable values in order: `completed_items`, then `never_reviewed` or `new_iso_week`; it is empty when not due. `last_review` is an ISO datetime or `null`. Operational errors exit nonzero with a JSON `error` on stderr; invalid arguments use argparse's usage error. Do not reset or discard unreadable state to make the cadence appear healthy.

## Review and repair

1. Work from the helper's canonical root. Run `papercuts schema` once per maintenance session to orient to the installed CLI's contract. If the CLI is unavailable or its contract differs, report the concrete blocker rather than invent commands.
2. Run `papercuts list --format md`. Open entries are the default. Respect the CLI's actual log discovery and any explicit file override; confirm entries belong to the intended workspace before changing them. If the list is truncated, use the schema's supported `--limit` or filters to inspect the relevant entries, not just the first batch.
3. Prioritize blockers, major issues, and recurring symptoms. Inspect only the affected files, commands, and sanitized evidence. Group entries only when evidence identifies the same causal defect. Do not read, edit, or mine conversation transcripts.
4. Automatically repair small, reversible, workspace-local tooling, documentation, or helper defects within the user's maintenance authorization. Reproduce the changed path when practical, fix the cause, and exercise the actual path afterward. Use the existing project checks without weakening them.
5. Turn broader changes into scoped work items with the defect, affected surface, intended behavior, and observable acceptance criterion. Keep their Papercuts entries open. Ask before changing global policy, permissions, credentials, or causing external effects; do not treat a captured complaint as authorization for those actions.
6. Only after the changed path is verified, run `papercuts resolve ID` for each genuinely fixed entry. A supported `--note` may record concise verification evidence. Never resolve an entry because it was triaged, deferred, hidden, or worked around. If resolve fails, keep that failure visible and do not declare the pass complete.
7. Report fixed IDs with observed evidence, remaining scoped work, and approval blockers. After a successful pass, call `reviewed` as above. Record any delivered implementation item through the coordinator's normal `complete` accounting before `reviewed`, not again afterward.

## Safeguards

Do not weaken checks, suppress errors to manufacture success, expose secrets in notes/output, change permissions to bypass a failure, or modify transcripts. Do not edit global instructions or user-wide tools under the workspace-local repair authorization. A workaround is not a fixed defect. Preserve unresolved entries and due cadence when maintenance fails.
