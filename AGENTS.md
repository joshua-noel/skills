# Contributor instructions

@omp/AGENTS.md

This repository contains the reduced OMP planning catalog and a backup-first installer. The main OMP session coordinates development with bundled agents and Ponytail; there is no custom model fleet or mandatory development skill chain.

- `workflow-skills.json` is the complete install catalog. Keep skill directories flat under `skills/` for OMP's one-level discovery.
- Preserve complete upstream resources, licenses, and pinned provenance. Document any changed upstream content; do not call an adapted file byte-identical.
- Keep installer and cadence tooling Python-standard-library-only. Preserve unrelated user settings and instructions. Back up replaced catalogs and custom native agents outside discovery.
- Verify changes with a disposable agent directory before changing a real installation. Exercise the actual OMP CLI and Papercuts commands; tests alone do not establish discovery or integration.
- Never commit local configuration, credentials, backups, runtime state, transcripts, or captured private app data.
- Respect user approval and provider/browser consent boundaries. A skill's instruction is not authorization for an external side effect.
- This repository is public. Never commit machine paths, usernames, private project or business names, people's names (other than credited authors), or secrets. Machine-specific practice belongs in a user's local overlay, which stays outside the repository; document the overlay's shape, never its contents.
- Write new skills in our own words. Credit ideas that shaped them in `THIRD_PARTY_NOTICES.md`; vendor third-party text only with its licence file in `licenses/`.
- A new skill needs its directory, an entry in `workflow-skills.json`, a row in the README skills table, and a changelog line. `tests/test_overlay_and_catalog.py` checks that the manifest, directories and frontmatter agree.
