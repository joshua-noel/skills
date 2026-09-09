---
name: setup-matt-pocock-skills
description: "Maintain a repository's optional tracker guidance, triage labels, and domain documentation layout when the user requests setup or those conventions change."
license: MIT
metadata:
  category: engineering
  origin: "mattpocock/skills"
  revision: "original-snapshot"
---

# Setup Matt Pocock's Skills

Inspect and document the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven maintenance guide, not an installer. Explore the repository, present the current and proposed configuration, and return an actionable change set to the workflow coordinator. Do not install Claude integrations or assume a missing plugin, command, or tracker is available. Use the package HANDOFF.md for current installation guidance. Existing engineering tasks do not require this setup skill.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` at the repo root: Codex reads this file natively; is there already an `## Agent skills` section?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `workflow/`: does the tracker guidance already exist? For this package, inspect `workflow/TRACKERS.md`.
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `$to-tickets`, `$triage`, and `$to-spec` read the configured guidance. This package supports local task records. GitHub and a Notion display mirror are optional, as described in `workflow/TRACKERS.md`.

Default posture: these skills use GitHub Issues with the Notion board as a read-side mirror. If the repository uses another tracker, document the difference and identify the tracker operations that need a coordinator-maintained adapter. The templates in this folder are references, not setup scripts.

- **GitHub + Notion mirror**: issues live in GitHub Issues (uses the `gh` CLI); the mirror is maintained by CI and agents never write to Notion.
- **GitLab or local markdown**: use the corresponding reference template in this skill folder and report the adapter work needed before engineering skills can rely on it.
- **Other** (Jira, Linear, etc.): capture the workflow and required operations as a coordinator-owned maintenance task.

Record the choice in the repository's tracker guidance. For this package, that is `workflow/TRACKERS.md`; preserve the configured tracker boundary and keep external pull requests out of triage unless the repository explicitly opts in. The coordinator applies any edit after reviewing the proposed change.

**Section B: Triage label vocabulary.** Skip this section entirely if the `$triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `CONTEXT.md` + `docs/adr/` at the repo root). This fits almost every repo; report it without creating files.

Offer **multi-context** (a root `CONTEXT-MAP.md` pointing to per-context `CONTEXT.md` files) only when exploration found monorepo signals. Include the choice in the coordinator handoff.

### 3. Prepare the maintenance handoff

Show the user a draft of:

- The `## Agent skills` block for the native `AGENTS.md` file
- The proposed tracker guidance at `workflow/TRACKERS.md` (or the adapter gap for another tracker)
- The proposed domain-doc consumer note, which points to `CONTEXT.md` and `docs/adr/`

Return this draft to the workflow coordinator. The coordinator owns approval and writes outside this skill directory.

### 4. Apply through the coordinator

The coordinator applies an approved maintenance change to the repository:

- Edit `AGENTS.md` when it exists; if it does not, include the proposed block in the handoff rather than creating an unrelated policy file.
- Preserve user edits around an existing `## Agent skills` block and update that block in place.
- Keep `workflow/TRACKERS.md` as the optional tracker reference for this package. Use the reference templates here only when the coordinator explicitly maintains another adapter.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `workflow/TRACKERS.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `workflow/TRACKERS.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `CONTEXT.md` and `docs/adr/`.
```

Include the `### Triage labels` sub-block only when `$triage` is installed and Section B ran. When it isn't, omit the block.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping reference (only if `$triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout

For "other" issue trackers, return a tracker-adapter brief to the coordinator. Do not invent a path or silently replace the package's canonical tracker guidance.

### 5. Done

Report the current configuration, proposed edits, unresolved adapter gaps, and which engineering skills will consume the tracker guidance. Mention that the coordinator can maintain `workflow/TRACKERS.md` directly; re-running this skill is useful when the tracker or domain layout changes.
