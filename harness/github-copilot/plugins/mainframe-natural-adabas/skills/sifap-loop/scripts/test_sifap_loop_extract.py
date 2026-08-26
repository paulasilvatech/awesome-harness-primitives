from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sifap_loop_extract import extract, main  # noqa: E402
from sifap_loop_graph import Graph, query, validate  # noqa: E402

PROGRAM = """\
* PAY0100 - payment inspection driver
DEFINE DATA
LOCAL USING PAYL001
END-DEFINE
INCLUDE PAYC001
INPUT USING MAP 'PAYM001'
CALLNAT 'PAY0110' #PAYMENT-ID
PERFORM PAYS001
END
"""

SUBPROGRAM = """\
DEFINE DATA
LOCAL
01 PAYMENT-VIEW VIEW OF PAYMENT
02 PAYMENT-ID
END-DEFINE
READ PAYMENT-VIEW BY PAYMENT-ID
  STORE PAYMENT-VIEW
END-READ
* CALLNAT 'GHOST0001' commented out and must be ignored
UPDATE
END
"""

DDM = """\
DB: 001 FILE: 010 - PAYMENT   DEFAULT SEQUENCE:
TYPE: ADABAS
  1 AA PAYMENT-ID   N  8  D
"""

JOB = """\
//PAYJOB JOB
//STEP1 EXEC NATBATCH,PROGRAM=PAY0100
"""


def build_corpus(root: Path) -> None:
    (root / "PAY0100.NSP").write_text(PROGRAM, encoding="utf-8")
    (root / "PAY0110.NSN").write_text(SUBPROGRAM, encoding="utf-8")
    (root / "PAYS001.NSS").write_text(
        "DEFINE SUBROUTINE X\nEND\n", encoding="utf-8")
    (root / "PAYC001.NSC").write_text("* copycode\n", encoding="utf-8")
    (root / "PAYM001.NSM").write_text("* map\n", encoding="utf-8")
    (root / "PAYL001.NSA").write_text("* data area\n", encoding="utf-8")
    (root / "PAYMENT.NSD").write_text(DDM, encoding="utf-8")
    (root / "PAYJOB.JCL").write_text(JOB, encoding="utf-8")


class ExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        build_corpus(self.root)
        self.builder = extract(self.root, "001-payment-inspection")
        self.edges = {
            (edge["from"], edge["type"], edge["to"])
            for edge in self.builder.edges.values()
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_every_member_becomes_a_node_with_evidence(self) -> None:
        for identifier in (
            "natural:PAY0100", "natural:PAY0110", "natural:PAYS001",
            "natural:PAYC001", "natural:PAYM001", "natural:PAYL001",
            "jcl:PAYJOB", "ddm:PAYMENT", "adabas:PAYMENT",
        ):
            with self.subTest(node=identifier):
                node = self.builder.nodes[identifier]
                self.assertTrue(node["evidence"])
                self.assertEqual(node["slice"], "001-payment-inspection")

    def test_structural_edges_are_extracted(self) -> None:
        for edge in (
            ("natural:PAY0100", "CALLNAT", "natural:PAY0110"),
            ("natural:PAY0100", "PERFORM", "natural:PAYS001"),
            ("natural:PAY0100", "INCLUDE", "natural:PAYC001"),
            ("natural:PAY0100", "USES_MAP", "natural:PAYM001"),
            ("natural:PAY0100", "USES_DATA_AREA", "natural:PAYL001"),
            ("jcl:PAYJOB", "RUNS", "natural:PAY0100"),
            ("adabas:PAYMENT", "DEFINED_BY", "ddm:PAYMENT"),
        ):
            with self.subTest(edge=edge):
                self.assertIn(edge, self.edges)

    def test_view_declarations_resolve_data_access(self) -> None:
        self.assertIn(
            ("natural:PAY0110", "READS", "adabas:PAYMENT"), self.edges)
        self.assertIn(
            ("natural:PAY0110", "STORES", "adabas:PAYMENT"), self.edges)

    def test_comments_are_ignored(self) -> None:
        targets = {edge[2] for edge in self.edges}
        self.assertNotIn("natural:GHOST0001", targets)

    def test_bare_update_is_reported_instead_of_guessed(self) -> None:
        self.assertTrue(
            any("bare UPDATE" in note for note in self.builder.unresolved),
            self.builder.unresolved,
        )
        self.assertNotIn(
            ("natural:PAY0110", "UPDATES", "adabas:PAYMENT"), self.edges)

    def test_every_edge_carries_a_line_anchor(self) -> None:
        for edge in self.builder.edges.values():
            if edge["type"] == "DEFINED_BY":
                continue
            with self.subTest(edge=edge["type"]):
                self.assertIn("#L", edge["evidence"])

    def test_missing_callnat_target_is_unresolved(self) -> None:
        (self.root / "PAY0100.NSP").write_text(
            "CALLNAT 'NOPE0001'\n", encoding="utf-8")
        builder = extract(self.root, None)
        self.assertTrue(
            any("NOPE0001" in note for note in builder.unresolved),
            builder.unresolved,
        )


class GraphContractTests(unittest.TestCase):
    """The extractor must emit what the graph tool accepts."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        build_corpus(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def extracted(self) -> Graph:
        out = self.root / "graph.json"
        main(["--corpus", str(self.root), "--out", str(out)])
        return Graph(json.loads(out.read_text(encoding="utf-8")))

    def test_extracted_graph_passes_validation(self) -> None:
        self.assertEqual(validate(self.extracted()), [])

    def test_extraction_records_recognized_corpus_coverage(self) -> None:
        graph = self.extracted()
        extraction = graph.document["extraction"]
        self.assertEqual(extraction["memberFiles"], 7)
        self.assertEqual(extraction["ddmFiles"], 1)
        self.assertEqual(extraction["recognizedFiles"], 8)
        self.assertEqual(len(extraction["unresolved"]), 1)

    def test_slice_order_places_callee_before_caller(self) -> None:
        components = query(
            self.extracted(), "slice-order", None, None)["components"]
        order = [member for group in components for member in group]
        self.assertLess(
            order.index("natural:PAY0110"), order.index("natural:PAY0100"))

    def test_dead_legacy_finds_the_unreferenced_member(self) -> None:
        (self.root / "ORPHAN01.NSN").write_text("END\n", encoding="utf-8")
        result = query(self.extracted(), "dead-legacy", None, None)
        self.assertIn("natural:ORPHAN01", result["unreferenced"])


class MergeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        build_corpus(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_merge_preserves_authored_nodes(self) -> None:
        authored = self.root / "graph.json"
        authored.write_text(
            json.dumps({
                "version": 1,
                "nodes": [{
                    "id": "rule:duplicate-line",
                    "type": "BusinessRule",
                    "evidence": "rules/duplicate-line.md",
                    "status": "accepted",
                    "owner": "Par 01",
                }],
                "edges": [],
            }),
            encoding="utf-8",
        )
        out = self.root / "merged.json"
        code = main([
            "--corpus", str(self.root), "--merge", str(authored),
            "--out", str(out),
        ])
        merged = json.loads(out.read_text(encoding="utf-8"))
        rule = next(
            n for n in merged["nodes"] if n["id"] == "rule:duplicate-line")
        self.assertEqual(code, 0)
        self.assertEqual(rule["owner"], "Par 01")
        self.assertIn("natural:PAY0100", {n["id"] for n in merged["nodes"]})

    def test_merge_does_not_duplicate_an_existing_edge(self) -> None:
        first = self.root / "first.json"
        main(["--corpus", str(self.root), "--out", str(first)])
        before = len(json.loads(first.read_text(encoding="utf-8"))["edges"])
        second = self.root / "second.json"
        main([
            "--corpus", str(self.root), "--merge", str(first),
            "--out", str(second),
        ])
        after = len(json.loads(second.read_text(encoding="utf-8"))["edges"])
        self.assertEqual(before, after)


class CommandLineTests(unittest.TestCase):
    def test_missing_corpus_returns_two(self) -> None:
        self.assertEqual(main(["--corpus", "/nonexistent/corpus"]), 2)

    def test_empty_corpus_returns_two(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(main(["--corpus", folder]), 2)

    def test_strict_returns_one_when_a_reference_is_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "PAY0100.NSP").write_text(
                "CALLNAT 'NOPE0001'\n", encoding="utf-8")
            out = root / "graph.json"
            code = main([
                "--corpus", str(root), "--out", str(out), "--strict",
            ])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
