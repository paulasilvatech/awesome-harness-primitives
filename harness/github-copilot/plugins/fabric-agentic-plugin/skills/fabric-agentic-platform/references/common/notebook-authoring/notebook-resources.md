# Notebook Resource Files — builtin/ and env/ Folders

How to access notebook resource files (small files stored with the notebook or Environment artifact).

## Overview

| Resource Type | Folder | Scope | Sharing |
|---|---|---|---|
| Built-in | `builtin/` | Notebook-specific | Only the owning notebook |
| Environment | `env/` | Environment-scoped | All notebooks attached to the same Environment artifact |

**Best Practice**: Always use `notebookutils.nbResPath` to get the absolute local path first, ensuring consistency across all APIs.

---

## Storage Limits

| Limit | Value |
|---|---|
| Maximum folder size | 500 MB |
| Maximum file size | 100 MB |
| Maximum files/folders | 100 |

For larger files, use a Lakehouse instead.

---

## Path Rules by API Type

### Python Built-in I/O (open, pandas, json, etc.)

Use absolute path from `notebookutils.nbResPath`. No `file:` prefix needed.

- `open(f"{notebookutils.nbResPath}/builtin/config.json")`
- `pd.read_csv(f"{notebookutils.nbResPath}/env/shared_data.csv")`
- For `import` statements: `from builtin.my_module import my_function` works directly

> Relative paths (e.g., `open("builtin/config.json")`) also work for Python I/O but absolute paths are recommended for consistency.

### Spark & notebookutils.fs APIs

**MUST** use `file:` prefix AND absolute path from `notebookutils.nbResPath`. Both are mandatory — omitting either causes failure.

- `spark.read.csv(f"file:{notebookutils.nbResPath}/builtin/data.csv")`
- `notebookutils.fs.ls(f"file:{notebookutils.nbResPath}/builtin")`
- `notebookutils.fs.cp(f"file:{notebookutils.nbResPath}/env/data.csv", "Files/destination.csv")`

**Common failure modes:**
- Missing `file:` prefix → path not found
- Using relative path (e.g., `file:builtin/data.csv`) → path not found
- Missing absolute path → path not found

---

## Quick Reference Table

| API Type | Resource Type | Path Format |
|---|---|---|
| Python I/O | builtin | `{notebookutils.nbResPath}/builtin/{path}` |
| Python I/O | env | `{notebookutils.nbResPath}/env/{path}` |
| Spark | builtin | `file:{notebookutils.nbResPath}/builtin/{path}` |
| Spark | env | `file:{notebookutils.nbResPath}/env/{path}` |
| notebookutils.fs | builtin | `file:{notebookutils.nbResPath}/builtin/{path}` |
| notebookutils.fs | env | `file:{notebookutils.nbResPath}/env/{path}` |

---

## Key Rules

1. **Always use `notebookutils.nbResPath`** for the absolute path — never construct paths manually.
2. **Spark & notebookutils.fs require `file:` prefix + absolute path** — mandatory, no exceptions.
3. **Python built-in I/O works without `file:` prefix** — but still prefer absolute paths.
4. **Use `builtin/` for notebook-specific files**, `env/` for shared files across notebooks.
5. **For files > 100 MB, use Lakehouse** — notebook resources are for small, supporting files.

**Documentation**: [Notebook resources](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook#notebook-resources)
