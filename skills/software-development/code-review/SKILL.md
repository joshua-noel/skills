---
name: code-review
description: "Review changes since a fixed point (commit, branch, tag, or merge-base) against repository standards and the originating specification. Use when a branch, pull request, or work-in-progress needs findings before the coordinator schedules repair or publication."
license: MIT
metadata:
  category: engineering
  origin: "mattpocock/skills"
  revision: "original-snapshot"
---

Two-axis review of the cumulative change against the baseline supplied by the coordinator:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Evaluate both axes in one bounded review pass and report the findings side by side. The workflow coordinator owns reviewer dispatch, any repair assignment, and publication decisions.

The coordinator brief supplies the acceptance criteria and baseline. Use `workflow/TRACKERS.md` only when a tracker is relevant. A local review does not require a tracker.

## Process

### 1. Pin the fixed point

Use the coordinator's baseline revision and declared worktree. Resolve the baseline with `git rev-parse`.
If it is missing, inspect the branch and task record before requesting a material missing input.

Review the actual cumulative change, including uncommitted files:

1. Inspect `git status --short` and the baseline record of pre-existing user changes.
2. For an explicit baseline revision, inspect `git diff <baseline>` for tracked working-tree changes, including staged content.
3. For a requested branch comparison, resolve `git merge-base <branch> HEAD` and compare the working tree against that revision.
4. Inspect `git diff --cached` and `git diff` when needed to distinguish staged and unstaged edits.
5. List new files with `git ls-files --others --exclude-standard` and read the in-scope files directly.

Workers need not commit before review. An empty committed diff does not mean the working change is empty.
Separate pre-existing user edits from this task. Do not require their removal or claim them as authored changes.
A missing baseline is a missing input. An empty entire review surface is a no-change result, not a code defect.

### 2. Identify the spec source

Use the user's request and the coordinator's acceptance criteria first. Seek supporting specifications in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched using the workflow in `workflow/TRACKERS.md` when available.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, record that no spec is available and evaluate the Spec axis against the user's stated scope, commit context, or ticket references. Do not invent requirements.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Review both axes

Use the pinned diff, commit list, standards sources, smell baseline, and spec evidence to produce two bounded reports:

- **Standards:** per file or hunk, report documented-standard breaches with the source rule, then label any Fowler smell as a judgement call and quote the relevant hunk. Skip checks already enforced by tooling.
- **Spec:** report missing or partial requirements, unrequested behavior, and implementations that look wrong. Quote the relevant specification or ticket evidence; when no spec exists, say so and limit the report to the stated scope.

Keep findings actionable and prioritized by impact. This skill reports; it does not edit the work, spawn reviewers, create commits, or start a repair loop.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
