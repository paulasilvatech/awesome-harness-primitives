from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cobol_db2_graph import (  # noqa: E402
    GATES,
    Graph,
    dead_legacy,
    extract,
    gate,
    main,
    slice_order,
    validate,
)

PROGRAM = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAY0100.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       COPY PAYCPY01.
       PROCEDURE DIVISION.
           CALL 'PAY0110' USING WS-ID.
      * CALL 'GHOST001' is a comment and must be ignored.
           CALL WS-DYNAMIC-NAME.
           EXEC SQL
             SELECT AMOUNT INTO :WS-AMT FROM PAYMENT WHERE ID = :WS-ID
           END-EXEC.
           STOP RUN.
"""

SUBPROGRAM = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAY0110.
       PROCEDURE DIVISION.
           EXEC SQL
             DECLARE PAYCUR CURSOR FOR SELECT ID FROM PAYMENT
           END-EXEC.
           EXEC SQL
             UPDATE PAYMENT SET AMOUNT = :WS-AMT WHERE ID = :WS-ID
           END-EXEC.
           GOBACK.
"""

DDL = """\
CREATE TABLE PAYMENT (
  ID      INTEGER NOT NULL,
  AMOUNT  DECIMAL(13,2) NOT NULL
);
"""

JOB = """\
//PAYJOB   JOB (ACCT),'PAYMENTS'
//* commented EXEC PGM=GHOST001 must be ignored
//STEP1    EXEC PGM=PAY0100
"""


def build_corpus(root: Path) -> None:
    (root / "PAY0100.CBL").write_text(PROGRAM, encoding="utf-8")
    (root / "PAY0110.CBL").write_text(SUBPROGRAM, encoding="utf-8")
    (root / "PAYCPY01.CPY").write_text(
        "       01 WS-ID PIC 9(8).\n", encoding="utf-8")
    (root / "PAYMENT.DDL").write_text(DDL, encoding="utf-8")
    (root / "PAYJOB.JCL").write_text(JOB, encoding="utf-8")


def node(identifier: str, node_type: str, **extra: object) -> dict:
    return {
        "id": identifier,
        "type": node_type,
        "evidence": "evidence.md",
        **extra,
    }


class ExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        build_corpus(self.root)
        self.builder = extract(self.root, "001-payments")
        self.edges = {
            (edge["from"], edge["type"], edge["to"])
            for edge in self.builder.edges.values()
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_every_member_becomes_a_node_with_evidence(self) -> None:
        for identifier in (
            "cobol:PAY0100", "cobol:PAY0110", "copybook:PAYCPY01",
            "jcl:PAYJOB", "ddl:PAYMENT", "db2:PAYMENT",
        ):
            with self.subTest(node=identifier):
                found = self.builder.nodes[identifier]
                self.assertTrue(found["evidence"])
                self.assertEqual(found["slice"], "001-payments")

    def test_structural_edges_are_extracted(self) -> None:
        for edge in (
            ("cobol:PAY0100", "CALLS", "cobol:PAY0110"),
            ("cobol:PAY0100", "COPIES", "copybook:PAYCPY01"),
            ("jcl:PAYJOB", "RUNS", "cobol:PAY0100"),
            ("db2:PAYMENT", "DEFINED_BY", "ddl:PAYMENT"),
        ):
            with self.subTest(edge=edge):
                self.assertIn(edge, self.edges)

    def test_embedded_sql_resolves_table_access(self) -> None:
        self.assertIn(("cobol:PAY0100", "SELECTS", "db2:PAYMENT"), self.edges)
        self.assertIn(("cobol:PAY0110", "UPDATES", "db2:PAYMENT"), self.edges)

    def test_cursor_declaration_becomes_a_node(self) -> None:
        self.assertIn(
            ("cobol:PAY0110", "DECLARES_CURSOR", "cursor:PAYCUR"), self.edges)

    def test_cobol_comments_are_ignored(self) -> None:
        targets = {edge[2] for edge in self.edges}
        self.assertNotIn("cobol:GHOST001", targets)

    def test_jcl_comments_are_ignored(self) -> None:
        notes = " ".join(self.builder.unresolved)
        self.assertNotIn("GHOST001", notes)

    def test_dynamic_call_is_reported_instead_of_guessed(self) -> None:
        self.assertTrue(
            any("dynamic CALL" in note for note in self.builder.unresolved),
            self.builder.unresolved,
        )

    def test_recognized_file_count_is_recorded(self) -> None:
        self.assertEqual(self.builder.recognized_files, 5)


class GraphContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        build_corpus(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def extracted(self) -> Graph:
        out = self.root / "graph.json"
        main(["extract", "--corpus", str(self.root), "--out", str(out)])
        return Graph(json.loads(out.read_text(encoding="utf-8")))

    def test_extracted_graph_passes_validation(self) -> None:
        self.assertEqual(validate(self.extracted()), [])

    def test_slice_order_places_callee_before_caller(self) -> None:
        order = [m for group in slice_order(self.extracted()) for m in group]
        self.assertLess(
            order.index("cobol:PAY0110"), order.index("cobol:PAY0100"))

    def test_dead_legacy_finds_the_unreferenced_program(self) -> None:
        (self.root / "ORPHAN01.CBL").write_text(
            "       PROGRAM-ID. ORPHAN01.\n", encoding="utf-8")
        self.assertIn("cobol:ORPHAN01", dead_legacy(self.extracted()))


class ValidationTests(unittest.TestCase):
    def test_rejects_unsupported_version(self) -> None:
        graph = Graph({"version": 2, "nodes": [], "edges": []})
        self.assertIn("version must equal 1", validate(graph))

    def test_rejects_node_without_evidence(self) -> None:
        graph = Graph({
            "version": 1,
            "nodes": [{"id": "cobol:A", "type": "CobolProgram"}],
            "edges": [],
        })
        self.assertIn("cobol:A: evidence is required", validate(graph))

    def test_rejects_disallowed_endpoint_types(self) -> None:
        graph = Graph({
            "version": 1,
            "nodes": [
                node("cobol:A", "CobolProgram"),
                node("pg:t", "PgTable"),
            ],
            "edges": [{
                "from": "cobol:A", "type": "CALLS", "to": "pg:t",
                "evidence": "c",
            }],
        })
        self.assertTrue(
            any("does not allow" in item for item in validate(graph)))


class GateTests(unittest.TestCase):
    def test_quality_gate_reports_unmigrated_db2_table(self) -> None:
        graph = Graph({
            "version": 1,
            "nodes": [node("db2:PAYMENT", "Db2Table", slice="s1")],
            "edges": [],
        })
        result = gate(graph, "quality", "s1")
        self.assertFalse(result["passed"])
        self.assertIn(
            "db2:PAYMENT: no outgoing MIGRATES_TO",
            result["rules"][1]["missing"],
        )

    def test_quality_gate_reports_unmigrated_vsam_dataset(self) -> None:
        graph = Graph({
            "version": 1,
            "nodes": [node("vsam:CUST", "VsamDataset", slice="s1")],
            "edges": [],
        })
        result = gate(graph, "quality", "s1")
        self.assertIn(
            "vsam:CUST: no outgoing MIGRATES_TO",
            result["rules"][2]["missing"],
        )

    def test_vision_gate_requires_owner_when_accepted(self) -> None:
        graph = Graph({
            "version": 1,
            "nodes": [node(
                "rule:a", "BusinessRule", slice="s1", status="accepted")],
            "edges": [],
        })
        missing = gate(graph, "vision", "s1")["rules"][0]["missing"]
        self.assertIn("rule:a: accepted without an owner", missing)

    def test_every_phase_has_at_least_one_rule(self) -> None:
        for phase, rules in GATES.items():
            with self.subTest(phase=phase):
                self.assertTrue(rules)


class CommandLineTests(unittest.TestCase):
    def test_missing_corpus_returns_two(self) -> None:
        self.assertEqual(main(["extract", "--corpus", "/nonexistent"]), 2)

    def test_empty_corpus_returns_two(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(main(["extract", "--corpus", folder]), 2)

    def test_strict_returns_one_when_a_reference_is_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "PAY0100.CBL").write_text(
                "       CALL 'NOPE0001'.\n", encoding="utf-8")
            out = root / "graph.json"
            code = main([
                "extract", "--corpus", str(root), "--out", str(out),
                "--strict",
            ])
        self.assertEqual(code, 1)

    def test_merge_preserves_authored_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            build_corpus(root)
            authored = root / "graph.json"
            authored.write_text(
                json.dumps({
                    "version": 1,
                    "nodes": [node(
                        "rule:dup", "BusinessRule",
                        status="accepted", owner="Par 01")],
                    "edges": [],
                }),
                encoding="utf-8",
            )
            out = root / "merged.json"
            main([
                "extract", "--corpus", str(root), "--merge", str(authored),
                "--out", str(out),
            ])
            merged = json.loads(out.read_text(encoding="utf-8"))
        identifiers = {n["id"] for n in merged["nodes"]}
        self.assertIn("rule:dup", identifiers)
        self.assertIn("cobol:PAY0100", identifiers)


if __name__ == "__main__":
    unittest.main()
