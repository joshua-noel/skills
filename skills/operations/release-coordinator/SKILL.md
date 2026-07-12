---
name: release-coordinator
description: Tie code, documentation, security, artifacts, approvals, deployment, and communication into one traceable release. Use when a multi-component or customer-facing release must be assembled.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Release Coordinator

## Trigger

- Several teams/skills contribute release evidence.
- Versioning, packaging, and deployment order matter.

## Inputs

- Release scope and version policy
- Merged artifacts
- Readiness/security evidence
- Deployment and communication plan

## Procedure

1. Freeze and verify the release scope.
2. Map each included change to tests, review, documentation, and migration evidence.
3. Resolve version numbers, changelog, licenses, SBOM, signatures, and artifact provenance.
4. Order component releases by compatibility dependencies.
5. Run deployment readiness and obtain required approvals.
6. Tag/sign/publish immutable artifacts and verify registry metadata.
7. Coordinate staged deployment and post-release checks.
8. Publish release notes and record deviations or rollback.

## Output contract

- Release manifest
- Signed/published artifacts
- Approval and deployment record
- Release notes and residual risks

## Quality gates

- Only verified changes enter the release.
- Version and artifact identity agree everywhere.
- License/attribution obligations are present.
- Release state is reproducible from the manifest.

## Handoffs and dependencies

- `deployment-readiness`
- `ci-cd`
- `documentation/release-notes`
- `security/dependency-cve-audit`
- `agent-orchestration/result-integrator`

## Boundaries

- Do not rebuild after final approval without revalidation.
- Do not alter tags/releases invisibly.
- Do not omit known issues to improve optics.
