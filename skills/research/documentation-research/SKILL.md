---
name: documentation-research
description: Find and reconcile authoritative product, platform, API, standards, and implementation documentation. Use when a technical answer depends on current official documentation.
license: MIT
metadata:
  category: research
  origin: custom-synthesis
  revision: "1.1.0"
---

# Documentation Research

## Trigger

- Configuration behavior or version support is uncertain.
- Multiple docs pages appear inconsistent.

## Inputs

- Exact product/library and version
- Task or error
- Environment
- Known documentation links

## Procedure

1. Identify the authoritative publisher and versioned documentation set.
2. Search exact error text, API symbols, configuration keys, and release notes.
3. Read prerequisites, defaults, limitations, and examples around the matching passage.
4. Check version history, deprecations, and known issues.
5. Cross-check reference docs with implementation or changelog when behavior is ambiguous.
6. Capture exact URLs/sections and access date.
7. Test examples against the stated version where possible.
8. Summarize what is documented versus inferred.

## Output contract

- Source-backed technical finding
- Version/applicability table
- Relevant excerpts paraphrased with citations
- Open ambiguities

## Quality gates

- Official and version-matched sources dominate.
- No example is generalized beyond its documented scope.
- Deprecated guidance is labeled.
- Inferences are explicit.

## Handoffs and dependencies

- `source-verification`
- `documentation/api-documentation`
- `software-development/debugging`

## Boundaries

- Do not rely on search snippets alone.
- Do not cite community answers as product guarantees.
- Do not copy long copyrighted passages.
