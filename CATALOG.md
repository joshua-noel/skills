# Skill catalog

The active catalog is exactly the 20 entries in `workflow-skills.json`. OMP discovers them as `skills/<name>/SKILL.md`; nested category catalogs are not installed. Skills from a [local overlay](README.md#local-overlay) are added on top at install time and are not listed here.

| Group | Skill | Role |
| --- | --- | --- |
| Clarify | [grilling](skills/grilling/SKILL.md) | Resolve human decisions in frontier rounds; look up facts rather than asking the user. |
| Clarify | [domain-modeling](skills/domain-modeling/SKILL.md) | Sharpen domain language, maintain `GLOSSARY.md`, and record consequential ADRs. |
| Clarify | [research](skills/research/SKILL.md) | Gather primary-source facts for a bounded question. |
| Plan | [prototype](skills/prototype/SKILL.md) | Build a runnable throwaway logic/state demo or UI variants to answer a design question. |
| Plan | [wayfinder](skills/wayfinder/SKILL.md) | Map large uncertain work as decision tickets; includes conditional [project setup](skills/wayfinder/setup/README.md). Planning by default. |
| Plan | [to-spec](skills/to-spec/SKILL.md) | Synthesize agreed scope into a specification. |
| Plan | [to-tickets](skills/to-tickets/SKILL.md) | Turn agreed scope into end-to-end implementation items with acceptance criteria and blocking edges. |
| Build | [ponytail](skills/ponytail/SKILL.md) | Minimize complete production changes; preserve correctness, security, accessibility, and requested behavior. |
| Build | [visual-edit](skills/visual-edit/SKILL.md) | Inspect and edit an authorized running local app in Builder.io's hosted Design surface. |
| Build | [eval-driven](skills/eval-driven/SKILL.md) | Test-first method for prompts, models and agents: pass/fail spec, dataset, evaluator before the change, per-example comparison, held-out set. |
| Review | [review-gates](skills/review-gates/SKILL.md) | Fresh security reviews, review file format, narrow re-checks, never merge on red or an unreviewed head, stopping rules. |
| Review | [goldfish-review](skills/goldfish-review/SKILL.md) | Fresh-context review of a spec, audit, design or plan. |
| Review | [demo-bar](skills/demo-bar/SKILL.md) | Quality bar for UI demos and mocks before the user sees them. |
| Communicate | [user-comms](skills/user-comms/SKILL.md) | Plain words, one question at a time with a recommendation, tables, status formats, UX first. |
| Communicate | [user-run-scripts](skills/user-run-scripts/SKILL.md) | Scripts and checklists the user runs by hand: one paste, preflight, resumable, rehearsed. |
| Communicate | [ste-writing](skills/ste-writing/SKILL.md) | Write or rewrite text at about 80% of ASD-STE100 Simplified Technical English. |
| Visualize | [visualize-diagram](skills/visualize-diagram/SKILL.md) | Draw a codebase, function, domain or architecture as one interactive SVG from a JSON spec. Dark by default. |
| Visualize | [visualize-webpage](skills/visualize-webpage/SKILL.md) | Explain the same subjects as one self-contained interactive HTML page with the diagram and a step-through. |
| Maintain | [coordinator](skills/coordinator/SKILL.md) | Run long, many-agent sessions: caps, resource slots, usage stops, restarts, progress notes. Machine specifics come from the local overlay. |
| Maintain | [papercuts-maintenance](skills/papercuts-maintenance/SKILL.md) | Review recorded friction on a persisted session-driven cadence and verify fixes. |

Development is OMP's default behavior, not another skill pipeline. The main session coordinates bundled workers. No custom orchestrator, model-specific fleet, mandatory TDD skill, deslop chain, or compatibility launcher is installed.

## Not vendored: `diagram-design`

[`diagram-design`](https://github.com/cathrynlavery/diagram-design) (MIT, Cathryn Lavery) draws 44 kinds of branded editorial diagrams and charts. It is a different job from `visualize-diagram`, which explains code as an interactive map. It is 5 MB with 200+ example files and its own style setup, so this repository does not copy it. Install it from upstream and add it through the [local overlay](README.md#local-overlay) if you want both.

## Included resources

- Domain glossary/ADR formats.
- Prototype logic/UI instructions.
- Tracker/domain setup templates.
- Upstream invocation metadata (`agents/openai.yaml`); these are not OMP task-agent definitions.
- Papercuts maintenance helper.
- Diagram renderer (`visualize-diagram/scripts/render.mjs`), page template and SVG inliner (`visualize-webpage/assets/page.html`, `scripts/inline.mjs`). Node only, no dependencies.
- Source licenses retained under `licenses/`.

The global instruction templates in `omp/` bridge upstream invocation wording to OMP, hold the house principles, and govern the planning-to-development handoff and safety precedence.
