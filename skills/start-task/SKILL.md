---
name: start-task
description: Start a software engineering task in the main Astra coordinator session, with Luna max workers and risk-based review. Use when the user invokes $start-task or requests the structured engineering workflow.
license: MIT
---

# Start task

Treat the text after this invocation as the task request.
Keep the main session as coordinator. Do not spawn a task_orchestrator or another coordinator.
The expected main model is gpt-6-astra with medium reasoning. Instructions cannot change the running model.
If the client reports a different model, tell the user to select Astra Medium before starting this workflow.

Read `workflow/COORDINATOR.md` and `workflow/ROUTING.md` from the installed Codex home.
Resolve Codex home from CODEX_HOME when set, otherwise from `~/.codex`.
Respect applicable project instructions and the user's existing authorization.
Inspect the repository and choose the small, standard, or risky execution path.
Use the configured fleet_* roles for independent bounded assignments.
Return the changed behavior, validation evidence, and any unresolved limitations.
