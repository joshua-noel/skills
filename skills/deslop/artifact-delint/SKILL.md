---
name: artifact-delint
description: Run a final cross-format quality pass that catches mechanical, visual, textual, structural, and packaging residue left by generated work. Use when a deliverable is ready to ship.
license: MIT
metadata:
  category: deslop
  origin: custom-synthesis
  revision: "1.1.0"
---

# Artifact Delint

## Trigger

- A ZIP, document, UI, code package, or research report was assembled from multiple agents.
- The output may contain placeholders or inconsistent metadata.

## Inputs

- Final artifact tree or render
- Acceptance criteria
- Manifest and licenses
- Format-specific validators

## Procedure

1. Search for TODO, FIXME, lorem ipsum, placeholder domains, dummy metrics, unresolved template tokens, and hidden instructions.
2. Check names, casing, versions, dates, links, paths, headings, and terminology for consistency.
3. Run parsers/linters/validators and inspect rendered output where applicable.
4. Remove temporary files, caches, debug logs, duplicate artifacts, and accidental secrets.
5. Verify manifests, licenses, attribution, source inventory, and archive paths.
6. Check accessibility, responsive behavior, copy humanization, and code quality through delegated gates.
7. Reopen the final packaged artifact and validate its contents.
8. Produce an evidence-based release checklist.

## Output contract

- Delinted artifact
- Validation report
- Known limitations
- Final inventory/hash where useful

## Quality gates

- No placeholder or private data remains.
- The packaged artifact opens and validates.
- Names and versions agree across files.
- Claims of completeness match inventory evidence.

## Handoffs and dependencies

- `text-humanizer`
- `ui-deslop`
- `code-deslop`
- `operations/release-coordinator`

## Boundaries

- Do not remove source licenses or audit evidence.
- Do not mark skipped checks as passed.
- Do not optimize archive size by deleting required documentation.
