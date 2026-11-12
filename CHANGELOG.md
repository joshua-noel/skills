# Changelog

## Unreleased

- Add 18 house principles, each with its reason, to the managed block in `omp/AGENTS.md`, and tighten the existing workflow text so nothing is said twice. A skill-routing table points each job to its skill. **If you pasted the principles by hand outside the markers, remove that copy after the next install**; the installer now warns about a "House principles" heading outside the block.
- Add seven on-demand skills written in our own words: `user-comms`, `review-gates`, `goldfish-review` (credits the Elephant-Goldfish Model), `user-run-scripts`, `demo-bar`, `eval-driven` (credits LangChain and Meta) and `coordinator`. The catalog is now 20 skills.
- Add an optional local overlay for machine- or person-specific instructions and extra skills. The installer merges it from `<agent-dir>/local-overlay`, `--overlay PATH` or `OMP_SKILLS_OVERLAY`, outside the repository, never prints its contents, and rejects collisions, markers and unsafe locations before changing anything.
- Decide `diagram-design` versus `visualize-*`: keep both, vendor neither's counterpart. `diagram-design` (MIT, Cathryn Lavery) is documented as an optional external companion installed through the overlay. `visualize-diagram` now says when to prefer it.
- Rewrite the README: purpose, audience, 60-second install, workflow diagram, skills by job with "use when", principles summary, managed blocks, overlay, update and uninstall, credits.
- Replace a project name in the `visualize-diagram` example spec with a generic one.
- Add tests for overlay handling, the duplicate-principles warning, catalog/README/manifest consistency, skill frontmatter, and a scan for machine-specific paths.
- Add `ste-writing`, `visualize-diagram` and `visualize-webpage`. The visualize skills render a JSON spec to one interactive 16:9 SVG (dark by default, `--light` on request) and wrap it in a self-contained HTML page with a step-through bar. Both write their text at about 80% of ASD-STE100. Verified on a real repository: hover paths, step highlight, tabs, and no-scroll fit at 1280–1920 px windows.
- Replace the custom engineering catalog and fleet launcher with seven pinned Matt Pocock planning/handoff skills, core Ponytail, Builder.io Visual Edit, and Papercuts maintenance. Bundle the upstream project setup guide and templates inside Wayfinder, loaded only when conventions are missing.
- Use OMP's main session, configured model roles, and five bundled task agents. Inspect context, grill unresolved intent, and confirm understanding before implementing and verifying. Specs and tickets are optional when useful.
- Add global capture instructions and per-workspace maintenance after five verified tasks or the first active session in a new ISO week, at safe task boundaries.
- Add a backup-first native installer preserving unrelated settings and user instructions, with rollback on failure.
- Verify sandbox and active skill URI discovery, bundled agents, Papercuts CLI round-trip, cadence behavior, local visual bridge route discovery, and hosted WebMCP discovery. Add nine regression tests for installation safety and cadence boundaries.
