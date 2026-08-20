# Power BI Source (`powerBiSource-v1`)

Creates an Activator source over a Power BI report visual / semantic model measure. Power BI-backed Activator alerts store a JSON-string query contract in `query.queryString` plus a `metricDefinition` blob that describes the semantic model metric, dimensions, filters, and lineage back to the report visual.

> **Design principle:** Scope Power BI-backed alerts to a report/page/visual whenever possible. PBIR/report definitions provide visual bindings and metadata; they do not contain a ready-to-run Activator source query.

> **Build deterministically:** Derive the query and metric definition from report visual bindings and semantic model metadata. Use Activator `updateDefinition` as the validation and persistence gate.

> **Activator API requirement:** `powerBiSource-v1.query.queryString` must be the Power BI source query payload expected by Activator. Activator does not accept semantic-model query text in this field.

> **Container requirement:** The parent `container-v1` must use exact case-sensitive `payload.type: "pbiMetrics"`. Do not use `powerBiQueries`; it is not a valid ALM `ContainerPayloadType` and fails before the Power BI source provider runs.

> **Personalization rule:** If the alert text or source card names a dimension value, the source payload must include that value in `source.dimensionValue`, in the stored query filter, and in `metricDefinition.definition.filter`. Do not store personalization only in display text.

> **Metric-definition filter contract:** `metricDefinition.definition.filter` uses the Power BI semantic-query filter shape (`Version`, `From`, and `Where`), not a report/API `BasicFilter` object. A `BasicFilter` can contain the expected value yet still be rejected during Activator definition import.

> **Current readback limitation:** Do not rely on Activator `getDefinition` to round-trip Power BI sources yet. Public ALM import can persist a `powerBiSource-v1`, while ALM export/readback can reject the same artifact when PBI ALM export is disabled. In that state, an empty or unavailable readback is not proof that import failed. Report the successful `updateDefinition` response and the separate export/readback limitation explicitly.

> **Persistence success gate:** For the current Power BI authoring path, do not
> claim persistence unless `updateDefinition` returns HTTP `200`. Use a
> header-aware request so the status is explicit. Treat every `4xx`/`5xx`,
> `Activator_Alm_*` error, or nonzero native-command exit as failure and stop;
> a locally valid payload or an existing empty Activator item is not evidence
> that the definition persisted. If the API returns `202`, poll the LRO and
> require terminal success before continuing.

For example, a filter for `SalesTransactions.region = East` uses:

```json
{
  "Version": 2,
  "From": [
    {
      "Name": "s",
      "Entity": "SalesTransactions",
      "Type": 0
    }
  ],
  "Where": [
    {
      "Condition": {
        "In": {
          "Expressions": [
            {
              "Column": {
                "Expression": {
                  "SourceRef": {
                    "Source": "s"
                  }
                },
                "Property": "region"
              }
            }
          ],
          "Values": [
            [
              {
                "Literal": {
                  "Value": "'East'"
                }
              }
            ]
          ]
        }
      }
    }
  ]
}
```

## Source Entity Shape

The exact service readback can include additional service-managed fields. Preserve existing service-managed fields when doing read-modify-write updates.

Create this parent container first:

```json
{
  "uniqueIdentifier": "<container-guid>",
  "payload": {
    "name": "Power BI metric sources",
    "type": "pbiMetrics"
  },
  "type": "container-v1"
}
```

Then build the metric definition and query as normal Python dictionaries using
the readable JSON shapes below. Only stringify them when assigning the two
string-valued source fields:

```python
import json

metric_definition = {
    # Use the readable DatasetMetric shape from the metricDefinition section.
}
metric_query = {
    # Use the readable stored query shape from the next section.
    "provider": {
        "datasetId": "<semantic-model-id>",
        "metric": metric_definition,
    },
}

source = {
    "uniqueIdentifier": "<powerbi-source-guid>",
    "payload": {
        "name": "Revenue by division",
        "runSettings": {"executionIntervalInSeconds": 300},
        "query": {
            "queryString": json.dumps(metric_query, separators=(",", ":"))
        },
        "metricDefinition": json.dumps(
            metric_definition, separators=(",", ":")
        ),
        "datasetId": "<semantic-model-id>",
        "reportWorkspaceId": "<report-workspace-id>",
        "reportId": "<report-id>",
        "pageId": "<page-id>",
        "visualId": "<visual-id>",
        "measureName": "Revenue",
        "dimensionValue": "East",
        "metadata": {
            "datasetId": "<semantic-model-id>",
            "reportWorkspaceId": "<report-workspace-id>",
            "reportId": "<report-id>",
            "pageId": "<page-id>",
            "visualId": "<visual-id>",
            "measureName": "Revenue",
        },
        "parentContainer": {
            "targetUniqueIdentifier": "<container-guid>"
        },
    },
    "type": "powerBiSource-v1",
}
```

The examples remain formatted as objects for readability, but the final
`query.queryString` and `metricDefinition` values sent in
`ReflexEntities.json` must be JSON strings.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | yes | Display name for the Activator source |
| `runSettings.executionIntervalInSeconds` | integer | yes | Poll frequency in seconds |
| `query.queryString` | string | yes | JSON-string Power BI source query payload |
| `metricDefinition` | string or object | yes | `DatasetMetric` definition; existing readbacks may store this as a JSON string |
| `datasetId` / `metadata.datasetId` | GUID | yes | Power BI semantic model / dataset ID |
| `reportWorkspaceId` / `metadata.reportWorkspaceId` | GUID or service value | yes | Workspace containing the report; `me` can appear in My Workspace readbacks |
| `reportId` / `metadata.reportId` | GUID | recommended | Report containing the selected visual |
| `pageId` / `metadata.pageId` | string | recommended | Page containing the selected visual |
| `visualId` / `metadata.visualId` | string | recommended | Selected visual ID |
| `measureName` / `metadata.measureName` | string | yes | Selected measure or implicit measure display name |
| `dimensionValue` | scalar | conditional | Required when the source is personalized to a specific dimension value |
| `parentContainer.targetUniqueIdentifier` | GUID | yes | Container ref for hand-authored graphs |

## Authoring Workflow

1. Resolve workspace and item IDs dynamically. Do not hardcode report, semantic model, or Activator IDs.
2. Read report definition:

   ```bash
   az rest --method POST \
     --url "https://api.fabric.microsoft.com/v1/workspaces/${REPORT_WS_ID}/reports/${REPORT_ID}/getDefinition" \
     --resource "https://api.fabric.microsoft.com" \
     --headers "Content-Type=application/json" \
     --body '{}'
   ```

3. Read semantic model definition:

   ```bash
   az rest --method POST \
     --url "https://api.fabric.microsoft.com/v1/workspaces/${MODEL_WS_ID}/semanticModels/${DATASET_ID}/getDefinition" \
     --resource "https://api.fabric.microsoft.com" \
     --headers "Content-Type=application/json" \
     --body '{}'
   ```

4. Extract visual bindings from the scoped report page/visual:
   - measure/value field
   - category or group-by dimensions
   - date/time axis, if the visual uses one
   - visual/page/report filters
   - title and labels used for generated alert text
5. Resolve bound fields against semantic model metadata. Use `semantic-model-consumption` metadata discovery patterns if model metadata lookup is needed.
6. Optionally sample low-cardinality dimension values through supported Power BI query surfaces so a personalized alert can use a real value. Treat those samples only as discovery inputs.

7. Build the candidate source deterministically:
   - selected measure
   - selected dimensions
   - optional dimension value
   - rule condition
   - title/description
8. Hydrate `query.queryString` and `metricDefinition`.
9. Ensure the persisted source query omits `top`.
10. Persist the source, capture the HTTP status explicitly, and
    continue only after HTTP `200` (or a terminally successful `202` LRO).

## Stored Query Shape

`query.queryString` is a JSON string that represents the Power BI source query persisted inside the Activator definition.

```json
{
  "version": "V1",
  "provider": {
    "datasetId": "<semantic-model-id>",
    "metric": {
      "name": "Revenue",
      "definition": {
        "datasetId": "<semantic-model-id>",
        "aggregation": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Sales" } },
            "Property": "Revenue"
          },
          "Name": "Revenue"
        },
        "dimensions": [
          {
            "Column": {
              "Expression": { "SourceRef": { "Entity": "Division" } },
              "Property": "Division Name"
            },
            "Name": "Division Name"
          }
        ],
        "filter": {
          "Version": 2,
          "From": [
            { "Name": "d", "Entity": "Division", "Type": 0 }
          ],
          "Where": [
            {
              "Condition": {
                "In": {
                  "Expressions": [
                    {
                      "Column": {
                        "Expression": { "SourceRef": { "Source": "d" } },
                        "Property": "Division Name"
                      }
                    }
                  ],
                  "Values": [
                    [{ "Literal": { "Value": "'East'" } }]
                  ]
                }
              }
            }
          ]
        }
      },
      "type": "DatasetMetric"
    }
  },
  "metrics": [{ "measure": "Revenue", "table": "Sales" }],
  "groupBy": [{ "table": "Division", "column": "Division Name" }],
  "filters": [
    {
      "target": [{ "table": "Division", "column": "Division Name" }],
      "in": [["East"]]
    }
  ]
}
```

### Query fields

| Field | Guidance |
|-------|----------|
| `provider.datasetId` | Semantic model ID |
| `provider.metric` | Inline `DatasetMetric` matching the source metric definition |
| `metrics` | Projection; use measure references or aggregations |
| `groupBy` | Dimension columns to return |
| `filters` | Filters that match report/visual filters and personalization |
| `top` | Omit from the persisted source |

The typed expression shapes used by the stored query include:

```json
{ "measure": "Revenue", "table": "Sales" }
{ "column": "Division Name", "table": "Division" }
{ "function": 2, "aggregate": { "table": "Sales", "column": "Revenue" } }
```

### Function ID mappings

Use the correct enum for the payload field you are writing. The stored query aggregation expression uses a smaller enum than the semantic model aggregation object inside `metricDefinition`.

#### Stored query aggregation (`query.queryString.metrics[].function`)

| ID | Name | Use |
|----|------|-----|
| `1` | `Min` | Minimum value |
| `2` | `Max` | Maximum value |
| `3` | `Count` | Count rows / values |
| `4` | `Any` | Any representative value |

#### Semantic model aggregation (`metricDefinition.definition.aggregation.Function`)

| ID | Name | Use |
|----|------|-----|
| `0` | `Sum` | Sum numeric values |
| `1` | `Avg` / `Average` | Average numeric values |
| `2` | `Min` | Minimum value |
| `3` | `Max` | Maximum value |
| `4` | `Count` | Count non-null values |
| `5` | `CountNonNull` | Count non-null values when exported with this explicit name |
| `6` | `Median` | Median value |
| `7` | `StandardDeviation` | Standard deviation |
| `8` | `Variance` | Variance |

If an exported or service-generated `metricDefinition` already has a richer semantic-model aggregation object, preserve it instead of reducing it to a primitive. Do not copy a `function` value from the stored query enum into `metricDefinition.definition.aggregation.Function` unless you have confirmed it maps to the semantic aggregation enum.

## `metricDefinition` Shape

`metricDefinition` should describe the same dataset, measure/aggregation, dimensions, and filters as `query.queryString`.

```json
{
  "name": "Revenue",
  "definition": {
    "datasetId": "<semantic-model-id>",
    "aggregation": {
      "Measure": {
        "Expression": { "SourceRef": { "Entity": "Sales" } },
        "Property": "Revenue"
      },
      "Name": "Revenue"
    },
    "dimensions": [
      {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "Division" } },
          "Property": "Division Name"
        },
        "Name": "Division Name"
      }
    ],
    "filter": {
      "Version": 2,
      "From": [
        { "Name": "d", "Entity": "Division", "Type": 0 }
      ],
      "Where": [
        {
          "Condition": {
            "In": {
              "Expressions": [
                {
                  "Column": {
                    "Expression": { "SourceRef": { "Source": "d" } },
                    "Property": "Division Name"
                  }
                }
              ],
              "Values": [
                [{ "Literal": { "Value": "'East'" } }]
              ]
            }
          }
        }
      ]
    }
  },
  "type": "DatasetMetric"
}
```

## Filters

Use the source query filter expressions in `query.queryString`. In `metricDefinition.definition.filter`, use the semantic-query contract shown below.

### In filter

```json
{
  "target": [{ "table": "Division", "column": "Division Name" }],
  "in": [["East"]]
}
```

### Comparison filter

```json
{
  "target": { "table": "Date", "column": "WeekStartDate" },
  "greaterThan": "2026-01-01T00:00:00Z"
}
```

### Semantic-query metric definition filter

```json
{
  "Version": 2,
  "From": [
    { "Name": "d", "Entity": "Division", "Type": 0 }
  ],
  "Where": [
    {
      "Condition": {
        "In": {
          "Expressions": [
            {
              "Column": {
                "Expression": { "SourceRef": { "Source": "d" } },
                "Property": "Division Name"
              }
            }
          ],
          "Values": [
            [{ "Literal": { "Value": "'East'" } }]
          ]
        }
      }
    }
  ]
}
```

## Persistence Flow

The stored query and `metricDefinition` are separate but matching contracts.
Validate their structure locally using the consistency checklist below, then
submit the full Activator definition once:

1. Build both payloads from the same report visual and semantic model metadata.
2. Ensure IDs, measure references, dimensions, filters, and personalization
   values agree across the source, query, and metric definition.
3. Persist with Activator `updateDefinition`.
4. Require explicit HTTP `200`, or poll a `202` LRO to terminal success.
5. Stop on any `4xx`, `5xx`, `Activator_Alm_*` error, or nonzero command exit.

## Consistency Checklist

Before calling `updateDefinition`, verify:

1. `query.queryString` parses as JSON.
2. The query has `provider` and at least one projection (`metrics` or `groupBy`).
3. The persisted query does not include `top`.
4. `metricDefinition` parses as JSON if stored as a string.
5. `provider.datasetId`, `metricDefinition.definition.datasetId`, and source `datasetId` match.
6. Measure references exist in the semantic model metadata.
7. Dimension references exist in the semantic model metadata.
8. Report/page/visual IDs match the scoped visual used to derive the source.
9. If `dimensionValue` is present, the same value appears in query filters and metric definition filters.
10. `reportWorkspaceId = "me"` is not used as a Fabric workspace ID for `getDefinition`; resolve the real workspace ID when calling Fabric APIs.
11. Power BI Activator readback is treated as unavailable until public PBI ALM export is enabled consistently; do not require `getDefinition` to prove a successful import.

## Minimal Non-Personalized Example

```json
{
  "provider": {
    "datasetId": "<semantic-model-id>",
    "metric": {
      "name": "Count of Table",
      "definition": {
        "datasetId": "<semantic-model-id>",
        "aggregation": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Table" } },
            "Property": "Count of Table"
          },
          "Name": "Count of Table"
        },
        "dimensions": [
          {
            "Column": {
              "Expression": { "SourceRef": { "Entity": "Table" } },
              "Property": "Category"
            },
            "Name": "Category"
          }
        ]
      },
      "type": "DatasetMetric"
    }
  },
  "metrics": [{ "measure": "Count of Table", "table": "Table" }],
  "groupBy": [{ "table": "Table", "column": "Category" }]
}
```
