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


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


install_claude = load("install_claude")
install_codex = load("install_codex")
install_omp = load("install_omp")
skillkit = load("skillkit")
MANIFEST_NAMES = [name for name, _ in skillkit.load_manifest(ROOT)]


def run(main, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(args))
    return code, out.getvalue(), err.getvalue()


class CopyInstallerTests(unittest.TestCase):
    def test_claude_installer_copies_skills_and_merges_claude_md(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / ".claude"
            (root / "skills/mine").mkdir(parents=True)
            (root / "skills/mine/SKILL.md").write_text("mine", encoding="utf-8")
            (root / "skills/grilling").mkdir()
            (root / "skills/grilling/SKILL.md").write_text("old copy", encoding="utf-8")
            (root / "CLAUDE.md").write_bytes(b"user header\r\n")

            code, out, _ = run(install_claude.main, "--claude-dir", str(root), "--dry-run")
            self.assertEqual(code, 0)
            self.assertEqual((root / "skills/grilling/SKILL.md").read_text(encoding="utf-8"), "old copy")

            code, out, err = run(install_claude.main, "--claude-dir", str(root))
            self.assertEqual((code, err), (0, ""))
            for name in MANIFEST_NAMES:
                self.assertTrue((root / "skills" / name / "SKILL.md").is_file(), name)
            self.assertEqual((root / "skills/mine/SKILL.md").read_text(encoding="utf-8"), "mine")
            backup = next((root / "backups").glob("agent-skills-*"))
            self.assertEqual((backup / "skills/grilling/SKILL.md").read_text(encoding="utf-8"), "old copy")
            self.assertEqual((backup / "CLAUDE.md").read_bytes(), b"user header\r\n")
            text = (root / "CLAUDE.md").read_bytes().decode("utf-8")
            self.assertTrue(text.startswith("user header\r\n"))
            self.assertIn("## House principles", text)
            self.assertNotIn("OMP", text)
            run(install_claude.main, "--claude-dir", str(root))
            self.assertEqual((root / "CLAUDE.md").read_bytes().decode("utf-8"), text)

    def test_codex_installer_copies_skills_and_merges_agents_md(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            home, skills = base / "codex", base / "agents-skills"
            code, _, err = run(install_codex.main, "--codex-home", str(home), "--skills-dir", str(skills))
            self.assertEqual((code, err), (0, ""))
            for name in MANIFEST_NAMES:
                self.assertTrue((skills / name / "SKILL.md").is_file(), name)
            text = (home / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("## House principles", text)
            self.assertNotIn("OMP", text)
            self.assertEqual(text.count(install_codex.MARKERS[0]), 1)

    def test_instructions_only_and_skills_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run(install_claude.main, "--claude-dir", str(root), "--instructions-only")
            self.assertTrue((root / "CLAUDE.md").is_file())
            self.assertFalse((root / "skills").exists())
            other = root / "other"
            run(install_claude.main, "--claude-dir", str(other), "--skills-only")
            self.assertTrue((other / "skills/grilling/SKILL.md").is_file())
            self.assertFalse((other / "CLAUDE.md").exists())
            with self.assertRaises(SystemExit):
                run(install_claude.main, "--claude-dir", str(root), "--skills-only", "--instructions-only")

    def test_damaged_markers_stop_the_install_before_any_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "CLAUDE.md").write_text(install_claude.MARKERS[0] + " only a start", encoding="utf-8")
            code, _, err = run(install_claude.main, "--claude-dir", str(root))
            self.assertEqual(code, 1)
            self.assertIn("marker", err)
            self.assertFalse((root / "skills").exists())


class OmpCoreTests(unittest.TestCase):
    def test_omp_block_is_core_then_omp_addon(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "agent"
            with patch.object(install_omp, "prerequisite_commands", return_value=("omp", "papercuts")), \
                 patch.object(install_omp, "config_command"), contextlib.redirect_stdout(io.StringIO()):
                install_omp.install(ROOT, target)
            text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(text.count(install_omp.START), 1)
            self.assertLess(text.index("## House principles"), text.index("## OMP"))
            self.assertLess(text.index("## OMP"), text.index(install_omp.END))
            self.assertLess(len(text.splitlines()), 60)


class StateDirTests(unittest.TestCase):
    def test_papercuts_state_dir_prefers_explicit_then_neutral_default(self):
        spec = importlib.util.spec_from_file_location("maintenance", ROOT / "skills/papercuts-maintenance/scripts/maintenance.py")
        maintenance = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(maintenance)
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            env = {"HOME": str(home), "USERPROFILE": str(home), "PAPERCUTS_STATE_DIR": str(home / "explicit")}
            with patch.dict("os.environ", env, clear=True):
                self.assertEqual(maintenance.default_state_dir(), home / "explicit")
            del env["PAPERCUTS_STATE_DIR"]
            with patch.dict("os.environ", env, clear=True):
                self.assertEqual(maintenance.default_state_dir(), home / ".papercuts" / "state")
            (home / ".omp" / "agent").mkdir(parents=True)
            with patch.dict("os.environ", env, clear=True):
                self.assertEqual(maintenance.default_state_dir(), home / ".omp" / "agent" / "papercuts-state")


class LayoutTests(unittest.TestCase):
    def test_claude_and_codex_plugin_manifests_agree_with_the_repository(self):
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["name"], codex["name"])
        self.assertRegex(claude["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertFalse(re.match(r"(?i)(claude|anthropic)", claude["name"]))
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(market["plugins"][0]["name"], claude["name"])
        self.assertEqual(market["plugins"][0]["source"], "./")
        codex_market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        entry = codex_market["plugins"][0]
        self.assertEqual((entry["name"], entry["source"]), (claude["name"], {"source": "local", "path": "./"}))
        self.assertEqual(codex_market["name"], market["name"])
        self.assertTrue((ROOT / "skills").is_dir())

    def test_claude_md_only_points_at_agents_md(self):
        text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("@AGENTS.md"))
        self.assertLess(len(text.splitlines()), 6)

    def test_core_and_skill_bodies_are_tool_neutral(self):
        forbidden = re.compile(r"skill://|/skill:|proc://|xd://|agent://|\bOMP\b|\bomp\b|\.omp\b")
        files = [ROOT / "core" / "AGENTS.md", *(ROOT / "skills" / name / "SKILL.md" for name in MANIFEST_NAMES)]
        for path in files:
            self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")), path.relative_to(ROOT))


if __name__ == "__main__":
    unittest.main()
