---
name: dataverse-python-advanced-patterns
description: >-
  Generate production-ready Microsoft Dataverse SDK for Python code using advanced error handling,
  retries, batch operations, optimized OData queries, metadata management, timeouts, cache
  invalidation, file upload, and pandas workflows. Use when the user asks for production Dataverse
  Python patterns beyond quickstart CRUD.
---

<!-- Generated from harness/github-copilot/plugins/dataverse-sdk-for-python/skills/dataverse-python-advanced-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Dataverse Python advanced patterns

Generate production-grade Microsoft Dataverse SDK for Python examples that combine robust error handling, retry policy, bulk operations, OData optimization, metadata operations, cache management, file transfer, and pandas integration.

## When to invoke

- "Generate production Dataverse Python code with retries."
- "Show Dataverse SDK batch create/update/delete with error recovery."
- "Optimize Dataverse OData queries in Python."
- "Create Dataverse table metadata and option sets from Python."
- "Upload large Dataverse files or use pandas with Dataverse."

## Production pattern map

| Pattern | Required APIs or concepts | Implementation rule |
| --- | --- | --- |
| Error handling and retry logic | `DataverseError`, `is_transient`, exponential backoff | Catch Dataverse-specific errors, retry only transient failures, and cap retries. |
| Batch operations | bulk create, bulk update, bulk delete | Preserve per-record success/failure details and make retry idempotent. |
| OData query optimization | filter, select, orderby, expand, paging | Select only needed columns, use logical names, and page deterministically. |
| Table metadata | custom tables, column type definitions, option sets | Use correct Dataverse logical names and `IntEnum` for option-set values. |
| Configuration and timeouts | `DataverseConfig`, `http_retries`, `http_backoff`, `http_timeout`, `language_code` | Put transport policy in configuration instead of ad hoc sleeps. |
| Cache management | picklist cache flush | Flush picklist cache after metadata or option-set changes. |
| File operations | chunked upload, simple upload | Use chunked upload for large files and simple upload for small files where supported. |
| Pandas integration | `PandasODataClient`, DataFrame workflows | Use pandas only when tabular analysis or export/import is requested. |

## Error handling and retry rules

| Situation | Action |
| --- | --- |
| `DataverseError` with `is_transient` true | Retry with exponential backoff and jitter. |
| Validation or permission error | Do not retry; report the table, operation, and logical name involved. |
| Partial batch failure | Persist successful IDs, retry failed transient records only, and avoid duplicating creates. |
| Timeout | Use `DataverseConfig.http_timeout` and idempotent retry boundaries. |

## Query and metadata rules

- Use logical table and column names, not display labels.
- Create/inspect/delete custom tables only when metadata work is requested, and include proper column type definitions for each table operation.
- Prefer `$select`/select to reduce payload size and avoid retrieving unused columns.
- Combine filter, select, orderby, expand, and paging intentionally; do not expand large relationships by default.
- Model option sets with `IntEnum` so code uses named constants while Dataverse receives numeric values.
- After creating, inspecting, deleting, or changing custom table metadata, flush picklist cache when option metadata can be stale.

## File and DataFrame rules

| Workflow | Use | Avoid |
| --- | --- | --- |
| Simple file upload | Small File column payloads accepted by the SDK in one request. | Loading large files entirely into memory without checking size. |
| Chunked upload | Large File column uploads or service limits requiring chunks. | Retrying from the beginning without checking committed chunks. |
| `PandasODataClient` | DataFrame analysis, transformation, import/export, or reporting. | Replacing simple CRUD with pandas just because it is available. |

## Output template

````markdown
## Dataverse Python advanced pattern

**Status:** generated | needs environment details | blocked
**Pattern:** retries | batch | OData | metadata | config | cache | file | pandas

### Code
```python
<production-ready snippet with docstrings and type hints>
```

### API coverage
| API or concept | Used where | Reason |
| --- | --- | --- |
| `DataverseError` | `<function>` | transient retry handling |
| `DataverseConfig` | `<client setup>` | timeout and retry policy |

### Validation
- Logical names verified: yes/no
- Retry boundaries documented: yes/no
- Official API references included for each class/method: yes/no
````

## Quality gate

- [ ] Generated code includes docstrings and type hints.
- [ ] `DataverseError` is caught and `is_transient` controls retry decisions.
- [ ] Exponential backoff is bounded and does not retry non-transient failures.
- [ ] Batch operations preserve per-record failures and avoid duplicate recovery writes.
- [ ] OData examples use filter, select, orderby, expand, and paging only when needed and with correct logical names.
- [ ] Metadata examples use proper column type definitions and `IntEnum` for option sets.
- [ ] `DataverseConfig` covers `http_retries`, `http_backoff`, `http_timeout`, and `language_code` when configuration is shown.
- [ ] Picklist cache flush is included after metadata changes.
- [ ] File upload distinguishes chunked vs. simple upload.
- [ ] `PandasODataClient` is used only for DataFrame workflows.
- [ ] Official API reference links are included for each class or method used when available from the user's context or docs.
