# Notebook Authoring — Shared Core

Shared guidance for writing code inside Microsoft Fabric Notebook cells using **Spark** (PySpark, Scala, SparkR, SQL). Referenced by `spark-authoring-cli`. Detailed guidance for each topic is in the [Module Index](#module-index).

## Notebook Fundamentals

1. **Fabric Notebook ≠ Jupyter Notebook** — When users say "Notebook", they mean Microsoft Fabric Notebook artifacts managed in a Fabric Workspace. Do not confuse with local Jupyter.
2. **Supported Languages** — **Python (PySpark)** (default kernel), **Scala**, **SparkR**, and **SQL** via magic commands.
3. **Language Magic Commands** — Use magic commands at the cell's first line:
   - SQL: `%%sql`
   - Scala: `%%spark`
   - PySpark: `%%pyspark` (optional — Python is default)
   - SparkR: `%%sparkr`
   - **Never change cell language attribute** — only add the magic command.
   - If user requests unsupported languages (C#, etc.), inform them and do not modify the notebook.
4. **Fabric Resources** — When a user mentions a name without clarification, assume it refers to a Fabric artifact or concept name unless context indicates otherwise.

---

## Module Index

Detailed guidance for each topic area. **Read the relevant module before generating code.** Local files and Microsoft Learn docs (fetch via MCP) are organized together by topic for easy lookup.

> **Reading priority**: Read local modules first (instant, no MCP call needed). Fetch MS Learn docs only when the local module doesn't cover the specific API or when you need up-to-date parameter details.

### 1. Context, Configuration & Parameters

_First step for any code generation — resolve where the notebook runs and what it connects to._

| Source | Module / Doc | When to Read |
|---|---|---|
| Local | [context-resolution.md](notebook-authoring/context-resolution.md) | lighter-config.json, ipynb metadata, workspace ID resolution, lakehouse ID lookup, artifact discovery (**VS Code only**) |
| Local | [context-and-params.md](notebook-authoring/context-and-params.md) | runtime.context, notebook parameters, pipeline parameters, Variable Library, getLibrary, %%configure defaultLakehouse, environment config |
| Fetch | [notebookutils.runtime](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-runtime) | `notebookutils.runtime.context` properties, currentNotebookName, currentWorkspaceId, defaultLakehouseId, isForPipeline, isReferenceRun, pipeline vs interactive detection |
| Fetch | [notebookutils.variableLibrary](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-variable-library) | `getLibrary()`, `get()` by reference path, centralized config, value sets, environment-specific variables (dev/test/prod) |
| Fetch | [Author & Execute notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/author-execute-notebook) | `%%configure` (session config, defaultLakehouse, mountPoints, environment), `%run` (reference run a notebook or script), magic commands (`%%sql`, `%%spark`, `%%pyspark`, `%%sparkr`), pipeline parameter cell, parameterized session config, IPython widgets, Python logging, secret redaction |

### 2. Lakehouse Paths, Tables & Schemas

_Resolve data locations and construct correct path/table references before reading or writing data._

| Source | Module / Doc | When to Read |
|---|---|---|
| Local | [lakehouse-paths.md](notebook-authoring/lakehouse-paths.md) | ABFSS path construction, relative path (`Files/`, `Tables/`), OneLake endpoint, default lakehouse mount `/lakehouse/default/`, workspace/lakehouse GUID in path, path format differences between Spark and Python notebooks |
| Local | [lakehouse-tables.md](notebook-authoring/lakehouse-tables.md) | Spark SQL table reference, two-part/three-part/four-part dotted name, backtick escaping, SHOW TABLES/SCHEMAS, CREATE/INSERT/MERGE, Delta time travel (`VERSION AS OF`, `TIMESTAMP AS OF`), schema discovery, cross-workspace Spark SQL |
| Fetch | [Lakehouse overview](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview) | lakehouse vs warehouse, SQL analytics endpoint, auto table discovery, Tables vs Files folder, capabilities overview |
| Fetch | [Lakehouse schemas](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-schemas) | schema-enabled lakehouse, four-part name (`workspace.lakehouse.schema.table`), cross-workspace Spark SQL, schema shortcuts, namespace differences |
| Fetch | [Delta Lake tables](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-and-delta-tables) | Delta format defaults, managed vs unmanaged tables, Spark config for Delta, shortcuts with Delta tables |
| Fetch | [Load data with notebook](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data) | `spark.read` / `spark.write`, Pandas API on Spark, relative vs ABFSS paths, `saveAsTable`, `df.write.format("delta")`, CSV/Parquet/JSON read patterns |
| Fetch | [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-shortcuts) | internal/external shortcuts, ADLS Gen2, S3, GCS, cross-workspace data access, shortcut limitations for cp/fastcp |
| Fetch | [Data ingestion comparison](https://learn.microsoft.com/en-us/fabric/data-engineering/load-data-lakehouse) | decision guide for ingestion method: notebooks, pipelines, dataflows, shortcuts, COPY INTO — read when choosing an approach |

### 3. File System & Storage Operations

_Read/write/copy/move files across ADLS Gen2, Blob Storage, and Lakehouse storage._

| Source | Module / Doc | When to Read |
|---|---|---|
| Fetch | [notebookutils.fs](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-file-system) | `ls`, `cp`, `fastcp`, `mv`, `rm`, `put`, `append`, `head`, `mkdirs`, `exists`, `getProperties` — file/directory CRUD operations, relative path behavior differences (Spark vs Python notebook), concurrent write limitations |
| Fetch | [notebookutils.fs mount](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-mount) | `mount`, `unmount`, `mounts`, `getMountPath` — attach ADLS Gen2/Blob/Lakehouse as local mount points, accountKey/sasToken/Entra auth, fileCacheTimeout, mount-process-unmount workflow, local file path access |

### 4. Credentials & External Connections

_Authenticate to Azure services, retrieve secrets, connect to external data sources._

| Source | Module / Doc | When to Read |
|---|---|---|
| Local | [connections.md](notebook-authoring/connections.md) | `notebookutils.credentials` for external services — getSecret (Key Vault), getToken (Entra), Azure SDK credential wrapper, connection code for PostgreSQL, MySQL, Azure SQL, Blob/ADLS, S3, Cosmos DB, Kusto |
| Fetch | [notebookutils.credentials](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-credentials) | `getToken` (audience: storage, pbi, keyvault, kusto), `getSecret` (Key Vault endpoint + secret name), `putSecret`, `isValidToken`, Azure SDK credential wrapper (`NotebookUtilsCredential`), token scope limitations for service principals |

### 5. Lakehouse & Notebook Artifact Management

_Programmatically create/get/update/delete Lakehouse and Notebook items._

| Source | Module / Doc | When to Read |
|---|---|---|
| Fetch | [notebookutils.lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-lakehouse) | `create` (with `enableSchemas`), `get`, `getWithProperties`, `update`, `delete`, `list`, `listTables`, `loadTable` — programmatic lakehouse lifecycle, cross-workspace CRUD, batch provisioning |
| Fetch | [notebookutils.notebook CRUD](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-notebook-management) | `create` (with .ipynb content, defaultLakehouse), `get`, `getDefinition`, `update`, `updateDefinition` (change content/lakehouse/environment), `delete`, `list` — notebook artifact lifecycle, backup/export, cross-workspace cloning |

### 6. Notebook Orchestration & Session

_Chain notebooks, run in parallel with DAG, manage session lifecycle._

| Source | Module / Doc | When to Read |
|---|---|---|
| Fetch | [notebookutils.notebook run](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-notebook-run) | `run` (reference notebook with timeout, parameters, cross-workspace), `runMultiple` (parallel execution, DAG dependencies, `@activity().exitValue()`, concurrency control, retry), `validateDAG`, `exit` (return value to caller/pipeline) — notebook orchestration patterns |
| Fetch | [notebookutils.session](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-session-management) | `stop()` (stop interactive session, release resources — **never call in pipeline mode**), `restartPython()` (restart Python interpreter, keeps Spark context in PySpark notebooks — use after `%pip install`) |

### 7. Notebook Resources & Library Management

_Access attached files, install/manage packages._

| Source | Module / Doc | When to Read |
|---|---|---|
| Local | [notebook-resources.md](notebook-authoring/notebook-resources.md) | `builtin/` folder, `env/` folder, `notebookutils.nbResPath`, `file:` prefix, small file embedding, resource folder path resolution, reference run resource access |
| Local | [library-mgmt.md](notebook-authoring/library-mgmt.md) | `%pip install` vs `!pip`, Environment artifact, custom wheel upload, `restartPython()` after install, built-in library list, runtime version check, Full/Quick publish mode |
| Fetch | [Manage Spark libraries](https://learn.microsoft.com/en-us/fabric/data-engineering/library-management) | `%pip`/`%conda` inline install, library precedence, pipeline library install considerations, session-scoped vs environment-scoped |
| Fetch | [Environment libraries](https://learn.microsoft.com/en-us/fabric/data-engineering/environment-manage-library) | Quick mode (5s publish) vs Full mode (stable snapshot), PyPI/Conda/Maven/custom .whl/.jar, publish mode selection, Full mode + custom live pool for fast startup |

### 8. Visualization & Output

_Render DataFrames, charts, and embedded reports in notebook output._

| Source | Module / Doc | When to Read |
|---|---|---|
| Fetch | [Notebook visualization](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-visualization) | `display(df)` (rich table view, chart view, multi-chart, summary view), `displayHTML()` (D3.js, custom HTML), `powerbiclient` (`Report`, `QuickVisualize`), Matplotlib, Plotly, Bokeh, Pandas rendering |

### 9. Delta Optimization & Performance

_Optimize Delta table read/write performance._

| Source | Module / Doc | When to Read |
|---|---|---|
| Fetch | [Delta optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) | V-Order write optimization, `OPTIMIZE` command, `VACUUM`, Z-Order, Optimize Write (`spark.microsoft.delta.optimizeWrite.enabled`), Low Shuffle Merge |
| Fetch | [Table compaction](https://learn.microsoft.com/en-us/fabric/data-engineering/table-compaction) | bin compaction, small file problem diagnosis, compaction patterns, `OPTIMIZE WHERE` |
| Fetch | [Tune file size](https://learn.microsoft.com/en-us/fabric/data-engineering/tune-file-size) | `spark.microsoft.delta.targetFileSize`, partitioned table tuning, write performance vs read performance trade-offs |
| Fetch | [Resource profiles](https://learn.microsoft.com/en-us/fabric/data-engineering/configure-resource-profile-configurations) | `writeHeavy`, `readHeavyForPBI`, `readHeavyForSpark`, custom profile config, when to apply which profile |

### 10. Spark Runtime & Compute Configuration

| Source | Module / Doc | When to Read |
|---|---|---|
| Fetch | [Apache Spark Runtimes](https://learn.microsoft.com/en-us/fabric/data-engineering/runtime) | runtime versions (1.2 = Spark 3.4, 1.3 = Spark 3.5, 2.0), Python/Java/Scala versions per runtime, built-in library list |
| Fetch | [Native Execution Engine](https://learn.microsoft.com/en-us/fabric/data-engineering/native-execution-engine-overview) | Velox-based execution, performance boost, enable/disable via `spark.native.enabled`, supported operators, fallback behavior |
| Fetch | [High Concurrency mode](https://learn.microsoft.com/en-us/fabric/data-engineering/configure-high-concurrency-session-notebooks) | share Spark session across notebooks, session isolation, conditions for sharing, pipeline high concurrency, REPL-level isolation |
| Fetch | [Environment compute](https://learn.microsoft.com/en-us/fabric/data-engineering/environment-manage-compute) | node size (Small/Medium/Large/XL/XXL), driver/executor core and memory config, Spark properties in Environment artifact |
| Fetch | [Spark best practices](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-best-practices-development-monitoring) | development patterns, runtime selection, High Concurrency tips, monitoring and diagnostics, MLV organization |

### 11. Data Science & ML Workflow

| Source | Module / Doc | When to Read |
|---|---|---|
| Local | [ml-workflow.md](notebook-authoring/ml-workflow.md) | MLflow experiment setup, `mlflow.set_experiment`, autologging, model registration, SynapseML, LightGBM, PREDICT function, batch scoring, MLFlowTransformer, scikit-learn, PyTorch, XGBoost, AutoML, model training workflow |
| Fetch | [MLflow autologging](https://learn.microsoft.com/en-us/fabric/data-science/mlflow-autologging) | autolog configuration, disable autologging, custom metric logging |
| Fetch | [ML experiments](https://learn.microsoft.com/en-us/fabric/data-science/machine-learning-experiment) | create experiment, compare runs, search runs, track training iterations |
| Fetch | [ML models](https://learn.microsoft.com/en-us/fabric/data-science/machine-learning-model) | register model, version model, model registry, model lineage |
| Fetch | [Model training overview](https://learn.microsoft.com/en-us/fabric/data-science/model-training-overview) | SparkML, SynapseML, scikit-learn, PyTorch, XGBoost — framework comparison and selection |
| Fetch | [PREDICT function](https://learn.microsoft.com/en-us/fabric/data-science/model-scoring-predict) | batch scoring with MLFlowTransformer, Spark SQL `PREDICT`, UDF-based scoring |

### 12. Troubleshooting & Advanced

| Source | Module / Doc | When to Read |
|---|---|---|
| Local | [troubleshooting.md](notebook-authoring/troubleshooting.md) | error diagnosis, `sparkdriver.log`, `sparkexecutor.log`, notebookutils log, blobfuse log, Python logging configuration, common error patterns |
| Fetch | [notebookutils.udf](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-user-data-function) | `getFunctions()` (retrieve UDF item functions), invoke functions with positional/named params, `itemDetails`/`functionDetails` inspection, cross-workspace UDF access |
| Fetch | [T-SQL notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/author-tsql-notebook) | T-SQL cells, set primary warehouse, cross-warehouse three-part naming queries, limitations (no parameter cell, no SPN support) |
| Fetch | [NotebookUtils overview](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-utilities) | full module list, general `notebookutils.help()`, getting started with NotebookUtils |
| Fetch | [MSSparkUtils (legacy)](https://learn.microsoft.com/en-us/fabric/data-engineering/microsoft-spark-utilities) | `mssparkutils` backward compatibility reference — **deprecated, use `notebookutils` instead** |

---

## Code Generation Approach

For each code generation or modification request, follow these 6 steps in order:

1. **Fetch notebook context** — resolve workspace, lakehouse, and environment info using local-files-first strategy (see [context-resolution.md](notebook-authoring/context-resolution.md))
2. **Detect user intent and required Fabric functionality**
3. **Prioritize data discovery** — verify data paths and schemas before generating code (see [Data Discovery Approach](#data-discovery-approach))
4. **Retrieve knowledge** — consult the [Module Index](#module-index) first, then fetch Microsoft Learn MCP docs for Fabric-specific APIs. Use internal knowledge only for standard operations (transformations, visualizations) or when retrieval fails.
5. **Generate code** — apply the [Code Generation Rules](#code-generation-rules)
6. **Validate and iterate** — check for correctness, fix issues if detected

---

## Data Discovery Approach

1. **NEVER assume table/file locations or schema names** — always verify actual paths before generating code.
2. When a request involves datasets or business-oriented data **and the required data resources are unclear**, first discover candidate resources (e.g., list lakehouse tables, list files, preview table).
3. Inspect returned resources and determine exactly which ones are strictly required.
4. If returned resources are vague or insufficient, call additional discovery to clarify.
5. Only after identifying minimal required resources, proceed with code generation. Ignore unrelated resources.

---

## Code Generation Rules

1. **Verify all prerequisites before generating code** — ensure the Code Generation Approach steps are complete; if any steps are missing, stop and complete them first.
2. **Prioritize existing notebook code context** — treat the current notebook's existing cells as the primary context. Align new code with existing variables, imports, and logic rather than redefining them, unless the user explicitly requests otherwise.
3. **Avoid standalone Spark application code** — do not generate entry points like `SparkSession.builder.appName(...)` or standalone scripts. Generated code must be directly executable **within a Fabric notebook cell**, using the built-in `spark` session and runtime context.
4. **Always use language magic for non-Python code** — see [Notebook Fundamentals § Language Magic Commands](#notebook-fundamentals). Never change cell language attribute — only add the magic command (not necessary if the user switches to the appropriate kernel).
5. **Preserve code style and format** — follow the existing code style and structure within the user's notebook unless explicitly requested otherwise.
6. **Handle cross-cell dependencies carefully** — if a change affects other cells (variable definitions, function changes, imports), identify impacted cells and suggest updates one by one.
7. **Prefer user-ingested libraries** — check the user's uploaded libraries in the notebook's `builtin` folder or attached Environment artifact. Avoid suggesting standard alternatives when custom versions exist.
8. **Incorporate workspace environment settings** — consider customized packages and libraries in the workspace environment. Prefer libraries already installed or configured.
9. **Use `%pip` instead of `!pip`** — `!pip` only installs on driver; `%pip` installs on driver and executors.
10. **Never hardcode secrets** — use `notebookutils.credentials.getSecret()` for Key Vault, `getToken()` for service tokens.
11. **Verify lakehouse schema-enabled status before path/table construction** — wrong format causes "path not found" or "table not found".
12. **Prefer GUIDs over names in ABFSS paths** — immutable, won't break on rename.
13. **Never mix IDs and names in the same ABFSS path** — causes runtime errors.
14. **Never call `session.stop()` in pipeline mode** — pipelines auto-stop sessions; calling it manually causes errors.
15. **Never call `notebookutils.notebook.exit()` inside try-catch** — `exit()` raises an exception internally; if caught by a surrounding try-catch, the exit does not take effect. Always call `exit()` outside try-catch blocks.

---

## Response Style

- **Concise but authoritative** — include reasoning behind design choices
- **Stepwise clarity** — number each code step with explanation
- **Runnable-only code** — every block must be directly executable in a Fabric Notebook cell
- **Verification guidance** — provide cells for confirming correctness
- **Follow-up suggestions** — after completing operations, offer 1–2 brief suggestions for next logical steps. Skip for pure conceptual Q&A.
