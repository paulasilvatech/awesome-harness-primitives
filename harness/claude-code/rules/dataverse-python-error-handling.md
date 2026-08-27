---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-error-handling.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Python Dataverse SDK error handling, retry, logging, diagnostics, and troubleshooting conventions.

# Dataverse Python Error Handling Conventions — SDK Diagnostics

These instructions apply to Python files that call the Dataverse SDK and need robust exception handling, retry decisions, logging, diagnostics, monitoring, or troubleshooting. They are authoritative for `DataverseError` handling, Azure SDK exception boundaries, transient retry policy, HTTP status interpretation, SDK logging, and support diagnostics; authentication setup, CRUD semantics, pandas analytics, and repository-wide observability primitives win where they define stricter rules.

## DataverseError Shape

Catch and inspect `DataverseError` from `PowerPlatform.Dataverse.core.errors` before generic exceptions. Preserve the constructor and key properties because support diagnostics depend on them:

```python
from PowerPlatform.Dataverse.core.errors import DataverseError

DataverseError(
    message: str,
    code: str,
    subcode: str | None = None,
    status_code: int | None = None,
    details: dict | None = None,
    source: str | None = None,
    is_transient: bool = False,
)
```

Use `e.message`, `e.code`, `e.subcode`, `e.status_code`, `e.source`, `e.is_transient`, `e.details`, and `e.to_dict()` in logs or support payloads. Distinguish Dataverse errors from `AzureError` in `azure.core.exceptions`, then use a final `Exception` catch only for unexpected failures.

## HTTP Status Handling

Handle common Dataverse failures by status code and cause.

| Status | Scenario | Convention |
| --- | --- | --- |
| `400 Bad Request` | Invalid request format, OData syntax, field names, required fields, business rule violations | Log validation details and fix the request; do not retry unchanged input. |
| `401 Unauthorized` | Invalid credentials, expired tokens, bad `base_url`, or misconfigured settings | Re-authenticate or fix credentials; do not retry blindly. |
| `403 Forbidden` | User lacks permissions for `contact`, `account`, metadata, or table operations | Escalate access and include request ID from `e.details.get('request_id')` when present. |
| `404 Not Found` | Record, table, or resource does not exist | Verify schema name and record ID; use fallback data only when that behavior is intentional. |
| `408 Request Timeout` | Network or service timeout | Retry only when `e.is_transient` allows it. |
| `413` | File too large | Use chunked upload mode or reduce file size. |
| `429 Too Many Requests` | Service protection limits or rate limiting | Retry with exponential backoff when `e.is_transient` is true. |
| `500`, `502`, `503`, `504` | Temporary service or infrastructure failure | Retry with exponential backoff and check service health. |
| `InvalidOperationException` | Plugin or workflow error | Check Dataverse plugin logs and workflow diagnostics. |

## Retry Policy

Retry only transient failures. Do not retry `401`, `403`, `400`, or ordinary `404` failures because credentials, permissions, bad requests, and missing resources require a state change.

```python
import time
from PowerPlatform.Dataverse.core.errors import DataverseError


def should_retry(error: DataverseError) -> bool:
    if not error.is_transient:
        return False
    retryable_codes = {408, 429, 500, 502, 503, 504}
    return error.status_code in retryable_codes


def call_with_exponential_backoff(func, *args, max_attempts=3, **kwargs):
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except DataverseError as e:
            if should_retry(e) and attempt < max_attempts - 1:
                wait_time = 2 ** attempt
                print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
```

The SDK has minimal built-in retry support for some scenarios; handle transient consistency, service protection limits, and bulk-operation retries explicitly in application code.

## Diagnostics and Logging

Log structured diagnostics without leaking secrets. Use `datetime.utcnow().isoformat()`, `type(error).__name__`, `message`, `code`, `subcode`, `status_code`, `source`, `is_transient`, and `details`. Convert diagnostic dictionaries with `json.dumps(..., indent=2)` only when the sink accepts multi-line JSON.

Configure logging intentionally:

```python
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataverse_sdk.log'),
        logging.StreamHandler(sys.stdout),
    ],
)
logging.getLogger('azure').setLevel(logging.DEBUG)
logging.getLogger('PowerPlatform').setLevel(logging.DEBUG)
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.DEBUG)
```

Enable SDK logging with `DataverseConfig` only when detailed HTTP diagnostics are safe:

```python
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig
from azure.identity import InteractiveBrowserCredential

cfg = DataverseConfig()
cfg.logging_enable = True
client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=InteractiveBrowserCredential(),
    config=cfg,
)
records = client.get("account", top=10)
```

Be careful with `azure.core.pipeline.policies.http_logging_policy` because HTTP logs can include sensitive data.

## Dataverse-Specific Scenarios

Keep scenario-specific handling close to the SDK call so the remediation is obvious.

| Scenario | API names | Handling convention |
| --- | --- | --- |
| Authentication | `DataverseClient`, `InteractiveBrowserCredential`, `base_url="https://<invalid-org>.crm.dynamics.com"` | Report authentication failure and fix credential or tenant configuration. |
| Authorization | `client.get("contact")` | Report access denied and request administrator permissions. |
| Missing record | `client.get("account", record_id="00000000-0000-0000-0000-000000000000")` | Verify table and record; use `record = {"name": "Unknown", "id": None}` only for intentional fallback. |
| OData query errors | `filter="invalid_column eq 0"` | Check OData column names and syntax. |
| File upload | `client.upload_file(table_name="account", record_id=record_id, column_name="document_column", file_path="large_file.pdf")` | Handle `413` as file too large and `400` as invalid column or file format. |
| Metadata operations | `client.create("EntityMetadata", table_def)`, `SchemaName`, `DisplayName`, `new_CustomTable`, `Custom Table` | Treat `already exists` and permission errors as configuration or access issues. |
| Bulk create | `client.create(table_name, payload)` | Return `succeeded` and `failed` collections with payload, ids, index, message, code, and status. |

## Monitoring Wrappers

Use small wrappers for operation timing and consistent error output. A `monitor_operation(operation_name)` decorator can record `start_time = time.time()`, duration, success, and failure messages for operations such as `get_accounts(client)` and `client.get("account", top=100)`. Prefer plain text success/failure markers if logs strip symbols; if using symbols, preserve `✓` and `✗` where the environment supports them.

Centralize reusable error logic in a `DataverseErrorHandler` or equivalent when multiple calls share retry and logging decisions. Include `log_file="dataverse_errors.log"`, `logging.FileHandler(log_file)`, `logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')`, `logger.setLevel(logging.ERROR)`, `log_error(error, context)`, and `is_retryable(error)` only when the class is actually used.

## Good / Bad Examples

The examples below illustrate specific exception ordering and retry boundaries.

**Good:**

```python
from azure.core.exceptions import AzureError
from PowerPlatform.Dataverse.core.errors import DataverseError

try:
    records = client.get("account", filter="statecode eq 0", top=100)
except DataverseError as e:
    if e.status_code == 401:
        print("Re-authenticate required")
    elif e.status_code == 404:
        print("Resource not found")
    elif should_retry(e):
        records = call_with_exponential_backoff(client.get, "account", top=100)
    else:
        print(f"Operation failed: {e.message}")
except AzureError as e:
    print(f"Azure error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

Why: The code handles Dataverse-specific errors first, checks retryability, separates Azure SDK errors, and keeps the catch-all last.

**Bad:**

```python
try:
    records = client.get("account")
except Exception:
    records = client.get("account")
```

Why: The code catches everything, retries non-transient failures, hides status codes, and loses diagnostics needed for support.

## Baseline Compatibility Vocabulary

Preserve these legacy names, status labels, placeholders, paths, and configuration tokens when editing this instruction; they exist so older TaskSync, documentation, Dataverse, pandas, and troubleshooting examples remain searchable and recognizable.

- `Plugin/workflow`, `Record/table`, `bulk_create_with_error_tracking`, `create_account_batch_1`, `create_with_retry`, `error_code`, `error_dict`, `error_handler`
- `error_info`, `error_message`, `error_record`, `error_type`, `http_error`, `invalid-id`, `invalid_payload`, `log_error_for_support`
- `max_retries`, `not-a-phone-number`, `record_ids`, `requests/responses`, `succeed/fail.`, `validation_error`

## Conventions

| Rule | Rationale |
|---|---|
| Catch `DataverseError` before `AzureError` and generic `Exception` | Dataverse-specific status, details, and retry fields would otherwise be lost |
| Log `message`, `code`, `subcode`, `status_code`, `source`, `is_transient`, `details`, and `to_dict()` where appropriate | Support and monitoring need structured evidence, not only display text |
| Retry only `408`, `429`, `500`, `502`, `503`, and `504` when `is_transient` is true | Retrying auth, permission, validation, or missing-resource errors wastes calls and hides root causes |
| Use exponential backoff with bounded `max_attempts` | Backoff respects service protection limits and avoids infinite retry loops |
| Enable `DataverseConfig.logging_enable` and HTTP logging only when sensitive data handling is acceptable | Detailed HTTP diagnostics can expose headers, payloads, or identifiers |
| Handle OData, file upload, metadata, and bulk-operation errors with scenario-specific messages | Users need remediation guidance tied to the failing SDK operation |
| Track bulk successes and failures separately | Partial success is common and must be recoverable without reprocessing everything blindly |
| Include timing wrappers for important SDK operations when monitoring is required | Duration and failure context make operational incidents diagnosable |

## Do / Do Not

| Do | Do not |
|---|---|
| Inspect `e.status_code`, `e.is_transient`, and `e.details` before deciding | Retry every `DataverseError` the same way |
| Re-authenticate on `401` and request permissions on `403` | Treat authentication and authorization failures as transient outages |
| Check OData syntax and field names for `400` query failures | Hide invalid filters behind generic error text |
| Use chunked upload or smaller files for `413` | Retry the same oversized upload unchanged |
| Use `time.sleep(2 ** attempt)` with a bounded attempt count for retryable statuses | Create unbounded or immediate retry loops |
| Log JSON diagnostics with timestamps and context | Print only `Unexpected error` without support details |
| Separate `succeeded` and `failed` records in bulk operations | Abort a whole batch without recording which items completed |
| Review plugin logs for `InvalidOperationException` | Assume all server-side failures are SDK bugs |

## Checklist Before Opening a PR

- [ ] `DataverseError` is caught before `AzureError` and generic `Exception`.
- [ ] Error logs include message, code, subcode, status code, source, transient flag, details, and context without secrets.
- [ ] Retry logic is bounded and limited to transient `408`, `429`, `500`, `502`, `503`, and `504` responses.
- [ ] `401`, `403`, `400`, ordinary `404`, and `413` scenarios have non-retry remediation paths.
- [ ] OData query, file upload, metadata, and bulk-operation errors have scenario-specific handling.
- [ ] SDK and HTTP logging are enabled only when safe for the environment.
- [ ] Monitoring wrappers or centralized handlers are used when multiple SDK calls need consistent diagnostics.

## References

- DataverseError API Reference: https://learn.microsoft.com/en-us/python/api/powerplatform-dataverse-client/powerplatform.dataverse.core.errors.dataverseerror
- Azure SDK Error Handling: https://learn.microsoft.com/en-us/azure/developer/python/sdk/fundamentals/errors
- Dataverse SDK Getting Started: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/get-started
- Service Protection API Limits: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update
