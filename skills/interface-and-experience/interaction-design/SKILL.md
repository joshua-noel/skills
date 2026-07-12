---
name: interaction-design
description: Design understandable behaviors, state transitions, feedback, and recovery across a user journey, with mandatory deslop review. Use when a workflow, form, command, navigation pattern, or stateful component needs behavior design.
license: MIT
metadata:
  category: interface-and-experience
  origin: custom-synthesis
  revision: "1.1.0"
---

# Interaction Design

## Trigger

- Users encounter uncertainty, errors, or high-consequence actions.
- Interaction details are missing from a visual design.

## Inputs

- User journey and task model
- System states and latency
- Error/permission model
- Input methods and accessibility needs

## Procedure

1. Map user intent, system response, state transition, and recovery for each step.
2. Reduce decision load and preserve user context.
3. Use progressive disclosure for real complexity, not to hide essential information.
4. Design immediate feedback, optimistic behavior only where safe, and clear pending states.
5. Make validation specific, timely, and non-destructive.
6. Guard high-consequence actions with proportionate confirmation and undo where possible.
7. Specify keyboard, screen-reader, touch, pointer, and interrupted-session behavior.
8. Run mandatory deslop gates and humanize all interface copy.

## Output contract

- Interaction flow/state model
- Behavior and feedback specification
- Error/recovery copy
- Deslop gate report

## Quality gates

- Every action has visible feedback.
- Errors identify the problem and recovery without blame.
- Focus and state survive interruptions where appropriate.
- All mandatory deslop gates pass.

## Handoffs and dependencies

- `deslop/ui-deslop (mandatory)`
- `deslop/design-pattern-detector (mandatory)`
- `deslop/artifact-delint (mandatory)`
- `deslop/text-humanizer when interface copy is produced`
- `hallmark-upstream/repository/skills/hallmark`
- `security/social-engineering-review for identity or high-risk workflows`

## Boundaries

- Do not use animation as the only feedback.
- Do not add confirmations to every action.
- Do not ship hidden destructive behavior or failed deslop gates.
