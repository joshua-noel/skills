---
name: repository-setup
description: Configure source control, collaboration, ownership, branch protection, templates, and repository automation for safe change. Use when a repository is new or inconsistently governed.
license: MIT
metadata:
  category: operations
  origin: custom-synthesis
  revision: "1.1.0"
---

# Repository Setup

## Trigger

- Teams need pull-request, issue, release, or ownership conventions.
- Supply-chain controls need enforcement.

## Inputs

- Hosting platform
- Team and access model
- Release workflow
- Compliance/security constraints

## Procedure

1. Initialize history with appropriate license and ignore rules.
2. Define branch strategy based on actual release cadence.
3. Add CODEOWNERS or equivalent for sensitive paths.
4. Create concise issue/PR templates that request evidence, risk, and testing.
5. Configure required checks, review rules, signed/verified commits or tags as appropriate, and protected environments.
6. Set least-privilege app/token access.
7. Add dependency and secret scanning with an ownership process.
8. Document contribution and emergency override procedures.

## Output contract

- Repository configuration
- Governance files
- Protection/check matrix
- Contributor workflow

## Quality gates

- Direct production changes require traceability.
- Protection rules cannot be bypassed casually.
- Bots have minimal permissions.
- Templates reduce ambiguity without becoming bureaucracy.

## Handoffs and dependencies

- `security/secrets-and-supply-chain`
- `ci-cd`
- `release-coordinator`
- `documentation/project-documentation`

## Boundaries

- Do not invent account or organization identifiers.
- Do not grant admin rights for convenience.
- Do not impose GitFlow on a project that does not need it.
