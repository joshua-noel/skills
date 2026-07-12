---
name: project-documentation
description: Create an elegant, task-oriented documentation set that lets contributors understand, run, use, and maintain a project. Use when a project needs readme, contributor, setup, architecture, or usage documentation.
license: MIT
metadata:
  category: documentation
  origin: custom-synthesis
  revision: "1.1.0"
---

# Project Documentation

## Trigger

- Existing documentation is fragmented or stale.
- Code/system/research outputs need a coherent handoff.

## Inputs

- Verified project structure and behavior
- Target audiences
- Setup/test/deploy commands
- Architecture and operational facts

## Procedure

1. Identify audience journeys: evaluate, install, use, develop, operate, troubleshoot, contribute.
2. Build an information architecture that reveals essentials first and links detail progressively.
3. Verify every command and path against the project.
4. Write concrete examples before abstract explanations.
5. Distinguish prerequisites, defaults, optional paths, and destructive actions.
6. Add architecture, security, operations, and support links where relevant.
7. Use diagrams only when they reduce cognitive load.
8. Run text-humanizer and artifact-delint before release.

## Output contract

- README and linked documentation set
- Navigation/index
- Verified command examples
- Freshness/ownership notes

## Quality gates

- A new user can reach a first success without hidden knowledge.
- No command is invented or stale.
- Headings and links support scanning.
- Copy is precise, human, and free of generic AI filler.

## Handoffs and dependencies

- `deslop/text-humanizer`
- `deslop/artifact-delint`
- `architecture-decision-record`
- `runbook-authoring`

## Boundaries

- Do not document features that do not exist.
- Do not turn every detail into the README.
- Do not use screenshots where maintainable text is clearer.
