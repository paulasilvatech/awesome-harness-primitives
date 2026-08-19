# `dbutils` → `notebookutils` Complete API Mapping

Exhaustive side-by-side reference for porting Databricks `dbutils` calls to Microsoft Fabric `notebookutils`.

---

## Quick Compatibility Summary

| `dbutils` Module | `notebookutils` Status | Action |
|---|---|---|
| `dbutils.fs` (file ops) | ✅ **Full equivalent** — `notebookutils.fs` | Direct namespace swap; OneLake/ABFSS paths instead of DBFS |
| `dbutils.fs` (mount/unmount/mounts) | ✅ **Supported** — `notebookutils.fs.mount/unmount/mounts/getMountPath` | Same API shape; OneLake Shortcuts are the higher-level alternative for sharing data |
| `dbutils.secrets` | ✅ **Equivalent** — `notebookutils.credentials` | Scope→Key Vault URL; key→secret name. Also exposes `getToken`, `putSecret`, `isValidToken` |
| `dbutils.notebook` | ✅ **Superset** — `notebookutils.notebook` | `run`/`exit` direct swap. Adds `runMultiple` (DAG), `validateDAG`, cross-workspace runs, and CRUD (`create`/`get`/`list`/`update`/`delete`) |
| `dbutils.widgets` | ⚠️ **No direct equivalent** | Mark a cell as a **parameters cell** (pipeline / parent-notebook injection writes a new cell beneath it that overrides the defaults). For centralized cross-notebook config, use `notebookutils.variableLibrary` |
| `dbutils.library.restartPython()` | ✅ **Supported** — `notebookutils.session.restartPython()` | Direct replacement |
| `dbutils.library.install*()` | ❌ **Not available at runtime** | Use Fabric **Environments** for library management (preferred) or in-session `%pip install` + `notebookutils.session.restartPython()` |
| `dbutils.data.summarize()` | ❌ **Not available** | Use `display(df.summary())` or pandas `.describe()` |
| `dbutils.jobs` | ⚠️ **Different model** | Fabric uses Pipelines / Spark Job Definitions; runtime/job context via `notebookutils.runtime.context` |
| `dbutils.secrets.listScopes()` / `.list()` | ❌ **Not available** | Key Vault URLs are referenced directly; enumerate secrets via Azure CLI / Key Vault SDK |
| `dbutils.fs.refreshMounts()` | ❌ **Not available** | Not needed — `notebookutils.fs.mount()` already attaches the mount to the driver **and all worker nodes** in one call, so there's no separate mount-registry propagation step |

---

## `dbutils.fs` → `notebookutils.fs`

Most `fs` methods are direct replacements — only paths change (DBFS → OneLake/ABFSS). A few have minor signature differences (called out below).

| `dbutils.fs` Method | `notebookutils.fs` Equivalent | Notes |
|---|---|---|
| `dbutils.fs.ls(path)` | `notebookutils.fs.ls(path)` | Returns `FileInfo` list (`name`, `path`, `size`, `isDir`, `isFile`) |
| `dbutils.fs.cp(src, dest, recurse=False)` | `notebookutils.fs.cp(src, dest, recurse=False)` | **Identical**. In Python notebooks, internally uses azcopy (same as `fastcp`) |
| `dbutils.fs.mv(src, dest, recurse=False)` | `notebookutils.fs.mv(src, dest, create_path=…, overwrite=False)` | ⚠️ **Signature differs**: no `recurse`; uses `create_path` and `overwrite`. `create_path` default is `False` in PySpark/Scala/R and `True` in Python notebooks — set it explicitly |
| `dbutils.fs.rm(path, recurse=False)` | `notebookutils.fs.rm(path, recurse=False)` | **Identical** |
| `dbutils.fs.mkdirs(path)` | `notebookutils.fs.mkdirs(path)` | **Identical** |
| `dbutils.fs.put(path, contents, overwrite=False)` | `notebookutils.fs.put(path, contents, overwrite=False)` | **Identical**. No atomicity guarantees for concurrent writes |
| `dbutils.fs.head(path, maxBytes=65536)` | `notebookutils.fs.head(path, max_bytes=102400)` | ⚠️ **Default differs**: Python/Scala `102400` (100 KB), R `65535` (Scala uses `maxBytes`) |
| `dbutils.fs.append(path, contents, createIfNotExists)` | `notebookutils.fs.append(file, content, createFileIfNotExists=False)` | **Equivalent**. Add `time.sleep(0.5)` between writes in loops (async flush) |
| `dbutils.fs.mount(source, mountPoint, …)` | `notebookutils.fs.mount(source, mountPoint, extraConfigs=None)` | ✅ **Supported**. Microsoft Entra (default), `accountKey`, or `sasToken` auth. `extraConfigs` also accepts `timeout` (default 30 s — increase for mounts under high executor count) and `fileCacheTimeout`. [(docs)](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-mount) |
| `dbutils.fs.unmount(mountPoint)` | `notebookutils.fs.unmount(mountPoint)` | ✅ **Supported**. Not automatic on session end — call it explicitly |
| `dbutils.fs.mounts()` | `notebookutils.fs.mounts()` | ✅ **Supported**. Returns array of `MountPointInfo` |
| `dbutils.fs.refreshMounts()` | ❌ Not available | Not needed — `notebookutils.fs.mount()` attaches the mount to the driver and **all worker nodes** in one call, so there's no separate mount-registry propagation step. (Note: file-content cache freshness is a different concern — control that via `fileCacheTimeout` in the `mount()` `extraConfigs`.) |
| `dbutils.fs.updateMount(...)` | ❌ Not available | `unmount()` then `mount()` again with new config |
| `dbutils.fs.help()` | `notebookutils.fs.help()` | **Identical** |
| _(no dbutils equivalent)_ | `notebookutils.fs.exists(path)` | New — prefer over try/except for existence checks |
| _(no dbutils equivalent)_ | `notebookutils.fs.fastcp(src, dest, recurse=True, extraConfigs=None)` | New — azcopy-backed; use for large/bulk copies. Doesn't work across OneLake regions — fall back to `cp`. For S3/GCS-typed OneLake Shortcuts use a **mounted path** instead of the `abfss://` path. [(docs)](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-file-system) |
| _(no dbutils equivalent)_ | `notebookutils.fs.getMountPath(mountPoint, scope="")` | New — returns the local FS path (`/synfs/notebook/{sessionId}/...`) for a mount |
| _(no dbutils equivalent)_ | `notebookutils.fs.getProperties(path)` | New — Python notebooks only (not in PySpark/Scala/R). Returns a map of file properties (e.g. size, timestamps) |

### Path Migration: DBFS → OneLake

```python
# Databricks: DBFS path
dbutils.fs.ls("dbfs:/mnt/mydata/bronze/")
dbutils.fs.ls("/mnt/mydata/bronze/")         # shorthand

# Fabric: OneLake path (Files section of attached Lakehouse)
notebookutils.fs.ls("Files/mydata/bronze/")  # relative path

# Or explicit OneLake path
notebookutils.fs.ls(
    "abfss://MyWorkspace@onelake.dfs.fabric.microsoft.com/BronzeLakehouse.Lakehouse/Files/mydata/bronze/"
)
```

### Migrating `dbutils.fs.mount()`

Fabric supports **two** patterns for accessing remote storage. Pick the one that fits your scenario:

**Option A — `notebookutils.fs.mount()` (direct equivalent of `dbutils.fs.mount()`)**

Use this when you need a local file-system path (e.g. for libraries that don't speak ABFSS), when you're porting code that already relies on a mount, or for ad-hoc mounts inside a session.

```python
# BEFORE — Databricks
dbutils.fs.mount(
    source="abfss://container@storageaccount.dfs.core.windows.net/",
    mount_point="/mnt/mydata",
    extra_configs={
        "fs.azure.account.oauth2.client.secret": dbutils.secrets.get("myScope", "clientSecret"),
        # ...other OAuth configs
    }
)

# AFTER — Fabric: Microsoft Entra (default, recommended) — no credentials in code
notebookutils.fs.mount(
    "abfss://container@storageaccount.dfs.core.windows.net",
    "/mydata"
)

try:
    # Access the mounted data:
    local_path = notebookutils.fs.getMountPath("/mydata")      # /synfs/notebook/{sessionId}/mydata
    with open(f"{local_path}/file.csv", "r") as f:
        data = f.read()
finally:
    # Mounts are NOT released automatically when the session ends — always unmount.
    notebookutils.fs.unmount("/mydata")
```

Alternative auth modes — pick **one** of these in place of the Entra `mount()` call above (don't mount the same point twice without an `unmount()` in between):

```python
# Auth via account key from Key Vault
account_key = notebookutils.credentials.getSecret("https://my-kv.vault.azure.net/", "storageKey")
notebookutils.fs.mount(
    "abfss://container@storageaccount.dfs.core.windows.net",
    "/mydata",
    {"accountKey": account_key}
)

# Or auth via SAS token from Key Vault
sas_token = notebookutils.credentials.getSecret("https://my-kv.vault.azure.net/", "storageSas")
notebookutils.fs.mount(
    "abfss://container@storageaccount.dfs.core.windows.net",
    "/mydata",
    {"sasToken": sas_token}
)
```

> Fabric mounts are **job-level**, not durable workspace-level shortcuts. Unmounting is **not automatic** when a session ends — mount points stay on the node until you call `unmount()` explicitly, so always pair `mount()` with `unmount()` (a `try/finally` block is the safe pattern).

**Option B — OneLake Shortcuts (preferred for cross-workspace / persistent data sharing)**

Use this when the same external location is consumed by many notebooks/pipelines, or when you want the storage to appear permanently inside a Lakehouse without per-session setup.

```python
# Create a OneLake Shortcut once (Portal or REST API):
# https://learn.microsoft.com/fabric/onelake/onelake-shortcuts
# Then access directly — no runtime mounting required:
df = spark.read.parquet("Files/mydata/bronze/customers/")
```

---

## `dbutils.secrets` → `notebookutils.credentials`

The concept maps directly — Databricks secret scopes correspond to Azure Key Vault instances.

| `dbutils.secrets` Method | `notebookutils.credentials` Equivalent | Notes |
|---|---|---|
| `dbutils.secrets.get(scope, key)` | `notebookutils.credentials.getSecret(keyVaultUrl, secretName)` | `scope` → Key Vault URL; `key` → secret name. Secrets are auto-redacted in notebook output |
| `dbutils.secrets.getBytes(scope, key)` | `notebookutils.credentials.getSecret(keyVaultUrl, secretName)` | Returns string; encode to bytes if needed |
| `dbutils.secrets.list(scope)` | ❌ Not available | Use Azure CLI / Key Vault SDK to list secrets |
| `dbutils.secrets.listScopes()` | ❌ Not available | Key Vault URLs are referenced directly |
| `dbutils.secrets.help()` | `notebookutils.credentials.help()` | |

`notebookutils.credentials` also exposes capabilities that have no `dbutils.secrets` equivalent:

| Method | Description |
|---|---|
| `notebookutils.credentials.getToken(audience)` | Get a Microsoft Entra token for `storage`, `pbi`, `keyvault`, or `kusto` audiences. Use to call Azure Storage, Fabric/Power BI REST, Key Vault, and Kusto without managing credentials |
| `notebookutils.credentials.putSecret(keyVaultUrl, secretName, secretValue)` | Write/update a secret in Azure Key Vault (requires Set permission). **Not available in the public Scala API** |
| `notebookutils.credentials.isValidToken(token)` | Check whether a token is unexpired before reusing it in long-running jobs. **Not available in the public Scala API** |

```python
# BEFORE — Databricks
password = dbutils.secrets.get(scope="prod-secrets", key="db-password")
api_key  = dbutils.secrets.get(scope="prod-secrets", key="api-key")

# AFTER — Fabric
password = notebookutils.credentials.getSecret(
    "https://my-keyvault.vault.azure.net/",
    "db-password"
)
api_key = notebookutils.credentials.getSecret(
    "https://my-keyvault.vault.azure.net/",
    "api-key"
)
```

> The Fabric notebook's managed identity (or the signed-in user) must have **Key Vault Secrets User** role on the Key Vault.

---

## `dbutils.notebook` → `notebookutils.notebook`

`notebookutils.notebook` is a **superset** of `dbutils.notebook`. `run`/`exit` are direct replacements, and it also adds DAG-based parallel execution, cross-workspace runs, and CRUD operations on notebook artifacts.

| `dbutils.notebook` Method | `notebookutils.notebook` Equivalent | Notes |
|---|---|---|
| `dbutils.notebook.run(path, timeout, arguments)` | `notebookutils.notebook.run(path, timeout_seconds=90, arguments=None, workspace="")` | `path` is the child notebook **name**. `workspace` is the **workspace ID** for cross-workspace runs (Runtime ≥ 1.2). For workspace **name or ID**, use `runMultiple()` with the activity-level `workspace` field. ⚠️ **Lakehouse-binding rule**: the child must use the parent's default lakehouse, inherit it, or have none — otherwise the run is blocked. Pass `useRootDefaultLakehouse=True` in `arguments` to bypass. [(docs)](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-notebook-run) |
| `dbutils.notebook.exit(value)` | `notebookutils.notebook.exit(value)` | **Identical**. Don't wrap in `try/except` — the exit signal won't propagate |
| `dbutils.notebook.help()` | `notebookutils.notebook.help()` | **Identical** |

`notebookutils.notebook` also adds:

| Method | Description |
|---|---|
| `runMultiple(dag, config=None)` | Run notebooks in parallel with a DAG. Root keys: `activities`, `timeoutInSeconds`, `concurrency`. Per-activity keys: `name`, `path`, `args`, `workspace` (name **or** ID), `timeoutPerCellInSeconds`, `retry`, `retryIntervalInSeconds`, `dependencies`. Returns `{activity: {exitVal, exception}}`. Replaces hand-rolled Threads/Futures in Databricks |
| `validateDAG(dag)` | Validates DAG structure (duplicate names, missing/circular deps) before `runMultiple` |
| `create / get / getDefinition / update / updateDefinition / delete / list` | Notebook artifact CRUD — useful for CI/CD and templating workflows. No `dbutils` equivalent |

```python
# BEFORE — Databricks
result = dbutils.notebook.run(
    "/path/to/silver_transform",
    timeout=600,
    arguments={"input_date": "2024-01-01", "env": "prod"}
)
dbutils.notebook.exit("completed")

# AFTER — Fabric: single notebook
result = notebookutils.notebook.run(
    "silver_transform",          # notebook name in the same workspace
    600,
    {"input_date": "2024-01-01", "env": "prod"}
)

# AFTER — Fabric: cross-workspace (pass the workspace ID)
result = notebookutils.notebook.run(
    "silver_transform",
    600,
    {"input_date": "2024-01-01"},
    "fe0a6e2a-a909-4aa3-a698-0a651de790aa"   # workspace ID (single run() requires ID)
)

notebookutils.notebook.exit("completed")
```

```python
# AFTER — Fabric: parallel DAG (replaces Databricks Threads/Futures patterns)
DAG = {
    "activities": [
        {"name": "Extract",   "path": "bronze_ingest", "args": {"date": "2024-01-01"}},
        {"name": "Transform", "path": "silver_transform",
         "args": {"in": "@activity('Extract').exitValue()"},
         "dependencies": ["Extract"], "retry": 2, "retryIntervalInSeconds": 30},
    ],
    "concurrency": 4,
    "timeoutInSeconds": 3600,
}
notebookutils.notebook.validateDAG(DAG)
results = notebookutils.notebook.runMultiple(DAG)
```

---

## `dbutils.widgets` — No Direct Equivalent

Databricks widgets are interactive UI controls. Fabric uses **parameter cells** (mark a cell as "parameters" in the UI — values are overridden at runtime), with `notebookutils.variableLibrary` for centralized configuration.

### Pattern 1: Parameter cell (most common — works for both pipeline injection and parent→child runs)

```python
# BEFORE — Databricks: define widget, read in notebook
dbutils.widgets.text("input_date", "2024-01-01", "Input Date")
input_date = dbutils.widgets.get("input_date")

# AFTER — Fabric: mark a cell as a parameters cell. In the notebook UI, open the cell's
# More commands ("...") and select "Mark cell as parameters" (older UI: "Toggle parameter cell").
# Declare defaults — at runtime, the engine adds a NEW cell beneath the parameters cell that
# overrides these values. Override sources:
#   - Fabric Pipeline notebook activity (Base parameters)
#   - notebookutils.notebook.run(..., arguments={...}) from a parent notebook
input_date = "2024-01-01"
env = "dev"
```

### Pattern 2: Centralized config via Variable Library

```python
# AFTER — Fabric: pull environment-specific values from a Variable Library
# (deployment pipelines activate the right value set per stage)
cfg = notebookutils.variableLibrary.getLibrary("app_config")
input_date = cfg.input_date
api_endpoint = cfg.api_endpoint
```

> ⚠️ **Caveats** (per [docs](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-variable-library)): `notebookutils.variableLibrary` is **same-workspace only** — cross-workspace reads (including child notebooks in a cross-workspace reference run) are not supported. **Service Principal (SPN) identity is not supported** for variable library calls, so this pattern can't drive centralized config in SPN-authenticated CI/CD pipelines today.

### Pattern 3: Parent notebook passes parameters to child

```python
# AFTER — Fabric: parent calls child with explicit args
result = notebookutils.notebook.run(
    "child_notebook",
    300,
    {"input_date": "2024-01-01", "table_name": "fact_orders"}
)
# In child_notebook, the parameter cell values are replaced with the passed args at runtime
```

---

## `dbutils.library` → Fabric Environments + `notebookutils.session`

`dbutils.library.install*()` runtime install isn't available in Fabric — use **Fabric Environments** for reproducible library management. The interpreter restart helper, however, **is** available as `notebookutils.session.restartPython()`.

| `dbutils.library` Method | Fabric Equivalent | Notes |
|---|---|---|
| `dbutils.library.installPyPI(pkg, version)` | Fabric **Environment** item (preferred) — add the package to its pip list; or `%pip install <pkg>==<version>` in-session | Environment attach gives reproducible, workspace-scoped library sets |
| `dbutils.library.install("dbfs:/...whl")` | Upload the wheel as a **custom library** in a Fabric Environment, or `%pip install /lakehouse/default/Files/mylib.whl` | |
| `dbutils.library.restartPython()` | `notebookutils.session.restartPython()` | ✅ **Direct replacement** (Python and PySpark notebooks only — not available in Scala/R). In PySpark, restarts only the Python interpreter and keeps the Spark context. Import new packages in the next cell |
| `dbutils.library.list()` | ❌ Not available | Inspect Environment configuration in the Fabric Portal / REST API |

```python
# BEFORE — Databricks: runtime library install
dbutils.library.installPyPI("scikit-learn", version="1.3.0")
dbutils.library.install("dbfs:/mnt/libs/mylib-1.0.whl")
dbutils.library.restartPython()

# AFTER — Fabric option A (preferred): Fabric Environment
# 1. Create a Fabric Environment item in the workspace.
# 2. Add `scikit-learn==1.3.0` to the Environment's pip packages.
# 3. For custom .whl files, upload as a custom library on the Environment item.
# 4. Attach the Environment to the notebook (or set as workspace default).
# No code change needed — the library is available on session start.

# AFTER — Fabric option B (ad-hoc, session-scoped): %pip + restartPython
# Cell 1: install and restart
%pip install scikit-learn==1.3.0
notebookutils.session.restartPython()

# Cell 2 (a NEW cell — code after restartPython() in the same cell does NOT run):
import sklearn
```

### Also available: stop the interactive session

```python
notebookutils.session.stop()        # async; releases Spark resources to the pool
# PySpark/Scala/R: stop() accepts an optional `detach` parameter (Python notebook doesn't).
#   - Default behavior (detach=True): on a high-concurrency session, detaches the session
#     instead of stopping it entirely.
#   - stop(detach=False): fully stops a high-concurrency session.
```

---

## `dbutils.data` — Use display() or pandas

```python
# BEFORE — Databricks: summarize a DataFrame
dbutils.data.summarize(df)

# AFTER — Fabric: use built-in display or pandas
display(df.summary())           # Spark summary stats in Fabric display
display(df.describe())          # Alternative
df.toPandas().describe()        # Full pandas stats (for small DataFrames only)
```

---

## Runtime Context

`notebookutils.runtime.context` returns a read-only map. Property names use the `current*` / `default*` / `root*` prefix — they are **not** the same names as Databricks tags. The sample below shows the most common keys; the full key list (including `defaultLakehouseWorkspaceId`, `currentRunId`/`parentRunId`/`rootRunId`, `rootNotebookName`, `clusterId`, `poolName`, `environmentWorkspaceId`, `currentKernel`, `productType`, `hcReplId`, etc.) is on the [runtime context docs page](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-runtime).

```python
# BEFORE — Databricks: access job context
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
workspace = ctx.tags().get("orgId").get()
job_id    = ctx.tags().get("jobId").get()

# AFTER — Fabric
ctx = notebookutils.runtime.context

workspace_id        = ctx["currentWorkspaceId"]
workspace_name      = ctx["currentWorkspaceName"]
notebook_id         = ctx["currentNotebookId"]
notebook_name       = ctx["currentNotebookName"]

# Default lakehouse (only populated when one is attached)
lakehouse_id        = ctx.get("defaultLakehouseId")
lakehouse_name      = ctx.get("defaultLakehouseName")

# Execution mode flags — useful for pipeline-vs-interactive branching
is_pipeline         = ctx["isForPipeline"]
is_interactive      = ctx["isForInteractive"]
is_reference_run    = ctx["isReferenceRun"]

# Job / activity identity
activity_id         = ctx["activityId"]        # Livy job ID for current activity (closest to Databricks jobId)
environment_id      = ctx.get("environmentId")
user_id             = ctx["userId"]
user_name           = ctx["userName"]
```

> The runtime context does **not** expose pipeline parameters under a `parameters` key — parameter values arrive via parameter-cell overrides (see the `dbutils.widgets` section).
