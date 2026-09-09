#!/usr/bin/env python3
"""Append a safe, de-duplicated workflow papercut to PAPERCUTS.md.

The command deliberately has no network or package dependencies. It is kept
small because it runs from an agent workflow and must behave predictably when
several local processes record observations at once.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import stat
import sys
import time
from typing import Iterator, Union


PathLike = Union[str, os.PathLike[str]]
PAPERCUTS_FILENAME = "PAPERCUTS.md"
LOCK_FILENAME = ".papercut.lock"
MAX_MESSAGE_LENGTH = 2_000
MAX_MODEL_LENGTH = 100
LOCK_TIMEOUT_SECONDS = 5.0
LOCK_POLL_SECONDS = 0.02


class PapercutError(Exception):
    """A user-correctable logging error."""


class PathSafetyError(PapercutError):
    """The requested root or destination is unsafe to write."""


class InputError(PapercutError):
    """The model or message is empty, malformed, or sensitive."""


class LockTimeoutError(PapercutError):
    """The bounded lock wait expired."""


@dataclass(frozen=True)
class AppendResult:
    """The observable result of one append attempt."""

    added: bool
    path: Path
    message: str
    sanitized: bool


# These patterns intentionally target recognizable credential shapes instead
# of trying to identify every possible secret. False positives are safer than
# putting a likely credential into a committed markdown file.
_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\b(?:gh[pousr]|github_pat)_[A-Za-z0-9_]{8,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{8,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{8,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}\b", re.IGNORECASE),
    re.compile(
        r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"
    ),
    re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|auth(?:orization)?|secret|password|passwd|token)"
        r"\s*[:=]\s*['\"]?[^\s'\"]{8,}",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:https?|postgres(?:ql)?|mysql)://[^/\s:@]+:[^/\s@]+@",
        re.IGNORECASE,
    ),
)


def _reject_secrets(value: str) -> None:
    """Reject obvious credentials without echoing the matched value."""

    if any(pattern.search(value) for pattern in _SECRET_PATTERNS):
        raise InputError(
            "message appears to contain a secret-like token; redact it before logging"
        )


def _normalise_message(value: str) -> tuple[str, bool]:
    if not isinstance(value, str):
        raise InputError("message must be text")

    # Keep line-oriented markdown safe while allowing ordinary copied text to
    # be cleaned up. Newlines and tabs are reported as sanitization by main().
    if any(ord(char) < 32 and char not in "\r\n\t" for char in value) or "\x7f" in value:
        raise InputError("message contains an unsupported control character")
    normalised = " ".join(value.split())
    if not normalised:
        raise InputError("message must not be empty")
    if len(normalised) > MAX_MESSAGE_LENGTH:
        raise InputError(f"message must be at most {MAX_MESSAGE_LENGTH} characters")
    _reject_secrets(normalised)
    return normalised, normalised != value.strip()


def _normalise_model(value: str) -> str:
    if not isinstance(value, str):
        raise InputError("model must be text")
    if any(char.isspace() for char in value) or any(ord(char) < 32 for char in value):
        raise InputError("model must be a single line")
    if not value or len(value) > MAX_MODEL_LENGTH:
        raise InputError("model must be present and reasonably short")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/+-]*", value):
        raise InputError("model contains unsupported characters")
    _reject_secrets(value)
    return value


def _resolved_root(root: PathLike) -> Path:
    candidate = Path(root).expanduser()
    try:
        if not candidate.exists() or not candidate.is_dir():
            raise PathSafetyError("--root must name an existing directory")
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise PathSafetyError(f"cannot resolve --root safely: {exc}") from exc
    return resolved


def _destination(root: Path, filename: str) -> Path:
    """Validate a direct child before opening it for read or write."""

    candidate = root / filename
    try:
        # Reject existing links on every platform. POSIX O_NOFOLLOW closes the
        # final-component race; Windows has no standard equivalent, so a link
        # swapped after this check can still redirect the open operation there.
        if candidate.is_symlink():
            raise PathSafetyError(f"refusing symlink destination: {filename}")
        if candidate.exists() and not candidate.is_file():
            raise PathSafetyError(f"destination is not a regular file: {filename}")
        resolved = candidate.resolve(strict=False)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise PathSafetyError(f"destination escapes --root: {filename}") from exc
    except (OSError, RuntimeError) as exc:
        if isinstance(exc, PathSafetyError):
            raise
        raise PathSafetyError(f"cannot validate destination {filename}: {exc}") from exc
    return candidate


def _open_regular(path: Path, *, append: bool, mode: int) -> int:
    flags = os.O_RDWR | os.O_CREAT
    if append:
        flags |= os.O_APPEND
    flags |= getattr(os, "O_BINARY", 0)
    # POSIX closes the check/write race for the final path component. Windows
    # has no equivalent flag in the standard os module, so _destination's
    # immediate symlink check is the available guard there.
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags, mode)
    except OSError as exc:
        raise PathSafetyError(f"cannot open safe destination {path.name}: {exc}") from exc
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise PathSafetyError(f"destination is not a regular file: {path.name}")
    except Exception:
        os.close(descriptor)
        raise
    return descriptor


@contextmanager
def _locked(lock_path: Path, timeout: float = LOCK_TIMEOUT_SECONDS) -> Iterator[None]:
    """Acquire a cross-platform exclusive lock with a finite wait."""

    descriptor = _open_regular(lock_path, append=False, mode=0o600)
    acquired = False
    deadline = time.monotonic() + max(0.0, timeout)
    try:
        if os.name == "nt":
            import msvcrt

            # msvcrt.locking requires a byte-sized region. Seed the lock file
            # once; concurrent seed writes are harmless and remain locked below.
            os.lseek(descriptor, 0, os.SEEK_END)
            if os.lseek(descriptor, 0, os.SEEK_CUR) == 0:
                os.write(descriptor, b"\0")
            while True:
                os.lseek(descriptor, 0, os.SEEK_SET)
                try:
                    msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
                    acquired = True
                    break
                except OSError as exc:
                    if time.monotonic() >= deadline:
                        raise LockTimeoutError(
                            f"timed out after {timeout:.1f}s waiting for papercut lock"
                        ) from exc
                    time.sleep(min(LOCK_POLL_SECONDS, max(0.0, deadline - time.monotonic())))
        else:
            import fcntl

            while True:
                try:
                    fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except OSError as exc:
                    if time.monotonic() >= deadline:
                        raise LockTimeoutError(
                            f"timed out after {timeout:.1f}s waiting for papercut lock"
                        ) from exc
                    time.sleep(min(LOCK_POLL_SECONDS, max(0.0, deadline - time.monotonic())))
        yield
    finally:
        if acquired:
            if os.name == "nt":
                import msvcrt

                try:
                    os.lseek(descriptor, 0, os.SEEK_SET)
                    msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            else:
                import fcntl

                fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _canonical(value: str) -> str:
    return " ".join(value.split()).casefold()


def _already_recorded(existing: str, message: str) -> bool:
    wanted = _canonical(message)
    for line in existing.splitlines():
        if not line.startswith("- ") or " — `" not in line or "`: " not in line:
            continue
        stored = line.split("`: ", 1)[1]
        if _canonical(stored) == wanted:
            return True
    return False


def _timestamp(now: datetime | None = None) -> str:
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def append_papercut(
    root: PathLike,
    model: str,
    message: str,
    *,
    now: datetime | None = None,
    lock_timeout: float = LOCK_TIMEOUT_SECONDS,
) -> AppendResult:
    """Validate and append one papercut, returning whether it was new."""

    safe_model = _normalise_model(model)
    safe_message, sanitized = _normalise_message(message)
    resolved_root = _resolved_root(root)
    destination = _destination(resolved_root, PAPERCUTS_FILENAME)
    lock_path = _destination(resolved_root, LOCK_FILENAME)

    with _locked(lock_path, timeout=lock_timeout):
        # Revalidate after waiting: a caller may have replaced the destination
        # while this process was blocked on the lock.
        destination = _destination(resolved_root, PAPERCUTS_FILENAME)
        descriptor = _open_regular(destination, append=True, mode=0o644)
        with os.fdopen(descriptor, "a+b", closefd=True) as stream:
            stream.seek(0)
            existing_bytes = stream.read()
            existing = existing_bytes.decode("utf-8", errors="replace")
            if _already_recorded(existing, safe_message):
                return AppendResult(False, destination, safe_message, sanitized)
            separator = "" if not existing or existing.endswith(("\n", "\r")) else "\n"
            entry = f"{separator}- {_timestamp(now)} — `{safe_model}`: {safe_message}\n"
            stream.seek(0, os.SEEK_END)
            stream.write(entry.encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
    return AppendResult(True, destination, safe_message, sanitized)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Append one safe, de-duplicated workflow papercut to PAPERCUTS.md."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="existing project root containing PAPERCUTS.md (default: current directory)",
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        help="model name to record with the observation",
    )
    parser.add_argument("message", nargs="+", help="one or two sentence observation")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    raw_message = " ".join(args.message)
    try:
        result = append_papercut(args.root, args.model, raw_message)
    except PapercutError as exc:
        print(f"papercut: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"papercut: write failed: {exc}", file=sys.stderr)
        return 3

    if result.sanitized:
        print("papercut: sanitized surrounding or repeated whitespace", file=sys.stderr)
    if result.added:
        print(f"recorded papercut in {result.path}")
    else:
        print("duplicate papercut; nothing written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
