# Dataset Inlining — Synapse Datasets → Fabric Inline Activity Properties

Synapse pipelines reference datasets as separate workspace items. Fabric Data Factory has no standalone Dataset items — dataset properties are declared inline inside each activity's `typeProperties` (source, sink, or dataset block).

This file explains how to extract dataset properties from Synapse and embed them directly into pipeline activity JSON.

---

## Why Inlining Is Required

| Synapse | Fabric |
|---|---|
| Dataset is a separate JSON resource with its own name | No Dataset item type in Fabric |
| Activity references dataset by `referenceName` | Activity carries all connector settings inline |
| Dataset can be reused across multiple activities | Each activity carries its own copy of the settings |

> If a Synapse dataset is reused by 5 Copy activities, you must inline its properties into all 5 activities in Fabric.

---

## How to Get Dataset Definitions from Synapse

```python
import requests

SYNAPSE_TOKEN = "<synapse-data-plane-token>"
SYNAPSE_ENDPOINT = "https://myworkspace.dev.azuresynapse.net"
headers = {"Authorization": f"Bearer {SYNAPSE_TOKEN}"}

def get_all_datasets():
    url = f"{SYNAPSE_ENDPOINT}/datasets?api-version=2020-12-01"
    items = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("value", []))
        url = data.get("nextLink")
    return items

def build_dataset_map(datasets: list) -> dict:
    """Return {datasetName: datasetProperties} for lookup during inlining."""
    return {d["name"]: d["properties"] for d in datasets}

datasets = get_all_datasets()
dataset_map = build_dataset_map(datasets)
```

---

## Activity → Dataset Slot Mapping

Different activity types reference datasets in different slots:

| Activity Type | Dataset Slot | `typeProperties` Key |
|---|---|---|
| `Copy` (source) | Source dataset | `source.storeSettings` + `source.formatSettings` |
| `Copy` (sink) | Sink dataset | `sink.storeSettings` + `sink.formatSettings` |
| `Lookup` | Dataset | `dataset` |
| `GetMetadata` | Dataset | `dataset` (or inlined storeSettings) |
| `Delete` | Dataset | `dataset` |

---

## Inlining Patterns by Connector

### Parquet on ADLS Gen2

**Synapse Dataset (`properties`):**
```json
{
  "type": "Parquet",
  "linkedServiceName": {
    "referenceName": "AzureDataLakeStorage1",
    "type": "LinkedServiceReference"
  },
  "typeProperties": {
    "location": {
      "type": "AzureBlobFSLocation",
      "fileSystem": "raw",
      "folderPath": "sales/orders",
      "fileName": "orders.parquet"
    },
    "compressionCodec": "snappy"
  }
}
```

**Fabric Copy Activity — Source inline:**
```json
{
  "source": {
    "type": "ParquetSource",
    "storeSettings": {
      "type": "AzureBlobFSReadSettings",
      "recursive": false
    }
  }
}
```

**Fabric Copy Activity — fully inlined** (connection and location in-place). Note that `linkedService` is a **root-level activity property**, a sibling of `typeProperties` (which contains `source`/`sink`) — *not* nested inside `source`:

```json
{
  "name": "CopyParquet",
  "type": "Copy",
  "typeProperties": {
    "source": {
      "type": "ParquetSource",
      "storeSettings": {
        "type": "AzureBlobFSReadSettings",
        "recursive": false,
        "fileSystem": "raw",
        "folderPath": "path/to/data"
      }
    },
    "sink": { "type": "ParquetSink" }
  },
  "linkedService": {
    "referenceName": "AzureDataLakeStorage1",
    "type": "LinkedServiceReference"
  }
}
```

> Fabric Data Factory has no Dataset item type. The `inputs`/`outputs` arrays and `DatasetReference` objects from Synapse are removed entirely during inlining — connection and location settings move inline into the activity.

> The `linkedServiceName.referenceName` from the Synapse dataset becomes the Fabric connection name in the activity's `linkedService` or dataset block.

---

### CSV / DelimitedText on Azure Blob Storage

**Synapse Dataset:**
```json
{
  "type": "DelimitedText",
  "linkedServiceName": {
    "referenceName": "AzureBlobStorage1",
    "type": "LinkedServiceReference"
  },
  "typeProperties": {
    "location": {
      "type": "AzureBlobStorageLocation",
      "container": "landing",
      "folderPath": "incoming",
      "fileName": "data.csv"
    },
    "columnDelimiter": ",",
    "rowDelimiter": "\n",
    "quoteChar": "\"",
    "escapeChar": "\\",
    "firstRowAsHeader": true,
    "nullValue": "NULL"
  }
}
```

**Fabric Copy Source inline:**
```json
{
  "source": {
    "type": "DelimitedTextSource",
    "storeSettings": {
      "type": "AzureBlobStorageReadSettings",
      "recursive": false
    },
    "formatSettings": {
      "type": "DelimitedTextReadSettings"
    }
  }
}
```

---

### Azure SQL Table

**Synapse Dataset:**
```json
{
  "type": "AzureSqlTable",
  "linkedServiceName": {
    "referenceName": "AzureSqlDB_Sales",
    "type": "LinkedServiceReference"
  },
  "typeProperties": {
    "schema": "dbo",
    "table": "Orders"
  }
}
```

**Fabric Copy Sink inline:**
```json
{
  "sink": {
    "type": "AzureSqlSink",
    "writeBehavior": "upsert",
    "upsertSettings": {
      "useTempDB": true,
      "keys": ["OrderId"]
    },
    "tableOption": "autoCreate",
    "disableMetricsCollection": false
  }
}
```

---

### Delta Lake on ADLS Gen2

**Synapse Dataset:**
```json
{
  "type": "Parquet",
  "linkedServiceName": {
    "referenceName": "AzureDataLakeStorage1",
    "type": "LinkedServiceReference"
  },
  "typeProperties": {
    "location": {
      "type": "AzureBlobFSLocation",
      "fileSystem": "silver",
      "folderPath": "products"
    }
  }
}
```

**Fabric Copy Sink (Delta):**
```json
{
  "sink": {
    "type": "ParquetSink",
    "storeSettings": {
      "type": "AzureBlobFSWriteSettings"
    },
    "formatSettings": {
      "type": "ParquetWriteSettings"
    }
  }
}
```

> For true Delta Lake tables in Fabric, consider writing via a `TridentNotebook` activity using `delta.write()` — it gives full ACID semantics including schema evolution, merge, and table history.

---

### Binary (File Copy — no format parsing)

```json
{
  "source": {
    "type": "BinarySource",
    "storeSettings": {
      "type": "AzureBlobFSReadSettings",
      "recursive": true,
      "deleteFilesAfterCompletion": false
    }
  },
  "sink": {
    "type": "BinarySink",
    "storeSettings": {
      "type": "AzureBlobFSWriteSettings"
    }
  }
}
```

---

## Python Inlining Helper

The following Python function resolves a dataset reference and inlines the necessary connector settings into a Copy/Lookup/GetMetadata/Delete activity:

```python
import copy, json

# Dataset type → source/sink activity type mapping
DATASET_TYPE_TO_SOURCE = {
    "Parquet": "ParquetSource",
    "DelimitedText": "DelimitedTextSource",
    "Json": "JsonSource",
    "Avro": "AvroSource",
    "Orc": "OrcSource",
    "Excel": "ExcelSource",
    "AzureSqlTable": "AzureSqlSource",
    "SqlServerTable": "SqlServerSource",
    "AzureMySqlTable": "AzureMySqlSource",
    "AzurePostgreSqlTable": "AzurePostgreSqlSource",
    "CosmosDbSqlApiCollection": "CosmosDbSqlApiSource",
    "RestResource": "RestSource",
    "HttpFile": "HttpSource",
    "Binary": "BinarySource",
}

DATASET_TYPE_TO_SINK = {
    "Parquet": "ParquetSink",
    "DelimitedText": "DelimitedTextSink",
    "Json": "JsonSink",
    "Avro": "AvroSink",
    "Orc": "OrcSink",
    "AzureSqlTable": "AzureSqlSink",
    "SqlServerTable": "SqlServerSink",
    "AzureMySqlTable": "AzureMySqlSink",
    "AzurePostgreSqlTable": "AzurePostgreSqlSink",
    "CosmosDbSqlApiCollection": "CosmosDbSqlApiSink",
    "Binary": "BinarySink",
}

# Tabular (non-file) dataset types — these do not have a `location` /
# `location_type` / `storeSettings`; instead, table identity + query live
# directly under the activity's source/sink (e.g., tableName, schema, query).
TABULAR_DATASET_TYPES = {
    "AzureSqlTable",
    "SqlServerTable",
    "AzureMySqlTable",
    "AzurePostgreSqlTable",
    "CosmosDbSqlApiCollection",
}

# Fields copied straight through from a tabular dataset's typeProperties
# into the activity's source/sink block.
TABULAR_PASSTHROUGH_FIELDS = ("tableName", "schema", "table", "collectionName", "query")

ADLS_LOCATION_TYPES = {
    "AzureBlobFSLocation": ("AzureBlobFSReadSettings", "AzureBlobFSWriteSettings"),
    "AzureBlobStorageLocation": ("AzureBlobStorageReadSettings", "AzureBlobStorageWriteSettings"),
    "AzureDataLakeStoreLocation": ("AzureDataLakeStoreReadSettings", "AzureDataLakeStoreWriteSettings"),
}

# Fallback mapping from Synapse dataset top-level `type` to a Fabric location
# type, used when the flat-schema dataset (e.g., AzureBlob with folderPath/
# fileName) does not carry a nested `typeProperties.location.type`.
DATASET_TYPE_TO_LOCATION_TYPE = {
    "AzureBlob":              "AzureBlobStorageLocation",
    "AzureBlobFSFile":        "AzureBlobFSLocation",
    "AzureDataLakeStoreFile": "AzureDataLakeStoreLocation",
    "DelimitedText":          "AzureBlobStorageLocation",
    "Json":                   "AzureBlobStorageLocation",
    "Parquet":                "AzureBlobStorageLocation",
    "Avro":                   "AzureBlobStorageLocation",
    "Orc":                    "AzureBlobStorageLocation",
    "Binary":                 "AzureBlobStorageLocation",
}

# Dataset type → formatSettings.type for Lookup/GetMetadata/Delete activities.
# Storage-level types (AzureBlob, AzureBlobFS, etc.) are intentionally absent:
# they use storeSettings only and do not require formatSettings.
# Binary is included because it is a format type (binary file payload) even
# though it has no schema — it pairs with BinaryReadSettings on GetMetadata,
# Lookup, and Delete activities (see the Validation→GetMetadata example in
# activity-mapping.md).
DATASET_TYPE_TO_FORMAT_SETTINGS = {
    "DelimitedText": "DelimitedTextReadSettings",
    "Json":          "JsonReadSettings",
    "Parquet":       "ParquetReadSettings",
    "Avro":          "AvroReadSettings",
    "Orc":           "OrcReadSettings",
    "Excel":         "ExcelReadSettings",
    "Xml":           "XmlReadSettings",
    "Binary":        "BinaryReadSettings",
}


def inline_dataset(activity: dict, dataset_map: dict, connection_map: dict) -> dict:
    """
    Inline dataset references in a Copy, Lookup, GetMetadata, or Delete activity.
    
    Args:
        activity: The Synapse activity dict (will be deep-copied).
        dataset_map: {datasetName: datasetProperties} from Synapse.
        connection_map: {linkedServiceName: fabricConnectionName}
    
    Returns:
        Activity with dataset references inlined.
    """
    activity = copy.deepcopy(activity)
    activity_type = activity.get("type")
    props = activity.get("typeProperties", {})

    if activity_type == "Copy":
        # Synapse Copy activities reference one source dataset (inputs[0]) and
        # one sink dataset (outputs[0]). Validate that assumption up front so
        # multi-input/output configurations don't silently lose dataset
        # references when only the first entry gets inlined.
        inputs = activity.get("inputs", [])
        outputs = activity.get("outputs", [])
        if len(inputs) > 1 or len(outputs) > 1:
            raise ValueError(
                f"Copy activity '{activity.get('name')}' has {len(inputs)} input(s) "
                f"and {len(outputs)} output(s); only single-input / single-output "
                f"Copy activities are supported by this inlining helper. Split the "
                f"activity in Synapse before re-running Phase 3."
            )

        # Inline source dataset from Synapse inputs[0] (DatasetReference)
        src_conn = None
        if inputs:
            src_ds_name = inputs[0].get("referenceName")
            if src_ds_name:
                if src_ds_name not in dataset_map:
                    raise KeyError(
                        f"Activity '{activity.get('name')}' references unknown source "
                        f"dataset '{src_ds_name}'. Add it to dataset_map (Phase 3 "
                        f"dataset inventory) or remove the reference."
                    )
                src_conn = _inline_copy_source(props, src_ds_name, dataset_map[src_ds_name], connection_map)
                activity.pop("inputs", None)

        # Inline sink dataset
        sink_conn = None
        if outputs:
            sink_ds_name = outputs[0].get("referenceName")
            if sink_ds_name:
                if sink_ds_name not in dataset_map:
                    raise KeyError(
                        f"Activity '{activity.get('name')}' references unknown sink "
                        f"dataset '{sink_ds_name}'. Add it to dataset_map (Phase 3 "
                        f"dataset inventory) or remove the reference."
                    )
                sink_conn = _inline_copy_sink(props, sink_ds_name, dataset_map[sink_ds_name], connection_map)
                activity.pop("outputs", None)

        # Emit connection references at the activity root level — linkedService is a
        # sibling of typeProperties per the Fabric Data Pipeline schema (see SKILL.md).
        # Same-system copy: one activity["linkedService"] covers both source and sink.
        # Cross-system copy: source connection at the activity root; sink connection
        # embedded inside the sink block so both identities are preserved in the JSON.
        if src_conn and sink_conn and src_conn != sink_conn:
            activity["linkedService"] = {"referenceName": src_conn, "type": "LinkedServiceReference"}
            props.setdefault("sink", {})["linkedService"] = {
                "referenceName": sink_conn, "type": "LinkedServiceReference",
            }
        elif src_conn or sink_conn:
            activity["linkedService"] = {
                "referenceName": src_conn or sink_conn, "type": "LinkedServiceReference",
            }

    elif activity_type in ("Lookup", "GetMetadata", "Delete"):
        ds_ref = props.get("dataset", {})
        ds_name = ds_ref.get("referenceName")
        if ds_name:
            if ds_name not in dataset_map:
                raise KeyError(
                    f"Activity '{activity.get('name')}' references unknown dataset "
                    f"'{ds_name}'. Add it to dataset_map (Phase 3 dataset inventory) "
                    f"or remove the reference."
                )
            ds_props = dataset_map[ds_name]
            # Pop the original dataset reference up-front so the helper can
            # write a new typed `dataset` block (for tabular sources) without
            # being clobbered by an unconditional pop after the call.
            props.pop("dataset", None)
            conn = _inline_dataset_reference(props, ds_name, ds_props, connection_map)
            if conn:
                activity["linkedService"] = {"referenceName": conn, "type": "LinkedServiceReference"}

    activity["typeProperties"] = props
    return activity


def _get_read_settings_type(location_type: str, dataset_name: str = "<unknown>", dataset_type: str = "<unknown>") -> str:
    mapped = ADLS_LOCATION_TYPES.get(location_type)
    if mapped is None:
        raise ValueError(
            f"Unsupported location_type '{location_type}' for dataset "
            f"'{dataset_name}' (type='{dataset_type}'). "
            f"Supported: {sorted(ADLS_LOCATION_TYPES.keys())}."
        )
    return mapped[0]


def _get_write_settings_type(location_type: str, dataset_name: str = "<unknown>", dataset_type: str = "<unknown>") -> str:
    mapped = ADLS_LOCATION_TYPES.get(location_type)
    if mapped is None:
        raise ValueError(
            f"Unsupported location_type '{location_type}' for dataset "
            f"'{dataset_name}' (type='{dataset_type}'). "
            f"Supported: {sorted(ADLS_LOCATION_TYPES.keys())}."
        )
    return mapped[1]


def _normalize_location(ds_type_props: dict) -> dict:
    """Return a unified location dict regardless of dataset schema:
    - Nested schema: typeProperties.location.{type, fileSystem, folderPath, …}
      (e.g., AzureBlobFSFile, AzureDataLakeStoreFile)
    - Flat schema:   typeProperties.{folderPath, fileName, …} at top level
      (e.g., AzureBlob, AzureDataLakeStore v1)
    """
    nested = ds_type_props.get("location")
    if nested:
        return nested
    # Flat schema — path fields sit directly under typeProperties
    return {k: ds_type_props[k]
            for k in ("type", "fileSystem", "container", "folderPath", "fileName")
            if k in ds_type_props}


def _inline_copy_source(props: dict, ds_name: str, ds_props: dict, connection_map: dict) -> str:
    ds_type = ds_props.get("type")
    if not ds_type:
        # Fail fast: an empty/missing dataset `type` would produce an invalid
        # "NoneSource" / "Source" identifier that later trips schema validation
        # in non-obvious ways downstream.
        raise ValueError(
            f"Dataset '{ds_name}' has no `type` field — cannot infer Fabric "
            f"source type. Fix the dataset definition in Synapse or add a "
            f"mapping override for it before re-running Phase 3."
        )
    linked_svc = ds_props.get("linkedServiceName", {}).get("referenceName", "")
    fabric_conn = connection_map.get(linked_svc, linked_svc)  # fall back to same name
    source = props.setdefault("source", {})
    # Resolve the source activity "type":
    # 1. Use the explicit mapping when one exists (e.g. Parquet → ParquetSource).
    # 2. Otherwise preserve any pre-existing source.type the activity already
    #    declared — storage-only Synapse datasets (AzureBlob, AzureBlobFSFile,
    #    AzureDataLakeStoreFile) carry no file-format info, and the activity is
    #    where the Synapse author chose the right reader (e.g. ParquetSource,
    #    DelimitedTextSource, BinarySource). Synthesizing "AzureBlobSource"
    #    from the dataset type would be schema-invalid in Fabric / ADF.
    # 3. If neither path produces a valid type, fail fast with a clear message
    #    instead of silently writing an invalid identifier.
    mapped = DATASET_TYPE_TO_SOURCE.get(ds_type)
    if mapped:
        source["type"] = mapped
    elif source.get("type"):
        # Preserve the existing activity source.type (e.g. ParquetSource).
        pass
    else:
        raise ValueError(
            f"Cannot infer Fabric Copy source type for dataset '{ds_name}' "
            f"(dataset type='{ds_type}'). Storage-only dataset types (AzureBlob, "
            f"AzureBlobFSFile, AzureDataLakeStoreFile, …) carry no file-format "
            f"information — set `source.type` on the activity in Synapse (e.g. "
            f"`ParquetSource`, `DelimitedTextSource`, `BinarySource`) or add an "
            f"entry to DATASET_TYPE_TO_SOURCE before re-running Phase 3."
        )

    if ds_type in TABULAR_DATASET_TYPES:
        # Tabular connectors: no storeSettings; copy table identity/query through.
        ds_tp = ds_props.get("typeProperties", {}) or {}
        for key in TABULAR_PASSTHROUGH_FIELDS:
            if key in ds_tp:
                source[key] = ds_tp[key]
        return fabric_conn

    location = _normalize_location(ds_props.get("typeProperties", {}))
    # Flat-schema datasets (AzureBlob with folderPath/fileName) carry no
    # location.type — fall back to the dataset type.
    location_type = location.get("type") or DATASET_TYPE_TO_LOCATION_TYPE.get(ds_type, "")
    # Inline location fields (fileSystem/container, folderPath, fileName) into storeSettings
    store = source.setdefault("storeSettings", {})
    store["type"] = _get_read_settings_type(location_type, ds_name or "<unknown>", ds_type or "<unknown>")
    for key in ("fileSystem", "container", "folderPath", "fileName"):
        if key in location:
            store[key] = location[key]
    return fabric_conn


def _inline_copy_sink(props: dict, ds_name: str, ds_props: dict, connection_map: dict) -> str:
    ds_type = ds_props.get("type")
    if not ds_type:
        # Fail fast: an empty/missing dataset `type` would produce an invalid
        # "NoneSink" / "Sink" identifier that later trips schema validation
        # in non-obvious ways downstream.
        raise ValueError(
            f"Dataset '{ds_name}' has no `type` field — cannot infer Fabric "
            f"sink type. Fix the dataset definition in Synapse or add a "
            f"mapping override for it before re-running Phase 3."
        )
    linked_svc = ds_props.get("linkedServiceName", {}).get("referenceName", "")
    fabric_conn = connection_map.get(linked_svc, linked_svc)
    sink = props.setdefault("sink", {})
    # See _inline_copy_source for the resolution rules; symmetric handling on the sink.
    mapped = DATASET_TYPE_TO_SINK.get(ds_type)
    if mapped:
        sink["type"] = mapped
    elif sink.get("type"):
        # Preserve the existing activity sink.type (e.g. ParquetSink).
        pass
    else:
        raise ValueError(
            f"Cannot infer Fabric Copy sink type for dataset '{ds_name}' "
            f"(dataset type='{ds_type}'). Storage-only dataset types (AzureBlob, "
            f"AzureBlobFSFile, AzureDataLakeStoreFile, …) carry no file-format "
            f"information — set `sink.type` on the activity in Synapse (e.g. "
            f"`ParquetSink`, `DelimitedTextSink`, `BinarySink`) or add an entry "
            f"to DATASET_TYPE_TO_SINK before re-running Phase 3."
        )

    if ds_type in TABULAR_DATASET_TYPES:
        ds_tp = ds_props.get("typeProperties", {}) or {}
        for key in TABULAR_PASSTHROUGH_FIELDS:
            if key in ds_tp:
                sink[key] = ds_tp[key]
        return fabric_conn

    location = _normalize_location(ds_props.get("typeProperties", {}))
    location_type = location.get("type") or DATASET_TYPE_TO_LOCATION_TYPE.get(ds_type, "")
    # Inline location fields (fileSystem/container, folderPath, fileName) into storeSettings
    store = sink.setdefault("storeSettings", {})
    store["type"] = _get_write_settings_type(location_type, ds_name or "<unknown>", ds_type or "<unknown>")
    for key in ("fileSystem", "container", "folderPath", "fileName"):
        if key in location:
            store[key] = location[key]
    return fabric_conn


def _inline_dataset_reference(props: dict, ds_name: str, ds_props: dict, connection_map: dict) -> str:
    """For Lookup, GetMetadata, Delete — inline the dataset reference."""
    ds_type = ds_props.get("type")
    linked_svc = ds_props.get("linkedServiceName", {}).get("referenceName", "")
    fabric_conn = connection_map.get(linked_svc, linked_svc)

    if ds_type in TABULAR_DATASET_TYPES:
        # Tabular Lookup/GetMetadata: emit a typed dataset block instead of storeSettings.
        ds_tp = ds_props.get("typeProperties", {}) or {}
        dataset_block = {"type": ds_type}
        for key in TABULAR_PASSTHROUGH_FIELDS:
            if key in ds_tp:
                dataset_block[key] = ds_tp[key]
        props["dataset"] = dataset_block
        return fabric_conn

    location = _normalize_location(ds_props.get("typeProperties", {}))
    location_type = location.get("type") or DATASET_TYPE_TO_LOCATION_TYPE.get(ds_type, "")

    store = {"type": _get_read_settings_type(location_type, ds_name or "<unknown>", ds_type or "<unknown>")}
    # Carry over location fields so the activity can still locate the data
    # after the dataset reference is removed (matches _inline_copy_source pattern)
    for key in ("fileSystem", "container", "folderPath", "fileName"):
        if key in location:
            store[key] = location[key]
    props["storeSettings"] = store
    # Carry over formatSettings only when we know the concrete type;
    # emitting an empty {} is invalid schema for most activity types.
    fmt_type = DATASET_TYPE_TO_FORMAT_SETTINGS.get(ds_type)
    if fmt_type:
        props["formatSettings"] = {"type": fmt_type}
    return fabric_conn


def inline_all_activities(
    activities: list,
    dataset_map: dict,
    connection_map: dict,
) -> tuple[list, list[str]]:
    """
    Inline datasets in all activities, including nested inner activities.
    
    Returns:
        (transformed_activities, list_of_warning_messages)
    """
    warnings = []
    result = []

    for activity in activities:
        try:
            activity = inline_dataset(activity, dataset_map, connection_map)
        except Exception as e:
            warnings.append(f"Activity '{activity.get('name')}': {e}")

        # Recurse into containers
        for key in ("activities", "ifTrueActivities", "ifFalseActivities", "defaultActivities"):
            if key in activity.get("typeProperties", {}):
                inner, inner_w = inline_all_activities(
                    activity["typeProperties"][key], dataset_map, connection_map
                )
                activity["typeProperties"][key] = inner
                warnings.extend(inner_w)

        if activity.get("type") == "Switch":
            for case in activity.get("typeProperties", {}).get("cases", []):
                inner, inner_w = inline_all_activities(
                    case.get("activities", []), dataset_map, connection_map
                )
                case["activities"] = inner
                warnings.extend(inner_w)

        result.append(activity)

    return result, warnings
```

---

## Dataset Parameters

Some Synapse datasets use parameters (e.g., dynamic file paths). When inlining, incorporate the parameter values into the activity's `typeProperties` directly or via pipeline expression:

**Synapse Dataset with parameter:**
```json
{
  "type": "Parquet",
  "parameters": {
    "folderPath": { "type": "String" }
  },
  "typeProperties": {
    "location": {
      "type": "AzureBlobFSLocation",
      "fileSystem": "raw",
      "folderPath": {
        "value": "@dataset().folderPath",
        "type": "Expression"
      }
    }
  }
}
```

**Fabric — Inline with pipeline expression:**
```json
{
  "source": {
    "type": "ParquetSource",
    "storeSettings": {
      "type": "AzureBlobFSReadSettings",
      "recursive": false,
      "wildcardFolderPath": {
        "value": "@pipeline().parameters.folderPath",
        "type": "Expression"
      }
    }
  }
}
```

> Replace `@dataset().paramName` with the actual pipeline parameter or expression that the activity was passing to the dataset at runtime.

---

## Connection Reference Placement in Fabric Data Pipeline JSON

In Fabric Data Pipeline JSON, `linkedService` is a **root-level property of the activity** — a sibling of `typeProperties`, not nested inside `source` or `sink`:

```json
{
  "name": "CopyData",
  "type": "Copy",
  "typeProperties": {
    "source": { "type": "ParquetSource", "storeSettings": { "..." : "..." } },
    "sink":   { "type": "ParquetSink",   "storeSettings": { "..." : "..." } }
  },
  "linkedService": { "referenceName": "MyADLSConnection", "type": "LinkedServiceReference" }
}
```

The same rule applies to `GetMetadata`, `Lookup`, and `Delete` activities.

### Same-System Copy (source and sink share one connection)

A single `activity.linkedService` covers both sides:

```json
{
  "name": "CopyBlobToBlob",
  "type": "Copy",
  "typeProperties": {
    "source": { "type": "ParquetSource", "storeSettings": { "type": "AzureBlobFSReadSettings" } },
    "sink":   { "type": "ParquetSink",   "storeSettings": { "type": "AzureBlobFSWriteSettings" } }
  },
  "linkedService": { "referenceName": "ADLSGen2Connection", "type": "LinkedServiceReference" }
}
```

### Cross-System Copy (source and sink use different connections)

The source connection goes to the activity root (`activity.linkedService`). The sink connection is embedded directly inside the `sink` block, since only one root-level `linkedService` key exists:

```json
{
  "name": "CopySqlToParquet",
  "type": "Copy",
  "typeProperties": {
    "source": {
      "type": "AzureSqlSource",
      "queryTimeout": "02:00:00"
    },
    "sink": {
      "type": "ParquetSink",
      "storeSettings": { "type": "AzureBlobFSWriteSettings" },
      "linkedService": { "referenceName": "ADLSGen2Connection", "type": "LinkedServiceReference" }
    }
  },
  "linkedService": { "referenceName": "AzureSqlConnection", "type": "LinkedServiceReference" }
}
```

The Python inlining helper (`inline_dataset`) applies this pattern automatically: when source and sink resolve to the same Fabric connection name a single root key is emitted; when they differ the source connection goes to `activity["linkedService"]` and the sink connection is written into `typeProperties.sink.linkedService`.
