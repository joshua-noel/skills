#!/usr/bin/env python3
"""Install the skills and core instructions for Codex by copying.

Skills go to ~/.agents/skills/<name> (Codex's user skills location). The core instructions go
between managed markers in <codex home>/AGENTS.md (Codex's global instructions file). The plugin
route (see README) is an alternative that needs no copying.
"""

import argparse
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skillkit import REPO, install_copy  # noqa: E402

MARKERS = ("<!-- agent-skills:start -->", "<!-- agent-skills:end -->")


def default_codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, help="Codex home directory (default: CODEX_HOME, else ~/.codex)")
    parser.add_argument("--skills-dir", type=Path, help="skills directory (default: ~/.agents/skills)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing anything")
    parser.add_argument("--instructions-only", action="store_true", help="Only merge the core instructions into AGENTS.md (use with the plugin route)")
    parser.add_argument("--skills-only", action="store_true", help="Only copy the skills")
    args = parser.parse_args(argv)
    if args.instructions_only and args.skills_only:
        parser.error("choose at most one of --instructions-only and --skills-only")
    home = (args.codex_home or default_codex_home()).expanduser().resolve()
    skills_dir = (args.skills_dir or Path.home() / ".agents" / "skills").expanduser().resolve()
    try:
        install_copy(
            REPO, skills_dir, home / "AGENTS.md", home / "backups", MARKERS, "Codex",
            dry_run=args.dry_run, with_skills=not args.instructions_only, with_instructions=not args.skills_only,
        )
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
