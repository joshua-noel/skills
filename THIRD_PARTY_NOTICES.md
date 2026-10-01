# Third-party notices

## Matt Pocock planning skills

- Source: https://github.com/mattpocock/skills
- Commit: `d81f3a183412e71a5b1e84ca21bc1a35eea03a60`
- License: MIT, Copyright (c) 2026 Matt Pocock; see `licenses/mattpocock-LICENSE`.
- Complete source directories copied to flat `skills/<name>/`: engineering `domain-modeling`, `research`, `prototype`, `wayfinder`, `setup-matt-pocock-skills`, `to-spec`, `to-tickets`; productivity `grilling`.
- The copied files, including referenced formats/templates and invocation metadata, are unmodified. OMP integration is original guidance in `omp/`, not a claim that upstream has native OMP commands.

## Ponytail

- Source: https://github.com/DietrichGebert/ponytail
- Commit: `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` (`v4.10.0`).
- License: MIT, Copyright (c) 2026 DietrichGebert; see `licenses/ponytail-LICENSE`.
- Complete `skills/ponytail` directory copied unchanged to `skills/ponytail`.
- Companion audit/debt/gain/help/review skills are not part of this installation.

## Builder.io Visual Edit

- Source: https://github.com/BuilderIO/skills
- Commit: `eb07be67e6d924b958445f706f5ac386243df6b4`.
- License: MIT, Copyright (c) 2026 Builder.io; see `licenses/BuilderIO-LICENSE`.
- Complete `skills/visual-edit` directory copied unchanged to `skills/visual-edit`.
- Runtime tooling uses the separately distributed `@agent-native/core`; it is not vendored. Hosted Design and its account/consent requirements are not supplied by this repository.

## Papercuts

- Source: https://github.com/treygoff24/papercuts
- Tested CLI package: crates.io `papercuts` version `0.2.0`, installed with `--locked`.
- License: MIT. The CLI is an external prerequisite, not vendored code.
- The global capture block is the user-requested text from the upstream README. The cadence helper, maintenance instructions, installer, and OMP integration are original code/guidance under the root MIT license.

The previous specialist catalog, Hallmark snapshot, custom model-fleet launcher, and Python Papercut logger have been removed by the clean OMP cutover. Their earlier history remains in Git; this branch does not claim to ship them.
