# SIFAP engineering graph

One JSON document links legacy Natural and Adabas artifacts to business rules, requirements, target
code, tests, and delivery. Every phase adds nodes and edges to the same document, so each gate is a
query rather than an assertion, and coverage is computed from recorded evidence.

## Document shape

```json
{
  "version": 1,
  "nodes": [
    {
      "id": "natural:PAY0100",
      "type": "NaturalProgram",
      "label": "PAY0100",
      "evidence": "01-archaeology/legacy-sifap/natural-programs/PAY0100.NSP",
      "slice": "001-payment-inspection"
    }
  ],
  "edges": [
    {
      "from": "natural:PAY0100",
      "type": "CALLNAT",
      "to": "natural:PAY0110",
      "evidence": "01-archaeology/legacy-sifap/natural-programs/PAY0100.NSP#L120"
    }
  ]
}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `version` | yes | Document format version. Only `1` is accepted. |
| `nodes[].id` | yes | Unique identifier. Use the `namespace:name` convention below. |
| `nodes[].type` | yes | One value from the node vocabulary. |
| `nodes[].evidence` | yes | Path, path with line anchor, or command reference proving the node exists. |
| `nodes[].label` | no | Display name. Defaults to the id. |
| `nodes[].slice` | no | Slice identifier used by `--slice` scoping. |
| `nodes[].status` | no | `open`, `accepted`, `rejected`, or `deferred`. Required on `BusinessRule` by the vision gate. |
| `nodes[].greenfield` | no | Boolean. On a `Requirement`, satisfies the architecture gate without a legacy source. |
| `nodes[].owner` | no | Person or pair accountable. Required on accepted rules by the vision gate. |
| `nodes[].note` | no | Short rationale. Required on rejected or deferred rules by the vision gate. |
| `edges[].from`, `edges[].to` | yes | Existing node ids. |
| `edges[].type` | yes | One value from the edge vocabulary, with endpoints matching the table below. |
| `edges[].evidence` | yes | Path or line anchor proving the relationship. |

Identifier convention: `natural:`, `jcl:`, `adabas:`, `ddm:`, `rule:`, `req:`, `adr:`, `java:`, `api:`,
`pg:`, `test:`, `ci:`, `infra:`, `doc:`. The convention is not enforced; uniqueness and evidence are.

## Node vocabulary

| Layer | Types |
| --- | --- |
| Legacy code | `NaturalProgram`, `NaturalSubprogram`, `NaturalSubroutine`, `Copycode`, `Map`, `DataArea`, `JclJob` |
| Legacy data | `Ddm`, `AdabasFile`, `AdabasField`, `Descriptor` |
| Bridge | `BusinessRule`, `Requirement`, `Decision` |
| Target | `JavaType`, `Endpoint`, `PgTable`, `PgColumn`, `Test`, `Workflow`, `InfraResource`, `Runbook` |

## Edge vocabulary

Edge names read as `from <type> to`: `Requirement VERIFIED_BY Test`.

| Type | From | To |
| --- | --- | --- |
| `CALLNAT` | `NaturalProgram`, `NaturalSubprogram` | `NaturalProgram`, `NaturalSubprogram` |
| `PERFORM` | `NaturalProgram`, `NaturalSubprogram` | `NaturalSubroutine` |
| `INCLUDE` | `NaturalProgram`, `NaturalSubprogram` | `Copycode` |
| `USES_MAP` | `NaturalProgram`, `NaturalSubprogram` | `Map` |
| `USES_DATA_AREA` | `NaturalProgram`, `NaturalSubprogram`, `Copycode` | `DataArea` |
| `RUNS` | `JclJob` | `NaturalProgram` |
| `READS`, `UPDATES`, `STORES`, `DELETES` | `NaturalProgram`, `NaturalSubprogram` | `AdabasFile` |
| `DEFINED_BY` | `AdabasFile` | `Ddm` |
| `HAS_FIELD` | `AdabasFile` | `AdabasField` |
| `INDEXED_BY` | `AdabasFile` | `Descriptor` |
| `DERIVES_RULE` | any legacy layer node | `BusinessRule` |
| `SATISFIED_BY` | `BusinessRule` | `Requirement` |
| `DECIDED_BY` | `Requirement` | `Decision` |
| `IMPLEMENTED_BY` | `Requirement` | `JavaType`, `Endpoint`, `PgTable` |
| `VERIFIED_BY` | `Requirement` | `Test` |
| `MIGRATES_TO` | `AdabasFile` to `PgTable`, `AdabasField` to `PgColumn` | see left |
| `EXPOSED_BY` | `JavaType` | `Endpoint` |
| `DEPLOYED_BY` | `Endpoint`, `InfraResource` | `Workflow` |
| `DOCUMENTED_BY` | `Decision` | `Runbook` |

Call edges used for ordering and reachability are `CALLNAT`, `PERFORM`, `INCLUDE`, `USES_MAP`,
`USES_DATA_AREA`, and `RUNS`.

## Validation rules

`validate` fails when any of these is true:

- `version` is absent or is not `1`.
- A node id is missing, empty, or duplicated.
- A node type is outside the vocabulary.
- A node has no `evidence` value.
- An edge references an unknown node id.
- An edge type is outside the vocabulary, or its endpoint types are not allowed for that type.
- An edge has no `evidence` value.
- A `status` value is outside `open`, `accepted`, `rejected`, `deferred`.

Validation proves the document is well formed. It does not prove the evidence paths exist in the target
repository; the phase gate and the reviewer do that.

## Gate queries

| Phase | Subject | Required | Reported failure |
| --- | --- | --- | --- |
| `archaeology` | `BusinessRule` | Incoming `DERIVES_RULE` | Rule candidate without legacy evidence |
| `vision` | `BusinessRule` | `status` set and not `open`; `owner` when accepted; `note` when rejected or deferred | Undecided or unowned rule candidate |
| `architecture` | `Requirement` | Incoming `SATISFIED_BY`, or `greenfield` set to `true` | Requirement without a source |
| `architecture` | `Decision` | Incoming `DECIDED_BY` | Decision record nothing points to |
| `implementation` | `Requirement` | Outgoing `IMPLEMENTED_BY` | Requirement with no implementation |
| `quality` | `Requirement` | Outgoing `VERIFIED_BY` | Unverified requirement |
| `quality` | `AdabasFile` | Outgoing `MIGRATES_TO` | Legacy file with no target mapping |
| `operations` | `Endpoint` | Outgoing `DEPLOYED_BY` | Endpoint with no pipeline |
| `operations` | `Decision` | Outgoing `DOCUMENTED_BY` | Undocumented decision |

`--slice <value>` restricts subjects to nodes carrying that `slice` value. Without it, the gate covers
every node and the result is reported as unscoped.

A gate with zero subjects passes vacuously and is reported as `0 subjects`. Read that as missing
evidence, not as coverage.

## Analysis queries

| Query | Answer | Loop use |
| --- | --- | --- |
| `slice-order` | Strongly connected components over call edges, in dependency order | Sequence slices so a component is migrated after what it depends on. A component with more than one member is a call cycle that cannot be split. |
| `dead-legacy` | Legacy nodes with no incoming call edge, excluding `JclJob` entry points | Candidates for exclusion from scope; confirm against the corpus before dropping anything. |
| `blast-radius --node <id>` | Forward and reverse reachability over every edge | Size the impact of changing or retiring one artifact. |
| `coverage` | Subject, satisfied, and missing counts per gate rule | Track loop progress without counting produced files. |

## Rendering

`mermaid` prints a `flowchart LR` with one class per layer. Use `--focus <id> --depth <n>` to render a
neighborhood instead of the whole graph; a full SIFAP graph is unreadable as a single diagram.
