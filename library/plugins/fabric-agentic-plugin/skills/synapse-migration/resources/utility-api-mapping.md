# Synapse `mssparkutils` → Fabric `notebookutils` API Mapping

Side-by-side reference for porting `mssparkutils` calls to `notebookutils` in Microsoft Fabric.

> Most `mssparkutils` APIs have **identical signatures** in `notebookutils`. The primary change is the import/namespace. Differences are explicitly noted.

---

## Import Change

```python
# Synapse (remove this)
from notebookutils import mssparkutils  # or: import mssparkutils

# Fabric (use this — no import needed; notebookutils is pre-instantiated)
# notebookutils is available globally in Fabric notebooks
```

---

## File System (`fs`)

| `mssparkutils` | `notebookutils` | Notes |
|---|---|---|
| `mssparkutils.fs.ls(path)` | `notebookutils.fs.ls(path)` | Returns list of `FileInfo` objects |
| `mssparkutils.fs.cp(src, dest, recurse=False)` | `notebookutils.fs.cp(src, dest, recurse=False)` | **Identical** |
| `mssparkutils.fs.mv(src, dest, recurse=False)` | `notebookutils.fs.mv(src, dest, recurse=False)` | **Identical** |
| `mssparkutils.fs.rm(path, recurse=False)` | `notebookutils.fs.rm(path, recurse=False)` | **Identical** |
| `mssparkutils.fs.mkdirs(path)` | `notebookutils.fs.mkdirs(path)` | **Identical** |
| `mssparkutils.fs.put(path, content, overwrite=False)` | `notebookutils.fs.put(path, content, overwrite=False)` | **Identical** |
| `mssparkutils.fs.head(path, maxBytes=65536)` | `notebookutils.fs.head(path, maxBytes=65536)` | **Identical** |
| `mssparkutils.fs.append(path, content, createFileIfNotExists)` | `notebookutils.fs.append(path, content, createFileIfNotExists)` | **Identical** |
| `mssparkutils.fs.help()` | `notebookutils.fs.help()` | **Identical** |

### Path Format

```python
# Synapse: ADLS Gen2 path
mssparkutils.fs.ls("abfss://container@storageaccount.dfs.core.windows.net/path")

# Fabric: OneLake path
notebookutils.fs.ls("abfss://workspacename@onelake.dfs.fabric.microsoft.com/lakehouse.Lakehouse/Files/path")

# Fabric: also works with relative Lakehouse path (within attached Lakehouse)
notebookutils.fs.ls("Files/path")
```

---

## Credentials (`credentials`)

| `mssparkutils` | `notebookutils` | Notes |
|---|---|---|
| `mssparkutils.credentials.getToken(audience)` | `notebookutils.credentials.getToken(audience)` | **Identical** |
| `mssparkutils.credentials.getSecret(keyVaultUrl, secretName)` | `notebookutils.credentials.getSecret(keyVaultUrl, secretName)` | **Identical** |
| `mssparkutils.credentials.getConnectionStringOrCreds(linkedServiceName)` | **Not available** in Fabric | Linked Services do not exist in Fabric — replace with Data Connection or Key Vault secret |

```python
# Synapse — read from Linked Service (NOT available in Fabric)
conn_str = mssparkutils.credentials.getConnectionStringOrCreds("MyLinkedService")

# Fabric — read secret from Key Vault
secret = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/",
    "my-connection-string"
)
```

---

## Notebook (`notebook`)

| `mssparkutils` | `notebookutils` | Notes |
|---|---|---|
| `mssparkutils.notebook.run(name, timeout, args)` | `notebookutils.notebook.run(name, timeout, args)` | **Identical** |
| `mssparkutils.notebook.exit(value)` | `notebookutils.notebook.exit(value)` | **Identical** |
| `mssparkutils.notebook.help()` | `notebookutils.notebook.help()` | **Identical** |

```python
# Run a child notebook and receive its output value
result = notebookutils.notebook.run(
    "child_notebook_name",
    timeout=300,
    arguments={"input_param": "value"}
)
```

---

## Runtime (`runtime` / `env`)

> **Namespace change**: Synapse used `mssparkutils.env`; Fabric uses `notebookutils.runtime`.

| `mssparkutils` | `notebookutils` | Notes |
|---|---|---|
| `mssparkutils.env.getJobId()` | `notebookutils.runtime.context["activityId"]` | Context dict replaces individual env getters; `activityId` is the Livy job ID |
| `mssparkutils.env.getWorkspaceName()` | `notebookutils.runtime.context["currentWorkspaceName"]` | |
| `mssparkutils.env.getUserId()` | `notebookutils.runtime.context["userId"]` | |
| `mssparkutils.env.getUserName()` | `notebookutils.runtime.context["userName"]` | |
| `mssparkutils.env.getNotebookPath()` | `notebookutils.runtime.context["notebookPath"]` | |

```python
# Synapse
workspace = mssparkutils.env.getWorkspaceName()

# Fabric
ctx = notebookutils.runtime.context
workspace = ctx["currentWorkspaceName"]
notebook_path = ctx["notebookPath"]
job_id = ctx["activityId"]
```

---

## Lakehouse (`lakehouse`)

> **Fabric-only** — no equivalent in Synapse.

```python
# Get the default Lakehouse attached to the notebook
lh = notebookutils.lakehouse.get()
print(lh.id, lh.name, lh.workspaceId)

# List all Lakehouses in the workspace
all_lakehouses = notebookutils.lakehouse.list()

# Get a specific Lakehouse
lh = notebookutils.lakehouse.get(name="my_lakehouse")
```

---

## Connections (`connection`)

> **Fabric-only** — replaces Synapse Linked Services for external data source access.

```python
# Get a connection by name (configured in Fabric Data Connections)
conn = notebookutils.connection.get("MyConnectionName")

# Use the connection token for downstream API calls
token = notebookutils.connection.getConnectionToken("MyConnectionName")
```

See [connectivity-migration.md](connectivity-migration.md) for how to migrate Synapse Linked Services to Fabric Data Connections.
