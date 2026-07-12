---
name: threat-modeling
description: Identify assets, trust boundaries, adversaries, abuse cases, and mitigations early enough to shape the design. Use when a new feature crosses trust boundaries or handles sensitive data.
license: MIT
metadata:
  category: security
  origin: custom-synthesis
  revision: "1.1.0"
---

# Threat Modeling

## Trigger

- Authentication, authorization, payments, uploads, integrations, or AI actions are involved.
- An architecture needs security review.

## Inputs

- Architecture/data flows
- Assets and actors
- Security/privacy requirements
- Deployment and identity model

## Procedure

1. Scope the system and identify assets and security objectives.
2. Draw data flows, entry points, trust boundaries, identities, and privileged operations.
3. Enumerate plausible threats using STRIDE plus business abuse cases.
4. Assess likelihood, impact, preconditions, and detectability.
5. Map preventive, detective, and recovery controls to each high-risk threat.
6. Verify authorization at every object/action boundary.
7. Consider supply chain, insiders, social engineering, prompt/tool injection, and operational misuse where relevant.
8. Assign owners and validation tests.

## Output contract

- Threat model
- Prioritized threat register
- Mitigation and verification plan
- Residual-risk decisions

## Quality gates

- Threats are specific to real flows.
- Controls have implementation owners.
- Residual risk is explicit.
- The model includes abuse by valid accounts, not only anonymous attackers.

## Handoffs and dependencies

- `system-design/architecture-design`
- `secure-code-review`
- `social-engineering-review`
- `operations/deployment-readiness`

## Boundaries

- Defensive analysis only; do not create weaponized exploit steps.
- Do not label all risks “high.”
- Do not treat compliance as proof of security.
