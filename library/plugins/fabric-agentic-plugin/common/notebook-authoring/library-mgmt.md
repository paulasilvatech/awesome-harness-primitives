# Library Management — Environments, Inline Install, and Custom Libraries

How to install, manage, and discover libraries in Fabric Notebooks.

> **Public documentation — fetch for detailed guidance:**
> - [Manage Apache Spark libraries in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/library-management) — best practices, supported library types, inline install (%pip/%conda), pipeline considerations
> - [Manage libraries in Fabric environments](https://learn.microsoft.com/en-us/fabric/data-engineering/environment-manage-library) — built-in libraries, external repositories (PyPI/Conda/Maven/private), custom libraries (.whl/.jar/.tar.gz), publish modes (Quick vs Full)
> - [Environment public APIs](https://learn.microsoft.com/en-us/fabric/data-engineering/environment-public-api) — REST API for environment CRUD, list/upload/delete libraries, publish operations

---

## Built-in Library Lists

Each Fabric Spark runtime ships with pre-installed Python libraries. The authoritative, version-pinned lists are maintained in the [microsoft/synapse-spark-runtime](https://github.com/microsoft/synapse-spark-runtime/tree/main/Fabric) GitHub repo.

**To check if a library is already built-in**, fetch the raw YAML for the target runtime:

| Runtime | Spark | Python | Java | Scala | Delta Lake | OS | YAML File |
|---|---|---|---|---|---|---|---|
| 1.2 | 3.4.3 | 3.10 | 11 | 2.12.17 | 2.4 | Mariner 2.0 | [`Fabric-Python310-CPU.yml`](https://github.com/microsoft/synapse-spark-runtime/blob/main/Fabric/Runtime%201.2%20(Spark%203.4)/Fabric-Python310-CPU.yml) |
| 1.3 | 3.5.5 | 3.11 | 11 | 2.12.18 | 3.2 | Mariner 2.0 | [`Fabric-Python311-CPU.yml`](https://github.com/microsoft/synapse-spark-runtime/blob/main/Fabric/Runtime%201.3%20(Spark%203.5)/Fabric-Python311-CPU.yml) |
| 2.0 | 4.0.1 | 3.12 | 21 | 2.13.16 | 4.0 | Azure Linux 3.0 | [`Fabric-Python313-CPU.yml`](https://github.com/microsoft/synapse-spark-runtime/blob/main/Fabric/Runtime%202.0%20(Spark%204.0)/Fabric-Python313-CPU.yml) |

> All files are in [`microsoft/synapse-spark-runtime`](https://github.com/microsoft/synapse-spark-runtime/tree/main/Fabric). Version details from `Components.json` in each runtime folder.

The YAML is a conda `dependencies:` list with `name=version` entries. Search for the library name to confirm availability and version.

**When to check**: before suggesting `%pip install` for a common library — it may already be built-in.

---

## Import Patterns for User-Uploaded Libraries

```python
# User-uploaded module in builtin/ folder — direct import
from builtin.my_module import my_function

# User-uploaded module in env/ folder — direct import
from env.shared_utils import helper

# User-uploaded wheel installed in Environment — standard import
import my_custom_package
```

---

## Key Rules

1. **Check built-in libraries first** — fetch the runtime YAML above before suggesting `%pip install`. Don't install what's already pre-loaded.
2. **Use Environment artifacts for production** — install libraries via Environment (Full mode) for reproducible, versioned dependency management. `%pip install` is session-scoped and non-persistent — use only for prototyping and interactive exploration.
3. **Prefer user-ingested libraries** — check uploaded libraries in `builtin/` or attached Environment before suggesting standard alternatives.
4. **Restart Python after inline installs** — `notebookutils.session.restartPython()` (variables defined before install are lost).
5. **Use `%pip` not `!pip`** — `!pip` only installs on the driver node; `%pip` installs on driver and executors.
6. **`%pip install` is disabled in pipeline runs by default** — if needed, add `_inlineInstallationEnabled=True` as a notebook activity parameter.
7. **Full mode for production, Quick mode for iteration** — Full mode creates a stable snapshot with dependency resolution; Quick mode skips resolution and installs at session start.
