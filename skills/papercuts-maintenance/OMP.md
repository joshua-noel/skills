# papercuts-maintenance in OMP

Read this with `SKILL.md`.

- The main OMP session is the coordinator. It uses bundled agents and OMP defaults for repairs; this skill adds no pipeline or model fleet.
- The helper's state directory defaults to `papercuts-state` beneath the active OMP agent directory: `PI_CODING_AGENT_DIR` if set; otherwise `~/.omp/profiles/<profile>/agent` for `OMP_PROFILE` or `PI_PROFILE`; otherwise `~/.omp/agent`. This applies when `PAPERCUTS_STATE_DIR` is not set and an OMP agent directory exists or one of those variables is set.
- The global OMP instructions run `status` at the start of an active session and `complete <stable-id>` after each verified item.
