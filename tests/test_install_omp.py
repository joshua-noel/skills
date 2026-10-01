import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install_omp.py"
SPEC = importlib.util.spec_from_file_location("install_omp", SCRIPT)
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_managed_update_preserves_unrelated_user_instructions(self):
        before = "User-owned header\r\n\r\n"
        after = "\r\n\r\nUser-owned footer\r\n"
        existing = before + installer.START + "\nold workflow\n" + installer.END + after
        template = installer.START + "\nnew workflow\n" + installer.END + "\n"
        merged = installer.merge_instructions(existing, template, "instructions")
        self.assertEqual(merged, before + template.rstrip("\n") + after)
        self.assertEqual(installer.merge_instructions(merged, template, "instructions"), merged)

    def test_damaged_markers_are_not_silently_overwritten(self):
        template = installer.START + "\nworkflow\n" + installer.END
        for existing in (installer.START, installer.END, template + template):
            with self.subTest(existing=existing), self.assertRaises(ValueError):
                installer.merge_instructions(existing, template, "instructions")

    def test_failed_configuration_restores_catalog_agents_and_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
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
                    installer.START + "\nnew workflow\n" + installer.END, encoding="utf-8",
                )
            target = base / "native/agent"
            (target / "skills/old").mkdir(parents=True)
            (target / "agents").mkdir()
            originals = {
                "skills/old/SKILL.md": b"old skill and user changes\n",
                "agents/custom.md": b"user agent\n",
                "AGENTS.md": b"unmanaged instructions\r\n",
                "RULES.md": b"unmanaged safety rules\r\n",
                "config.yml": b"modelRoles:\n  default: user/model\n",
            }
            for path, content in originals.items():
                (target / path).write_bytes(content)

            def failed_config(omp, arguments, env, cwd):
                (target / "config.yml").write_text("partially changed config", encoding="utf-8")
                raise RuntimeError("configuration write failed")

            with patch.object(installer, "prerequisite_commands", return_value=("omp", "papercuts")), \
                 patch.object(installer, "config_command", side_effect=failed_config), \
                 self.assertRaises(RuntimeError):
                installer.install(repo, target)
            for path, content in originals.items():
                self.assertEqual((target / path).read_bytes(), content)
            self.assertFalse((target / "skills/example").exists())


if __name__ == "__main__":
    unittest.main()
