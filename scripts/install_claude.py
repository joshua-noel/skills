#!/usr/bin/env python3
"""Install the skills and core instructions for Claude Code by copying.

Skills go to <claude dir>/skills/<name> (Claude Code's personal skills location). The core
instructions go between managed markers in <claude dir>/CLAUDE.md. The plugin route
(see README) is an alternative that needs no copying.
"""

import argparse
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skillkit import REPO, install_copy  # noqa: E402

MARKERS = ("<!-- agent-skills:start -->", "<!-- agent-skills:end -->")


def default_claude_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude-dir", type=Path, help="Claude Code config directory (default: CLAUDE_CONFIG_DIR, else ~/.claude)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing anything")
    parser.add_argument("--instructions-only", action="store_true", help="Only merge the core instructions into CLAUDE.md (use with the plugin route)")
    parser.add_argument("--skills-only", action="store_true", help="Only copy the skills")
    args = parser.parse_args(argv)
    if args.instructions_only and args.skills_only:
        parser.error("choose at most one of --instructions-only and --skills-only")
    root = (args.claude_dir or default_claude_dir()).expanduser().resolve()
    try:
        install_copy(
            REPO, root / "skills", root / "CLAUDE.md", root / "backups", MARKERS, "Claude Code",
            dry_run=args.dry_run, with_skills=not args.instructions_only, with_instructions=not args.skills_only,
        )
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
