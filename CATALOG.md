# Skill catalog

The active catalog is exactly the 13 entries in `workflow-skills.json`. OMP discovers them as `skills/<name>/SKILL.md`; nested category catalogs are not installed.

| Skill | Role |
| --- | --- |
| [grilling](skills/grilling/SKILL.md) | Resolve human decisions in frontier rounds; look up facts rather than asking the user. |
| [domain-modeling](skills/domain-modeling/SKILL.md) | Sharpen domain language, maintain `GLOSSARY.md`, and record consequential ADRs. |
| [research](skills/research/SKILL.md) | Gather primary-source facts for a bounded question. |
| [prototype](skills/prototype/SKILL.md) | Build a runnable throwaway logic/state demo or UI variants to answer a design question. |
| [wayfinder](skills/wayfinder/SKILL.md) | Map large uncertain work as decision tickets; includes conditional [project setup](skills/wayfinder/setup/README.md). Planning by default. |
| [to-spec](skills/to-spec/SKILL.md) | Synthesize agreed scope into a specification. |
| [to-tickets](skills/to-tickets/SKILL.md) | Turn agreed scope into end-to-end implementation items with acceptance criteria and blocking edges. |
| [ponytail](skills/ponytail/SKILL.md) | Minimize complete production changes; preserve correctness, security, accessibility, and requested behavior. |
| [visual-edit](skills/visual-edit/SKILL.md) | Inspect and edit an authorized running local app in Builder.io's hosted Design surface. |
| [papercuts-maintenance](skills/papercuts-maintenance/SKILL.md) | Review recorded friction on a persisted session-driven cadence and verify fixes. |
| [ste-writing](skills/ste-writing/SKILL.md) | Write or rewrite text at about 80% of ASD-STE100 Simplified Technical English. |
| [visualize-diagram](skills/visualize-diagram/SKILL.md) | Draw a codebase, function, domain or architecture as one interactive SVG from a JSON spec. Dark by default. |
| [visualize-webpage](skills/visualize-webpage/SKILL.md) | Explain the same subjects as one self-contained interactive HTML page with the diagram and a step-through. |

Development is OMP's default behavior, not another skill pipeline. The main session coordinates bundled workers. No custom orchestrator, model-specific fleet, mandatory TDD skill, deslop chain, or compatibility launcher is installed.

## Included resources

- Domain glossary/ADR formats.
- Prototype logic/UI instructions.
- Tracker/domain setup templates.
- Upstream invocation metadata (`agents/openai.yaml`); these are not OMP task-agent definitions.
- Papercuts maintenance helper.
- Diagram renderer (`visualize-diagram/scripts/render.mjs`), page template and SVG inliner (`visualize-webpage/assets/page.html`, `scripts/inline.mjs`). Node only, no dependencies.
- Source licenses retained under `licenses/`.

The global instruction templates in `omp/` bridge upstream invocation wording to OMP and govern the planning-to-development handoff and safety precedence.
