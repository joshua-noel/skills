# Changelog

## Unreleased

- Add `ste-writing`, `visualize-diagram` and `visualize-webpage`. The visualize skills render a JSON spec to one interactive 16:9 SVG (dark by default, `--light` on request) and wrap it in a self-contained HTML page with a step-through bar. Both write their text at about 80% of ASD-STE100. Verified on a real repository: hover paths, step highlight, tabs, and no-scroll fit at 1280–1920 px windows.
- Replace the custom engineering catalog and fleet launcher with seven pinned Matt Pocock planning/handoff skills, core Ponytail, Builder.io Visual Edit, and Papercuts maintenance. Bundle the upstream project setup guide and templates inside Wayfinder, loaded only when conventions are missing.
- Use OMP's main session, configured model roles, and five bundled task agents. Inspect context, grill unresolved intent, and confirm understanding before implementing and verifying. Specs and tickets are optional when useful.
- Add global capture instructions and per-workspace maintenance after five verified tasks or the first active session in a new ISO week, at safe task boundaries.
- Add a backup-first native installer preserving unrelated settings and user instructions, with rollback on failure.
- Verify sandbox and active skill URI discovery, bundled agents, Papercuts CLI round-trip, cadence behavior, local visual bridge route discovery, and hosted WebMCP discovery. Add nine regression tests for installation safety and cadence boundaries.
