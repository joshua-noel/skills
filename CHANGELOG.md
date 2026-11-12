# Changelog

## Unreleased

- Make the repository tool-neutral. `AGENTS.md` is now the one source of the core instructions (workflow plus the 8 principles); `CLAUDE.md` imports it; the OMP-specific text moved to an OMP-only add-on (`omp/AGENTS.md`) that the OMP installer appends. Skill bodies no longer name OMP tools or URIs; unavoidable OMP steps are in optional `OMP.md` files (`visualize-diagram`, `visualize-webpage`, `papercuts-maintenance`, `visual-edit`).
- Add installers for Claude Code (`scripts/install_claude.py`) and Codex (`scripts/install_codex.py`) next to the OMP one, all reading `workflow-skills.json`, with `--dry-run`, backups, and byte-preserving managed-block merges. Add plugin layouts: `.claude-plugin/` (plugin and marketplace manifests) and a root `plugin.json` with `.agents/plugins/marketplace.json` for Codex.
- The papercuts helper's default state directory is now `$PAPERCUTS_STATE_DIR`, else the OMP agent directory when OMP is present, else `~/.papercuts/state`.
- Fix the OMP installer message that said custom agents are retired; overlay agents are reinstalled.
- Add 8 house principles to the managed block in `omp/AGENTS.md` and shorten the existing workflow text. The block is about 40 lines.
- Add on-demand skills written in our own words: `review-gates` (code gates plus fresh-eyes document review, crediting the Elephant-Goldfish Model in the notices), `user-run-scripts`, `demo-bar`, `eval-driven` and `coordinator` (which also holds the status-report format). The catalog is now 18 skills.
- Move the Visual Edit browser steps into `skills/visual-edit/OMP.md`; the global block keeps one trigger line.
- Add an optional local overlay: extra skills and custom agents (`agents/<name>.md`, so the install no longer retires them) from `--overlay PATH` or `<agent-dir>/local-overlay`, outside the repository. Contents are never printed, and collisions, mismatched names and unsafe locations stop the install before anything changes.
- Decide `diagram-design` versus `visualize-*`: keep both, vendor neither's counterpart. `diagram-design` (MIT, Cathryn Lavery) is an optional external companion installed through the overlay.
- Rewrite the README around install, one skills list, the overlay, update and uninstall. `CATALOG.md` is removed; the README holds the only skills list.
- Make the `visualize-diagram` example spec generic. Remove the unused `licenses/Skills-Lab-LICENSE`.
- Add tests for overlay handling, skill frontmatter, manifest/directory agreement, and a scan for machine-specific paths.
- Add `ste-writing`, `visualize-diagram` and `visualize-webpage`. The visualize skills render a JSON spec to one interactive 16:9 SVG (dark by default, `--light` on request) and wrap it in a self-contained HTML page with a step-through bar. Both write their text at about 80% of ASD-STE100. Verified on a real repository: hover paths, step highlight, tabs, and no-scroll fit at 1280–1920 px windows.
- Replace the custom engineering catalog and fleet launcher with seven pinned Matt Pocock planning/handoff skills, core Ponytail, Builder.io Visual Edit, and Papercuts maintenance. Bundle the upstream project setup guide and templates inside Wayfinder, loaded only when conventions are missing.
- Use OMP's main session, configured model roles, and five bundled task agents. Inspect context, grill unresolved intent, and confirm understanding before implementing and verifying. Specs and tickets are optional when useful.
- Add global capture instructions and per-workspace maintenance after five verified tasks or the first active session in a new ISO week, at safe task boundaries.
- Add a backup-first native installer preserving unrelated settings and user instructions, with rollback on failure.
- Verify sandbox and active skill URI discovery, bundled agents, Papercuts CLI round-trip, cadence behavior, local visual bridge route discovery, and hosted WebMCP discovery. Add nine regression tests for installation safety and cadence boundaries.
