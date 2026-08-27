---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-sdk.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Python Dataverse SDK preview conventions for installation, authentication, CRUD, bulk operations, file upload, paging, and table metadata. Use when writing Python code that calls Microsoft Dataverse.

# Dataverse SDK for Python Conventions — Official Preview Client

These instructions apply to Python files that install, authenticate, configure, or call the preview Microsoft Dataverse SDK for Python. They are authoritative for `PowerPlatform-Dataverse-Client` client setup, `DataverseClient` usage, CRUD calls, bulk operations, file upload, paging, and table metadata examples in matched files; organization authentication, tenant policy, and production retry standards win where they define stricter requirements.

## Runtime, Package, and Configuration

Use the official preview package and keep examples aligned with Microsoft Learn guidance.

| Concern | Convention |
| --- | --- |
| Python runtime | Use Python 3.10+ for SDK examples and project code that imports the package. |
| Package install | Install with `pip install PowerPlatform-Dataverse-Client`. |
| Dataverse access | Assume a Dataverse environment with read/write privileges and network access to PyPI. |
| Base URL | Use the environment URL shape `https://<myorg>.crm.dynamics.com`; replace `<myorg>` with the tenant-specific organization name. |
| Configuration | Create a `DataverseConfig()` and adjust `cfg.http_retries`, `cfg.http_backoff`, and `cfg.http_timeout` when HTTP behavior must be tuned. |
| Defaults | Remember that `DataverseConfig()` defaults to `language_code=1033`. |

## Authentication and Client Construction

Create the client with an Azure Identity credential and the official SDK types.

```python
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()  # defaults to language_code=1033
client = DataverseClient(
    base_url="https://<myorg>.crm.dynamics.com",
    credential=InteractiveBrowserCredential(),
    config=cfg,
)
```

Use `InteractiveBrowserCredential` for quickstart and local interactive examples. Use the project-approved Azure Identity credential for non-interactive automation instead of embedding usernames, passwords, client secrets, or tokens in Python source.

## CRUD and Bulk Data Operations

Preserve the SDK method semantics when writing examples or production wrappers.

| Operation | Convention |
| --- | --- |
| Create one row | `client.create("account", {"name": "Acme, Inc.", "telephone1": "555-0100"})[0]` returns the first GUID from a `list[str]`. |
| Retrieve one row | `client.get("account", account_id)` retrieves a single record by table logical name and GUID. |
| Update one row | `client.update("account", account_id, {"telephone1": "555-0199"})` returns `None`. |
| Delete one row | `client.delete("account", account_id)` deletes by table logical name and GUID. |
| Bulk create | `client.create("account", [{"name": "Contoso"}, {"name": "Fabrikam"}])` returns IDs for created records. |
| Broadcast patch | `client.update("account", ids, {"telephone1": "555-0200"})` applies one patch to many IDs. |
| One-to-one patches | `client.update("account", ids, [{"telephone1": "555-1200"}, {"telephone1": "555-1300"}])` aligns each patch with the matching ID. |

Use Dataverse logical table and column names such as `account`, `accountid`, `name`, `createdon`, `telephone1`, and metadata keys such as `entity_logical_name` and generated primary-name columns such as `f"{logical}name"` exactly as the target environment defines them.

## Files, Paging, and Metadata

Use the SDK's built-in helpers instead of hand-rolling Web API calls for supported operations.

| Scenario | Convention |
| --- | --- |
| Simple file upload | `client.upload_file('account', record_id, 'sample_filecolumn', 'test.pdf')`. |
| Chunked file upload | `client.upload_file('account', record_id, 'sample_filecolumn', 'test.pdf', mode='chunk', if_none_match=True)`. |
| Retrieve multiple | Use `client.get("account", select=["accountid", "name", "createdon"], orderby=["name asc"], top=10, page_size=3)` and iterate the returned `pages`. |
| Table creation | `client.create_table("SampleItem", {"code": "string", "count": "int", "amount": "decimal", "when": "datetime", "active": "bool"})`. |
| Table cleanup | Delete sample data with `client.delete(logical, rec_id)` before `client.delete_table("SampleItem")`. |

Keep quickstart snippets copyable, but remove sample records and sample tables from production paths once examples are no longer needed.

## Good / Bad Examples

The examples below illustrate safe SDK construction and CRUD semantics.

**Good**

```python
cfg = DataverseConfig()
cfg.http_timeout = 30
client = DataverseClient(
    base_url="https://<myorg>.crm.dynamics.com",
    credential=InteractiveBrowserCredential(),
    config=cfg,
)
account_id = client.create("account", {"name": "Northwind"})[0]
account = client.get("account", account_id)
```

Why: the code uses the official client, explicit configuration, credential abstraction, and the documented `create` return shape.

**Bad**

```python
client = DataverseClient(
    base_url="https://<myorg>.crm.dynamics.com",
    credential="password",
)
account_id = client.create("account", {"name": "Northwind"})
```

Why: the code embeds an invalid credential shape and treats `create` as a scalar instead of a `list[str]`.

## Conventions

| Rule | Rationale |
| --- | --- |
| Install the SDK with `pip install PowerPlatform-Dataverse-Client` and import `DataverseClient` from `PowerPlatform.Dataverse.client`. | Examples stay aligned with the official preview package and avoid obsolete client names. |
| Construct clients with Azure Identity credentials and `DataverseConfig`. | Authentication and HTTP behavior remain explicit and testable. |
| Treat `client.create` as returning `list[str]` and `client.update` as returning `None`. | Callers handle IDs and side effects according to the SDK contract. |
| Use bulk `create` and `update` overloads for many rows. | SDK-supported batching stays clearer than manual loops when semantics match. |
| Use `select`, `orderby`, `top`, and `page_size` for retrieve-multiple calls. | Paging remains bounded and deterministic. |
| Use `create_table` and `delete_table` only for metadata scenarios and clean up sample tables. | Metadata examples do not leave unwanted tables in Dataverse. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `InteractiveBrowserCredential` for local quickstarts and approved non-interactive Azure Identity credentials for automation. | Store passwords, secrets, or bearer tokens directly in Python files. |
| Tune `cfg.http_retries`, `cfg.http_backoff`, and `cfg.http_timeout` when needed. | Hide retry and timeout behavior inside unexplained wrapper code. |
| Use logical names such as `account`, `telephone1`, and `sample_filecolumn`. | Invent display names where the SDK expects Dataverse logical names. |
| Iterate `pages` from retrieve-multiple calls. | Assume a retrieve-multiple call returns one unbounded list. |
| Delete sample records and tables created by quickstarts. | Leave `SampleItem` or sample account records behind after test runs. |

## Checklist Before Opening a PR

- [ ] Python code that uses Dataverse targets Python 3.10+ and the `PowerPlatform-Dataverse-Client` package.
- [ ] `DataverseClient` is built with a valid `base_url`, Azure Identity credential, and `DataverseConfig` when HTTP settings matter.
- [ ] CRUD code handles `create`, `get`, `update`, and `delete` return semantics correctly.
- [ ] Bulk operations use broadcast or one-to-one patches intentionally.
- [ ] File uploads, paging, and metadata helpers use documented SDK methods and parameters.
- [ ] Sample records, files, and tables are cleaned up or isolated from production data.

## References

- Getting started: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/get-started
- Working with data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data
- SDK source/examples: https://github.com/microsoft/PowerPlatform-DataverseClient-Python
