"""Helpers shared by the per-tool installers. Python standard library only."""

import json
from pathlib import Path
import re
import shutil
import tempfile
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
START = "<!-- omp-workflow:start -->"
END = "<!-- omp-workflow:end -->"
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def read_text(path):
    # Do not normalize line endings in unrelated user text.
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def write_text(path, text):
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)


def managed_block(text, description, start=START, end=END):
    """Return the span of a managed block, rejecting ambiguous or damaged markers."""
    if start not in text and end not in text:
        return None
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"{description}: expected exactly one start/end marker pair")
    first = text.index(start)
    last = text.index(end)
    if last < first:
        raise ValueError(f"{description}: managed block end precedes its start")
    return first, last + len(end)


def merge_instructions(existing, template, description, start=START, end=END):
    """Replace or append the managed block in `existing`; keep all other text byte for byte."""
    template_span = managed_block(template, description + " template", start, end)
    block = (
        template[slice(*template_span)]
        if template_span
        else start + "\n" + template.rstrip("\r\n") + "\n" + end
    )
    existing_span = managed_block(existing, description, start, end)
    if existing_span:
        first, last = existing_span
        return existing[:first] + block + existing[last:]
    separator = "" if not existing else ("\n" if existing.endswith("\n") else "\n\n")
    return existing + separator + block + "\n"


def load_manifest(repo=REPO):
    """Return [(name, source_dir)] from workflow-skills.json, validating names and paths."""
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
        if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
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
    return skills


def core_instructions(repo=REPO):
    """The tool-neutral core instructions: `core/AGENTS.md`."""
    return read_text(repo / "core" / "AGENTS.md").rstrip("\r\n") + "\n"


def install_copy(repo, skills_dir, instructions_file, backup_root, markers, label,
                 dry_run=False, with_skills=True, with_instructions=True):
    """Copy the manifest skills into `skills_dir` and merge the core instructions.

    Only the manifest's skill directories are replaced; other skills are left alone.
    Anything replaced is first copied to a new directory under `backup_root`.
    """
    start, end = markers
    skills = load_manifest(repo) if with_skills else []
    merged = None
    if with_instructions:
        existing = read_text(instructions_file) if instructions_file.exists() else ""
        merged = merge_instructions(existing, core_instructions(repo), str(instructions_file), start, end)
    for name, _ in skills:
        target = skills_dir / name
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            raise ValueError(f"{target}: expected a real skill directory or nothing")
    print(f"{label} skills directory: {skills_dir}")
    print(f"{label} instructions file: {instructions_file}")
    if skills:
        print("Skills: " + ", ".join(name for name, _ in skills))
    if dry_run:
        print("Dry run: no files were changed.")
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix=f"agent-skills-{stamp}-", dir=backup_root))
    print(f"Backup: {backup}")
    if skills:
        skills_dir.mkdir(parents=True, exist_ok=True)
        for name, source in skills:
            target = skills_dir / name
            # Stage outside the scanned skills directory so an interrupted run leaves nothing to discover.
            staged = Path(tempfile.mkdtemp(prefix=".skillkit-", dir=skills_dir.parent)) / name
            shutil.copytree(source, staged, symlinks=True)
            if target.exists():
                shutil.copytree(target, backup / "skills" / name, symlinks=True)
                shutil.rmtree(target)
            shutil.move(str(staged), str(target))
            staged.parent.rmdir()
    if merged is not None:
        if instructions_file.exists():
            shutil.copy2(instructions_file, backup / instructions_file.name)
        instructions_file.parent.mkdir(parents=True, exist_ok=True)
        write_text(instructions_file, merged)
    print("Done. Start a new session to reload skills and instructions.")
