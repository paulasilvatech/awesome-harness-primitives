---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-best-practices.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces production Python conventions for the PowerPlatform Dataverse SDK, including installation, authentication, client reuse, CRUD operations, metadata, paging, files, OData, cache, testing, deployment, and troubleshooting.

# Dataverse Python Conventions — Production SDK Usage

These instructions apply to Python code that uses the `PowerPlatform-Dataverse-Client` SDK and Azure Identity to integrate with Microsoft Dataverse. They are authoritative for SDK installation assumptions, authentication patterns, `DataverseClient` lifecycle, CRUD usage, table/column metadata, paging, file operations, OData filters, cache management, error handling, testing, deployment hygiene, and troubleshooting in matched Python files; project-specific secret management, CI packaging, and enterprise authentication policies win when they are stricter.

## Installation, Dependencies, and Versions

Use the published SDK for application code and editable installs only when developing the SDK itself.

| Scenario | Command or dependency | Convention | Rationale |
| --- | --- | --- | --- |
| Production SDK install | `pip install PowerPlatform-Dataverse-Client` | Install the published PyPI package. | Application builds should consume released artifacts. |
| Authentication dependency | `pip install azure-identity` | Use Azure Identity credentials for token acquisition. | SDK authentication integrates with Azure and Microsoft Entra patterns. |
| Optional data manipulation | `pip install pandas` | Add `pandas` only when tabular manipulation is required. | Avoid unnecessary runtime dependencies. |
| SDK development | `git clone https://github.com/microsoft/PowerPlatform-DataverseClient-Python.git`, `cd PowerPlatform-DataverseClient-Python`, `pip install -e .` | Use editable mode for live SDK development. | Source edits should be visible without repeated package builds. |
| Development tools | `pip install pytest pytest-cov black isort mypy ruff` | Use the project-approved test, coverage, formatting, import sorting, type-checking, and linting tools when the repo opts into them. | Consistent local checks reduce CI failures. |
| Python | Python `>= 3.10`; recommended Python 3.11+; supported 3.10, 3.11, 3.12, 3.13, 3.14. | Do not target older interpreters. | The SDK support matrix starts at Python 3.10. |
| Core dependencies | `azure-identity >= 1.17.0`, `azure-core >= 1.30.2`, `requests >= 2.32.0`. | Keep dependency ranges compatible with the SDK. | Authentication and HTTP behavior depend on these libraries. |
| Optional dependencies | `pandas`, `reportlab`. | Use `reportlab` only for PDF-oriented examples or features. | Optional packages should match actual functionality. |
| Development tool versions | `pytest >= 7.0.0`, `black >= 23.0.0`, `mypy >= 1.0.0`, `ruff >= 0.1.0`. | Match these minimums when introducing local tooling. | Older tool versions may lack expected checks. |

Verify imports with the real SDK names before adding application code:

```python
from PowerPlatform.Dataverse import __version__
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import InteractiveBrowserCredential

print(f"SDK Version: {__version__}")
print("Installation successful!")
```

## Authentication and Configuration

Choose credentials by runtime context and keep secrets outside source code.

| Context | Credential | Pattern | Rationale |
| --- | --- | --- | --- |
| Local interactive development, interactive testing, and single-user scenarios | `InteractiveBrowserCredential` | `credential = InteractiveBrowserCredential()` then `DataverseClient("https://yourorg.crm.dynamics.com", credential)`. | Browser sign-in is simple and user-scoped. |
| Server-side applications, Azure automation, and scheduled jobs | `ClientSecretCredential` | Pass `tenant_id`, `client_id`, and `client_secret` from secure configuration. | Non-interactive jobs need application credentials. |
| Highly secure environments and certificate-pinning requirements | `ClientCertificateCredential` | Use `certificate_path="path/to/certificate.pem"`. | Certificates reduce reliance on shared secrets. |
| Local testing with Azure CLI installed and Azure DevOps pipelines | `AzureCliCredential` | Reuse the signed-in CLI identity. | CLI authentication avoids copying credentials during development. |

Use `DataverseConfig` only for supported settings. Set `language_code=1033` when English (US) responses are required. Treat `http_retries`, `http_backoff`, and `http_timeout` as reserved for internal use unless the SDK documentation explicitly exposes them.

```python
from PowerPlatform.Dataverse.core.config import DataverseConfig
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import ClientSecretCredential

config = DataverseConfig(language_code=1033)
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = DataverseClient("https://yourorg.crm.dynamics.com", credential, config)
```

## Client Lifecycle

Create one `DataverseClient` per logical application configuration and reuse it.

| Pattern | Convention | Rationale |
| --- | --- | --- |
| Singleton service | Wrap `DataverseClient` construction in an application service such as `DataverseService` and reuse the instance. | Reusing the client avoids repeated authentication and connection setup. |
| Repeated function construction | Do not create a new credential and client inside every `fetch_account` call. | Repeated construction is slow and can amplify throttling. |
| Dependency injection | Pass the client or service into workers, handlers, and repositories. | Tests can substitute fakes and configuration stays centralized. |

```python
class DataverseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            credential = InteractiveBrowserCredential()
            cls._instance = DataverseClient("https://yourorg.crm.dynamics.com", credential)
        return cls._instance

service = DataverseService()
account = service.get("account", account_id)
```

## CRUD Operations

Use the SDK methods directly and shape payloads to minimize network and server work.

| Operation | API | Convention | Rationale |
| --- | --- | --- | --- |
| Create one record | `client.create("account", record_data)` | Store the returned `created_ids` and use `record_id = created_ids[0]` when one record is expected. | The SDK returns IDs consistently for single and bulk creates. |
| Bulk create | `client.create("account", records)` | Send a list when creating multiple records; the SDK automatically uses `CreateMultiple` for arrays larger than one record. | Manual loops are slower and harder to recover. |
| Read by ID | `client.get("account", "account-guid-here")` | Use the table logical name and the record GUID. | Direct reads are simpler and cheaper than filtered scans. |
| Query with OData | `client.get("account", filter=..., select=..., orderby=..., top=..., page_size=...)` | Use lowercase logical names, a `select` list, server-side `filter`, `orderby`, `top`, and `page_size`. | Server-side filtering and column selection reduce payload size. |
| SQL analytics | `client.query_sql("SELECT TOP 10 name, creditlimit FROM account WHERE creditlimit > 50000 ORDER BY name")` | Use `query_sql` only for read-only analytics; never assume DML is allowed. | SQL support can be disabled by org policy and should not mutate data. |
| Single update | `client.update("account", "account-guid", data)` | Send only changed columns. | Minimal updates reduce side effects and payload size. |
| Bulk update broadcast | `client.update("account", account_ids, data)` | Use a list such as `account_ids = ["id1", "id2", "id3"]` when all selected records receive the same values, such as `manager-guid`. | Broadcast updates avoid repeated calls for identical changes. |
| Paired update | Loop over `{record_id: data}` updates. | Use separate calls when each record has different values. | The SDK pattern distinguishes broadcast data from per-record data. |
| Delete one record | `client.delete("account", "account-guid")` | Delete by logical table name and GUID. | Direct deletion is explicit. |
| Bulk delete | `client.delete("account", record_ids, use_bulk_delete=True)` | Use `record_ids` and `use_bulk_delete=True` for large lists. | The SDK can route large deletes through optimized bulk behavior such as `BulkDelete`. |

Keep CRUD placeholders recognizable in examples and tests: `record_data`, `account_id`, `record_id`, `account_ids`, `record_ids`, `created_ids`, `table_name`, and `filter` should name the real value they carry. Preserve review labels such as `PATTERN`, `ANTI-PATTERN`, `Create/update`, and `Table/column` when converting examples into prose so reviewers can map old guidance to the new convention.

## OData, SQL, Paging, and Large Results

Push work to Dataverse while keeping result sets bounded.

| Concern | Convention | Rationale |
| --- | --- | --- |
| Case sensitivity | Use lowercase logical names in OData filters: `name eq 'Contoso'`, not `Name eq 'Contoso'`. Schema-name existence checks may be case-insensitive, but API names and values remain case-sensitive when the business value requires it. | Dataverse logical names are the API contract; values are data. |
| Filter examples | Use `eq`, `gt`, `lt`, `contains`, `and`, `or`, and `not`: `(name eq 'Contoso') and (creditlimit gt 50000)`, `(industrycode eq 1) or (industrycode eq 2)`, `not(statecode eq 1)`. | Standard OData operators keep filters understandable. |
| Select | Always pass `select=["name", "creditlimit", "telephone1"]` or the minimal required columns. | Fetching all columns is slow and can expose unnecessary data. |
| Expand | Use `expand=["parentaccountid($select=name)"]` with a matching `select=["name", "parentaccountid"]` only when related data is needed. | Expands are useful but can increase payload and query cost. |
| Page iteration | Iterate pages: `for page in client.get("account", top=500, page_size=500): ...`. | Streaming page-by-page avoids loading everything at once. |
| Accumulation | Use `all_accounts` only when the caller truly needs every row in memory. | Large in-memory lists can exhaust workers. |
| Manual paging | Use `skip_count` and `page_size` only for complex paging scenarios. | SDK pagination is preferred for normal reads. |
| Read-only SQL | Use `SELECT`, `FROM`, `WHERE`, and `ORDER BY` in `query_sql`; do not issue DML. | SQL queries are read-only and may be disabled. |
| Fallback | If SQL is unavailable, fall back to OData `client.get`. | Org policy should not break core read paths. |

Use the vocabulary from diagnostic examples consistently: `WRONG` means an uppercase logical-name filter, `CORRECT` means lowercase logical names, `AND/OR` names compound OData operations, `SELECT` marks read-only SQL, and `CRUD` covers create, read, update, and delete paths.

## Error Handling, Recovery, and Rate Limits

Catch SDK-specific exceptions before broad exceptions and make retries bounded.

| Exception or condition | Convention | Rationale |
| --- | --- | --- |
| `DataverseError` | Catch as the base SDK failure only after more specific exceptions. | Specific handlers keep recovery precise. |
| `ValidationError` | Handle validation-specific failures near input construction. | Invalid payloads should not be retried blindly. |
| `MetadataError` | Treat table/column lookup and metadata operations as configuration or schema failures. | Metadata failures usually need a fix, not a retry loop. |
| `HttpError` | Retry only transient failures and propagate persistent HTTP errors. | Unbounded retry hides outages and wastes quota. |
| `SQLParseError` | Correct the SQL query or fall back to OData. | Syntax errors are deterministic. |
| Retry helper | Use bounded `create_with_retry(table_name, record_data, max_retries=3)` with exponential `backoff_seconds = 2 ** attempt`. | Bounded backoff handles transient failures without infinite loops. |
| HTTP 429 | Reduce request frequency, wait before retrying, and lower page size such as `top=500` instead of `top=5000`. | Throttling is a capacity signal. |
| Bulk recovery | Use `create_with_recovery(records)` to collect `success` and `failed` entries and retry individual records only after a bulk failure. | Per-record recovery preserves successful work and exposes bad rows. |

Use `HttpError` for HTTP-level errors and avoid catching `Exception` unless the code records enough context and re-raises or maps the failure intentionally.

## Metadata, Tables, Columns, and Cache

Treat metadata operations as schema changes that require exact names and cache awareness.

| Task | API | Convention | Rationale |
| --- | --- | --- | --- |
| Create custom table | `client.create_table("new_CustomTable", primary_column_schema_name="new_Name", columns=columns)` | Define columns with types such as `string`, `int`, `decimal`, `bool`, `datetime`, or an `IntEnum` such as `Priority` values `LOW`, `MEDIUM`, `HIGH` for option set/picklist fields. | Schema creation should express Dataverse column intent clearly. |
| Read table metadata | `client.get_table_info("account")` | Use returned `table_info` keys: `table_schema_name`, `table_logical_name`, `entity_set_name`, and `primary_id_attribute`. | Metadata drives correct API calls and diagnostics. |
| List tables | `client.list_tables()` | Print or inspect each table's schema and logical names before using custom names. | Discovery prevents spelling and casing mistakes. |
| Add columns | `client.create_columns("new_CustomTable", {"new_Status": "string", "new_Priority": "int"})` | Add columns deliberately and document their purpose. | Metadata changes affect downstream clients. |
| Delete columns | `client.delete_columns("new_CustomTable", ["new_Status", "new_Priority"])` | Delete only when callers and reports no longer depend on the columns. | Column deletion can break integrations. |
| Delete table | `client.delete_table("new_CustomTable")` | Treat table deletion as destructive and environment-gated. | Table deletion risks data loss. |
| Cache | `client.flush_cache()` | Flush cache after metadata changes, bulk deletes, or metadata synchronization. | Cached metadata can become stale after schema changes. |

When troubleshooting `MetadataError: Table Not Found`, list tables and use the exact schema or logical name, including `new_customprefixed_table` when that is the real name.

## File Operations

Use the SDK file APIs and choose chunking by size.

| File scenario | API | Convention | Rationale |
| --- | --- | --- | --- |
| Small file upload | `client.upload_file(table_name="account", record_id=record_id, file_column_name="new_documentfile", file_path=file_path)` | Use a single PATCH-style upload for files under 128 MB, such as `document.pdf`. | Small uploads do not need chunk orchestration. |
| Large file upload | `client.upload_file(..., file_column_name="new_videofile", file_path=Path("large_video.mp4"), chunk_size=4 * 1024 * 1024)` | Let the SDK chunk large files and set `chunk_size` deliberately, commonly 4 MB chunks. | Chunking avoids request size limits and improves recovery. |
| Paths | Use `Path` objects for `file_path`. | Path handling stays portable and testable. |

## Performance Patterns

Favor server-side filtering, batch APIs, selected columns, and client reuse.

| Do | Do not | Rationale |
| --- | --- | --- |
| Use `select` to fetch only needed columns. | Call `client.get("account")` when only two columns are needed. | Smaller payloads are faster and safer. |
| Batch create/update records, such as `client.create("account", [record1, record2, record3])`. | Create records one-by-one in loops. | Batch APIs reduce network overhead. |
| Use paging and `process_page(page)` for streaming work. | Convert all results with `list(client.get("account"))` by default. | Paging keeps memory bounded. |
| Reuse `DataverseClient(url, credential)` throughout the app. | Instantiate a new client inside every loop iteration. | Client reuse avoids repeated authentication. |
| Apply server-side filters such as `creditlimit gt 50000`. | Fetch broad data and filter locally without reason. | Dataverse can reduce data before transfer. |

## Upsert and Recovery Patterns

Use explicit lookup-then-create/update logic when the SDK call path does not provide a native upsert abstraction.

```python
def upsert_account(name, data):
    results = list(client.get("account", filter=f"name eq '{name}'"))
    if results:
        account_id = results[0]["accountid"]
        client.update("account", account_id, data)
        return account_id, "updated"

    ids = client.create("account", {"name": name, **data})
    return ids[0], "created"
```

Why: `upsert_account` makes lookup, update, and create behavior explicit; production code should still escape or parameterize user-provided filter values where the SDK supports it.

Use `create_with_recovery` for bulk creates that need per-record error tracking. Return a result shape with `success` and `failed` entries so callers can retry or report exact failures.

## Troubleshooting

Diagnose common failures with the fastest safe check.

| Symptom | Check | Fix |
| --- | --- | --- |
| `ImportError: No module named 'PowerPlatform'` | Run `pip show PowerPlatform-Dataverse-Client` and verify `which python` points to the intended virtual environment. | Reinstall with `pip install --upgrade PowerPlatform-Dataverse-Client` in the active environment. |
| Authentication failed | Try `InteractiveBrowserCredential(tenant_id="your-tenant-id")`, verify credentials have Dataverse access, and confirm org URL shape. | Use `https://yourorg.crm.dynamics.com`, avoid accidental trailing slash `https://yourorg.crm.dynamics.com/` unless the SDK accepts it, and use regional hosts such as `https://yourorg.crm4.dynamics.com` when appropriate. |
| HTTP 429 rate limiting | Inspect request frequency and page size. | Add exponential backoff, reduce concurrency, and lower `top` from 5000 to 500 when needed. |
| Metadata table not found | Run `client.list_tables()` and inspect `table_schema_name` and `table_logical_name`. | Use the exact schema or logical name expected by the API. |
| SQL query not enabled | Wrap `query_sql()` and catch the SDK error. | Fall back to OData `client.get`. |

Keep examples with placeholders such as `your-client-id`, `your-client-secret`, `your-tenant-id`, `account-guid`, `account-guid-here`, and `manager-guid` as placeholders only; do not commit real credentials or tenant-specific secrets.

## Good / Bad Examples

The examples below illustrate secure configuration, client reuse, OData filtering, selected columns, and bounded paging.

**Good:**

```python
from azure.identity import ClientSecretCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = DataverseClient("https://yourorg.crm.dynamics.com", credential)

for page in client.get(
    "account",
    filter="creditlimit gt 50000",
    select=["name", "creditlimit", "telephone1"],
    orderby="name",
    top=500,
    page_size=500,
):
    process_page(page)
```

Why: The code reuses a configured client, filters on the server, selects only needed columns, orders results, and processes bounded pages.

**Bad:**

```python
def load_accounts():
    credential = InteractiveBrowserCredential()
    client = DataverseClient("https://yourorg.crm.dynamics.com", credential)
    all_accounts = list(client.get("account"))
    return [row for row in all_accounts if row.get("creditlimit", 0) > 50000]
```

Why: The code creates a new interactive client in a function, fetches every column and row, loads all results into memory, and filters locally.

## Conventions

| Rule | Rationale |
|---|---|
| Use `PowerPlatform-Dataverse-Client` with supported Python and dependency versions. | Unsupported runtimes and libraries can fail at import or authentication time. |
| Choose `InteractiveBrowserCredential`, `ClientSecretCredential`, `ClientCertificateCredential`, or `AzureCliCredential` according to runtime context. | Authentication should match whether the process is interactive, automated, certificate-based, or CLI-backed. |
| Reuse a `DataverseClient` instead of constructing clients repeatedly. | Client reuse reduces authentication overhead and throttling risk. |
| Use `select`, `filter`, `orderby`, `top`, and `page_size` for reads. | Dataverse should do filtering, sorting, and paging before data reaches Python. |
| Treat `query_sql` as read-only and optional by org policy. | SQL support may be disabled and must not mutate data. |
| Use SDK-specific exceptions and bounded retries with exponential backoff. | Precise error handling prevents infinite retry and masks fewer defects. |
| Flush cache after metadata changes, bulk deletes, or metadata synchronization. | Stale metadata can make valid table and column operations fail. |
| Use `upload_file` with chunking for large files and direct upload for small files under 128 MB. | File upload behavior should fit request limits and recovery needs. |
| Never commit real tenant IDs, client secrets, certificates, or org-specific credentials. | Secrets in source code create security incidents. |

## Do / Do Not

| Do | Do not |
|---|---|
| Install production code with `pip install PowerPlatform-Dataverse-Client`. | Depend on an editable SDK checkout for application runtime. |
| Store `tenant_id`, `client_id`, `client_secret`, and `certificate_path` in secure configuration. | Hardcode `your-client-id`, `your-client-secret`, or real secrets in source files. |
| Use lowercase Dataverse logical names in OData filters. | Write filters such as `Name eq 'Contoso'` when the logical name is `name`. |
| Use bulk `create`, broadcast `update`, and `use_bulk_delete=True` where appropriate. | Loop individual CRUD calls when an SDK batch pattern fits. |
| Iterate pages and stream work through `process_page`. | Materialize `all_accounts` unless every row is truly required. |
| Use `get_table_info`, `list_tables`, `create_columns`, and `delete_columns` for metadata work. | Guess table and column names after receiving `MetadataError`. |
| Use `flush_cache` after schema or bulk delete changes. | Keep using cached metadata after table/column changes. |
| Fall back from disabled SQL to OData. | Make `query_sql` the only path for critical reads. |

## Checklist Before Opening a PR

- [ ] Python version and dependencies match the supported SDK matrix.
- [ ] Authentication uses the correct Azure Identity credential for the runtime and no secrets are committed.
- [ ] `DataverseClient` construction is centralized and reused.
- [ ] CRUD calls use server-side `filter`, `select`, `orderby`, `top`, and `page_size` where applicable.
- [ ] Bulk create, update, delete, upsert, and recovery logic use SDK patterns rather than unnecessary loops.
- [ ] SQL usage is read-only and has an OData fallback when org policy disables SQL.
- [ ] Error handling catches SDK-specific exceptions and uses bounded retry for transient `HttpError` or HTTP 429 cases.
- [ ] Metadata changes use exact table and column names and call `flush_cache` when cache may be stale.
- [ ] File uploads choose direct or chunked `upload_file` behavior based on file size.
- [ ] Troubleshooting notes preserve safe placeholders and do not include real credentials or tenant-specific secrets.

## References

- Official Repository: https://github.com/microsoft/PowerPlatform-DataverseClient-Python
- SDK development clone URL: https://github.com/microsoft/PowerPlatform-DataverseClient-Python.git
- PyPI Package: https://pypi.org/project/PowerPlatform-Dataverse-Client/
- Azure Identity Documentation: https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme
- Dataverse Web API Documentation: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview
- Example Dataverse org URL: https://yourorg.crm.dynamics.com
- Example Dataverse org URL with slash: https://yourorg.crm.dynamics.com/
- Example regional Dataverse org URL: https://yourorg.crm4.dynamics.com
