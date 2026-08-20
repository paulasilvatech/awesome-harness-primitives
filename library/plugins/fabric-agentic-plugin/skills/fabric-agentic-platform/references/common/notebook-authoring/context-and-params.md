# Runtime Context & Parameterization

How to access notebook runtime context, pass parameters, and manage configuration.

## Table of Contents

| Section | Notes |
|---|---|
| [Runtime Context](#runtime-context) | notebookutils.runtime.context — notebook, workspace, lakehouse metadata |
| [Parameterization Patterns](#parameterization-patterns) | When and how to parameterize notebooks |
| [Variable Library](#variable-library) | Centralized config with getLibrary + pipeline integration |
| [Configuration Management](#configuration-management) | Environment-specific configs, validation |

---

## Runtime Context

**Use `notebookutils.runtime.context` for accessing notebook and workspace metadata.** This is the cleanest, most reliable API.

```python
context = notebookutils.runtime.context
workspace_id = context["currentWorkspaceId"]
lakehouse_name = context["defaultLakehouseName"]
```

| Context Key | Description |
|---|---|
| `currentNotebookName` | Current notebook name |
| `currentNotebookId` | Current notebook ID |
| `currentWorkspaceId` | Workspace ID |
| `currentWorkspaceName` | Workspace name |
| `activityId` | Activity ID |
| `poolName` | Spark pool name |
| `userId` / `userName` | Current user identity |
| `defaultLakehouseName` | Default lakehouse name (if attached) |
| `defaultLakehouseId` | Default lakehouse ID (if attached) |
| `defaultLakehouseWorkspaceName` | Lakehouse workspace name |
| `defaultLakehouseWorkspaceId` | Lakehouse workspace ID |
| `environmentId` | Environment ID |
| `environmentWorkspaceId` | Environment workspace ID |
| `isForPipeline` | Whether running in a pipeline |
| `isReferenceRun` | Whether it's a reference notebook run |

**Documentation**: [Runtime context](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-runtime)

---

## Parameterization Patterns

### When to Parameterize

Make these configurable:
- **Data paths**: Source file paths, target table names, partition values
- **Processing dates**: Date ranges for incremental loads, effective dates
- **Environment settings**: Workspace IDs, lakehouse IDs (different per dev/test/prod)
- **Business logic**: Thresholds, filters, feature flags

### Method 1: Default Parameters in Notebook

First code cell defines parameters with default values. Pipelines can override these at runtime.

```python
# Parameters cell — values overridden by pipeline activity
source_path = "Files/raw/sales/"
target_table = "silver.cleaned_sales"
processing_date = "2024-01-15"
max_retry = 3
```

### Method 2: Pipeline Activity Parameters

Pipeline JSON includes parameters mapped to notebook parameter names:

```json
{
  "type": "TridentNotebook",
  "typeProperties": {
    "notebookId": "<notebook-guid>",
    "parameters": {
      "processing_date": { "value": "@formatDateTime(utcnow(), 'yyyy-MM-dd')", "type": "Expression" },
      "source_path": { "value": "Files/raw/sales/", "type": "string" }
    }
  }
}
```

### Method 3: Livy Session Parameters

Pass parameters via Livy API during session creation or statement execution — useful for ad-hoc runs from CLI/scripts.

---

## Variable Library

Create a Variable Library item to centralize config (lakehouse names, workspace IDs, feature flags). Use Value Sets (`valueSets/dev.json`, `valueSets/prod.json`) to promote across environments without code changes.

### In Notebooks

```python
# ✅ CORRECT — getLibrary() + dot notation
lib = notebookutils.variableLibrary.getLibrary("MyConfig")
lakehouse_name = lib.lakehouse_name
enable_logging = lib.enable_logging  # returns string "true"/"false"

# Boolean: compare as string (bool("false") is True in Python!)
if enable_logging.lower() == "true":
    print("Logging enabled")

# ❌ WRONG — .get() does not exist, causes runtime failure
# notebookutils.variableLibrary.get("MyConfig", "lakehouse_name")
```

**Documentation**: [Variable library utilities](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-variable-library)

### In Data Pipelines

1. Declare `libraryVariables` in pipeline `properties` (sibling to `activities`):
   ```json
   "libraryVariables": {
     "notebook_id": {
       "libraryName": "sales_analytics_config",
       "libraryId": "<variable-library-item-id>",
       "variableName": "notebook_id",
       "type": "String"
     }
   }
   ```
2. Reference via expression syntax in activity `typeProperties`:
   ```json
   "notebookId": {
     "value": "@pipeline().libraryVariables.notebook_id",
     "type": "Expression"
   }
   ```
- Each entry needs `libraryName`, `libraryId`, `variableName`, and `type`
- Use `@pipeline().libraryVariables.<name>` — not `@variables()` (that is for regular pipeline variables)

---

## Configuration Management

- **Environment-specific configs**: Separate JSON files for dev/test/prod with workspace IDs, paths
- **Config loading pattern**: Read from OneLake Files or environment variables
- **Validation**: Assert required parameters are present before proceeding

```python
# Load environment-specific config
import json
config_path = f"Files/config/{environment}.json"
if notebookutils.fs.exists(config_path):
    config = json.loads(notebookutils.fs.head(config_path, maxBytes=10240))
else:
    raise ValueError(f"Config not found: {config_path}")

# Validate required keys
for key in ["workspace_id", "lakehouse_name", "source_path"]:
    assert key in config, f"Missing required config key: {key}"
```
