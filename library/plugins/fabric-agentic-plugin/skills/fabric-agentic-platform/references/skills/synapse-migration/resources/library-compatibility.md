# Library Compatibility: Synapse Spark 3.5 vs. Fabric Runtime 1.3

> **Last validated**: April 2026 against Fabric Runtime 1.3 (Spark 3.5, Delta 3.2). Library versions change with runtime updates — re-verify after Fabric Runtime upgrades.

Identify and resolve library gaps **before** running migrated notebooks to prevent `ImportError`, `ClassNotFoundException`, and silent behavioral differences.

---

## Quick Compatibility Check

Run this workflow to identify which gaps actually affect your code:

```
1. Export Synapse library list        →  pip freeze (in a Synapse notebook cell)
2. Export custom pool libraries       →  Synapse Studio → Manage → Spark Pools → {pool} → Packages
3. Search notebooks for imports       →  grep -r "import\|from .* import" across all .py / .ipynb files
4. Cross-reference against gap tables →  Only libraries that appear in BOTH your code AND the tables below need action
5. Pre-install in Fabric Environment  →  Add to environment.yml or upload as custom library before running notebooks
```

> **Reference manifests**: For a full line-by-line comparison of every built-in library, see the [microsoft/synapse-spark-runtime](https://github.com/microsoft/synapse-spark-runtime) GitHub repo. Compare `Fabric/Runtime 1.3` vs `Synapse/spark3.5` release notes.

---

## Python Libraries Missing from Fabric Runtime 1.3

40 Python libraries present in Synapse Spark 3.5 are absent from Fabric Runtime 1.3.

| Category | Libraries | Action |
|---|---|---|
| **CUDA / GPU** (10 libs) | `libcublas`, `libcufft`, `libcufile`, `libcurand`, `libcusolver`, `libcusparse`, `libnpp`, `libnvfatbin`, `libnvjitlink`, `libnvjpeg` | **Migration blocker** — Fabric does not support GPU pools. Refactor to CPU-based alternatives or keep on Synapse. |
| **HTTP / API clients** | `httpx`, `httpcore`, `h11`, `google-auth`, `jmespath` | Install via Environment: `pip install httpx google-auth jmespath` |
| **ML / Interpretability** | `interpret`, `interpret-core` | Install via Environment: `pip install interpret` |
| **Data serialization** | `marshmallow`, `jsonpickle`, `frozendict`, `fixedint` | Install via Environment if needed: `pip install marshmallow jsonpickle` |
| **Logging / Telemetry** | `fluent-logger`, `humanfriendly`, `library-metadata-cooker`, `impulse-python-handler` | `fluent-logger`: install if used. Others are Synapse-internal — likely not needed in user code. |
| **Jupyter internals** | `jupyter-client`, `jupyter-core`, `jupyter-ui-poll`, `jupyterlab-widgets`, `ipython-pygments-lexers` | Fabric manages Jupyter infrastructure internally. Generally not needed in user code. |
| **System / C libraries** | `libgcc`, `libstdcxx`, `libgrpc`, `libabseil`, `libexpat`, `libnsl`, `libzlib` | Low-level system libs. Usually not imported directly. Only install if you have C extensions that depend on them. |
| **File / concurrency** | `filelock`, `fsspec`, `knack` | Install via Environment if used: `pip install filelock fsspec` |

---

## Java/Scala Libraries Missing from Fabric Runtime 1.3

| Library | Synapse Version | Action |
|---|---|---|
| `azure-cosmos-analytics-spark` | 2.2.5 | Install as a **custom JAR** in the Fabric Environment if your Spark jobs use the Cosmos DB analytics connector. |
| `junit-jupiter-params` | 5.5.2 | Test-only library. Not needed in production notebooks. |
| `junit-platform-commons` | 1.5.2 | Test-only library. Not needed in production notebooks. |

---

## R Libraries

Near-identical. Only 1 gap:

| Library | Synapse | Fabric | Action |
|---|---|---|---|
| `lightgbm` | 4.6.0 | Not included | Install via Environment if needed |
| `FabricTelemetry` | Not included | 1.0.2 | Fabric-internal — no action |

---

## Notable Version Differences (Python)

68 Python libraries exist on both platforms but with different versions. Most are minor, but **17 have major version jumps** that can cause behavioral changes or breakage:

| Library | Fabric Version | Synapse Version | Risk | Impact |
|---|---|---|---|---|
| `xgboost` (`libxgboost`) | 2.0.3 | 3.0.1 | **High** | XGBoost API changes between v2 and v3. Test all model training/prediction code. |
| `flask` | 2.2.5 | 3.0.3 | **High** | Flask 3.x has breaking changes. If serving Flask APIs from notebooks, test thoroughly. |
| `libprotobuf` | 3.20.3 | 4.25.3 | **High** | Protobuf 4.x has breaking changes for custom `.proto` definitions. |
| `libpq` | 12.17 | 17.4 | **Medium** | PostgreSQL client library. Major version jump — test DB connections. |
| `libgcc-ng` / `libstdcxx-ng` | 11.2.0 | 15.2.0 | **Medium** | GCC runtime. May affect C extension compatibility. |
| `lxml` | 4.9.3 | 5.3.0 | **Medium** | Minor API changes. Test XML parsing workflows. |
| `markupsafe` | 2.1.3 | 3.0.2 | **Low** | MarkupSafe 3.x drops Python 3.7 support but API is compatible with 3.8+. |

> **Direction**: Synapse generally ships **newer** versions of system-level libraries (GCC, protobuf, libpq) while Fabric ships newer versions of data/ML libraries. If you need a specific version, pin it in your Fabric Environment configuration.

### Version Pinning Example

If a notebook depends on XGBoost 3.x behavior (available in Synapse but not the default in Fabric):

```yaml
# environment.yml — pin in your Fabric Environment
dependencies:
  - pip:
    - xgboost==3.0.1  # Fabric ships 2.0.3; pin to match Synapse version
```

---

## Pre-Migration Audit Script

Run this in a **Synapse** notebook cell to generate a dependency diff:

```python
import subprocess, json

# Get installed packages
result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
synapse_pkgs = dict(line.split("==") for line in result.stdout.strip().split("\n") if "==" in line)

# Known Fabric RT 1.3 missing packages (from gap tables above)
fabric_missing = {
    "httpx", "httpcore", "h11", "google-auth", "jmespath",
    "interpret", "interpret-core",
    "marshmallow", "jsonpickle", "frozendict", "fixedint",
    "fluent-logger", "humanfriendly",
    "filelock", "fsspec", "knack"
}

# Check which missing packages are actually installed in this Synapse pool
gaps = {pkg: ver for pkg, ver in synapse_pkgs.items() if pkg.lower() in fabric_missing}
if gaps:
    print("⚠ Libraries to pre-install in Fabric Environment:")
    for pkg, ver in sorted(gaps.items()):
        print(f"  {pkg}=={ver}")
else:
    print("✅ No missing-library gaps detected for this pool.")
```

Then search notebooks for actual usage:

```bash
# Search all notebooks for imports of gap libraries
grep -rn "import httpx\|import google.auth\|import interpret\|import marshmallow\|import jsonpickle\|import fsspec\|import filelock" *.py *.ipynb
```

---

## Resolution Workflow

```
For each gap library found in your code:
├── GPU library (libcu*, libnv*)
│   └── MIGRATION BLOCKER — refactor to CPU or keep on Synapse
├── Installable via pip/conda
│   └── Add to Fabric Environment environment.yml → publish
├── Custom JAR (azure-cosmos-analytics-spark)
│   └── Upload JAR to Fabric Environment custom libraries → publish
└── Version difference (e.g., xgboost 2.x vs 3.x)
    └── Pin specific version in environment.yml OR test with Fabric default
```

> After resolving all gaps, the Fabric Environment from [Phase 0](spark-pool-migration.md) should include all required libraries before running Phase 2/3 notebooks and SJDs.
