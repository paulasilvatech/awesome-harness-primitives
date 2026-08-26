from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_traceability import main  # noqa: E402


class TraceabilityValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.specs = self.root / "specs"
        self.legacy = (
            self.root
            / "01-archaeology/legacy-sifap/natural-programs"
        )
        self.specs.mkdir(parents=True)
        self.legacy.mkdir(parents=True)
        (self.legacy / "PAYMENT.NSN").write_text("END\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_spec(self, name: str, text: str) -> Path:
        path = self.specs / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_validator(self) -> int:
        return main(["--root", str(self.root), "--path", "specs"])

    def test_accepts_real_legacy_source(self) -> None:
        self.write_spec(
            "feature.md",
            "### REQ-001 - Preserve payment\n\n"
            "WHEN a payment is valid, the system SHALL accept it.\n\n"
            "- source_legacy: 01-archaeology/legacy-sifap/"
            "natural-programs/PAYMENT.NSN#L1-L1\n",
        )
        self.assertEqual(0, self.run_validator())

    def test_accepts_concrete_greenfield_justification(self) -> None:
        self.write_spec(
            "feature.md",
            "### REQ-002 - Audit access\n\n"
            "The system SHALL record administrative access.\n\n"
            "- source_legacy: [GREENFIELD] the legacy system has no "
            "access audit trail\n",
        )
        self.assertEqual(0, self.run_validator())

    def test_rejects_missing_source(self) -> None:
        self.write_spec("feature.md", "### REQ-003 - Missing evidence\n")
        self.assertEqual(1, self.run_validator())

    def test_rejects_placeholder_source(self) -> None:
        self.write_spec(
            "feature.md",
            "### REQ-004 - Placeholder\n\n"
            "- source_legacy: 01-archaeology/legacy-sifap/"
            "natural-programs/<PROGRAM>.NSN\n",
        )
        self.assertEqual(1, self.run_validator())

    def test_rejects_duplicate_identifier(self) -> None:
        source = (
            "- source_legacy: [GREENFIELD] approved operational "
            "requirement\n"
        )
        self.write_spec("one.md", "### REQ-005 - One\n\n" + source)
        self.write_spec("two.md", "### REQ-005 - Two\n\n" + source)
        self.assertEqual(1, self.run_validator())


if __name__ == "__main__":
    unittest.main()
