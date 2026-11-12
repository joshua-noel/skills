#!/usr/bin/env python3
"""Install the manifest's native OMP workflow with a reversible cutover."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skillkit import (  # noqa: E402
    END, START, core_instructions, load_manifest, managed_block, merge_instructions, read_text, write_text,
)

INSTRUCTIONS = ("AGENTS.md", "RULES.md")
BACKUP_ITEMS = ("skills", "agents", *INSTRUCTIONS, "config.yml")
BUNDLED_AGENTS = frozenset({"task", "scout", "sonic", "reviewer", "security-reviewer"})


def prerequisite_commands():
    omp = shutil.which("omp")
    papercuts = shutil.which("papercuts")
    if not papercuts and os.name == "nt":
        cargo_papercuts = Path.home() / ".cargo" / "bin" / "papercuts.exe"
        if cargo_papercuts.is_file():
            papercuts = str(cargo_papercuts)
    if not omp:
        raise ValueError("OMP is not on PATH. Install OMP and open a new shell before retrying.")
    if not papercuts:
        raise ValueError(
            "Papercuts is not installed. Run `cargo install papercuts --locked`, "
            "add the Cargo bin directory to PATH, and retry."
        )
    return omp, papercuts


def default_agent_dir():
    explicit = os.environ.get("PI_CODING_AGENT_DIR")
    if explicit:
        return Path(explicit)
    profile = os.environ.get("OMP_PROFILE") or os.environ.get("PI_PROFILE")
    if profile and profile != "default":
        if profile in (".", "..") or "/" in profile or "\\" in profile or ":" in profile:
            raise ValueError("OMP_PROFILE/PI_PROFILE must be a profile name, not a path")
        return Path.home() / ".omp" / "profiles" / profile / "agent"
    return Path.home() / ".omp" / "agent"


def load_overlay(agent_dir, repo, explicit, taken):
    """Read extra skills and custom agents from the optional local overlay.

    Returns None when there is no overlay, else (root, [(name, skill_dir)], [(name, agent_file)]).
    Contents are never printed.
    """
    root = (explicit if explicit is not None else agent_dir / "local-overlay").expanduser().resolve()
    if not root.is_dir():
        if explicit is not None:
            raise ValueError(f"{root}: overlay directory does not exist")
        return None
    repo_root = repo.resolve()
    if root == repo_root or repo_root in root.parents:
        raise ValueError(f"{root}: the overlay must live outside this repository")
    for name in ("skills", "agents"):
        replaced = (agent_dir / name).resolve()
        if root == replaced or replaced in root.parents:
            raise ValueError(f"{root}: the overlay must not live inside {replaced}, which the install replaces")
    skills = []
    skills_dir = root / "skills"
    for source in sorted(skills_dir.iterdir()) if skills_dir.is_dir() else ():
        if not source.is_dir():
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source.name):
            raise ValueError(f"{source}: invalid flat skill name {source.name!r}")
        if source.name.casefold() in taken:
            raise ValueError(f"{source}: overlay skill name collides with a repository skill")
        skill_file = source / "SKILL.md"
        if not skill_file.is_file():
            raise ValueError(f"{source}: missing SKILL.md")
        front = re.match(r"---\r?\n(.*?)\r?\n---", read_text(skill_file), re.DOTALL)
        declared = re.search(r"(?m)^name:\s*[\"']?([^\s\"']+)", front.group(1)) if front else None
        if not declared or declared.group(1) != source.name:
            raise ValueError(f"{skill_file}: frontmatter name must equal the directory name {source.name!r}")
        skills.append((source.name, source))
    agents = []
    agents_dir = root / "agents"
    for source in sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else ():
        name = source.stem
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"{source}: invalid agent name {name!r}")
        if name in BUNDLED_AGENTS:
            raise ValueError(f"{source}: overlay agent name collides with a bundled OMP agent")
        front = re.match(r"---\r?\n(.*?)\r?\n---", read_text(source), re.DOTALL)
        declared = re.search(r"(?m)^name:\s*[\"']?([^\s\"']+)", front.group(1)) if front else None
        if not declared or declared.group(1) != name:
            raise ValueError(f"{source}: frontmatter name must equal the file name {name!r}")
        agents.append((name, source))
    return root, skills, agents


def preflight(repo, agent_dir, overlay_path=None):
    skills = load_manifest(repo)
    names = {name.casefold() for name, _ in skills}

    if agent_dir == (agent_dir.parent / "backups").resolve():
        raise ValueError(f"{agent_dir}: choose an agent directory distinct from its sibling backups directory")
    if agent_dir.exists() and not agent_dir.is_dir():
        raise ValueError(f"{agent_dir}: agent directory is not a directory")
    for name in BACKUP_ITEMS:
        target = agent_dir / name
        if target.is_symlink():
            raise ValueError(f"{target}: replace this symlink with a real file/directory before installing")
        if target.exists():
            expected_type = target.is_dir() if name in ("skills", "agents") else target.is_file()
            if not expected_type:
                raise ValueError(f"{target}: unexpected file type")
    for name in ("skills", "agents"):
        target = (agent_dir / name).resolve()
        source_root = (repo / "skills").resolve()
        if source_root == target or target in source_root.parents:
            raise ValueError(f"{target}: installing here would move the source repository")

    overlay = load_overlay(agent_dir, repo, overlay_path, names)
    if overlay:
        skills.extend(overlay[1])
    instructions = {}
    for name in INSTRUCTIONS:
        template = read_text(repo / "omp" / name)
        if name == "AGENTS.md":
            # The tool-neutral core, then the OMP-only add-on.
            template = core_instructions(repo) + "\n" + template
        target = agent_dir / name
        existing = read_text(target) if target.exists() else ""
        instructions[name] = merge_instructions(existing, template, str(target))
    omp, papercuts = prerequisite_commands()
    return skills, instructions, omp, papercuts, overlay


def config_values(skills):
    return {
        "skills.includeSkills": [name for name, _ in skills],
        "skills.enableSkillCommands": True,
        "skills.enableClaudeUser": False,
        "skills.enableCodexUser": False,
        "skills.enableAgentsUser": False,
    }


def config_command(omp, arguments, env, cwd):
    try:
        subprocess.run(
            [omp, "config", *arguments], env=env, cwd=cwd,
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "no diagnostic output").strip()
        raise RuntimeError(
            f"OMP config {' '.join(arguments[:2])} failed (exit {exc.returncode}): {detail}. "
            "Check the target config.yml and OMP version, then retry."
        ) from exc


def rollback(agent_dir, backup, moved, replaced, config_started, original_config):
    # Delete only newly installed copies, never originals or previous backups.
    for name in reversed(replaced):
        target = agent_dir / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    for name in reversed(moved):
        shutil.copytree(backup / name, agent_dir / name, symlinks=True)
    for name in INSTRUCTIONS:
        if name in replaced and (backup / name).exists():
            shutil.copy2(backup / name, agent_dir / name)
    if config_started:
        target = agent_dir / "config.yml"
        if original_config:
            shutil.copy2(backup / "config.yml", target)
        elif target.exists():
            target.unlink()


def install(repo, agent_dir, dry_run=False, overlay_path=None):
    skills, instructions, omp, papercuts, overlay = preflight(repo, agent_dir, overlay_path)
    values = config_values(skills)
    print(f"Agent directory: {agent_dir}")
    print(f"OMP: {omp}")
    print(f"Papercuts: {papercuts}")
    print("Native skills: " + ", ".join(name for name, _ in skills))
    if overlay:
        print(f"Local overlay: {overlay[0]} ({len(overlay[1])} skills, {len(overlay[2])} agents); contents not shown")
    if dry_run:
        print(f"Dry run: backups will be stored outside discovery under {agent_dir.parent / 'backups'}")
        print("Would stage the catalog, move the native agents directory to the backup (agents from the")
        print("overlay are reinstalled), preserve unmanaged instructions,")
        print("and set only these OMP configuration values:")
        for key, value in values.items():
            print(f"  {key} = {json.dumps(value)}")
        print("No files or configuration were changed.")
        return

    backup_root = agent_dir.parent / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    # Stage every resource and instruction before moving anything out of discovery.
    with tempfile.TemporaryDirectory(prefix=".omp-workflow-stage-", dir=backup_root) as staging:
        stage = Path(staging)
        incoming = stage / "skills"
        incoming.mkdir()
        for name, source in skills:
            shutil.copytree(source, incoming / name, symlinks=True)
        for name, content in instructions.items():
            write_text(stage / name, content)
        if overlay and overlay[2]:
            (stage / "agents").mkdir()
            for name, source in overlay[2]:
                shutil.copy2(source, stage / "agents" / f"{name}.md")

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup = Path(tempfile.mkdtemp(prefix=f"omp-workflow-{stamp}-", dir=backup_root))
        print(f"Backup: {backup}")
        for name in (*INSTRUCTIONS, "config.yml"):
            source = agent_dir / name
            if source.exists():
                shutil.copy2(source, backup / name)

        existed = agent_dir.exists()
        original_config = (agent_dir / "config.yml").exists()
        moved = []
        replaced = []
        config_started = False
        agent_dir.mkdir(parents=True, exist_ok=True)
        try:
            for name in ("skills", "agents"):
                target = agent_dir / name
                if target.exists():
                    target.rename(backup / name)
                    moved.append(name)
            incoming.rename(agent_dir / "skills")
            replaced.append("skills")
            if overlay and overlay[2]:
                (stage / "agents").rename(agent_dir / "agents")
                replaced.append("agents")
            for name in INSTRUCTIONS:
                replaced.append(name)
                shutil.copy2(stage / name, agent_dir / name)
            env = os.environ.copy()
            env["PI_CODING_AGENT_DIR"] = str(agent_dir)
            # OMP must not pick up the checkout's project-level configuration.
            with tempfile.TemporaryDirectory(prefix="omp-config-") as config_cwd:
                config_started = True
                for key, value in values.items():
                    config_command(omp, ["set", key, json.dumps(value)], env, config_cwd)
        except (Exception, KeyboardInterrupt) as exc:
            try:
                rollback(agent_dir, backup, moved, replaced, config_started, original_config)
                if not existed and agent_dir.exists() and not any(agent_dir.iterdir()):
                    agent_dir.rmdir()
            except Exception as rollback_error:
                raise RuntimeError(
                    f"Installation failed: {exc}. Rollback also failed: {rollback_error}. "
                    f"Restore the original files from {backup} before starting OMP."
                ) from exc
            raise RuntimeError(f"Installation failed; previous installation restored. Backup: {backup}. {exc}") from exc

    print("Installed the manifest skills and global managed instructions; overlay skills and agents are reinstalled.")
    print("Other native agents were moved to the backup; restore any you still want from there or add them to the overlay.")
    print("Existing model roles, tools, advisor, memory, providers, and other configuration are unchanged.")
    print("Start a new OMP session to reload skills and global instructions.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent-dir", type=Path,
        help="OMP agent directory (default: PI_CODING_AGENT_DIR, active profile, or ~/.omp/agent)",
    )
    parser.add_argument(
        "--overlay", type=Path,
        help="directory outside this repository with extra skills in skills/ (default: <agent-dir>/local-overlay if present)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and show changes without writing anything")
    args = parser.parse_args(argv)
    repo = Path(__file__).resolve().parent.parent
    try:
        target = args.agent_dir if args.agent_dir is not None else default_agent_dir()
        install(repo, target.expanduser().resolve(), args.dry_run, args.overlay)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
