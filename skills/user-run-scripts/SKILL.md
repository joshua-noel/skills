---
name: user-run-scripts
description: Writing anything the user will run by hand: an install or migration script, a setup checklist, an admin command, a recovery procedure. Use before handing the user a command, script or manual steps to execute.
---

# Scripts the user runs

The user gets one sitting. If a script fails halfway, that sitting is lost and trust drops. Everything here exists to make the first run the only run.

## Shape

- **One paste.** The user copies one block and runs it. If the work needs elevated rights, tell them once, at the top, and make it a single elevated session. Never split the work across several prompts.
- **Short lines that cannot wrap.** Keep each line under about 80 characters. A wrapped line can split a command in the paste. Break long commands with the shell's own continuation, or put the steps in a script file and run that.
- **Plain output.** Each step prints one line saying what it is doing and one saying it worked. No stack traces on the happy path.
- **No secrets in the script.** Read credentials from where the user keeps them; never print them (principle: no secrets).

## Order

1. **Preflight.** Before changing anything, check everything the script needs: the tool versions, the free disk space, the right directory, the account or permission, that nothing else holds the files, that the processes you plan to stop are the ones you think (check name and command line, not a stored pid), and that pinned versions match.
2. **Snapshot.** Before a risky step, take a snapshot or backup and print where it is and how to restore it. Risky means deleting, overwriting, migrating, or anything you cannot undo with one command.
3. **Change.** Make the changes in small steps. After each step, verify the result, not just the exit code.
4. **Verify.** End with a check that shows the goal was reached, and print a one-line "done".

## Resumable and safe to re-run

- Every step first checks whether it was already done, and skips if so. Run twice, the second run changes nothing.
- Record progress where the script can read it, so a stop at step 4 resumes at step 4, not step 1.
- Never leave a half-applied state as the last action. Do the swap last, as one operation.

## Stops

When the script must stop, it prints **one plain sentence**: what stopped it, and what the user does next. For example: `Stopped: another program is using the data file. Close it and run this again.` No code names, no jargon, no stack dump. Put details in a log file and name the path.

## Rehearse

You do not hand over a script you have not run.

- Run it end to end in a disposable place: a sandbox, a VM, a temporary directory or a dry run mode.
- Run the failure paths too: missing prerequisite, already done, interrupted and resumed.
- Add a `--dry-run` (or equivalent) that prints what would happen without changing anything.
- Say plainly what you could **not** rehearse and why, for example "I could not test the elevated step; it only runs `X`." Put this in the hand-off message, above the script. Do not hide it.

## Hand-off message

1. What the script does, in one sentence.
2. What could go wrong, and how it stops.
3. What was rehearsed and what was not.
4. The paste block.
5. How to undo it.
