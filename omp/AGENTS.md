## OMP

The main OMP session is the coordinator. Use OMP's built-in task agents and model routing; add no custom orchestrator, model fleet or mandatory review chain. Do not inspect or reconfigure model roles per task. Project instructions, approvals and safety rules still apply. The coordinator owns dispatch, integration and tracker changes; workers report back to it.

Where an upstream skill says "call the Skill tool", `read` `skill://<name>`; `/skill:<name>` invokes one. Use OMP's task and ask tools. Some skills carry an `OMP.md` with OMP-specific steps: read it together with the skill.

- **Visual editing:** when asked to inspect or edit the running local app in Builder.io Design, read `skill://visual-edit` and `skill://visual-edit/OMP.md`.
- **Papercuts:** at the start of an active session read `skill://papercuts-maintenance` and run its `status`. After each verified implementation item, only the coordinator runs `complete <stable-id>`. Maintenance never delays a clear user task.
