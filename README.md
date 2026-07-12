# Custom Agent Skills

A category-first agent-skill library for decomposing prompts, delegating work, building and operating software, researching evidence, documenting systems, auditing security, designing interfaces, and removing generated slop.

## What is included

- **10 required categories** under `skills/`.
- **59 original skills**, each with triggers, inputs, procedure, output contract, quality gates, handoffs, and boundaries.
- **Ponytail vendored upstream** as its six original skills, unmodified, with its MIT license.
- **Hallmark vendored wholesale** as the complete upstream repository snapshot: skill, all references, documentation, examples, tests, site assets, and MIT license.
- A machine-readable `manifest.json`, source lock, catalog, validators, and upstream sync tooling.

## Recommended entry point

For a compound request:

```text
prompt-decomposer/request-fragmenter
  -> prompt-decomposer/constraint-mapper
  -> prompt-decomposer/acceptance-criteria-extractor
  -> prompt-decomposer/skill-routing-plan
  -> agent-orchestration/work-delegator
  -> specialist skills
  -> agent-orchestration/result-integrator
  -> deslop/artifact-delint
```

A simple, single-domain task can enter directly through its specialist skill.

## Category map

| Category | Responsibility |
|---|---|
| `prompt-decomposer` | Breaks an incoming request into atomic, testable work fragments and maps each fragment to capable skills without performing the work. |
| `agent-orchestration` | Delegates decomposed work, manages dependencies and concurrency, recovers from failures, and integrates results. |
| `software-development` | Implements, diagnoses, tests, reviews, refactors, and optimizes software while minimizing unnecessary complexity. |
| `system-design` | Designs understandable, maintainable, scalable, and reliable software systems with explicit trade-offs and contracts. |
| `research` | Plans and executes evidence-driven research across documentation, repositories, standards, and the public web. |
| `documentation` | Turns verified code, architecture, operations, and research into polished, navigable project documentation. |
| `security` | Performs defensive security review, threat modeling, vulnerability triage, and supply-chain risk analysis. |
| `operations` | Bootstraps and connects projects, repositories, environments, CI/CD, releases, deployments, and incident workflows. |
| `interface-and-experience` | Creates usable, accessible, expressive interfaces and interactions that must pass the deslop skill gates. |
| `deslop` | Detects and removes generic AI-generated patterns from prose, code, interfaces, visual artifacts, and voice. |


## Interface/deslop contract

Interface skills cannot declare success on their own. They must call and pass:

- `deslop/ui-deslop`
- `deslop/design-pattern-detector`
- `deslop/artifact-delint`
- `deslop/text-humanizer` whenever interface copy is generated or rewritten

The vendored Hallmark skill is available as a specialist design engine, but the package-level deslop gates remain mandatory.

## Validation

From the package root:

```bash
python scripts/build_manifest.py
python scripts/validate_skills.py
```

The validator checks category coverage, frontmatter, unique names, required sections, interface/deslop dependencies, vendored Ponytail files, every Hallmark repository file against its recorded SHA-256 digest, and manifest integrity.

## Upstream status and refresh

See `THIRD_PARTY_NOTICES.md`, `sources.lock.json`, and each upstream directory’s `UPSTREAM_STATUS.md`. To refresh upstream files in a network-enabled environment:

```bash
python scripts/sync_upstream.py --all
python scripts/build_manifest.py
python scripts/validate_skills.py
```

## License

Original package content is MIT licensed. Vendored upstream content remains subject to the upstream MIT notices included beside it.
