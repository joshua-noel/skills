---
name: ci-cd
description: Build a least-privilege, reproducible CI/CD pipeline that validates changes and promotes immutable artifacts safely. Use when a project needs automated checks, builds, releases, or deployments.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Ci Cd

## Trigger

- Existing pipelines are slow, flaky, or insecure.
- Multiple environments require promotion.

## Inputs

- Repository workflow
- Build/test commands
- Artifact/deployment targets
- Identity and approval model

## Procedure

1. Define triggers and path filters deliberately.
2. Separate fast feedback, full validation, build, security, release, and deploy stages.
3. Cache only reproducible inputs and key caches by lockfiles/tool versions.
4. Build once and promote the same immutable artifact.
5. Use workload identity or short-lived credentials and protected environments.
6. Pin third-party actions/images and limit permissions per job.
7. Add concurrency controls, timeouts, retries only for transient steps, and clear logs.
8. Test pipeline changes safely and document manual recovery.

## Output contract

- Pipeline definitions
- Stage/check matrix
- Artifact provenance path
- Rollback/re-run procedure

## Quality gates

- Failures are actionable.
- A failed check cannot be hidden by later success.
- Production deploys use reviewed immutable artifacts.
- Untrusted pull requests cannot access secrets.

## Handoffs and dependencies

- `security/secrets-and-supply-chain`
- `deployment-readiness`
- `release-coordinator`
- `software-development/code-quality-gate`

## Boundaries

- Do not use broad permanent credentials.
- Do not rebuild separately per environment.
- Do not retry deterministic test failures.
