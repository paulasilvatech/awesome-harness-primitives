# SIFAP phase gates

Each loop declares entry criteria, exit criteria, typical defects, and the checks that produce evidence.
Exit criteria are observable: every item is decided by a command, a query, or an inspected artifact.
None of them is satisfied by a produced-artifact count.

Replace `<graph>` with the slice graph path and `<slice>` with the slice identifier in every command.

## L0 archaeology

**Pair:** Day 1 kickoff. **Lead:** `sifap-archaeologist`. **Budget:** 3 inner iterations.

**Entry:** an agreed legacy scope and read access to the Natural/Adabas corpus.

### L0 exit criteria

| # | Criterion | Check |
| --- | --- | --- |
| A0 | Every recognized member and DDM file in the corpus was scanned, and every unresolved extraction note is answered or accepted. | `sifap_loop_extract.py --strict`; verify `extraction.recognizedFiles` against the corpus inventory. |
| A1 | Every inspected artifact is listed with its type and evidence path. | Inventory table review. |
| A2 | Every behavior claim cites an inspected file and line range. | Reviewer spot-check against source. |
| A3 | Every rule candidate has an incoming `DERIVES_RULE` edge from a legacy node. | `gate --phase archaeology` |
| A4 | Field formats were compared against DDM or FDT definitions where both exist. | Mismatch table present or explicitly empty. |
| A5 | Unresolved domain meaning is recorded as an open question, not as a claim. | Open-question list review. |

A0 covers the whole corpus; A1 to A5 cover the scope the pair chose to read in depth. Both are required:
a deep reading of one member proves nothing about the members nobody opened.

**Typical defects:** inferred purpose promoted to observed behavior; a `CALLNAT` target never opened;
packed decimal read as floating point; MU/PE occurrence semantics dropped; a corpus mapped only where
somebody happened to look.

### L0 commands

```bash
python3 scripts/sifap_loop_extract.py --corpus <legacy-root> --slice <slice> --out <graph>
python3 scripts/sifap_loop_graph.py validate --graph <graph>
python3 scripts/sifap_loop_graph.py gate --graph <graph> --phase archaeology
python3 scripts/sifap_loop_graph.py query --graph <graph> --query dead-legacy
python3 scripts/sifap_loop_graph.py query --graph <graph> --query slice-order
```

## L1 vision

**Pair:** Par 01, Product Owner and Requirements Engineer. **Lead:** `sifap-architect`. **Budget:** 2 inner iterations.

**Entry:** archaeology gate closed, and rule candidates exist with evidence.

### L1 exit criteria

| # | Criterion | Check |
| --- | --- | --- |
| V1 | No rule candidate is left with status `open`. | `gate --phase vision` |
| V2 | Every accepted candidate has a named owner and a stated business outcome. | Node `owner` attribute present. |
| V3 | Every rejected or deferred candidate records why, so it is not rediscovered later. | Node `note` attribute present. |
| V4 | Acceptance intent is expressed as observable behavior, not as an implementation instruction. | Reviewer reading of the candidate list. |
| V5 | Slice boundaries are declared, so downstream gates can be scoped. | Nodes carry a `slice` value. |

**Typical defects:** the whole backlog accepted without prioritization; scope defined by legacy program
count instead of by business outcome; acceptance written as "migrate PAY0100".

### L1 commands

```bash
python3 scripts/sifap_loop_graph.py gate --graph <graph> --phase vision --slice <slice>
```

## L2 architecture

**Pair:** Par 02, Enterprise Architect and Software Architect. **Lead:** `sifap-architect`. **Budget:** 3 inner iterations.

**Entry:** vision gate closed, and accepted rule candidates carry owners.

### L2 exit criteria

| # | Criterion | Check |
| --- | --- | --- |
| C1 | Every requirement has a source: an incoming `SATISFIED_BY` edge or an explicit `greenfield` flag. | `gate --phase architecture` |
| C2 | Every requirement passes EARS form and `source_legacy` validation. | `validate_traceability.py` from `sifap-requirements-traceability`. |
| C3 | Every binding technical choice has a `Decision` node with a `DECIDED_BY` edge. | `gate --phase architecture` |
| C4 | Bounded contexts and module boundaries are declared before implementation starts. | Architecture artifact review. |
| C5 | Unresolved meaning from L0 was answered or explicitly deferred with an owner. | Open-question list closed out. |

**Typical defects:** one requirement hiding two behaviors; a `source_legacy` path adjusted to make the
validator pass; a dependency added without a decision record; MU/PE storage decided implicitly in code.

### L2 commands

Run the requirement validator bundled with `sifap-requirements-traceability`, then the graph gate.

```bash
python3 scripts/sifap_loop_graph.py gate --graph <graph> --phase architecture --slice <slice>
```

## L3 implementation

**Pair:** Par 03, Technical Lead and Developer. **Lead:** `sifap-builder`. **Budget:** 3 inner iterations.

**Entry:** architecture gate closed, and the slice is bounded.

### L3 exit criteria

| # | Criterion | Check |
| --- | --- | --- |
| I1 | Every in-scope requirement has an `IMPLEMENTED_BY` edge to a target node. | `gate --phase implementation` |
| I2 | The build and the focused tests for the slice pass. | Project build and test commands. |
| I3 | Behavior differences from the legacy system are classified as defect or accepted deviation. | Drift table with an owner per row. |
| I4 | No requirement outside the slice was implemented opportunistically. | Diff review against the slice scope. |
| I5 | Numeric, date, and occurrence semantics follow the recorded decisions. | Code review against the L2 decisions. |

**Typical defects:** scope creep into the next slice; a test written after the fact to match the code;
monetary values mapped to binary floating point; a no-record legacy branch silently dropped.

### L3 commands

```bash
python3 scripts/sifap_loop_graph.py gate --graph <graph> --phase implementation --slice <slice>
python3 scripts/sifap_loop_graph.py query --graph <graph> --query blast-radius --node <node-id>
```

## L4 quality

**Pair:** Par 04, DBA and QA Engineer. **Lead:** `sifap-quality`. **Budget:** 3 inner iterations.

**Entry:** implementation gate closed with build and test evidence.

### L4 exit criteria

| # | Criterion | Check |
| --- | --- | --- |
| Q1 | Every in-scope requirement has a `VERIFIED_BY` edge to a test node. | `gate --phase quality` |
| Q2 | Every in-scope Adabas file has a `MIGRATES_TO` edge to a target table. | `gate --phase quality` |
| Q3 | Every migrated field keeps its precision, scale, and occurrence semantics. | Mapping review against DDM or FDT. |
| Q4 | Legacy and target outputs reconcile on record counts and monetary totals for the same input. | Reconciliation run with recorded actual numbers. |
| Q5 | Fixtures are synthetic and contain no production or regulated data. | Fixture review. |

**Typical defects:** a descriptor treated as a primary key; an MU field flattened into a delimited
string; reconciliation declared without recorded totals; production extract used as a fixture.

### L4 commands

```bash
python3 scripts/sifap_loop_graph.py gate --graph <graph> --phase quality --slice <slice>
python3 scripts/sifap_loop_graph.py query --graph <graph> --query coverage --slice <slice>
```

## L5 operations

**Pair:** Par 05, DevOps Engineer and Tech Writer. **Lead:** `sifap-operations`. **Budget:** 2 inner iterations.

**Entry:** quality gate closed with reconciliation evidence.

### L5 exit criteria

| # | Criterion | Check |
| --- | --- | --- |
| O1 | Every exposed endpoint has a `DEPLOYED_BY` edge to a pipeline or workflow node. | `gate --phase operations` |
| O2 | Every decision from L2 has a `DOCUMENTED_BY` edge to a published record. | `gate --phase operations` |
| O3 | Pipeline actions are pinned and identity uses a workload or managed identity. | Workflow and infrastructure review. |
| O4 | Required human approvals for merge, deployment, and infrastructure are recorded. | Approval evidence with names and dates. |
| O5 | Residual risks carry an owner and a next checkpoint. | Retrospective record. |

**Typical defects:** an unpinned action tag; a secret in Terraform state output; a merge recorded as
approved without a reviewer; a runbook that documents the intent instead of the deployed behavior.

### L5 commands

```bash
python3 scripts/sifap_loop_graph.py gate --graph <graph> --phase operations --slice <slice>
```
