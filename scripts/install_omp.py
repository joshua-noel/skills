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


START = "<!-- omp-workflow:start -->"
END = "<!-- omp-workflow:end -->"
INSTRUCTIONS = ("AGENTS.md", "RULES.md")
BACKUP_ITEMS = ("skills", "agents", *INSTRUCTIONS, "config.yml")


def managed_block(text, description):
    """Return a managed block, rejecting ambiguous or damaged markers."""
    if START not in text and END not in text:
        return None
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError(f"{description}: expected exactly one start/end marker pair")
    start = text.index(START)
    end = text.index(END)
    if end < start:
        raise ValueError(f"{description}: managed block end precedes its start")
    return start, end + len(END)


def merge_instructions(existing, template, description):
    template_span = managed_block(template, description + " template")
    block = (
        template[slice(*template_span)]
        if template_span
        else START + "\n" + template.rstrip("\r\n") + "\n" + END
    )
    existing_span = managed_block(existing, description)
    if existing_span:
        start, end = existing_span
        return existing[:start] + block + existing[end:]
    separator = "" if not existing else ("\n" if existing.endswith("\n") else "\n\n")
    return existing + separator + block + "\n"


def read_text(path):
    # Do not normalize line endings in unrelated user text.
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def write_text(path, text):
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)


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


def preflight(repo, agent_dir):
    manifest_path = repo / "workflow-skills.json"
    manifest = json.loads(read_text(manifest_path))
    if not isinstance(manifest, dict) or manifest.get("version") != 2:
        raise ValueError(f"{manifest_path}: expected manifest version 2")
    entries = manifest.get("skills")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{manifest_path}: skills must be a nonempty list")
    names = set()
    skills = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(f"{manifest_path}: every skill must contain name and path")
        name = entry.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"{manifest_path}: invalid flat skill name {name!r}")
        if name.casefold() in names:
            raise ValueError(f"{manifest_path}: duplicate skill name {name!r}")
        names.add(name.casefold())
        expected = "skills/" + name
        if entry.get("path") != expected:
            raise ValueError(f"{manifest_path}: {name!r} must use path {expected!r}")
        source = repo / expected
        if source.is_symlink() or not source.is_dir():
            raise ValueError(f"{source}: expected a real skill directory")
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"{source}: missing SKILL.md")
        skills.append((name, source))

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

    instructions = {}
    for name in INSTRUCTIONS:
        template_path = repo / "omp" / name
        template = read_text(template_path)
        target = agent_dir / name
        existing = read_text(target) if target.exists() else ""
        instructions[name] = merge_instructions(existing, template, str(target))
    omp, papercuts = prerequisite_commands()
    return skills, instructions, omp, papercuts


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


def install(repo, agent_dir, dry_run=False):
    skills, instructions, omp, papercuts = preflight(repo, agent_dir)
    values = config_values(skills)
    print(f"Agent directory: {agent_dir}")
    print(f"OMP: {omp}")
    print(f"Papercuts: {papercuts}")
    print("Native skills: " + ", ".join(name for name, _ in skills))
    if dry_run:
        print(f"Dry run: backups will be stored outside discovery under {agent_dir.parent / 'backups'}")
        print("Would stage the catalog, retire native custom agents, preserve unmanaged instructions,")
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

    print("Installed the manifest skills and global managed instructions; custom agents are retired.")
    print("Existing model roles, tools, advisor, memory, providers, and other configuration are unchanged.")
    print("Start a new OMP session to reload skills and global instructions.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent-dir", type=Path,
        help="OMP agent directory (default: PI_CODING_AGENT_DIR, active profile, or ~/.omp/agent)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and show changes without writing anything")
    args = parser.parse_args(argv)
    repo = Path(__file__).resolve().parent.parent
    try:
        target = args.agent_dir if args.agent_dir is not None else default_agent_dir()
        install(repo, target.expanduser().resolve(), args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
