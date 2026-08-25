from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "check_traceability.py"
SPEC = importlib.util.spec_from_file_location("check_traceability", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def entry(index: int, result: str = "pass") -> dict[str, object]:
    item: dict[str, object] = {
        "id": f"TR-{index:03d}",
        "story_id": f"US-{index:03d}",
        "acceptance_id": f"AC-{index:03d}",
        "scenario_id": f"SC-{index:03d}",
        "risk": "high",
        "test_layer": "component",
        "result": result,
        "evidence": {"type": "command", "reference": f"test-command-{index}"},
    }
    if result == "manual":
        item["test_layer"] = "manual"
        item["evidence"] = {"type": "manual", "reference": "reviewed procedure"}
        item["manual_procedure"] = "Complete the documented critical flow."
    elif result == "fail":
        item["defect_id"] = f"DEF-{index:03d}"
        item["retest"] = "Repeat the exact failed scenario."
    elif result in {"blocked", "not-applicable"}:
        item["limitation"] = "Required environment is unavailable."
    return item


class TraceabilityTests(unittest.TestCase):
    def test_accepts_all_supported_result_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            data = {
                "version": 1,
                "entries": [
                    entry(1, "pass"),
                    entry(2, "fail"),
                    entry(3, "manual"),
                    entry(4, "not-applicable"),
                    entry(5, "blocked"),
                ],
            }
            errors, results = MODULE.validate_traceability(data, Path(temp))
        self.assertEqual([], errors)
        self.assertEqual(5, sum(results.values()))

    def test_rejects_missing_and_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            first = entry(1)
            second = entry(2)
            second["id"] = first["id"]
            second["acceptance_id"] = first["acceptance_id"]
            second["scenario_id"] = first["scenario_id"]
            del first["story_id"]
            errors, _ = MODULE.validate_traceability(
                {"version": 1, "entries": [first, second]}, Path(temp)
            )
        joined = "\n".join(errors)
        self.assertIn("missing non-empty story_id", joined)
        self.assertIn("duplicate trace id", joined)
        self.assertIn("duplicate acceptance/scenario", joined)

    def test_rejects_unsupported_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            errors, _ = MODULE.validate_traceability(
                {"version": 1, "entries": [entry(1, "passed")]}, Path(temp)
            )
        self.assertTrue(any("unsupported result" in error for error in errors))

    def test_validates_existing_path_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = root / "results" / "case.txt"
            evidence.parent.mkdir()
            evidence.write_text("passed\n", encoding="utf-8")
            item = entry(1)
            item["evidence"] = {"type": "path", "reference": "results/case.txt"}
            errors, _ = MODULE.validate_traceability(
                {"version": 1, "entries": [item]}, root
            )
        self.assertEqual([], errors)

    def test_rejects_missing_and_escaping_evidence_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            missing = entry(1)
            missing["evidence"] = {"type": "path", "reference": "missing.txt"}
            escaping = entry(2)
            escaping["evidence"] = {"type": "path", "reference": "../outside.txt"}
            errors, _ = MODULE.validate_traceability(
                {"version": 1, "entries": [missing, escaping]}, root
            )
        joined = "\n".join(errors)
        self.assertIn("does not exist", joined)
        self.assertIn("unsafe evidence path", joined)

    def test_cli_emits_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            traceability = root / "traceability.json"
            traceability.write_text(
                json.dumps({"version": 1, "entries": [entry(1)]}),
                encoding="utf-8",
            )
            result = MODULE.main([str(traceability), "--root", str(root), "--json"])
        self.assertEqual(0, result)


if __name__ == "__main__":
    unittest.main()
