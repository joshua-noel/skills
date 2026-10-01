import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "skills/papercuts-maintenance/scripts/maintenance.py"


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        self.root.mkdir()
        self.state = Path(self.temporary.name) / "state"

    def run_helper(self, command, *arguments, now="2026-09-30T12:00:00+00:00", root=None):
        result = subprocess.run(
            [sys.executable, str(HELPER), command, *arguments,
             "--root", str(root or self.root), "--state-dir", str(self.state), "--now", now],
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)

    def test_completion_retries_do_not_count_again_after_review(self):
        self.run_helper("reviewed")
        first = self.run_helper("complete", "ticket-1")
        retry = self.run_helper("complete", "ticket-1")
        self.assertEqual(first["completed_since_review"], 1)
        self.assertEqual(retry["completed_since_review"], 1)
        self.run_helper("reviewed")
        old_retry = self.run_helper("complete", "ticket-1")
        self.assertEqual(old_retry["completed_since_review"], 0)
        self.assertFalse(old_retry["due"])

    def test_fifth_verified_item_triggers_review(self):
        self.run_helper("reviewed")
        for number in range(1, 5):
            result = self.run_helper("complete", f"ticket-{number}")
            self.assertFalse(result["due"])
        fifth = self.run_helper("complete", "ticket-5")
        self.assertTrue(fifth["due"])
        self.assertEqual(fifth["reasons"], ["completed_items"])

    def test_status_does_not_acknowledge_due_maintenance(self):
        self.assertEqual(self.run_helper("status")["reasons"], ["never_reviewed"])
        self.assertEqual(self.run_helper("status")["reasons"], ["never_reviewed"])
        self.run_helper("reviewed")
        next_week = "2026-10-05T09:00:00+00:00"
        self.assertEqual(self.run_helper("status", now=next_week)["reasons"], ["new_iso_week"])
        self.assertEqual(self.run_helper("status", now=next_week)["reasons"], ["new_iso_week"])

    def test_iso_week_year_transition(self):
        self.run_helper("reviewed", now="2026-12-31T12:00:00+00:00")
        same_week = self.run_helper("status", now="2027-01-01T12:00:00+00:00")
        self.assertFalse(same_week["due"])
        next_week = self.run_helper("status", now="2027-01-04T12:00:00+00:00")
        self.assertEqual(next_week["reasons"], ["new_iso_week"])

    def test_git_subdirectory_uses_the_same_workspace_state(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        child = self.root / "nested"
        child.mkdir()
        self.run_helper("reviewed")
        completed = self.run_helper("complete", "ticket-1", root=child)
        status = self.run_helper("status")
        self.assertEqual(completed["root"], status["root"])
        self.assertEqual(status["completed_since_review"], 1)

    def test_concurrent_completions_preserve_distinct_ids(self):
        self.run_helper("reviewed")
        processes = [subprocess.Popen(
            [sys.executable, str(HELPER), "complete", f"ticket-{number % 6}",
             "--root", str(self.root), "--state-dir", str(self.state),
             "--now", "2026-09-30T12:00:00+00:00"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ) for number in range(12)]
        for process in processes:
            stdout, stderr = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 0, stderr)
        status = self.run_helper("status")
        self.assertEqual(status["completed_since_review"], 6)
        self.assertEqual(status["reasons"], ["completed_items"])


if __name__ == "__main__":
    unittest.main()
