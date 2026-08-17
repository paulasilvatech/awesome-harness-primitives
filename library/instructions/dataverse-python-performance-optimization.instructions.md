---
applyTo: "**/*.py"
description: "Enforces performance conventions for Python Dataverse SDK queries, pagination, batching, client reuse, file uploads, OData and SQL alternatives, memory management, retries, consistency checks, and monitoring."
---

# Dataverse Python Performance Conventions — Queries, Batching, and Large Data

These instructions apply to Python Dataverse SDK code matched by `**/*.py`. They are authoritative for query shape, pagination, batching, client reuse, file upload sizing, OData and SQL query choices, memory management, rate-limit handling, transaction-consistency safeguards, and performance monitoring; service throttling policy, data governance, and project-specific data contracts win where they define stricter limits.

## SDK Limits and Query Shape

Design every operation with current Python Dataverse SDK limits in mind: minimal retry policy retries only network errors by default, `DeleteMultiple` is not available, general-purpose OData batching is limited, and SQL support is restricted to simple `SELECT` with optional `WHERE`, `TOP`, and `ORDER BY`; JOINs and complex SQL predicates are not supported.

Use server-side projection and filtering. Pass `select=["accountid", "name", "telephone1", "creditlimit"]` instead of retrieving all columns, and pass `filter="statecode eq 0"` instead of fetching everything and filtering in Python. Projection and filtering reduce payload size and memory usage, commonly by 30-50% when broad tables are narrowed to needed columns.

| Query concern | Convention | Examples |
| --- | --- | --- |
| Equality | Filter server-side. | `filter="statecode eq 0"` |
| Contains | Use OData functions when supported. | `filter="contains(name, 'Acme')"` |
| Multiple conditions | Combine predicates in OData. | `filter="statecode eq 0 and createdon gt 2025-01-01Z"` |
| Not equals | Use OData inequality. | `filter="statecode ne 2"` |
| Stable paging | Always set deterministic `orderby`. | `orderby=["createdon desc", "name asc"]` |
| Simple SQL | Use only for supported simple reads. | `sql="SELECT accountid, name FROM account WHERE statecode = 0 ORDER BY name"` |
| Unsupported SQL | Rewrite JOINs as separate supported queries. | Do not use `SELECT a.accountid, c.fullname FROM account a JOIN contact c ON a.accountid = c.parentcustomerid`. |

## Pagination and Memory

Prefer lazy pagination. Treat `client.get("account", top=5000, page_size=200)` as a page iterator and process records as pages arrive. Do not wrap large results in `list(...)` unless the result set is known to be small.

For large tables, process incrementally and release memory between pages when necessary. A long-running job may call `gc.collect()` after each page only when profiling shows pressure. For pandas integration, build DataFrames in chunks with `pd.DataFrame(page)`, combine with `pd.concat(dfs, ignore_index=True)` only up to a threshold such as `chunk_size=10000`, process the chunk, then clear `dfs`.

Avoid storing all pages, all records, or all intermediate DataFrames in memory. Save or emit each processed result before fetching the next page.

## Batch Operations and Table Complexity

Use SDK bulk APIs where available. `client.create("account", payloads)` should create many records in one call. `client.update("account", account_ids, {"statecode": 1})` should apply one update to many records in broadcast mode. `client.update("account", account_ids, updates)` should apply per-record updates when each record needs different values.

Tune batch size by table complexity.

| Table Type | Batch Size | Max Threads | Rationale |
| --- | ---: | ---: | --- |
| OOB (`Account`, `Contact`, `Lead`) | 200-300 | 30 | Standard tables usually tolerate larger batches. |
| Simple tables with few lookups | ≤10 | 50 | Small batches reduce plugin and lookup contention while parallelism stays useful. |
| Moderately complex tables | ≤100 | 30 | Mid-size batches balance throughput and service pressure. |
| Large or complex tables with >100 columns and >20 lookups | 10-20 | 10-20 | Complex validation, plugins, and relationship checks increase per-record cost. |

Use helpers such as `bulk_create_optimized(client, table_name, payloads, batch_size=200)` to slice payloads with `payloads[i:i + batch_size]`, create each batch, log `Created {len(ids)} records`, and yield IDs for downstream verification.

## Client Reuse and Connection Configuration

Reuse `DataverseClient` instances. Do not create a new client inside every batch loop. A singleton helper may use `_client = None`, `DefaultAzureCredential`, and `DataverseClient(base_url="https://myorg.crm.dynamics.com", credential=DefaultAzureCredential())` to create one client per process when dependency injection is unavailable.

Configure timeouts through `DataverseConfig`:

| Setting | Convention |
| --- | --- |
| `cfg.http_timeout = 30` | Bound request duration. |
| `cfg.connection_timeout = 5` | Bound connection establishment. |

Keep `base_url`, credentials, and client lifetime aligned with tenant isolation; do not reuse one client across tenants if the `base_url` or credential differs.

## Async Preparation and File Uploads

The SDK is currently synchronous. If code must fit an async application, isolate synchronous SDK calls behind a helper such as `get_accounts_async(client)` and use `asyncio.get_event_loop().run_in_executor(None, lambda: list(client.get("account")))` until native async support exists. Do not pretend SDK calls are nonblocking; keep thread-pool use bounded.

Use upload mode by file size. For files smaller than 128 MB, call `client.upload_file(table_name="account", record_id=record_id, column_name="document_column", file_path="small_file.pdf")`. For files larger than 128 MB, use chunked mode with `mode='chunk'` and `if_none_match=True`; the SDK splits into 4MB chunks, uploads chunks in parallel, and assembles them on the server.

## Rate Limits, Consistency, and Monitoring

Because the SDK has minimal retry support, implement bounded exponential backoff around throttled operations. Catch `DataverseError`, check `e.status_code == 429`, wait `2 ** attempt` seconds for retries such as 1s, 2s, and 4s, and raise after `max_retries=3`. Do not retry non-429 failures with throttling logic.

Bulk operations do not provide transactional guarantees. After bulk create or update, verify the expected count or IDs before downstream processing. A consistency helper such as `create_with_consistency_check(client, table_name, payloads)` should compare `len(ids)` with the actual created count and handle partial failure explicitly. Do not refer to undefined counters such as `count_created` unless the code computes them.

Monitor operation duration. A decorator such as `monitored_operation(operation_name)` may use `time.time()`, `logging.getLogger("dataverse")`, `logger.info(f"{operation_name}: {duration:.2f}s")`, and `logger.error(f"{operation_name} failed after {duration:.2f}s: {e}")` before re-raising. Test performance with production-like data because throughput changes with table complexity, plugins, lookup counts, and network latency.

## Good / Bad Examples

The examples below illustrate bounded, server-side, page-oriented reads.

**Good:**

```python
accounts = client.get(
    "account",
    select=["accountid", "name", "telephone1"],
    filter="statecode eq 0",
    orderby=["createdon desc", "name asc"],
    top=100000,
    page_size=5000,
)

for page in accounts:
    process(page)
```

Why: The query limits columns, filters on the server, orders pages deterministically, and processes each page without loading all records at once.

**Bad:**

```python
all_records = list(client.get("account", top=100000))
active_accounts = [a for a in all_records if a.get("statecode") == 0]
process(active_accounts)
```

Why: The code fetches too many columns and rows, filters client-side, and loads a large result set into memory.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `select`, `filter`, `orderby`, `top`, and `page_size` on `client.get`. | Server-side shaping reduces payload size, memory, and unstable paging. |
| Process lazy pages immediately instead of converting large iterators to `list`. | Memory stays bounded and time-to-first-result improves. |
| Use bulk `create` and `update` APIs with table-specific batch sizes. | Throughput improves without overloading complex Dataverse tables. |
| Reuse `DataverseClient` and configure `DataverseConfig` timeouts. | Connection and token overhead stays low and failures are bounded. |
| Use chunked upload for files larger than 128 MB and single-request upload below that threshold. | Large files avoid request-size limits while small files avoid chunk overhead. |
| Restrict SQL to supported simple `SELECT`, `WHERE`, `TOP`, and `ORDER BY` cases. | Unsupported JOINs and complex predicates fail or force inefficient workarounds. |
| Implement bounded backoff for `429` using `DataverseError.status_code`. | Throttling recovers when transient but does not hide persistent failures. |
| Verify bulk-operation consistency after partial failures. | Downstream processing does not assume all records were created or updated. |
| Log operation duration and test with production-like data. | Performance regressions become measurable and representative. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Retrieve only needed columns with `select`. | Fetch all columns and discard most of them in Python. |
| Filter with OData expressions such as `statecode eq 0`. | Fetch all records and use list comprehensions for security or performance filters. |
| Use `orderby` for predictable paging. | Page through changing data without deterministic order. |
| Use `client.create("account", payloads)` and `client.update("account", account_ids, updates)` for supported bulk work. | Loop one API call per record when bulk APIs fit the operation. |
| Use batch sizes such as OOB 200-300, simple ≤10, moderate ≤100, complex 10-20. | Apply one universal batch size to every Dataverse table. |
| Use `run_in_executor` only as a bounded bridge in async apps. | Treat synchronous SDK calls as natively async. |
| Use `mode='chunk'` and `if_none_match=True` for large uploads. | Send files larger than 128 MB as a single unguarded request. |
| Monitor `429` responses and operation durations. | Ignore throttling and retry behavior until production incidents occur. |

## Checklist Before Opening a PR

- [ ] Queries use `select`, server-side `filter`, deterministic `orderby`, and appropriate `top` or `page_size`.
- [ ] Large reads process pages lazily and do not materialize all records in memory.
- [ ] Bulk create and update operations use supported SDK APIs and batch sizes matched to table complexity.
- [ ] `DataverseClient` is reused safely for the tenant and credential scope.
- [ ] `DataverseConfig` sets request and connection timeouts where long-running jobs need bounded behavior.
- [ ] Async code isolates synchronous SDK calls behind a bounded executor bridge.
- [ ] File uploads choose single-request mode below 128 MB and chunked mode above 128 MB.
- [ ] SQL usage stays within simple supported `SELECT`, `WHERE`, `TOP`, and `ORDER BY` patterns.
- [ ] `429` handling uses bounded exponential backoff and re-raises non-retryable failures.
- [ ] Bulk operations verify expected IDs or counts before dependent processing.
- [ ] Operation duration is logged and performance-sensitive changes are tested with production-like data.

## References

- Dataverse Web API Performance: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update
- OData Query Options: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query-data-web-api
- SDK Working with Data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data
- Example Dataverse URL: https://myorg.crm.dynamics.com
