<!-- omp-workflow:start -->
## Papercuts

When you hit friction during work — a dead-end tool call, a broken link, a
misleading doc, a footgun config, a missing helper — file it before moving on:

    papercuts add "<what you hit and what would have prevented it>" --tag <area>

Don't stop working; file it and push through. Severity: minor (default) for
annoyances, major for time sinks, blocker for hard walls. Run `papercuts schema`
once if you need the full contract. Attach `--cmd`, `--exit`, or `--stderr-file`
when filing tool failures; never feed raw environment dumps.

Capture and remediation are separate: do not derail the current task for a
routine environment improvement. The main coordinator checks periodic
maintenance at session start and after verified work-item completion. Preserve
safety checks and accepted scope when addressing friction; use Ponytail for
small complete fixes, not for suppressing errors or weakening verification.

Papercuts uses the current repository's `.papercuts.jsonl` by default; outside
a repository it uses the global log. Use `PAPERCUTS_FILE` only when intentionally
selecting a private/global log, and review evidence for secrets before filing.
If logging is unavailable, report the failure and continue; do not claim it was
recorded or substitute a different logging interface silently.
<!-- omp-workflow:end -->
