---
name: release-notes
description: Turn verified changes into audience-specific release notes that explain impact, action, compatibility, and risk. Use when a version, deployment, migration, or feature set is being released.
license: MIT
metadata:
  category: documentation
  origin: custom-synthesis
  revision: "1.1.0"
---

# Release Notes

## Trigger

- Commit logs need conversion into customer or operator language.
- Breaking changes require clear action.

## Inputs

- Merged changes and issue links
- Version/date/environment
- Migration/deprecation details
- Known issues

## Procedure

1. Determine audience and release scope.
2. Group changes by user impact rather than commit type alone.
3. Lead with what changed and why it matters.
4. Call out breaking changes, required actions, security fixes, migrations, and rollback constraints.
5. Include upgrade steps and compatibility windows.
6. Separate known issues and workarounds from resolved items.
7. Verify every claim against code, tests, or tickets.
8. Humanize language and remove promotional inflation.

## Output contract

- Release notes
- Upgrade/migration section
- Known issues and rollback notes
- Traceability links

## Quality gates

- No internal-only detail leaks.
- Breaking changes are impossible to miss.
- Security details are useful without enabling abuse.
- Every item is actually in the release.

## Handoffs and dependencies

- `operations/release-coordinator`
- `security/dependency-cve-audit`
- `deslop/text-humanizer`

## Boundaries

- Do not paste raw commit history.
- Do not market routine fixes as transformational.
- Do not omit required operator action.
