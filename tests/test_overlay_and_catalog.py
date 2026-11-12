import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_omp", ROOT / "scripts/install_omp.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


def make_repo(base):
    repo = base / "repo"
    skill = repo / "skills/example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: example\ndescription: Example\n---\n", encoding="utf-8")
    (repo / "workflow-skills.json").write_text(json.dumps({
        "version": 2, "skills": [{"name": "example", "path": "skills/example"}],
    }), encoding="utf-8")
    (repo / "omp").mkdir()
    for name in installer.INSTRUCTIONS:
        (repo / "omp" / name).write_text(
            installer.START + f"\nrepo {name}\n" + installer.END, encoding="utf-8",
        )
    return repo


def make_overlay(root, skill="machine-practice", declared=None, agent=None, agent_declared=None):
    if skill:
        (root / "skills" / skill).mkdir(parents=True)
        (root / "skills" / skill / "SKILL.md").write_text(
            f"---\nname: {declared or skill}\ndescription: x\n---\nsecret-ish detail\n", encoding="utf-8")
    if agent:
        (root / "agents").mkdir(parents=True, exist_ok=True)
        (root / "agents" / f"{agent}.md").write_text(
            f"---\nname: {agent_declared or agent}\ndescription: x\n---\nsecret-ish agent prompt\n", encoding="utf-8")


class OverlayTests(unittest.TestCase):
    def run_install(self, repo, target, overlay=None, dry_run=False):
        calls, out = [], io.StringIO()
        with patch.object(installer, "prerequisite_commands", return_value=("omp", "papercuts")), \
             patch.object(installer, "config_command", side_effect=lambda omp, args, env, cwd: calls.append(args)), \
             contextlib.redirect_stdout(out):
            installer.install(repo, target, dry_run, overlay)
        return calls, out.getvalue()

    def test_overlay_skills_are_installed_allowlisted_and_survive_reinstall(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo, target = make_repo(base), base / "home/agent"
            make_overlay(target / "local-overlay")
            for _ in range(2):
                calls, out = self.run_install(repo, target)
                self.assertTrue((target / "skills/machine-practice/SKILL.md").is_file())
                self.assertTrue((target / "skills/example/SKILL.md").is_file())
                self.assertTrue((target / "local-overlay/skills/machine-practice/SKILL.md").is_file())
                allowlist = next(a for a in calls if a[1] == "skills.includeSkills")
                self.assertEqual(json.loads(allowlist[2]), ["example", "machine-practice"])
                self.assertNotIn("secret-ish", out)

    def test_dry_run_with_overlay_changes_nothing_and_hides_contents(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo, target, overlay = make_repo(base), base / "home/agent", base / "private-overlay"
            make_overlay(overlay)
            _, out = self.run_install(repo, target, overlay, dry_run=True)
            self.assertFalse(target.exists())
            self.assertIn("contents not shown", out)
            self.assertNotIn("secret-ish", out)

    def test_bad_overlays_are_rejected_before_any_change(self):
        cases = {
            "collision": lambda root: make_overlay(root, skill="example"),
            "bad name": lambda root: make_overlay(root, skill="Bad_Name"),
            "name mismatch": lambda root: make_overlay(root, declared="other"),
        }
        for label, build in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                repo, target, overlay = make_repo(base), base / "home/agent", base / "overlay"
                build(overlay)
                with self.assertRaises(ValueError):
                    self.run_install(repo, target, overlay)
                self.assertFalse((target / "skills").exists())

    def test_overlay_agents_replace_the_retired_ones_and_survive_reinstall(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo, target = make_repo(base), base / "home/agent"
            make_overlay(target / "local-overlay", skill=None, agent="researcher")
            (target / "agents").mkdir()
            (target / "agents/old.md").write_text("old agent", encoding="utf-8")
            for _ in range(2):
                _, out = self.run_install(repo, target)
                self.assertIn("secret-ish agent prompt", (target / "agents/researcher.md").read_text(encoding="utf-8"))
                self.assertFalse((target / "agents/old.md").exists())
                self.assertIn("1 agents", out)
                self.assertNotIn("secret-ish", out)

    def test_bad_overlay_agents_are_rejected_before_any_change(self):
        cases = {
            "bundled name": lambda root: make_overlay(root, skill=None, agent="scout"),
            "name mismatch": lambda root: make_overlay(root, skill=None, agent="triage", agent_declared="other"),
            "bad name": lambda root: make_overlay(root, skill=None, agent="Bad_Name"),
        }
        for label, build in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                repo, target, overlay = make_repo(base), base / "home/agent", base / "overlay"
                build(overlay)
                with self.assertRaises(ValueError):
                    self.run_install(repo, target, overlay)
                self.assertFalse((target / "skills").exists())

    def test_overlay_inside_repo_or_replaced_dirs_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo, target = make_repo(base), base / "home/agent"
            for overlay in (repo / "local", target / "skills/overlay"):
                make_overlay(overlay)
                with self.subTest(overlay=overlay), self.assertRaises(ValueError):
                    self.run_install(repo, target, overlay, dry_run=True)

    def test_missing_explicit_overlay_is_an_error_but_missing_default_is_not(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo, target = make_repo(base), base / "home/agent"
            self.run_install(repo, target, dry_run=True)
            with self.assertRaises(ValueError):
                self.run_install(repo, target, base / "missing", dry_run=True)


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((ROOT / "workflow-skills.json").read_text(encoding="utf-8"))
        cls.names = [entry["name"] for entry in manifest["skills"]]

    def test_every_skill_has_matching_frontmatter_and_a_description(self):
        for name in self.names:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            front = re.match(r"---\r?\n(.*?)\r?\n---", text, re.DOTALL)
            self.assertIsNotNone(front, name)
            self.assertRegex(front.group(1), rf"(?m)^name: {re.escape(name)}\s*$")
            self.assertRegex(front.group(1), r"(?m)^description: (?:[>|][-+]?\s*$|.{40,})")

    def test_skill_directories_match_the_manifest(self):
        on_disk = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
        self.assertEqual(on_disk, sorted(self.names))

    def test_public_repository_has_no_machine_paths(self):
        # Generic shapes only; checks for specific private names are done at review time.
        pattern = re.compile(r"\b[A-Za-z]:[\\/](?:Users|[A-Za-z0-9_-]+[\\/])|/home/[a-z][\w.-]*/|/Users/[A-Za-z][\w.-]*/")
        skip = {".git", "__pycache__", ".tmp", "node_modules"}
        for path in ROOT.rglob("*"):
            if path.is_dir() or skip & set(path.parts) or path.suffix in {".png", ".webp", ".ico"}:
                continue
            if path.relative_to(ROOT).as_posix() == "tests/test_overlay_and_catalog.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(pattern.search(text), f"machine-specific path in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    unittest.main()
