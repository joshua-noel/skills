# Codex skills

The current software engineering workflow uses Astra medium as coordinator and Luna max for bounded work.
Its agents, installer, and operating rules live in [joshua-noel/agents](https://github.com/joshua-noel/agents).

`workflow-skills.json` selects 46 skills: the 45-skill workflow library and the updated `start-task` launcher.
The launcher keeps coordination in the main session. Papercut records local friction, with transcript review only on request.
ASD-STE100 improves technical instruction clarity while preserving meaning and literal commands.

Existing matching skills were updated in place. Other specialist skills and vendored source notices remain available.
Use the installer from the agents repository to merge this set into an existing local Codex installation with backups.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution and source limitations.
