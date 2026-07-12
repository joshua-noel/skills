# Skill catalog

## prompt-decomposer

Breaks an incoming request into atomic, testable work fragments and maps each fragment to capable skills without performing the work.

- [`acceptance-criteria-extractor`](skills/prompt-decomposer/acceptance-criteria-extractor/SKILL.md) — Turn request fragments and constraints into observable, testable completion criteria.
- [`constraint-mapper`](skills/prompt-decomposer/constraint-mapper/SKILL.md) — Extract, normalize, rank, and attach constraints to the exact work fragments they govern.
- [`request-fragmenter`](skills/prompt-decomposer/request-fragmenter/SKILL.md) — Convert a compound prompt into atomic work fragments that can be assigned, verified, and recombined without losing intent.
- [`skill-routing-plan`](skills/prompt-decomposer/skill-routing-plan/SKILL.md) — Map each work fragment to the smallest sufficient set of existing skills and expose routing gaps before execution.

## agent-orchestration

Delegates decomposed work, manages dependencies and concurrency, recovers from failures, and integrates results.

- [`dependency-aware-scheduler`](skills/agent-orchestration/dependency-aware-scheduler/SKILL.md) — Transform routed work into an executable dependency graph with critical path, checkpoints, and safe concurrency.
- [`escalation-and-recovery`](skills/agent-orchestration/escalation-and-recovery/SKILL.md) — Recover from blocked, failed, low-confidence, or contradictory work without losing completed value.
- [`parallel-work-coordinator`](skills/agent-orchestration/parallel-work-coordinator/SKILL.md) — Run independent work streams concurrently while preventing context drift, duplicated effort, and write conflicts.
- [`result-integrator`](skills/agent-orchestration/result-integrator/SKILL.md) — Merge specialist outputs into one coherent deliverable while preserving correctness, traceability, and user intent.
- [`work-delegator`](skills/agent-orchestration/work-delegator/SKILL.md) — Assign each routed fragment to the most capable agent or skill with a bounded brief and explicit return contract.

## software-development

Implements, diagnoses, tests, reviews, refactors, and optimizes software while minimizing unnecessary complexity.

- [`code-quality-gate`](skills/software-development/code-quality-gate/SKILL.md) — Run a deterministic anti-slop quality pass over generated or heavily edited code and convert findings into real fixes.
- [`code-review`](skills/software-development/code-review/SKILL.md) — Review a change against both engineering standards and the intended specification, prioritizing defects over preferences.
- [`debugging`](skills/software-development/debugging/SKILL.md) — Find and fix the causal defect behind a reproducible failure, then prevent recurrence.
- [`dependency-minimizer`](skills/software-development/dependency-minimizer/SKILL.md) — Choose the least costly dependency strategy using existing capabilities before adding new packages or services.
- [`implementation`](skills/software-development/implementation/SKILL.md) — Implement the smallest complete software change that satisfies the specification and fits the existing codebase.
- [`performance-optimization`](skills/software-development/performance-optimization/SKILL.md) — Improve measured latency, throughput, memory, bundle size, or resource efficiency without sacrificing correctness or maintainability.
- [`refactoring`](skills/software-development/refactoring/SKILL.md) — Improve internal structure while preserving externally observable behavior and reducing future change cost.
- [`test-driven-change`](skills/software-development/test-driven-change/SKILL.md) — Use red–green–refactor to deliver behavior in small vertical slices with trustworthy tests.
- [`ponytail-upstream`](skills/software-development/ponytail-upstream/UPSTREAM_STATUS.md) — Exact upstream Ponytail skill suite.

## system-design

Designs understandable, maintainable, scalable, and reliable software systems with explicit trade-offs and contracts.

- [`api-and-contract-design`](skills/system-design/api-and-contract-design/SKILL.md) — Design stable, evolvable service and module contracts with explicit semantics, errors, compatibility, and observability.
- [`architecture-design`](skills/system-design/architecture-design/SKILL.md) — Design a software architecture whose boundaries, responsibilities, data flow, and trade-offs are clear enough to implement and evolve.
- [`architecture-review`](skills/system-design/architecture-review/SKILL.md) — Audit a proposed or existing architecture for clarity, fitness, coupling, failure behavior, and evolutionary cost.
- [`data-modeling`](skills/system-design/data-modeling/SKILL.md) — Design data structures, storage boundaries, lifecycle, integrity, and access patterns for correctness and evolution.
- [`domain-modeling`](skills/system-design/domain-modeling/SKILL.md) — Model domain concepts, language, states, invariants, and boundaries so software reflects the problem rather than accidental storage or UI structure.
- [`scalability-and-reliability`](skills/system-design/scalability-and-reliability/SKILL.md) — Design capacity, resilience, graceful degradation, and recovery around concrete load and failure scenarios.

## research

Plans and executes evidence-driven research across documentation, repositories, standards, and the public web.

- [`documentation-research`](skills/research/documentation-research/SKILL.md) — Find and reconcile authoritative product, platform, API, standards, and implementation documentation.
- [`repository-analysis`](skills/research/repository-analysis/SKILL.md) — Crawl and understand a software repository’s structure, skills, patterns, licenses, and reusable concepts without misattributing copied work.
- [`research-planner`](skills/research/research-planner/SKILL.md) — Turn a question into a bounded evidence plan with subquestions, source strategy, freshness needs, and synthesis criteria.
- [`source-verification`](skills/research/source-verification/SKILL.md) — Verify provenance, authority, recency, scope, and claim support before evidence enters a deliverable.
- [`web-evidence-synthesis`](skills/research/web-evidence-synthesis/SKILL.md) — Collect, compare, and synthesize web evidence into a decision-ready answer with calibrated confidence.

## documentation

Turns verified code, architecture, operations, and research into polished, navigable project documentation.

- [`api-documentation`](skills/documentation/api-documentation/SKILL.md) — Produce accurate, example-rich API documentation that explains semantics, authentication, errors, lifecycle, and compatibility.
- [`architecture-decision-record`](skills/documentation/architecture-decision-record/SKILL.md) — Capture a consequential architecture decision, its context, options, trade-offs, and follow-up in a durable ADR.
- [`design-document`](skills/documentation/design-document/SKILL.md) — Convert a system or feature design into an implementation-ready document with context, decisions, interfaces, risks, and validation.
- [`project-documentation`](skills/documentation/project-documentation/SKILL.md) — Create an elegant, task-oriented documentation set that lets contributors understand, run, use, and maintain a project.
- [`release-notes`](skills/documentation/release-notes/SKILL.md) — Turn verified changes into audience-specific release notes that explain impact, action, compatibility, and risk.
- [`runbook-authoring`](skills/documentation/runbook-authoring/SKILL.md) — Write an executable operational runbook for recurring procedures, alerts, incidents, recovery, and verification.

## security

Performs defensive security review, threat modeling, vulnerability triage, and supply-chain risk analysis.

- [`dependency-cve-audit`](skills/security/dependency-cve-audit/SKILL.md) — Assess direct and transitive dependency vulnerabilities for actual applicability, exploitability, and safe remediation.
- [`secrets-and-supply-chain`](skills/security/secrets-and-supply-chain/SKILL.md) — Audit secrets, build provenance, dependencies, CI identities, artifacts, and release paths against supply-chain compromise.
- [`secure-code-review`](skills/security/secure-code-review/SKILL.md) — Review code and configuration for exploitable trust, data, identity, injection, cryptographic, and failure-handling weaknesses.
- [`social-engineering-review`](skills/security/social-engineering-review/SKILL.md) — Evaluate workflows, messages, identity proofs, and support processes for phishing, impersonation, coercion, and recovery abuse.
- [`threat-modeling`](skills/security/threat-modeling/SKILL.md) — Identify assets, trust boundaries, adversaries, abuse cases, and mitigations early enough to shape the design.
- [`zero-day-triage`](skills/security/zero-day-triage/SKILL.md) — Defensively triage newly disclosed or suspected zero-day risk and coordinate containment without speculative exploitation.

## operations

Bootstraps and connects projects, repositories, environments, CI/CD, releases, deployments, and incident workflows.

- [`ci-cd`](skills/operations/ci-cd/SKILL.md) — Build a least-privilege, reproducible CI/CD pipeline that validates changes and promotes immutable artifacts safely.
- [`deployment-readiness`](skills/operations/deployment-readiness/SKILL.md) — Decide whether a change is safe to deploy by verifying artifact, configuration, migration, observability, security, capacity, and rollback evidence.
- [`environment-setup`](skills/operations/environment-setup/SKILL.md) — Make local, test, and shared environments reproducible, diagnosable, and safe to reset.
- [`incident-operations`](skills/operations/incident-operations/SKILL.md) — Coordinate incident detection, containment, diagnosis, recovery, communication, and learning with clear roles and evidence.
- [`project-bootstrap`](skills/operations/project-bootstrap/SKILL.md) — Create a coherent project skeleton with conventions, tooling, quality gates, documentation, and secure defaults matched to the chosen stack.
- [`release-coordinator`](skills/operations/release-coordinator/SKILL.md) — Tie code, documentation, security, artifacts, approvals, deployment, and communication into one traceable release.
- [`repository-setup`](skills/operations/repository-setup/SKILL.md) — Configure source control, collaboration, ownership, branch protection, templates, and repository automation for safe change.

## interface-and-experience

Creates usable, accessible, expressive interfaces and interactions that must pass the deslop skill gates.

- [`accessibility-review`](skills/interface-and-experience/accessibility-review/SKILL.md) — Audit and remediate an interface for perceivability, operability, understandability, robustness, and inclusive use while retaining deliberate design.
- [`design-system`](skills/interface-and-experience/design-system/SKILL.md) — Create or evolve a design system that encodes product decisions, accessibility, and composable behavior without turning every UI into the same generic template.
- [`interaction-design`](skills/interface-and-experience/interaction-design/SKILL.md) — Design understandable behaviors, state transitions, feedback, and recovery across a user journey, with mandatory deslop review.
- [`interface-design`](skills/interface-and-experience/interface-design/SKILL.md) — Design a visually intentional, responsive interface that makes hierarchy and action obvious while conforming to mandatory deslop gates.
- [`motion-design`](skills/interface-and-experience/motion-design/SKILL.md) — Design purposeful, interruptible, performant motion that communicates causality and spatial change without becoming decorative sludge.
- [`ux-audit`](skills/interface-and-experience/ux-audit/SKILL.md) — Evaluate an end-to-end experience against user goals, comprehension, efficiency, accessibility, trust, and distinctiveness, then prioritize evidence-based improvements.
- [`hallmark-upstream`](skills/interface-and-experience/hallmark-upstream/UPSTREAM_STATUS.md) — Complete exact upstream Hallmark repository snapshot and integrity metadata.

## deslop

Detects and removes generic AI-generated patterns from prose, code, interfaces, visual artifacts, and voice.

- [`artifact-delint`](skills/deslop/artifact-delint/SKILL.md) — Run a final cross-format quality pass that catches mechanical, visual, textual, structural, and packaging residue left by generated work.
- [`code-deslop`](skills/deslop/code-deslop/SKILL.md) — Remove AI-generated code artifacts that obscure intent, hide failure, duplicate logic, or pretend incomplete work is complete.
- [`design-pattern-detector`](skills/deslop/design-pattern-detector/SKILL.md) — Detect repeated AI-default visual, structural, interaction, and copy patterns before they harden into a design.
- [`text-humanizer`](skills/deslop/text-humanizer/SKILL.md) — Rewrite AI-shaped prose into precise, natural, context-aware human writing while preserving verified meaning.
- [`ui-deslop`](skills/deslop/ui-deslop/SKILL.md) — Remove recognizable AI-default interface patterns and replace them with intentional structure, hierarchy, restraint, and product-specific character.
- [`voice-and-tone`](skills/deslop/voice-and-tone/SKILL.md) — Define and enforce a usable voice system grounded in audience, context, and real examples rather than generic brand adjectives.

