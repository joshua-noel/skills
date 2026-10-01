# OMP planning skills

Clarify with Matt Pocock's planning skills. Develop approved work items with Oh My Pi's built-in coordinator, bundled agents, repository conventions, and Ponytail. Record friction with Papercuts and address it at work-item boundaries. Use Builder.io Visual Edit when requested.

## Install

Requires Python 3, [Oh My Pi](https://github.com/can1357/oh-my-pi), Node/npm for Visual Edit, and [Papercuts](https://github.com/treygoff24/papercuts). Install the tested CLI version once:

```sh
cargo install papercuts --version 0.2.0 --locked
papercuts schema
```

From this checkout:

```sh
python scripts/install_omp.py --dry-run
python scripts/install_omp.py
```

Use `--agent-dir PATH` to target another native OMP agent directory. The default honors `PI_CODING_AGENT_DIR`, then `OMP_PROFILE`/`PI_PROFILE`, then `~/.omp/agent`.

The installer stages the 11 skills, backs up the old native skill catalog and custom native agents outside discovery, installs complete flat skill directories, and merges managed blocks into global `AGENTS.md`/`RULES.md`. It configures the skill allowlist through `omp config`, disables foreign user skill imports, and preserves unrelated settings, including model roles, advisor, tools, and memory. Failed installation restores the previous target files.

Restart OMP after installation. Its main model remains the coordinator; bundled `task`, `scout`, `sonic`, `reviewer`, and `security-reviewer` remain available. No new agents or model assignments are installed. Project instructions and approval rules still apply. Skill filtering also applies to project skills: add an approved extra skill to `skills.includeSkills` when a project genuinely needs one.

The printed backup directory contains the replaced files. To undo, close OMP, move the newly installed `skills` catalog aside, and restore the backed-up `skills`, `agents` (if present), `AGENTS.md`, `RULES.md`, and `config.yml`. If a file did not exist before installation, remove its newly created version instead. Backups, credentials, and runtime logs never belong in this repository.

## Workflow

For a clear request such as "do xyz", OMP works directly with the configured `/models` roles and Ponytail. No spec, ticket, interview, or separate planning approval is required. Use the following planning tools only when the work benefits from them; Papercuts maintenance does not delay the task.

1. Clarify actual unresolved decisions; research facts and prototype when useful.
2. Use Wayfinder for large foggy work, not every small change.
3. Resolve decision tickets, then turn the result into a spec and independently verifiable implementation items with acceptance criteria and dependencies.
4. Ask OMP to implement the ready items normally. Ponytail minimizes the complete solution without dropping requirements or safety.
5. Capture friction immediately. Review it at a safe boundary after five completed implementation tasks or the first active session in a new ISO calendar week.

Invoke skills using OMP's native `/skill:<name>` commands. Read [CATALOG.md](CATALOG.md) for the full set. The upstream text is retained; [omp/AGENTS.md](omp/AGENTS.md) adapts Skill-tool calls and command spellings to OMP without another orchestration pipeline.

## Papercuts maintenance

Capture uses `papercuts add`, not the old Python `PAPERCUTS.md` logger. The default journal is `.papercuts.jsonl` in the current Git repository, or `~/.papercuts/log.jsonl` outside a repository. Use `PAPERCUTS_FILE` for an intentionally private log; do not attach secrets or raw environment dumps.

The coordinator follows [papercuts-maintenance](skills/papercuts-maintenance/SKILL.md): checks persisted state at session start, records each verified work item's stable ID once, reviews open cuts when due, and resolves only exercised causal fixes. State lives in the active OMP agent directory's `papercuts-state/`, per workspace. This is instruction-driven during active sessions, not a timer, daemon, or an autonomous process while OMP is idle.

Small reversible local helper/tooling/doc fixes are automatic within the authorized workspace. Larger fixes become work items; global policy, credentials, permissions, and external actions require approval. Interrupted/failed maintenance remains due.

## Visual Edit

`/skill:visual-edit` uses hosted `https://design.agent-native.com` plus the target local app and local bridge. OMP's headed browser supports page WebMCP, so the hosted MCP connector is not required. Node/npm must be available. The bridge CLI is fetched on demand with `npx @agent-native/core@latest`; version `0.198.7` was checked for this setup.

The skill is installed globally, not into the target app. It does not start a local Design server. Authentication, local-network permissions, sharing, and folder write consent are not preapproved by this installation. Connect a live app only when the user requests it; pull source-edit handoffs, verify the applied changes, then acknowledge their revision.

## Sources

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for pinned commits and MIT notices. The old custom engineering catalog and model-fleet launcher have been retired, not retained as aliases.
