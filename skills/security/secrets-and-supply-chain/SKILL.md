---
name: secrets-and-supply-chain
description: Audit secrets, build provenance, dependencies, CI identities, artifacts, and release paths against supply-chain compromise. Use when a repository or pipeline is being set up or reviewed.
license: MIT
metadata:
  category: security
  origin: custom-synthesis
  revision: "1.1.0"
---

# Secrets And Supply Chain

## Trigger

- Credentials may be embedded or overprivileged.
- Third-party actions/packages/build artifacts enter production.

## Inputs

- Repository and history scan
- CI/CD configuration
- Dependency manifests
- Artifact registry and identity model

## Procedure

1. Scan current files and reachable history for credentials and sensitive endpoints; redact findings.
2. Inventory build and deploy identities, permissions, trust policies, and token lifetimes.
3. Pin third-party actions/images/dependencies by immutable references where supported.
4. Verify checksums/signatures, provenance, SBOM, and artifact promotion path.
5. Separate build from release authority and use environment protections.
6. Review install scripts, generators, and untrusted pull-request execution.
7. Rotate exposed credentials and investigate use rather than only deleting them.
8. Add preventive scanning and branch/release controls.

## Output contract

- Supply-chain findings
- Credential response actions
- Hardening plan
- CI policy and verification evidence

## Quality gates

- No secret value appears in the report.
- Least privilege is concrete per identity.
- Production artifacts are traceable to reviewed source.
- Untrusted code cannot access protected secrets.

## Handoffs and dependencies

- `operations/repository-setup`
- `operations/ci-cd`
- `dependency-cve-audit`

## Boundaries

- Do not test stolen credentials.
- Do not rotate without preserving service continuity and audit evidence.
- Do not trust tags that can be moved.
