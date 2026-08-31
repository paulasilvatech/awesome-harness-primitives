import importlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

CONVERTER = importlib.import_module("convert_from_copilot")
copy_skill_resource = CONVERTER.copy_skill_resource
ignored_resource_path = CONVERTER.ignored_resource_path
replace_generated_tree = CONVERTER.replace_generated_tree


class IgnoredResourcePathTests(unittest.TestCase):
    def test_ignores_generated_and_local_artifacts(self) -> None:
        ignored = (
            Path(".DS_Store"),
            Path("assets/.DS_Store"),
            Path("__pycache__/module.pyc"),
            Path("scripts/cache-generator/obj/project.assets.json"),
            Path("scripts/cache-generator/bin/Debug/tool"),
        )

        for path in ignored:
            with self.subTest(path=path):
                self.assertTrue(ignored_resource_path(path))

    def test_keeps_skill_resources(self) -> None:
        kept = (
            Path("assets/icon.svg"),
            Path("scripts/generate.py"),
            Path("references/guide.md"),
        )

        for path in kept:
            with self.subTest(path=path):
                self.assertFalse(ignored_resource_path(path))


class ReplaceGeneratedTreeTests(unittest.TestCase):
    def test_replaces_tree_without_leaving_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            staged = root / "staged"
            target = root / "target"
            staged.mkdir()
            target.mkdir()
            (staged / "new.txt").write_text("new", encoding="utf-8")
            (target / "old.txt").write_text("old", encoding="utf-8")

            replace_generated_tree(staged, target)

            self.assertEqual(
                (target / "new.txt").read_text(encoding="utf-8"),
                "new",
            )
            self.assertFalse((target / "old.txt").exists())
            self.assertFalse(staged.exists())
            self.assertFalse(any(root.glob(".target.backup-*")))


class CopySkillResourceTests(unittest.TestCase):
    def test_maps_portable_web_tool_tokens_in_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.md"
            target = root / "target.md"
            source.write_text(
                "Use web_fetch and web_search.  \n"
                "Keep WebFetchToolResult unchanged.\n",
                encoding="utf-8",
            )

            copy_skill_resource(source, target)

            self.assertEqual(
                target.read_text(encoding="utf-8"),
                "Use WebFetch and WebSearch.\n"
                "Keep WebFetchToolResult unchanged.\n",
            )


if __name__ == "__main__":
    unittest.main()
