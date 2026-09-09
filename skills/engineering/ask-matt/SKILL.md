---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
license: MIT
metadata:
  category: engineering
  origin: "mattpocock/skills"
  revision: "original-snapshot"
---

# Ask Matt

Use this router when you want a path through the workflow rather than a single isolated technique. A **flow** is a sequence of skills that preserves the user's intent from idea to verified result. The workflow coordinator owns dispatch, review scheduling, budget decisions, commits, and publication.

## Main flow: idea to ship

1. Use `$grill-with-docs` in a repository to sharpen the idea while retaining resolved terms in `CONTEXT.md` and durable decisions in ADRs. Without a working directory, use `$grill-me`; both rely on `$grilling`.
2. If a design question needs a runnable answer, use `$handoff` to capture the current context, `$prototype` to build the throwaway logic or UI artifact, then `$handoff` again to bring the decision back. Keep the prototype clearly marked and preserve it only when it is useful as a primary source.
3. For work that spans sessions, use `$to-spec` and then `$to-tickets` to produce independently verifiable tickets with blocking edges. The coordinator dispatches approved tickets and decides context boundaries. For a contained change, use `$implement` in the current task.
4. Use `$tdd` when test-first work or a regression test gives the clearest behavior signal. Use `$code-review` when a branch or pull request needs a bounded standards and specification review. Code review reports findings; the coordinator schedules any repair pass.

## On-ramps

- Use `$triage` for incoming issues or external pull requests that are not yet ready for implementation. Tickets already produced by `$to-tickets` do not need triage.
- Use `$diagnosing-bugs` for intermittent failures, regressions, or bugs that resist a first inspection. It builds a tight feedback loop before forming hypotheses and records a regression test when a sound seam exists.
- Use `$wayfinder` for a large, uncertain effort whose route cannot fit in one session. It maps decisions and fog; the coordinator publishes and dispatches the resulting work.

When wayfinding clears, return through `$to-spec`, `$to-tickets`, and `$implement`. A small effort can go directly to `$implement` once its scope is clear.

## Codebase health

Use `$improve-codebase-architecture` to surface deepening opportunities in recently changed or friction-heavy areas. Use `$codebase-design` to reason about module depth, interfaces, seams, adapters, leverage, and locality. Take a selected improvement through `$grill-with-docs` before implementation.

## Vocabulary and documentation

- `$domain-modeling` sharpens domain terms and records only decisions that meet its ADR threshold.
- `$writing-for-agents` provides the information-hierarchy and completion-criterion discipline for skills, `AGENTS.md`, and pointed-at docs.
- `$architecture-decision-record`, `$design-document`, `$project-documentation`, `$api-documentation`, `$runbook-authoring`, and `$release-notes` produce focused documentation from verified facts.
- `$to-questionnaire` turns a missing stakeholder fact into an asynchronous questionnaire.

## Phase boundaries

At a boundary, choose the smallest context move that preserves the information the next phase needs: continue, use `$handoff` for a new harness or directory, or compact through the host's native context controls. A coordinator-assigned workstream may run separately when it has a bounded brief and return contract; this router does not create nested agents.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) when the choice between continuing, handing off, and compacting is itself unclear.

## Standalone skills

- `$resolving-merge-conflicts` works through an existing merge or rebase conflict by intent and finishes with repository validation.
- `$prototype` answers a hard logic or UI question with a runnable throwaway artifact.
- `$research` gathers primary-source evidence into one cited Markdown file in the repository.
- `$wizard` documents only the manual steps a human must perform, such as credential provisioning or an unfamiliar dashboard. It does not replace agent-executable work.
- `$grilling` runs the interview primitive; `$grill-me` is the stateless wrapper and `$grill-with-docs` is the repository wrapper.
- `$accessibility-review`, `$interaction-design`, and any interface skill should pass the available deslop gates when they produce interface work.
- `$artifact-delint`, `$code-deslop`, `$design-pattern-detector`, `$text-humanizer`, `$ui-deslop`, and `$voice-and-tone` handle the corresponding deslop or editorial gate when relevant.
- `$dependency-cve-audit`, `$secrets-and-supply-chain`, `$secure-code-review`, `$social-engineering-review`, `$threat-modeling`, and `$zero-day-triage` apply only when the relevant security risk or review need exists.

## Precondition

Before the first engineering flow, run `$setup-matt-pocock-skills` to inspect and document the repository's tracker, triage labels, and domain-document layout. It is a maintenance guide for the current Codex repository; it does not install integrations.
