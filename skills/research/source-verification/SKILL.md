---
name: source-verification
description: Verify provenance, authority, recency, scope, and claim support before evidence enters a deliverable. Use when a source is load-bearing, surprising, disputed, or current.
license: MIT
metadata:
  category: research
  origin: custom-synthesis
  revision: "1.1.0"
---

# Source Verification

## Trigger

- A repository, document, or webpage may be stale or copied.
- Direct quotes or precise attribution are required.

## Inputs

- Candidate source
- Claim it is meant to support
- Alternative sources
- Required freshness

## Procedure

1. Confirm publisher, author, document identity, and canonical location.
2. Separate publication, revision, effective, and event dates.
3. Read enough context to verify scope and qualifiers.
4. Trace secondary claims to the primary source where possible.
5. Check version, jurisdiction, population, and definitions.
6. Compare against at least one independent source for critical factual claims.
7. Record retractions, supersession, conflicts, and access limitations.
8. Mark the claim verified, partially supported, disputed, or unsupported.

## Output contract

- Verification record per claim
- Canonical citation metadata
- Unsupported or disputed claim list

## Quality gates

- Citation text actually entails the claim.
- Source authority matches the subject.
- No outdated version is treated as current.
- Quote limits and licensing are respected.

## Handoffs and dependencies

- `web-evidence-synthesis`
- `documentation-research`
- `repository-analysis`

## Boundaries

- Do not infer trustworthiness from polished presentation.
- Do not cite a search result page as the evidence.
- Do not remove qualifiers that change meaning.
