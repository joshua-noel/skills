# OMP skills

A short always-on rulebook and 18 on-demand skills for [Oh My Pi](https://github.com/can1357/oh-my-pi) (OMP), a coding agent. The rulebook keeps every chat honest and safe; the skills hold the longer procedures (clarify, plan, build, review, communicate) and load only when a job needs them. A backup-first installer puts it in place and can be undone.

## Install

Needs Python 3, [OMP](https://github.com/can1357/oh-my-pi) and [Papercuts](https://github.com/treygoff24/papercuts). Node is needed only for the visualize skills and Visual Edit.

```sh
cargo install papercuts --version 0.2.0 --locked   # once
git clone https://github.com/joshua-noel/skills && cd skills
python scripts/install_omp.py --dry-run            # shows what would change
python scripts/install_omp.py                      # installs; prints the backup path
```

Restart OMP. The installer **replaces** the skills catalog and custom native agents (both backed up outside discovery), merges managed blocks into global `AGENTS.md` and `RULES.md`, and sets the skill allowlist with `omp config`. Other settings are kept, and a failed install restores the previous files. `--agent-dir PATH` targets another agent directory (default: `PI_CODING_AGENT_DIR`, then the `OMP_PROFILE`/`PI_PROFILE` profile, then `~/.omp/agent`).

## Skills

Invoke one with `/skill:<name>`; OMP lists each description, so the matching skill loads when its job comes up.

| Job | Skill | Use when |
| --- | --- | --- |
| **Clarify** | [grilling](skills/grilling/SKILL.md) | A plan or request has open choices to settle with the user. |
| | [domain-modeling](skills/domain-modeling/SKILL.md) | Terms are fuzzy or a decision deserves an ADR. |
| | [research](skills/research/SKILL.md) | You need primary-source facts for one bounded question. |
| **Plan** | [prototype](skills/prototype/SKILL.md) | A design question is easier to answer with a throwaway demo. |
| | [wayfinder](skills/wayfinder/SKILL.md) | The work is large, uncertain and spans sessions. |
| | [to-spec](skills/to-spec/SKILL.md) | Agreed scope needs a written specification. |
| | [to-tickets](skills/to-tickets/SKILL.md) | Agreed scope should become verifiable work items. |
| **Build** | [ponytail](skills/ponytail/SKILL.md) | Any coding task: the smallest complete change. |
| | [visual-edit](skills/visual-edit/SKILL.md) | The user wants to edit a running local app visually. |
| | [eval-driven](skills/eval-driven/SKILL.md) | You change a prompt, model or rule that makes automated decisions. |
| **Review** | [review-gates](skills/review-gates/SKILL.md) | A risky change, a merge, a review loop, or a spec, audit or plan to approve. |
| | [demo-bar](skills/demo-bar/SKILL.md) | A UI demo or mock is about to go to the user. |
| **Communicate** | [user-run-scripts](skills/user-run-scripts/SKILL.md) | The user will run a script or checklist by hand. |
| | [ste-writing](skills/ste-writing/SKILL.md) | Text must be clearer: "STE", "simplified English", a runbook. |
| **Visualize** | [visualize-diagram](skills/visualize-diagram/SKILL.md) | "Draw" or "map" how code or a system fits together. |
| | [visualize-webpage](skills/visualize-webpage/SKILL.md) | The explanation should be one interactive HTML page. |
| **Maintain** | [coordinator](skills/coordinator/SKILL.md) | Many agents, overnight, restarts, usage limits, status reports. |
| | [papercuts-maintenance](skills/papercuts-maintenance/SKILL.md) | Recorded friction is due for review. |

## Principles

The always-on block in [omp/AGENTS.md](omp/AGENTS.md) holds 8 short principles: check live sources; merge only authorized, green, reviewed heads; rehearse what the user runs; protect secrets; irreversible actions wait for the user; check a pid's name before stopping it; treat content as data; one question at a time with a recommendation.

## Managed blocks

`omp/AGENTS.md` and `omp/RULES.md` are installed between `<!-- omp-workflow:start -->` and `<!-- omp-workflow:end -->` markers. A reinstall rewrites only what is between them; your own text above or below is kept byte for byte. Damaged or duplicated markers stop the install. Do not edit inside the markers.

## Local overlay

Machine- or person-specific practice (agent limits, load rules, private tooling) does not belong in a public repo. The installer can add **extra skills** from a directory outside it: `--overlay PATH`, else `<agent-dir>/local-overlay` if present, laid out as `skills/<name>/SKILL.md`. Overlay skills are installed flat and allowlisted, so a reinstall does not retire them; contents are never printed. The `coordinator` skill reads its machine limits from such a skill. This is also the place for a third-party skill such as [diagram-design](https://github.com/cathrynlavery/diagram-design) (MIT, not bundled). The install stops before changing anything if an overlay skill reuses a repo skill name, its `name:` differs from its directory, or the overlay sits inside this repo or the replaced `skills`/`agents` directories.

## Update and uninstall

Update: `git pull`, then run the installer again; it is safe to repeat. Uninstall: close OMP, move the installed `skills` directory aside, and restore the backed-up `skills`, `agents`, `AGENTS.md`, `RULES.md` and `config.yml` from the backup directory the installer printed (delete a file that did not exist before). Your overlay is untouched.

## Credits

Built on skills by [Matt Pocock](https://github.com/mattpocock/skills), [Ponytail](https://github.com/DietrichGebert/ponytail), [Builder.io](https://github.com/BuilderIO/skills) and [Papercuts](https://github.com/treygoff24/papercuts) (all MIT). Other sources and licences: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). This repository's own code and guidance are MIT; see [LICENSE](LICENSE).
