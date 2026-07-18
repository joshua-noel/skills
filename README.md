# Custom Agent Skills

My personal skills library for Codex CLI — drafted with GPT-5.6 Sol, then reviewed and tightened by Claude Fable 5. Everything my [agent fleet](https://github.com/joshua-noel/agents) knows how to do, it learned from one of these.

The idea is simple: lots of small, single-purpose instruction sets instead of one bloated prompt. An agent loads the two or three skills that match the job, follows them, and moves on. Agents reference skills by name, so the folder layout is just for humans browsing.

## What's in here

Ten categories under `skills/`, sixty-one original skills, and two vendored upstreams I didn't write: [Ponytail](https://github.com/DietrichGebert/ponytail) and [Hallmark](https://github.com/nutlope/hallmark), both snapshotted 12/07/26.

The newest addition is `start-task` — the launcher that wires this library into my agent pipeline. `$start-task <request>` hands a repository change to an orchestrator that clarifies scope one question at a time, plans with tests that each have to survive a devil's-advocate pass, implements, scrubs out AI residue, and runs exactly one merged review-and-repair cycle before asking me to approve the push. Its interrogation step is powered by `system-design/grill-with-docs`, which stress-tests a plan against the existing domain model and writes decisions down (CONTEXT.md, ADRs) as they crystallize.

## Category map

| Category | What it covers |
|---|---|
| `prompt-decomposer` | Breaks an incoming request into atomic, testable work fragments and maps each to capable skills without doing the work itself. |
| `agent-orchestration` | Delegates decomposed work, manages dependencies and concurrency, recovers from failures, and integrates results. |
| `software-development` | Implements, diagnoses, tests, reviews, refactors, and optimizes software while keeping complexity down. |
| `system-design` | Designs understandable, maintainable, scalable systems with explicit trade-offs and contracts. |
| `research` | Plans and runs evidence-driven research across documentation, repositories, standards, and the public web. |
| `documentation` | Turns verified code, architecture, operations, and research into polished, navigable docs. |
| `security` | Defensive security review, threat modeling, vulnerability triage, and supply-chain risk analysis. |
| `operations` | Bootstraps projects, repositories, environments, CI/CD, releases, deployments, and incident workflows. |
| `interface-and-experience` | Usable, accessible, expressive interfaces — every one gated by the deslop skills. |
| `deslop` | Detects and removes generic AI-generated patterns from prose, code, interfaces, artifacts, and voice. |
| `start-task` | The pipeline launcher described above. |

## The interface/deslop contract

Interface skills can't declare success on their own. Anything that produces UI has to call and pass `deslop/ui-deslop`, `deslop/design-pattern-detector`, and `deslop/artifact-delint` — plus `deslop/text-humanizer` whenever interface copy gets written or rewritten. Hallmark is available as a specialist design engine, but it doesn't get to skip the gates either.

## License

Original content is MIT licensed. The vendored upstreams keep their own MIT notices, included beside them.
