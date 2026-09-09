# Third-party notices

This package contains exact upstream files and original skills synthesized from public design ideas. Exact upstream files remain under their original licenses and are stored beneath an `*-upstream` directory.

## Vendored upstream

### Ponytail

- Source: https://github.com/DietrichGebert/ponytail
- Ref captured: `main` (latest release observed during assembly: `v4.8.4`)
- Retrieved: 2026-07-12
- License: MIT
- Vendored location: `skills/software-development/ponytail-upstream/`
- Files are unmodified upstream skill files plus the upstream license.

### Hallmark

- Source: https://github.com/nutlope/hallmark
- Commit captured: `aeb42fb354ff4efa36ab475773a082315a3af2ce`
- Package version: `1.1.0`
- Source archive SHA-256: `22508f6acc344148f5d32e777fc5799782c95a60f5c9ea32e2db2b877df4c29a`
- Retrieved from the user-supplied full repository archive: 2026-07-12
- License: MIT
- Vendored location: `skills/interface-and-experience/hallmark-upstream/repository/`
- The complete 282-file repository snapshot is preserved unchanged. Package-authored hash inventory and status metadata sit beside, not inside, the repository snapshot.

## Sources used for original synthesis

The following repositories informed concepts, organization, checklists, or quality gates. Their text was not represented as byte-identical vendoring unless placed in an `*-upstream` directory.

- Matt Pocock engineering skills — https://github.com/mattpocock/skills/tree/main/skills/engineering — MIT
- David Ondrej skills — https://github.com/davidondrej/skills — MIT
- AI Slop / ais-lop — https://github.com/scanaislop/aislop — MIT
- Humanizer — https://github.com/blader/humanizer — MIT
- Emil Kowalski skills — https://github.com/emilkowalski/skills — MIT

The custom skills combine these sources with established engineering, security, research, documentation, operations, accessibility, and system-design practices. They are newly written for this package and licensed under the root MIT license.

## OpenAI workflow additions (2026-09-08)

The active workflow set is listed in `workflow-skills.json`. Existing matching skills were adapted in place.
Matt Pocock-derived skills retain origin metadata. The source workflow did not identify exact historical commits.
Its current MIT license notice is included in `licenses/mattpocock-LICENSE`.
ASD-STE100 is pinned to danyuchn/asd-ste100-skill commit `6f7bb361ae9b97a9fcb5f5c57cbac40eacf2d438`.
The adapted skill retains its MIT license, linter, and references in `skills/documentation/asd-ste100`.
Papercut is a local logging skill based on the workflow owner's supplied instructions.
