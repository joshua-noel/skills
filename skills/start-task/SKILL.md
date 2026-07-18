---
name: start-task
description: Coordinate a repository change through repository-grounded clarification, adversarially-validated planning, user-approved scope, focused implementation, deslop cleanup, one merged review and repair pass, and optional publication. Use when the user invokes $start-task or asks for the structured repository-change launcher.
---

# Start Task

Treat the request following the skill invocation as the task request.

1. Confirm the working directory is a Git repository. Record the task request, branch, HEAD, concise status, and applicable top-level instructions.
2. Spawn the `task_orchestrator` custom agent with that invocation baseline. The coordinator owns repository inspection, prompt validation through `grill-with-docs`, clarification, task sizing, planning, test adversary verdicts, plan review, implementation, deslop cleanup, changelog maintenance, the merged bounded review, Git state, fleet progress tracking, and publication approval.
3. Relay the coordinator's questions, scope confirmation, plan approval, material replan, dirty-worktree commit approval, publication approval, progress, blockers, and final result without changing their meaning.
4. Return each user answer to the same coordinator thread. Do not perform specialist work in the launcher or start another review or repair path.
5. Stop when the coordinator reports completion, unresolved review defects, or a terminal blocker.

The coordinator must inspect before asking questions, then run `grill-with-docs` to validate the request one decision at a time. It must not plan until the user confirms a shared understanding. Resolved domain terminology and significant architectural decisions are recorded lazily in the target repository by `domain-modeling`; no artifact is created when there is nothing to record. The coordinator splits oversized requests with `request-fragmenter` and `acceptance-criteria-extractor` into user-approved independently shippable subtasks and processes each subtask on its own branch and pull request, maintaining a concise ledger of subtask, stage, assigned agent, gate state, and blockers.

Planning assumes proportionate tests for every behavior change. Each plan's test list passes once through `test_adversary`; only tests that demonstrably catch a reachable failure mode or verify an acceptance criterion survive, and uncovered reachable failure paths are added as MISSING. Complex, cross-component, security-sensitive, or operationally risky plans additionally receive one `plan_reviewer` critique. The user approves the corrected plan before any implementation.

Each implementer assignment loads Ponytail in full mode while preserving the approved requirements, surviving tests, and workflow gates. Every completed subtask must add or update the repository-root `CHANGELOG.md` with a concise entry under its existing unreleased section, preserving the repository's established changelog format; create `CHANGELOG.md` with an `Unreleased` section when none exists. After the implementation commit, `deslop_editor` removes mechanical AI residue as at most one refactor-type commit without changing behavior, tests, or interfaces.

Review is one merged initial pass on the cumulative diff — `feature_reviewer` always; `security_auditor` when the change touches authentication, sessions, cryptography, secrets, input parsing at trust boundaries, permissions, payment or personal-data paths, dependencies, or CI; `design_reviewer` when it touches user-facing markup, styles, components, copy, or interaction flows — followed by one cohesive repair pass of all merged confirmed findings and targeted verification of those repairs by each reviewer that raised them. No further automatic review or repair cycles.

Model routing is fixed per agent and documented in `~/.codex/agents/README.md`. When a specialist run fails, the coordinator escalates one variable at a time — reasoning effort one step, then model tier — and never assigns `ultra` to a subagent or `max` without explicit user approval.
