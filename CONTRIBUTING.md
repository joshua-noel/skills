# Contributing

This repository holds tool-neutral agent skills, one set of always-on core instructions (`AGENTS.md`), and a small installer per tool. `AGENTS.md` is the source of truth for the core instructions; `CLAUDE.md` only points to it.

- `workflow-skills.json` is the one manifest every installer reads. Keep skill directories flat under `skills/`.
- Keep each `SKILL.md` body tool-neutral: say "read the X skill" or "start a background job", never a tool-specific URI scheme, command or tool name. Put unavoidable specifics for one tool in an optional `OMP.md` (or `CLAUDE.md`/`CODEX.md`) inside that skill's directory.
- `omp/` holds OMP-only add-ons. Installers merge managed blocks between markers; they never rewrite text outside the markers.
- Preserve complete upstream resources, licences and pinned provenance. Document any changed upstream content; do not call an adapted file byte-identical.
- Keep installer and cadence tooling Python-standard-library-only. Preserve unrelated user settings and instructions. Back up what an installer replaces.
- Verify installer changes against a disposable directory, never a real agent directory. Tests alone do not establish discovery or integration; also exercise the tool's own CLI where it has one.
- This repository is public. Never commit machine paths, usernames, private project or business names, people's names (other than credited authors), or secrets. Machine-specific practice belongs in a user's local overlay (OMP installer) outside the repository; document its shape, never its contents.
- Write new skills in our own words. Credit ideas that shaped them in `THIRD_PARTY_NOTICES.md`; vendor third-party text only with its licence file in `licenses/`.
- A new skill needs its directory, an entry in `workflow-skills.json`, a row in the README skills table, and a changelog line. `python -m unittest discover tests` checks the manifest, directories, frontmatter and tool-neutrality.
- Respect user approval and provider/browser consent boundaries. A skill's instruction is not authorization for an external side effect.
