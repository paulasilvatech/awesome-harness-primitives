---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-file-operations.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Applies PowerPlatform Dataverse Client 1.x conventions for Python file-column uploads, record lifecycle, validation, retries, integrity, and auditability.

# Dataverse Python File Operations Conventions - SDK 1.x Uploads and Auditability

These instructions apply to Python files that use `PowerPlatform-Dataverse-Client` 1.x for Microsoft Dataverse file columns. They are authoritative for the public `DataverseClient` file-upload contract, related record operations, validation, retry boundaries, integrity checks, and audit logging in matched files; project-wide Python, authentication, security, observability, and data-retention rules win where they are stricter. The dated SDK and Microsoft Learn evidence in `docs/HARNESS-VALIDATION.md` must be refreshed before changing version-sensitive behavior.

## SDK 1.x Contract and Migration Guard

Use the GA operation namespaces introduced in version 1.0:

| Need | Public API |
| --- | --- |
| Create a record | `client.records.create(table, data)` |
| Read one record | `client.records.get(table, record_id, select=[...])` |
| Read multiple records | `client.records.get(table, filter=..., select=[...], page_size=...)` |
| Update records | `client.records.update(table, ids, changes)` |
| Delete records | `client.records.delete(table, ids)` |
| Upload a file column | `client.files.upload(table, record_id, file_column, path, ...)` |

Do not use removed beta shortcuts such as `client.create`, `client.get`, `client.update`, `client.delete`, or `client.upload_file`. In the 1.0 GA client these names raise `AttributeError` with the GA replacement and migration command. Use the SDK's `dataverse-migrate` codemod for a broader v0-to-v1 migration instead of preserving compatibility wrappers indefinitely.

Construct the client with an HTTPS environment URL and an Azure Identity credential. Prefer a context manager so the HTTP session and caches are closed:

```python
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = DefaultAzureCredential()

with DataverseClient(
    base_url="https://yourorg.crm.dynamics.com",
    credential=credential,
) as client:
    ...
```

Use `InteractiveBrowserCredential` only for an intentional interactive developer flow. Never hardcode real tenant IDs, client IDs, secrets, record IDs, access tokens, or production organization URLs.

## File Upload Contract

The public upload signature is:

```python
client.files.upload(
    table,
    record_id,
    file_column,
    path,
    *,
    mode=None,
    mime_type=None,
    if_none_match=True,
)
```

Follow these semantics:

- `table` is the Dataverse table schema name.
- `record_id` is the target record GUID.
- `file_column` is the file-column schema name.
- `path` is a local path string; normalize caller input with `Path` and pass `str(path)`.
- `mode` accepts `"auto"`, `"small"`, or `"chunk"`. `None` is equivalent to `"auto"`.
- `mime_type` is optional. In SDK 1.0 it is transmitted only by the single-PATCH path; chunk mode sends `application/octet-stream`.
- `if_none_match=True` is create-only behavior and fails when the column already contains a file.
- Set `if_none_match=False` only when overwrite is explicitly intended and authorized.
- A successful upload returns `None`; do not expect a response payload.

The SDK can create a missing file column automatically before upload. Treat that as a schema mutation: provision columns through normal metadata or deployment controls whenever possible, and allow runtime creation only when it is intentional, reviewed, and supported by the caller's privileges.

## Upload Mode and Chunking

Prefer `mode="auto"` unless a test or operational requirement needs a forced path.

| Mode | Verified behavior |
| --- | --- |
| `auto` | Uses a single PATCH when the file is smaller than 128 MiB and chunked transfer at 128 MiB or larger. |
| `small` | Reads the file and uploads it with one PATCH; files larger than 128 MiB are rejected. |
| `chunk` | Starts a native chunked PATCH session, streams the file in segments, and sends each segment as `application/octet-stream`. |

Do not pass `chunk_size`; it is not a public `client.files.upload` parameter. In chunk mode the SDK uses the server's `x-ms-chunk-size` recommendation when available and otherwise falls back to 4 MiB. Do not prescribe 8 MiB chunks or reimplement the native session unless the public API cannot meet a documented requirement.

Do not assume an explicit `mime_type` is persisted for a file that uses chunk mode, including an auto-selected file of 128 MiB or larger. Keep a correct filename extension and verify stored metadata when MIME type is a business requirement.

The separate Dataverse block-message protocol described by Microsoft Learn limits `UploadBlock` payloads to 4 MB or less. Do not mix that protocol's `InitializeFileBlocksUpload`/`UploadBlock`/`CommitFileBlocksUpload` contract with the Python SDK's native chunked PATCH implementation.

## Record Lifecycle and Queries

File bytes cannot be set in the ordinary create or update payload. Create the metadata record first, then upload to its file column:

```python
record_id = client.records.create(
    "new_document",
    {
        "new_name": "Contract",
        "new_status": "pending",
    },
)

client.files.upload(
    table="new_document",
    record_id=record_id,
    file_column="new_file",
    path=str(file_path),
    mode="auto",
)

client.records.update(
    "new_document",
    record_id,
    {"new_status": "completed"},
)
```

`client.records.create` returns one GUID string for a single dictionary and a list of GUID strings for a list of dictionaries. Do not index `[0]` after a single-record create.

For a single record, pass `record_id` to `client.records.get`; it returns a typed `Record` with dict-like access. For multiple records, omit `record_id`; the method returns an iterable of pages, and each page contains `Record` objects. Use `page_size` as the page-size hint. `top` is a maximum total record count, so omit it when an export must retrieve every matching record.

A retrieved file column contains a file identifier rather than the bytes. Its supporting filename column uses the file-column schema name with `_Name` appended. Do not treat either value as downloaded file content.

## Validation, Integrity, and Audit Logging

- Convert input to `Path` and require `path.is_file()` before remote mutation.
- Enforce the Dataverse column's configured maximum size and any stricter project policy. Do not use a universal arbitrary maximum such as 500 MB.
- Derive allowed extensions and MIME types from the business contract; do not present one global extension allow-list as a Dataverse requirement.
- Use `mimetypes.guess_type(path.name)` when a best-effort MIME type is useful, with `application/octet-stream` as the fallback.
- Calculate SHA-256 incrementally for integrity-sensitive workflows. Compare with downloaded content or a project-defined hash field only when that retrieval or schema contract exists.
- Do not invent logical columns such as `new_filehash`, status fields, or option-set values. Reuse names and values from inspected Dataverse metadata.
- Check local disk capacity only for workflows that generate or stage intermediate files; an ordinary upload does not require a second local copy.
- Use timezone-aware UTC timestamps, such as `datetime.now(timezone.utc).isoformat()`, unless the project provides a clock abstraction.
- Emit structured audit events for attempted, completed, and failed operations. Include only identifiers and diagnostics allowed by the project's privacy and retention policy; never log credentials, bearer tokens, file contents, or unrestricted server response bodies.
- Clean up generated intermediate files in `finally` blocks without deleting caller-owned input files.

## Retry and Failure Handling

Catch `HttpError` for Web API failures and use its structured fields:

- Retry only when `error.is_transient` is true and the operation is safe to repeat.
- Honor `error.retry_after` when present; otherwise use bounded exponential backoff with jitter.
- Cap attempts and elapsed time, and re-raise the final exception.
- Preserve `status_code`, service and client request IDs, correlation ID, and trace context in redacted diagnostics when available.
- Do not label a full re-upload as "resume"; the public 1.0 file API does not expose a continuation-token resume contract.
- Do not retry validation failures, authentication or authorization failures, missing files, occupied columns under create-only semantics, or other permanent errors.

When a workflow updates a Dataverse status record, write failure state only after the upload exception is captured, and do not replace the original exception with a secondary status-update failure.

## Good / Bad Examples

**Good:**

```python
import mimetypes
from pathlib import Path


def upload_document(
    client,
    *,
    table: str,
    record_id: str,
    file_column: str,
    file_path: Path,
    overwrite: bool = False,
) -> None:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    mime_type, _ = mimetypes.guess_type(path.name)
    client.files.upload(
        table=table,
        record_id=record_id,
        file_column=file_column,
        path=str(path),
        mode="auto",
        # SDK 1.0 applies this value only when auto selects the small path.
        mime_type=mime_type or "application/octet-stream",
        if_none_match=not overwrite,
    )
```

Why: The code uses the GA namespace and public parameters, validates the local file, lets the SDK choose the upload strategy, makes overwrite semantics explicit, and correctly expects no return value.

**Bad:**

```python
response = client.upload_file(
    table_name="account",
    record_id=account_id,
    file_column_name="new_file",
    file_path=path,
    chunk_size=8 * 1024 * 1024,
)
```

Why: `client.upload_file` is a removed beta shortcut, its named parameters do not match the GA API, `chunk_size` is not public, and the successful 1.x API does not return an upload response.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `client.files.upload` and `client.records.*` in SDK 1.x code. | Removed beta shortcuts fail at runtime. |
| Default to `mode="auto"` and let the SDK negotiate chunk size. | The SDK owns the verified 128 MiB boundary and server chunk recommendation. |
| Treat explicit MIME type as a small-upload feature in SDK 1.0. | Chunk mode sends `application/octet-stream`; large-file metadata must be verified separately. |
| Make `if_none_match` behavior explicit for create versus overwrite. | File replacement is deliberate instead of an accidental destructive side effect. |
| Treat runtime file-column creation as a schema mutation. | Metadata changes remain governed and permission-aware. |
| Use structured `HttpError` fields for retry and diagnostics. | Permanent failures are not retried and transient failures retain traceability. |
| Validate against real Dataverse metadata and project policy. | Examples do not invent logical names, option values, or file limits. |
| Keep integrity and audit data bounded and privacy-safe. | Operational evidence does not become a secret or data-leak path. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `Path` locally and pass `str(path)` to the SDK. | Assume the public parameter is named `file_path`. |
| Use `mode="auto"`, `"small"`, or `"chunk"`. | Pass a custom `chunk_size` to `client.files.upload`. |
| Use `if_none_match=True` for create-only uploads and `False` for an approved replacement. | Overwrite an occupied file column implicitly. |
| Use the GUID string returned by a single `client.records.create`. | Index `[0]` unless the create input was a list. |
| Iterate pages from multi-record `client.records.get`. | Treat `top=5000` as a page size or as an all-record export. |
| Retry only transient, repeatable failures and honor `retry_after`. | Retry every `HttpError` or claim an upload was resumed. |
| Verify logical names, limits, and option values from metadata. | Copy sample `new_*` names into production as universal contracts. |

## Checklist Before Opening a PR

- [ ] Code targets an inspected `PowerPlatform-Dataverse-Client` 1.x dependency.
- [ ] Removed beta shortcuts are absent; file and record calls use GA namespaces.
- [ ] Upload calls use only `table`, `record_id`, `file_column`, `path`, `mode`, `mime_type`, and `if_none_match`.
- [ ] Auto, small, and chunk modes are used with the verified 128 MiB behavior; no public `chunk_size` is assumed.
- [ ] Large-file workflows do not assume `mime_type` is transmitted by chunk mode.
- [ ] Create-only versus overwrite behavior is explicit and authorized.
- [ ] Single-record creation uses the returned GUID string; paginated reads use `page_size` correctly.
- [ ] File limits, extensions, MIME types, logical names, and option values come from real metadata or project policy.
- [ ] Retry logic checks `is_transient`, honors `retry_after`, is bounded, and preserves the final failure.
- [ ] Integrity checks and audit events are streaming, redacted, and aligned with privacy and retention policy.
- [ ] Generated intermediates are cleaned up and caller-owned inputs are preserved.
- [ ] Version-sensitive claims remain supported by the dated evidence in `docs/HARNESS-VALIDATION.md`.

## References

- PowerPlatform Dataverse Client 1.0 file operations: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/operations/files.py
- PowerPlatform Dataverse Client 1.0 upload implementation: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/data/_upload.py
- PowerPlatform Dataverse Client 1.0 record operations: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/operations/records.py
- PowerPlatform Dataverse Client file upload example: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/examples/advanced/file_upload.py
- Microsoft Dataverse file-column data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/file-column-data
