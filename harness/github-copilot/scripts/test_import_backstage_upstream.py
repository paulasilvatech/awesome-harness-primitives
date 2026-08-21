#!/usr/bin/env python3
"""Focused tests for import_backstage_upstream.py.

Run with either:
    python3 harness/github-copilot/scripts/test_import_backstage_upstream.py
    python3 -m unittest harness.github-copilot.scripts.test_import_backstage_upstream  (not a valid package path; use the first form)

These tests build small, self-contained synthetic upstream fixtures (a real
but tiny local Git repository) instead of depending on the ephemeral,
machine-local offline checkout referenced in the import task, so they remain
deterministic and portable across environments. All scratch directories are
created under this script's own directory (never under /tmp) and removed in
tearDown.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

import import_backstage_upstream as m  # noqa: E402

SCRATCH_ROOT = SCRIPTS_DIR / ".import_backstage_upstream_test_scratch"

APACHE_LICENSE_TEXT = (
    "                                 Apache License\n"
    "                           Version 2.0, January 2004\n"
    "                        http://www.apache.org/licenses/\n"
)
MIT_LICENSE_TEXT = "MIT License\n\nPermission is hereby granted, free of charge...\n"


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def init_git_repo(root: Path) -> None:
    run_git(root, "init", "-q")
    run_git(root, "config", "user.email", "test@example.com")
    run_git(root, "config", "user.name", "Test User")


def commit_all(root: Path, message: str = "fixture commit") -> str:
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", message)
    return run_git(root, "rev-parse", "HEAD")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_upstream_fixture(
    root: Path,
    *,
    repository_url: str = m.UPSTREAM_REPOSITORY,
    license_text: str = APACHE_LICENSE_TEXT,
    include_notice: bool = True,
    include_index: bool = False,
    omit_skill: str | None = None,
) -> str:
    """Build a tiny real upstream checkout and return its committed HEAD hash."""
    write(root / "package.json", json.dumps({"repository": {"url": repository_url}}))
    write(root / "LICENSE", license_text)
    if include_notice:
        write(root / "NOTICE", "Backstage\nCopyright 2020 The Backstage Authors\n")
    if include_index:
        write(root / "docs/.well-known/skills/index.md", "# Skills index\n")
    for name in m.SKILL_NAMES:
        if name == omit_skill:
            continue
        write(root / f"docs/.well-known/skills/{name}/SKILL.md", f"---\nname: {name}\n---\n\nBody for {name}.\n")
    write(root / ".claude/skills/catalog-db-performance.md", "---\nname: catalog-db-performance\n---\n\nBattery.\n")
    init_git_repo(root)
    return commit_all(root)


class ScratchTestCase(unittest.TestCase):
    def setUp(self) -> None:
        SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
        self._scratch_dir = Path(tempfile.mkdtemp(dir=str(SCRATCH_ROOT)))
        self._saved_expected_commit = m.EXPECTED_COMMIT

    def tearDown(self) -> None:
        m.EXPECTED_COMMIT = self._saved_expected_commit
        shutil.rmtree(self._scratch_dir, ignore_errors=True)

    def new_dir(self, name: str) -> Path:
        path = self._scratch_dir / name
        path.mkdir(parents=True, exist_ok=True)
        return path


class TestNormalizeRepoUrl(unittest.TestCase):
    def test_variants_normalize_to_same_url(self) -> None:
        expected = "https://github.com/backstage/backstage"
        variants = [
            "https://github.com/backstage/backstage",
            "https://github.com/backstage/backstage.git",
            "git+https://github.com/backstage/backstage.git",
            "git@github.com:backstage/backstage.git",
            "https://github.com/backstage/backstage/",
        ]
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(m.normalize_repo_url(variant), expected)


class TestVerifyLicense(ScratchTestCase):
    def test_accepts_apache_2(self) -> None:
        source = self.new_dir("source")
        write(source / "LICENSE", APACHE_LICENSE_TEXT)
        self.assertEqual(m.verify_license(source), m.LICENSE_ID)

    def test_rejects_non_apache_license(self) -> None:
        source = self.new_dir("source")
        write(source / "LICENSE", MIT_LICENSE_TEXT)
        with self.assertRaises(m.ImportError_):
            m.verify_license(source)

    def test_rejects_missing_license(self) -> None:
        source = self.new_dir("source")
        with self.assertRaises(m.ImportError_):
            m.verify_license(source)


class TestVerifyRepositoryIdentity(ScratchTestCase):
    def test_accepts_matching_dict_url(self) -> None:
        source = self.new_dir("source")
        write(source / "package.json", json.dumps({"repository": {"url": m.UPSTREAM_REPOSITORY}}))
        m.verify_repository_identity(source, m.UPSTREAM_REPOSITORY)  # should not raise

    def test_accepts_matching_string_repository(self) -> None:
        source = self.new_dir("source")
        write(source / "package.json", json.dumps({"repository": f"git+{m.UPSTREAM_REPOSITORY}.git"}))
        m.verify_repository_identity(source, m.UPSTREAM_REPOSITORY)  # should not raise

    def test_rejects_mismatched_repository(self) -> None:
        source = self.new_dir("source")
        write(source / "package.json", json.dumps({"repository": {"url": "https://github.com/example/other"}}))
        with self.assertRaises(m.ImportError_):
            m.verify_repository_identity(source, m.UPSTREAM_REPOSITORY)

    def test_rejects_missing_package_json(self) -> None:
        source = self.new_dir("source")
        with self.assertRaises(m.ImportError_):
            m.verify_repository_identity(source, m.UPSTREAM_REPOSITORY)


class TestVerifyCommit(ScratchTestCase):
    def test_accepts_matching_clean_head(self) -> None:
        source = self.new_dir("source")
        write(source / "README.md", "hello\n")
        init_git_repo(source)
        head = commit_all(source)
        m.verify_commit(source, head)  # should not raise

    def test_rejects_commit_mismatch(self) -> None:
        source = self.new_dir("source")
        write(source / "README.md", "hello\n")
        init_git_repo(source)
        commit_all(source)
        with self.assertRaises(m.ImportError_):
            m.verify_commit(source, "0" * 40)

    def test_rejects_dirty_checkout(self) -> None:
        source = self.new_dir("source")
        write(source / "README.md", "hello\n")
        init_git_repo(source)
        head = commit_all(source)
        write(source / "README.md", "modified\n")
        with self.assertRaises(m.ImportError_):
            m.verify_commit(source, head)

    def test_rejects_non_git_source(self) -> None:
        source = self.new_dir("source")
        with self.assertRaises(m.ImportError_):
            m.verify_commit(source, "0" * 40)


class TestPathSafety(ScratchTestCase):
    def test_rejects_symlink_component(self) -> None:
        root = self.new_dir("root")
        target = self.new_dir("outside")
        link = root / "LICENSE"
        link.symlink_to(target)
        with self.assertRaises(m.ImportError_):
            m.assert_no_symlink_in_path(root, PurePosixPath("LICENSE"), "destination")

    def test_rejects_parent_escape(self) -> None:
        root = self.new_dir("root")
        with self.assertRaises(m.ImportError_):
            m.assert_no_symlink_in_path(root, PurePosixPath("../escape"), "destination")

    def test_resolve_within_returns_path_for_safe_relative(self) -> None:
        root = self.new_dir("root")
        (root / "LICENSE").write_text("x", encoding="utf-8")
        resolved = m.resolve_within(root, PurePosixPath("LICENSE"), "source")
        self.assertEqual(resolved, (root / "LICENSE").resolve())


class TestBuildEntries(ScratchTestCase):
    def test_full_fixture_produces_expected_entries(self) -> None:
        source = self.new_dir("source")
        head = make_upstream_fixture(source, include_notice=True, include_index=False)
        m.EXPECTED_COMMIT = head
        entries = m.build_entries(source)
        dest_paths = {str(entry.dest_rel) for entry in entries}
        expected = {f"skills/{name}/references/upstream/SKILL.md" for name in m.SKILL_NAMES}
        expected.add(f"skills/{m.PERFORMANCE_SNAPSHOT_SKILL}/references/upstream/catalog-db-performance.md")
        expected.add("LICENSE")
        expected.add("NOTICE")
        self.assertEqual(dest_paths, expected)
        notice_entry = next(e for e in entries if e.dest_rel == PurePosixPath("NOTICE"))
        self.assertEqual(notice_entry.origin, "upstream")
        self.assertIn(b"Backstage Authors", notice_entry.data)

    def test_missing_notice_generates_local_fallback(self) -> None:
        source = self.new_dir("source")
        head = make_upstream_fixture(source, include_notice=False)
        m.EXPECTED_COMMIT = head
        entries = m.build_entries(source)
        notice_entry = next(e for e in entries if e.dest_rel == PurePosixPath("NOTICE"))
        self.assertEqual(notice_entry.origin, "generated")
        self.assertIsNone(notice_entry.source_rel)
        self.assertIn(b"NOT upstream content", notice_entry.data)
        self.assertIn(m.EXPECTED_COMMIT.encode(), notice_entry.data)

    def test_optional_index_included_when_present(self) -> None:
        source = self.new_dir("source")
        head = make_upstream_fixture(source, include_index=True)
        m.EXPECTED_COMMIT = head
        entries = m.build_entries(source)
        dest_paths = {str(entry.dest_rel) for entry in entries}
        self.assertIn("references/upstream/skills-index.md", dest_paths)

    def test_missing_required_skill_raises(self) -> None:
        source = self.new_dir("source")
        head = make_upstream_fixture(source, omit_skill="mui-to-bui-migration")
        m.EXPECTED_COMMIT = head
        with self.assertRaises(m.ImportError_):
            m.build_entries(source)


class TestApplyAndCheck(ScratchTestCase):
    def build_fixture_and_entries(self, **kwargs):
        source = self.new_dir("source")
        head = make_upstream_fixture(source, **kwargs)
        m.EXPECTED_COMMIT = head
        entries = m.build_entries(source)
        return source, entries

    def test_apply_then_check_round_trip_is_clean(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        m.apply_import(plugin_dir, entries)
        self.assertEqual(m.check_import(plugin_dir, entries), [])
        self.assertTrue((plugin_dir / "PROVENANCE.json").is_file())
        provenance = json.loads((plugin_dir / "PROVENANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(provenance["sourceRepository"], m.UPSTREAM_REPOSITORY)
        self.assertEqual(provenance["sourceCommit"], m.EXPECTED_COMMIT)
        self.assertEqual(provenance["importDate"], m.IMPORT_DATE)
        self.assertEqual(provenance["license"], m.LICENSE_ID)

    def test_check_detects_missing_file(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        m.apply_import(plugin_dir, entries)
        (plugin_dir / "LICENSE").unlink()
        findings = m.check_import(plugin_dir, entries)
        self.assertTrue(any("missing imported file: LICENSE" in f for f in findings))

    def test_check_detects_content_drift(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        m.apply_import(plugin_dir, entries)
        license_path = plugin_dir / "LICENSE"
        license_path.write_text(license_path.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        findings = m.check_import(plugin_dir, entries)
        self.assertTrue(any("imported file differs from source: LICENSE" in f for f in findings))

    def test_check_detects_stray_file_in_owned_directory(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        m.apply_import(plugin_dir, entries)
        stray = plugin_dir / "skills" / "mui-to-bui-migration" / "references" / "upstream" / "stray.txt"
        stray.write_text("stray\n", encoding="utf-8")
        findings = m.check_import(plugin_dir, entries)
        self.assertTrue(any("unreferenced imported file" in f and "stray.txt" in f for f in findings))

    def test_apply_prunes_stray_file_in_owned_directory(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        m.apply_import(plugin_dir, entries)
        stray = plugin_dir / "skills" / "mui-to-bui-migration" / "references" / "upstream" / "stray.txt"
        stray.write_text("stray\n", encoding="utf-8")
        m.apply_import(plugin_dir, entries)
        self.assertFalse(stray.exists())
        self.assertEqual(m.check_import(plugin_dir, entries), [])

    def test_optional_index_disappearance_is_reported_and_pruned(self) -> None:
        _, entries = self.build_fixture_and_entries(include_index=True)
        plugin_dir = self.new_dir("plugin")
        m.apply_import(plugin_dir, entries)
        index_path = plugin_dir / "references/upstream/skills-index.md"
        self.assertTrue(index_path.is_file())

        entries_without_index = [
            entry
            for entry in entries
            if entry.dest_rel != PurePosixPath("references/upstream/skills-index.md")
        ]
        findings = m.check_import(plugin_dir, entries_without_index)
        self.assertTrue(
            any(
                "unreferenced imported file: references/upstream/skills-index.md"
                in finding
                for finding in findings
            )
        )

        m.apply_import(plugin_dir, entries_without_index)
        self.assertFalse(index_path.exists())
        self.assertEqual(m.check_import(plugin_dir, entries_without_index), [])

    def test_check_does_not_write_anything(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        self.assertFalse(plugin_dir.exists() and any(plugin_dir.iterdir()))
        findings = m.check_import(plugin_dir, entries)
        self.assertTrue(findings)  # nothing imported yet -> reported, not written
        self.assertFalse((plugin_dir / "PROVENANCE.json").exists())

    def test_apply_rejects_symlink_destination(self) -> None:
        _, entries = self.build_fixture_and_entries()
        plugin_dir = self.new_dir("plugin")
        outside = self.new_dir("outside")
        plugin_dir.mkdir(parents=True, exist_ok=True)
        (plugin_dir / "LICENSE").symlink_to(outside)
        with self.assertRaises(m.ImportError_):
            m.apply_import(plugin_dir, entries)


class TestMainEntryPoint(ScratchTestCase):
    def test_main_apply_then_check(self) -> None:
        source = self.new_dir("source")
        head = make_upstream_fixture(source)
        m.EXPECTED_COMMIT = head
        plugin_dir = self.new_dir("plugin")
        exit_code = m.main(["--source", str(source), "--plugin-dir", str(plugin_dir)])
        self.assertEqual(exit_code, 0)
        exit_code = m.main(["--source", str(source), "--plugin-dir", str(plugin_dir), "--check"])
        self.assertEqual(exit_code, 0)

    def test_main_check_reports_drift_without_writing(self) -> None:
        source = self.new_dir("source")
        head = make_upstream_fixture(source)
        m.EXPECTED_COMMIT = head
        plugin_dir = self.new_dir("plugin")
        exit_code = m.main(["--source", str(source), "--plugin-dir", str(plugin_dir), "--check"])
        self.assertEqual(exit_code, 1)
        self.assertFalse(plugin_dir.exists() and any(plugin_dir.iterdir()))

    def test_main_fails_on_commit_mismatch(self) -> None:
        source = self.new_dir("source")
        make_upstream_fixture(source)
        # m.EXPECTED_COMMIT left at its real, unrelated default -> mismatch.
        plugin_dir = self.new_dir("plugin")
        exit_code = m.main(["--source", str(source), "--plugin-dir", str(plugin_dir)])
        self.assertEqual(exit_code, 1)


def tearDownModule() -> None:
    if SCRATCH_ROOT.is_dir() and not any(SCRATCH_ROOT.iterdir()):
        SCRATCH_ROOT.rmdir()


if __name__ == "__main__":
    unittest.main()
