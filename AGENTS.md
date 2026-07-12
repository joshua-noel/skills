# Agent instructions

## Routing order

1. Use `prompt-decomposer` when a request has multiple deliverables, constraints, or domains.
2. Send the resulting fragment/routing plan to `agent-orchestration` for ownership, dependency ordering, parallel work, recovery, and integration.
3. Route implementation work to the narrowest specialist category.
4. Treat `security` as a cross-cutting defensive gate for sensitive code, identity, data, dependencies, releases, and operations.
5. Treat `deslop` as a mandatory cross-cutting gate for generated prose, code, documentation, and artifacts.
6. Every `interface-and-experience` result must pass `deslop/ui-deslop`, `deslop/design-pattern-detector`, and `deslop/artifact-delint`; add `deslop/text-humanizer` when copy is produced.
7. Use `operations` to create the project/repository/environment and to carry validated outputs through CI, release, deployment, and incident readiness.

## Precedence

Safety and policy > explicit latest user constraints > project constraints > skill defaults. A skill may narrow its scope but may not weaken a higher-precedence constraint.

## Evidence

Never claim that a command, test, audit, or source check passed unless it actually ran or was directly inspected. Preserve provenance for vendored files, citations for research, and exact error evidence for failures.

## Composition

Each fragment has one accountable owner skill. Supporting skills return gates or specialist artifacts to that owner. The orchestrator integrates outputs and validates the end-to-end acceptance criteria.
