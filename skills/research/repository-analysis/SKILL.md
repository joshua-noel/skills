---
name: repository-analysis
description: Crawl and understand a software repository’s structure, skills, patterns, licenses, and reusable concepts without misattributing copied work. Use when a user references one or more repositories.
license: MIT
metadata:
  category: research
  origin: custom-synthesis
  revision: "1.1.0"
---

# Repository Analysis

## Trigger

- Existing skills or implementation patterns must be extracted.
- A codebase must be mapped before modification.

## Inputs

- Repository URLs or local checkouts
- Target concepts/files
- License and reuse intent
- Relevant branch/tag

## Procedure

1. Verify the canonical repository, branch/tag, release, and license.
2. Inventory top-level structure, manifests, contributor guidance, and entry points.
3. Locate target files using tree and semantic search.
4. Read referenced files transitively until the behavior or skill is self-contained.
5. Distinguish verbatim vendoring, adapted concepts, and original synthesis.
6. Preserve notices and source metadata for copied material.
7. Extract design principles and workflows without copying unnecessary prose.
8. Record missing files, unavailable transport, and version uncertainty.

## Output contract

- Repository map
- Extracted concepts and provenance
- License/reuse matrix
- Vendored/adapted/original inventory

## Quality gates

- Copied files are byte-identical or clearly marked modified.
- Every external source has attribution.
- The selected version is recorded.
- No claim of full vendoring without inventory verification.

## Handoffs and dependencies

- `security/secrets-and-supply-chain`
- `documentation/project-documentation`
- `operations/repository-setup`

## Boundaries

- Do not ingest secrets, generated binaries, or unrelated history.
- Do not strip license headers.
- Do not imply endorsement by upstream authors.
