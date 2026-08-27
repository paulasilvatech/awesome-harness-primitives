---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-api-reference.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Python Dataverse SDK API usage conventions for DataverseClient methods, DataverseConfig, DataverseError handling, OData options, and metadata operations.

# Dataverse SDK for Python Conventions — API Reference

These instructions apply to Python code that uses the PowerPlatform Dataverse SDK. They are authoritative for `DataverseClient` method usage, table and column metadata operations, `DataverseConfig`, `DataverseError`, OData query options, and SDK model names in matched Python files; project authentication, retry, logging, and data governance policies win where they define stricter runtime behavior.

## DataverseClient Operations

Initialize `DataverseClient` with the Dataverse base URL, Azure credential, and optional `DataverseConfig`. Use exact Dataverse table schema names and logical column names.

| Method | Convention | Return or behavior |
| --- | --- | --- |
| `create(table_schema_name, records)` | Create one record from a dict or bulk records from a list of dicts. | Returns a list of GUIDs. |
| `get(table_schema_name, record_id=None, select=None, filter=None, orderby=None, top=None, expand=None, page_size=None)` | Fetch one record by `record_id` or query records with OData options. | Single record or paged batches. |
| `update(table_schema_name, ids, changes)` | Update a single GUID, broadcast one changes dict to many IDs, or pair lists of IDs and change dicts one-to-one. | Performs single or bulk updates. |
| `delete(table_schema_name, ids, use_bulk_delete=True)` | Delete a single GUID or bulk records; keep async bulk delete behavior explicit. | Bulk delete returns a job id. |
| `create_table(table_schema_name, columns, solution_unique_name=None, primary_column_schema_name=None)` | Create custom tables and columns, including enum-backed choices. | Returns metadata such as `entity_logical_name`. |
| `create_columns(table_schema_name, columns)` | Add columns to an existing table. | Returns created column metadata. |
| `delete_columns(table_schema_name, columns)` | Remove columns from a table. | Returns removed column metadata. |
| `delete_table(table_schema_name)` | Delete a custom table only when destructive deletion is intended. | Irreversible table deletion. |
| `get_table_info(table_schema_name)` | Retrieve table metadata. | Includes `table_logical_name` and `entity_set_name` when found. |
| `list_tables()` | List custom tables. | Iterable table metadata. |
| `flush_cache(kind)` | Clear SDK caches such as `picklist`. | Returns removed cache entries or count. |

## Record CRUD Patterns

```python
ids = client.create("account", {"name": "Acme"})
print(ids[0])

ids = client.create("account", [{"name": "Contoso"}, {"name": "Fabrikam"}])

record = client.get("account", record_id="guid-here")

for batch in client.get(
    "account",
    filter="statecode eq 0",
    select=["name", "telephone1"],
    orderby=["createdon desc"],
    top=100,
    page_size=50,
):
    for record in batch:
        print(record["name"])

client.update("account", "guid-here", {"telephone1": "555-0100"})
client.update("account", [id1, id2, id3], {"statecode": 1})
client.update("account", [id1, id2], [{"name": "A"}, {"name": "B"}])

client.delete("account", "guid-here")
job_id = client.delete("account", [id1, id2, id3])
```

## Table and Metadata Patterns

Use SDK metadata methods for custom tables and columns instead of hand-building Web API metadata payloads in application code.

```python
from enum import IntEnum

class ItemStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    __labels__ = {
        1033: {"ACTIVE": "Active", "INACTIVE": "Inactive"}
    }

info = client.create_table("new_MyTable", {
    "new_Title": "string",
    "new_Quantity": "int",
    "new_Price": "decimal",
    "new_Active": "bool",
    "new_Status": ItemStatus,
})
print(info["entity_logical_name"])

created = client.create_columns("new_MyTable", {
    "new_Notes": "string",
    "new_Count": "int",
})

removed = client.delete_columns("new_MyTable", ["new_Notes", "new_Count"])
client.delete_table("new_MyTable")

info = client.get_table_info("new_MyTable")
if info:
    print(info["table_logical_name"])
    print(info["entity_set_name"])

tables = client.list_tables()
for table in tables:
    print(table)

removed = client.flush_cache("picklist")
```

## Configuration and Errors

Configure timeouts, retries, backoff, and language through `DataverseConfig`.

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()
cfg.http_retries = 3
cfg.http_backoff = 1.0
cfg.http_timeout = 30
cfg.language_code = 1033

client = DataverseClient(base_url=url, credential=cred, config=cfg)
```

Catch `DataverseError` for SDK-specific failures and inspect `is_transient` before retrying.

```python
from PowerPlatform.Dataverse.core.errors import DataverseError

try:
    client.create("account", {"name": "Test"})
except DataverseError as e:
    print(f"Code: {e.code}")
    print(f"Message: {e.message}")
    print(f"Transient: {e.is_transient}")
    print(f"Details: {e.to_dict()}")
```

## OData Query Options

- Use exact logical names in lowercase in `filter` expressions.
- Treat column names in `select` as auto-lowercased by the SDK.
- Treat navigation property names in `expand` as case-sensitive.
- Use `top` and `page_size` to bound query volume.
- Use `orderby` with explicit directions such as `createdon desc` when deterministic ordering matters.

## Good / Bad Examples

The examples below illustrate typed SDK querying instead of unbounded reads.

**Good:**

```python
for batch in client.get("account", select=["name"], filter="statecode eq 0", top=100, page_size=50):
    for record in batch:
        print(record["name"])
```

Why: The query selects only needed fields and bounds paging.

**Bad:**

```python
for batch in client.get("account"):
    for record in batch:
        print(record)
```

Why: The query has no field selection, filter, ordering, or paging intent.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `DataverseClient` methods for CRUD and metadata operations | SDK methods preserve expected contracts and return shapes |
| Bound queries with `select`, `filter`, `orderby`, `top`, and `page_size` | Dataverse reads stay efficient and deterministic |
| Use `DataverseConfig` for retries, backoff, timeout, and language | Runtime behavior stays centralized and testable |
| Catch `DataverseError` and inspect `is_transient` before retrying | Retry logic handles transient and permanent failures differently |
| Use exact logical names in filters and case-sensitive navigation names in `expand` | OData queries avoid schema casing mistakes |
| Use `flush_cache("picklist")` when cached labels must be refreshed | SDK metadata caches stay consistent with schema changes |
| Treat `delete_table` as irreversible | Destructive metadata operations require explicit intent |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `client.create("account", records)` for single or bulk create | Handcraft duplicate create loops without considering SDK bulk support |
| Use broadcast or paired `client.update` shapes intentionally | Mix IDs and changes lists with unclear one-to-one mapping |
| Use `use_bulk_delete=True` deliberately for bulk deletes | Hide async deletion behavior from callers |
| Model choices with `IntEnum` and `__labels__` when creating tables | Create opaque integer fields without labels |
| Import `DataverseConfig` and `DataverseError` from SDK modules | Catch broad exceptions and lose Dataverse error details |
| Use official API docs for method signatures | Guess optional parameter names from memory |

## Checklist Before Opening a PR

- [ ] `DataverseClient` CRUD calls use the documented method names and argument shapes.
- [ ] Queries include intentional `select`, `filter`, `orderby`, `top`, `expand`, or `page_size` options where applicable.
- [ ] Table and column metadata changes use `create_table`, `create_columns`, `delete_columns`, `delete_table`, `get_table_info`, `list_tables`, or `flush_cache` intentionally.
- [ ] `DataverseConfig` centralizes timeout, retry, backoff, and language behavior where configuration is needed.
- [ ] `DataverseError` handling preserves `code`, `message`, `is_transient`, and `to_dict()` details.
- [ ] OData filters use lowercase logical names and `expand` uses case-sensitive navigation names.
- [ ] Destructive deletes and metadata operations are explicitly intended and reviewed.

## References

- API docs: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.client.dataverseclient
- Config docs: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core.config.dataverseconfig
- Errors: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core.errors
