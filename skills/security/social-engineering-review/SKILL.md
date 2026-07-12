---
name: social-engineering-review
description: Evaluate workflows, messages, identity proofs, and support processes for phishing, impersonation, coercion, and recovery abuse. Use when a process relies on email, chat, phone, approvals, password reset, payment, or support identity checks.
license: MIT
metadata:
  category: security
  origin: custom-synthesis
  revision: "1.1.0"
---

# Social Engineering Review

## Trigger

- A campaign or message may manipulate users.
- An incident involved human trust rather than a software exploit.

## Inputs

- Workflow and communication samples
- Roles and approval rules
- Recovery/escalation process
- Threat context

## Procedure

1. Map who can request, approve, execute, and audit sensitive actions.
2. Identify urgency, authority, secrecy, reciprocity, and channel-switch manipulation opportunities.
3. Test identity proof against account takeover and insider scenarios.
4. Review out-of-band verification, two-person control, payment/change freezes, and safe escalation.
5. Assess message design for spoofability and confusing links/domains.
6. Design user-visible warnings and operator scripts that do not blame victims.
7. Plan simulations only with authorization, clear safeguards, and debrief.
8. Create measurable controls and reporting paths.

## Output contract

- Abuse-case map
- Control gaps
- Safer workflow and message recommendations
- Training/simulation guardrails

## Quality gates

- High-impact actions require independent verification.
- Recovery is not weaker than normal authentication.
- Controls account for pressure and fatigue.
- Recommendations preserve usability for legitimate users.

## Handoffs and dependencies

- `threat-modeling`
- `interface-and-experience/interaction-design`
- `documentation/runbook-authoring`

## Boundaries

- Do not craft deceptive phishing content for real targets.
- Do not collect credentials during training.
- Do not rely on awareness training as the only control.
