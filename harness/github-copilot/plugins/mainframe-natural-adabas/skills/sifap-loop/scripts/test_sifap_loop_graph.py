from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sifap_loop_graph import (  # noqa: E402
    GATES,
    Graph,
    gate,
    main,
    mermaid,
    query,
    validate,
)

EXAMPLE = Path(__file__).resolve().parents[1] / "assets" / "graph-example.json"
SLICE = "001-payment-inspection"


def node(node_id: str, node_type: str, **extra: object) -> dict[str, object]:
    return {
        "id": node_id,
        "type": node_type,
        "evidence": f"evidence/{node_id}.md",
        **extra,
    }


def edge(source: str, edge_type: str, target: str) -> dict[str, object]:
    return {
        "from": source,
        "type": edge_type,
        "to": target,
        "evidence": f"evidence/{source}.md#L1",
    }


def document(nodes: list[dict], edges: list[dict]) -> Graph:
    return Graph({"version": 1, "nodes": nodes, "edges": edges})


def example_graph() -> Graph:
    return Graph(json.loads(EXAMPLE.read_text(encoding="utf-8")))


class ValidationTests(unittest.TestCase):
    def test_example_graph_is_valid(self) -> None:
        self.assertEqual(validate(example_graph()), [])

    def test_rejects_unsupported_version(self) -> None:
        graph = Graph({"version": 2, "nodes": [], "edges": []})
        self.assertIn("version must equal 1", validate(graph))

    def test_rejects_node_without_evidence(self) -> None:
        graph = document([{"id": "natural:A", "type": "NaturalProgram"}], [])
        self.assertIn("natural:A: evidence is required", validate(graph))

    def test_rejects_duplicate_node_id(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram"),
             node("natural:A", "NaturalProgram")],
            [],
        )
        self.assertIn("natural:A: duplicate node id", validate(graph))

    def test_rejects_unknown_node_type(self) -> None:
        graph = document([node("x:A", "CobolProgram")], [])
        self.assertIn("x:A: unknown node type 'CobolProgram'", validate(graph))

    def test_rejects_unknown_status(self) -> None:
        graph = document([node("rule:A", "BusinessRule", status="maybe")], [])
        self.assertIn("rule:A: unknown status 'maybe'", validate(graph))

    def test_rejects_edge_to_unknown_node(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram")],
            [edge("natural:A", "CALLNAT", "natural:B")],
        )
        findings = validate(graph)
        self.assertTrue(
            any("unknown target node" in item for item in findings), findings)

    def test_rejects_edge_without_evidence(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram"),
             node("natural:B", "NaturalSubprogram")],
            [{"from": "natural:A", "type": "CALLNAT", "to": "natural:B"}],
        )
        findings = validate(graph)
        self.assertTrue(
            any("evidence is required" in item for item in findings), findings)

    def test_rejects_disallowed_endpoint_types(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram"),
             node("pg:payment", "PgTable")],
            [edge("natural:A", "CALLNAT", "pg:payment")],
        )
        findings = validate(graph)
        self.assertTrue(
            any("does not allow" in item for item in findings), findings)

    def test_rejects_unknown_edge_type(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram"),
             node("natural:B", "NaturalSubprogram")],
            [edge("natural:A", "INVOKES", "natural:B")],
        )
        findings = validate(graph)
        self.assertTrue(
            any("unknown edge type" in item for item in findings), findings)


class GateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = example_graph()

    def test_every_phase_gate_passes_on_the_example(self) -> None:
        for phase in GATES:
            with self.subTest(phase=phase):
                self.assertTrue(gate(self.graph, phase, SLICE)["passed"])

    def test_slice_scope_excludes_other_slices(self) -> None:
        result = gate(self.graph, "quality", "002-other")
        self.assertTrue(result["passed"])
        self.assertEqual(
            [entry["subjects"] for entry in result["rules"]], [0, 0])

    def test_quality_gate_reports_unverified_requirement(self) -> None:
        graph = document([node("req:REQ-001", "Requirement", slice=SLICE)], [])
        result = gate(graph, "quality", SLICE)
        self.assertFalse(result["passed"])
        self.assertIn(
            "req:REQ-001: no outgoing VERIFIED_BY",
            result["rules"][0]["missing"],
        )

    def test_quality_gate_reports_unmigrated_adabas_file(self) -> None:
        graph = document(
            [node("adabas:PAYMENT", "AdabasFile", slice=SLICE)], [])
        result = gate(graph, "quality", SLICE)
        self.assertIn(
            "adabas:PAYMENT: no outgoing MIGRATES_TO",
            result["rules"][1]["missing"],
        )

    def test_greenfield_requirement_satisfies_architecture_gate(self) -> None:
        graph = document(
            [node("req:REQ-050", "Requirement", slice=SLICE, greenfield=True)],
            [],
        )
        self.assertTrue(gate(graph, "architecture", SLICE)["passed"])

    def test_vision_gate_rejects_open_rule(self) -> None:
        graph = document(
            [node("rule:a", "BusinessRule", slice=SLICE, status="open")], [])
        missing = gate(graph, "vision", SLICE)["rules"][0]["missing"]
        self.assertIn("rule:a: status is undecided", missing)

    def test_vision_gate_requires_owner_when_accepted(self) -> None:
        graph = document(
            [node("rule:a", "BusinessRule", slice=SLICE, status="accepted")],
            [],
        )
        missing = gate(graph, "vision", SLICE)["rules"][0]["missing"]
        self.assertIn("rule:a: accepted without an owner", missing)

    def test_vision_gate_requires_note_when_deferred(self) -> None:
        graph = document(
            [node("rule:a", "BusinessRule", slice=SLICE, status="deferred")],
            [],
        )
        missing = gate(graph, "vision", SLICE)["rules"][0]["missing"]
        self.assertIn("rule:a: deferred without a note", missing)


class QueryTests(unittest.TestCase):
    def test_slice_order_places_callee_before_caller(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram"),
             node("natural:B", "NaturalSubprogram")],
            [edge("natural:A", "CALLNAT", "natural:B")],
        )
        components = query(graph, "slice-order", None, None)["components"]
        self.assertEqual(components, [["natural:B"], ["natural:A"]])

    def test_slice_order_groups_a_call_cycle(self) -> None:
        graph = document(
            [node("natural:A", "NaturalProgram"),
             node("natural:B", "NaturalSubprogram")],
            [edge("natural:A", "CALLNAT", "natural:B"),
             edge("natural:B", "CALLNAT", "natural:A")],
        )
        components = query(graph, "slice-order", None, None)["components"]
        self.assertEqual(components, [["natural:A", "natural:B"]])

    def test_dead_legacy_ignores_jcl_entry_points(self) -> None:
        graph = document(
            [node("jcl:JOB", "JclJob"),
             node("natural:A", "NaturalProgram"),
             node("natural:ORPHAN", "NaturalSubprogram")],
            [edge("jcl:JOB", "RUNS", "natural:A")],
        )
        result = query(graph, "dead-legacy", None, None)
        self.assertEqual(result["unreferenced"], ["natural:ORPHAN"])

    def test_blast_radius_reports_both_directions(self) -> None:
        result = query(example_graph(), "blast-radius", "adabas:PAYMENT", None)
        self.assertIn("pg:payment", result["depends_on"])
        self.assertIn("natural:PAY0100", result["depended_on_by"])

    def test_coverage_counts_subjects_per_rule(self) -> None:
        rows = query(example_graph(), "coverage", None, SLICE)["coverage"]
        by_rule = {row["rule"]: row for row in rows}
        self.assertEqual(by_rule["Q1"]["subjects"], 1)
        self.assertEqual(by_rule["Q1"]["missing"], 0)


class RenderTests(unittest.TestCase):
    def test_mermaid_renders_every_node_by_default(self) -> None:
        output = mermaid(example_graph(), None, 1)
        self.assertTrue(output.startswith("flowchart LR"))
        self.assertIn("n_natural_PAY0100", output)
        self.assertIn("-->|CALLNAT|", output)

    def test_focus_limits_the_rendered_neighborhood(self) -> None:
        output = mermaid(example_graph(), "natural:PAY0100", 1)
        self.assertIn("n_natural_PAY0110", output)
        self.assertNotIn("n_pg_payment_amount", output)


class CommandLineTests(unittest.TestCase):
    def test_validate_returns_zero_for_the_example(self) -> None:
        self.assertEqual(main(["validate", "--graph", str(EXAMPLE)]), 0)

    def test_gate_returns_one_when_a_rule_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "graph.json"
            path.write_text(
                json.dumps({
                    "version": 1,
                    "nodes": [node("req:REQ-001", "Requirement", slice=SLICE)],
                    "edges": [],
                }),
                encoding="utf-8",
            )
            exit_code = main([
                "gate", "--graph", str(path), "--phase", "quality",
                "--slice", SLICE,
            ])
        self.assertEqual(exit_code, 1)

    def test_missing_graph_file_returns_two(self) -> None:
        self.assertEqual(
            main(["validate", "--graph", "/nonexistent/graph.json"]), 2)

    def test_invalid_json_returns_two(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "graph.json"
            path.write_text("{", encoding="utf-8")
            self.assertEqual(main(["validate", "--graph", str(path)]), 2)


if __name__ == "__main__":
    unittest.main()
