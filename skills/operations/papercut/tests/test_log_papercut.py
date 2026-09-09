from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "log_papercut.py"
SPEC = importlib.util.spec_from_file_location("log_papercut", SCRIPT)
assert SPEC and SPEC.loader
log_papercut = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = log_papercut
SPEC.loader.exec_module(log_papercut)


class PapercutLoggerTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_append_is_deterministic_and_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = log_papercut.append_papercut(
                root,
                "gpt-5.6-luna",
                "The tool asked for a path twice.",
                now=log_papercut.datetime(2026, 9, 8, 12, 0, tzinfo=log_papercut.timezone.utc),
            )
            second = log_papercut.append_papercut(
                root,
                "another-model",
                "  The   tool asked for a path twice.  ",
                now=log_papercut.datetime(2026, 9, 8, 12, 1, tzinfo=log_papercut.timezone.utc),
            )
            contents = (root / "PAPERCUTS.md").read_text(encoding="utf-8")

            self.assertTrue(first.added)
            self.assertFalse(second.added)
            self.assertEqual(contents.count("The tool asked for a path twice."), 1)
            self.assertIn("2026-09-08T12:00:00Z", contents)
            self.assertIn("`gpt-5.6-luna`", contents)

    def test_concurrent_processes_append_without_lost_or_partial_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            processes = [
                subprocess.Popen(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "--root",
                        str(root),
                        "-m",
                        "gpt-5.6-luna",
                        f"friction observation {index}",
                    ],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                for index in range(12)
            ]
            results = [process.communicate(timeout=15) for process in processes]
            self.assertTrue(all(process.returncode == 0 for process in processes), results)

            lines = (root / "PAPERCUTS.md").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 12)
            self.assertEqual(
                {line.rsplit(": ", 1)[-1] for line in lines},
                {f"friction observation {index}" for index in range(12)},
            )

    def test_concurrent_duplicate_writes_leave_one_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            processes = [
                subprocess.Popen(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "--root",
                        str(root),
                        "-m",
                        "gpt-5.6-luna",
                        "same friction",
                    ],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                for _ in range(8)
            ]
            results = [process.communicate(timeout=15) for process in processes]
            self.assertTrue(all(process.returncode == 0 for process in processes), results)
            self.assertEqual(
                (root / "PAPERCUTS.md").read_text(encoding="utf-8").count("same friction"),
                1,
            )

    def test_secret_like_message_is_rejected_without_creating_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = self.run_cli(root, "-m", "gpt-5.6-luna", "api_key=sk-123456789012345678901234")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("secret-like", result.stderr)
            self.assertFalse((root / "PAPERCUTS.md").exists())

    def test_non_regular_destination_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "PAPERCUTS.md").mkdir()
            result = self.run_cli(root, "-m", "gpt-5.6-luna", "should not write a directory")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("regular file", result.stderr)

    def test_multiline_message_is_sanitized_and_kept_on_one_line(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = self.run_cli(root, "-m", "gpt-5.6-luna", "first line\nsecond line")
            contents = (root / "PAPERCUTS.md").read_text(encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("sanitized", result.stderr)
            self.assertEqual(len(contents.splitlines()), 1)
            self.assertIn("first line second line", contents)

    @unittest.skipUnless(hasattr(Path, "symlink_to"), "path symlinks unavailable")
    def test_destination_symlink_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "root"
            outside = Path(temp) / "outside.md"
            root.mkdir()
            outside.write_text("keep me\n", encoding="utf-8")
            try:
                (root / "PAPERCUTS.md").symlink_to(outside)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")

            result = self.run_cli(root, "-m", "gpt-5.6-luna", "should not escape root")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr)
            self.assertEqual(outside.read_text(encoding="utf-8"), "keep me\n")


if __name__ == "__main__":
    unittest.main()
