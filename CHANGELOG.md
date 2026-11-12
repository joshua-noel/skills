# Changelog

## Unreleased

- Add 8 house principles to the managed block in `omp/AGENTS.md` and shorten the existing workflow text. The block is about 40 lines.
- Add on-demand skills written in our own words: `review-gates` (code gates plus fresh-eyes document review, crediting the Elephant-Goldfish Model in the notices), `user-run-scripts`, `demo-bar`, `eval-driven` and `coordinator` (which also holds the status-report format). The catalog is now 18 skills.
- Move the Visual Edit browser steps into `skills/visual-edit/OMP.md`; the global block keeps one trigger line.
- Add an optional local overlay: extra skills from `--overlay PATH` or `<agent-dir>/local-overlay`, outside the repository. Contents are never printed, and collisions, mismatched names and unsafe locations stop the install before anything changes.
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
