#!/usr/bin/env python3
"""Repository-scoped Papercuts cadence; Python 3 standard library only."""

import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def default_state_dir():
    override = os.environ.get("PI_CODING_AGENT_DIR")
    if override:
        agent_dir = Path(override).expanduser()
    else:
        profile = os.environ.get("OMP_PROFILE") or os.environ.get("PI_PROFILE")
        agent_dir = Path.home() / ".omp"
        if profile:
            agent_dir = agent_dir / "profiles" / profile
        agent_dir = agent_dir / "agent"
    return agent_dir / "papercuts-state"


def canonical_root(value):
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("--root must be a directory")
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except FileNotFoundError:
        result = None
    if result is not None and result.returncode == 0:
        root = Path(result.stdout.strip()).resolve(strict=True)
    return os.path.normcase(str(root))


@contextmanager
def locked(path):
    # Keep this inode: deleting a lock file lets other processes lock a different one.
    with path.open("a+b") as handle:
        if os.fstat(handle.fileno()).st_size == 0:
            handle.write(b"\0")
            handle.flush()
        if os.name == "nt":
            import msvcrt
        else:
            import fcntl
        deadline = time.monotonic() + 10
        while True:
            try:
                handle.seek(0)
                if os.name == "nt":
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as error:
                if error.errno not in (11, 13, 35, 36):
                    raise
                if time.monotonic() >= deadline:
                    raise OSError("Timed out waiting for cadence state lock; retry the command") from error
                time.sleep(0.05)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_state(path, root):
    if not path.exists():
        return {
            "version": 1,
            "root": root,
            "completed_ids": [],
            "completed_since_review": 0,
            "last_review": None,
        }
    with path.open(encoding="utf-8") as handle:
        state = json.load(handle)
    if not isinstance(state, dict) or state.get("version") != 1 or state.get("root") != root:
        raise ValueError("Cadence state has an unsupported version or mismatched root")
    ids = state.get("completed_ids")
    count = state.get("completed_since_review")
    last_review = state.get("last_review")
    if (
        not isinstance(ids, list)
        or any(not isinstance(item, str) or not item.strip() for item in ids)
        or len(set(ids)) != len(ids)
        or type(count) is not int
        or not 0 <= count <= len(ids)
        or (last_review is not None and not isinstance(last_review, str))
    ):
        raise ValueError("Cadence state is invalid; preserve it and repair before retrying")
    if last_review is not None:
        datetime.fromisoformat(last_review)
    return state


def save_state(path, state):
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, ensure_ascii=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def status(state, now):
    reasons = []
    if state["completed_since_review"] >= 5:
        reasons.append("completed_items")
    if state["last_review"] is None:
        reasons.append("never_reviewed")
    else:
        review_week = datetime.fromisoformat(state["last_review"]).isocalendar()[:2]
        if now.isocalendar()[:2] > review_week:
            reasons.append("new_iso_week")
    return {
        "root": state["root"],
        "due": bool(reasons),
        "reasons": reasons,
        "completed_since_review": state["completed_since_review"],
        "last_review": state["last_review"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "complete", "reviewed"))
    parser.add_argument("work_item_id", nargs="?", help="Stable ID of a verified implementation item")
    parser.add_argument("--root", default=os.getcwd(), help="Workspace directory (Git root when available)")
    parser.add_argument("--state-dir", type=Path, default=default_state_dir())
    parser.add_argument("--now", help="ISO datetime override for deterministic cadence checks")
    args = parser.parse_args()
    if args.command == "complete":
        if not args.work_item_id or not args.work_item_id.strip() or args.work_item_id != args.work_item_id.strip():
            parser.error("complete requires a nonblank stable work-item ID without surrounding whitespace")
    elif args.work_item_id is not None:
        parser.error("only complete accepts a work-item ID")
    try:
        now = datetime.fromisoformat(args.now) if args.now else datetime.now().astimezone()
        root = canonical_root(args.root)
        state_dir = args.state_dir.expanduser().resolve()
        state_dir.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha256(root.encode("utf-8")).hexdigest()
        path = state_dir / (key + ".json")
        with locked(state_dir / (key + ".lock")):
            state = load_state(path, root)
            if args.command == "complete" and args.work_item_id not in state["completed_ids"]:
                state["completed_ids"].append(args.work_item_id)
                state["completed_since_review"] += 1
                save_state(path, state)
            elif args.command == "reviewed":
                state["last_review"] = now.isoformat()
                state["completed_since_review"] = 0
                save_state(path, state)
            result = status(state, now)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
