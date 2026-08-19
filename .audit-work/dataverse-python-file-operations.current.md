---
applyTo: "**/*.py"
description: "Enforces Python Dataverse SDK conventions for file uploads, chunking, validation, retries, audit logging, and practical file-operation workflows."
---

# Dataverse Python File Operations Conventions — Uploads, Chunking, and Auditability

These instructions apply to Python files that use the PowerPlatform-DataverseClient-Python SDK for Dataverse file columns and related file workflows. They are authoritative for `DataverseClient` upload patterns, file-size decisions, chunking, validation, retry behavior, audit logging, integrity checks, and practical create-upload-query flows in matched Python files; project-wide Python, authentication, and security primitives win where they define stricter dependency, credential, or secret-handling rules. Keep these rules as conventions for reliable Dataverse file operations, not as a procedural runbook.

## Client, Authentication, and File Column Basics

Use `from pathlib import Path` for file paths and `from PowerPlatform.Dataverse.client import DataverseClient` for SDK access. Build clients with Azure credentials such as `from azure.identity import ClientSecretCredential` only when the project already uses service-principal authentication, and pass the Dataverse environment URL to `DataverseClient`, for example `DataverseClient("https://yourorg.crm.dynamics.com", credential)`. Never hardcode real tenant IDs, client IDs, client secrets, record IDs, or production organization URLs in source.

Use `client.upload_file(table_name=..., record_id=..., file_column_name=..., file_path=...)` for file columns. Keep Dataverse logical names explicit: examples include `account`, `new_documentfile`, `new_videofile`, `new_largemedifile`, `new_contractfile`, `new_specfile`, `new_designfile`, `new_customerdocument`, `new_documentname`, `new_documenttype`, `new_customerid`, `new_uploadeddate`, `new_filesize`, `new_mediagallery`, `new_galleryname`, `new_createddate`, `new_mediaitem`, `new_itemname`, `new_mediatype`, `new_description`, `new_galleryid`, `new_mediafile`, `new_backuprecord`, `new_tablename`, `new_recordcount`, `new_backupdate`, `new_status`, `new_backupfile`, `new_report`, `new_reportname`, `new_reporttype`, `new_generateddate`, `new_reportfile`, `new_errormessage`, and `new_filehash`.

## Upload Strategy and Chunking

| File class | Convention | Rationale |
| --- | --- | --- |
| Small file | Use a single SDK upload when `file_size <= 128 * 1024 * 1024` (`< 128 MB`). | Documents, images, and PDFs under `128 MB` avoid unnecessary chunk management. |
| Large file | Use `chunk_size=4 * 1024 * 1024` for files `> 128 MB`, with `8 * 1024 * 1024` only when timeouts require larger chunks. | Large videos, databases, archives, and `large_file.zip` need chunked transfer to avoid request limits. |
| Automatic decision | Compute `file_path.stat().st_size`, set `max_single_patch = 128 * 1024 * 1024`, and pass `chunk_size = None` or a chunk size. | Strategy selection stays deterministic and testable. |
| Progress tracking | Log file name, size in MB, and a pre-upload SHA-256 hash. | Operators can prove what was uploaded and investigate corruption. |
| Batch uploads | Iterate a `files_dict` mapping `{column_name: file_path}` and return `{"success": [], "failed": []}`. | Multi-column uploads should report partial success rather than hiding failures. |
| Retry | Catch `HttpError`, retry up to `max_retries=3`, and use exponential backoff `2 ** attempt`. | Transient Dataverse or network errors should not fail immediately. |

Preserve SDK argument names exactly: `table_name`, `record_id`, `file_column_name`, `file_path`, and `chunk_size`. Keep wrapper names intention-revealing, such as `upload_file_smart`, `upload_with_tracking`, `batch_upload_files`, `upload_with_retry`, `upload_customer_document`, `create_media_gallery`, `backup_table_data`, `generate_and_store_report`, `validate_file_for_upload`, `validate_file_type`, `log_file_upload`, `upload_with_logging`, `check_upload_space`, and `verify_uploaded_file`.

## Validation, Integrity, and Audit Logging

Validate existence, size, type, space, and integrity before or after upload.

| Check | Required pattern | Failure prevented |
| --- | --- | --- |
| Existence | `if not file_path.exists(): raise FileNotFoundError(...)` | Clear failure when a path is wrong. |
| Size | Compare `file_path.stat().st_size` with `max_size_mb * 1024 * 1024`, commonly `max_size_mb=500` or `max_size_mb=128`. | Oversized uploads fail before expensive transfer. |
| Type | Define `ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.jpg', '.png', '.mp4', '.zip'}` and compare `file_path.suffix.lower()`. | Unsupported files are rejected consistently. |
| Disk buffer | Use `shutil.disk_usage(file_path.parent)` and require `file_size * 1.1` free space. | Local export or temp-buffer workflows avoid mid-operation disk failures. |
| Hash | Use `hashlib.sha256()` and read files in binary mode (`'rb'`) with `1024 * 1024` chunks. | `new_filehash` mismatches detect corruption. |
| Audit | Write JSON lines to `upload_audit.log` with `timestamp`, `table`, `record_id`, `file_name`, `file_size`, `status`, and `error`. | Upload attempts remain traceable for support and compliance. |

Use `datetime.now().isoformat()` for record timestamps such as `new_uploadeddate`, `new_createddate`, `new_backupdate`, and `new_generateddate` when no project-wide time abstraction exists. Use `json.dump(..., indent=2, default=str)` for JSON export and `json.dumps(log_entry) + "\n"` for audit log records.

## Dataverse Create, Query, Update, and Status Patterns

When a file belongs to a Dataverse record, create the metadata record first with `client.create(table, record)`, take the created ID from `ids[0]`, upload the file to the file column, then query or update status as needed. Query related records with `client.get(table, filter=..., select=[...], top=5000)` and iterate pages before records. Update status with `client.update(table, id, {...})` after the file operation succeeds or fails.

Use enum classes derived from `IntEnum` for Dataverse option-set values: `DocumentType.CONTRACT = 1`, `DocumentType.INVOICE = 2`, `DocumentType.SPECIFICATION = 3`, `DocumentType.OTHER = 4`; `MediaType.PHOTO = 1`, `MediaType.VIDEO = 2`, `MediaType.DOCUMENT = 3`; `ReportStatus.PENDING = 1`, `ReportStatus.PROCESSING = 2`, `ReportStatus.COMPLETED = 3`, and `ReportStatus.FAILED = 4`. Preserve literal report identifiers such as `SALES_SUMMARY` when they are data contracts.

For generated reports and backups, write files under a caller-provided project path such as `backups`, name backups with `f"{table_name}_{backup_time.strftime('%Y%m%d_%H%M%S')}.json"`, and clean up generated report files with `report_file.unlink(missing_ok=True)` in `finally` after upload and status update. Do not use forbidden temporary directories or leave generated files behind when the workflow expects cleanup.

## Dataverse Workflow Names and Data Variables

Keep workflow variable names recognizable when refactoring examples because they connect metadata creation, file upload, query, status, and audit operations: `account_id`, `customer_id`, `customer-guid-here`, `doc_path`, `doc_type`, `doc_record`, `doc_ids`, `doc_id`, `gallery_name`, `gallery_ids`, `gallery_id`, `media_files`, `media_info`, `item_ids`, `item_id`, `backup_file`, `backup_ids`, `backup_id`, `all_records`, `output_dir`, `report_type`, `report_time`, `report_ids`, `report_id`, `sales_data`, `large_video`, `original_hash`, `local_path`, `local_hash`, `remote_hash`, `log_file`, `max_size_bytes`, `backoff_seconds`, `exist_ok`, and `real-world`. Preserve placeholder credential names such as `tenant-id`, `client-id`, `client-secret`, `tenant_id`, `client_id`, and `client_secret` only as examples; real values must come from secure configuration. Raise `ValueError` for invalid sizes, extensions, and hash mismatches.

## Error Handling and Troubleshooting

Import SDK exceptions from `PowerPlatform.Dataverse.core.errors`, especially `HttpError` for upload retries and `DataverseError` where broader Dataverse failures need handling. Catch narrow exceptions where possible, log enough context to identify the table, record, column, and file, and re-raise after recording failure state.

| Issue | Convention | Rationale |
| --- | --- | --- |
| File upload timeout | Increase `chunk_size` from `4 * 1024 * 1024` to `8 * 1024 * 1024` for very large files. | Larger chunks can reduce request overhead when the service and network tolerate them. |
| Insufficient disk space | Check `total, used, free = shutil.disk_usage(file_path.parent)` and compare with `required_space = file_size * 1.1`. | Backups and generated files need room for source plus buffer. |
| File corruption | Compare local `hashlib.sha256(f.read()).hexdigest()` with `remote_data.get("new_filehash")`. | Hash mismatch proves the uploaded bytes are not the expected bytes. |
| Partial batch failure | Keep `results["success"]` and `results["failed"]` entries with `column`, `file`, `response`, and `error`. | Callers can retry failed columns without repeating successful uploads. |

## Good / Bad Examples

The examples below illustrate deterministic strategy selection, validation, and retry-safe upload boundaries.

**Good:**

```python
from pathlib import Path
import hashlib
import time
from PowerPlatform.Dataverse.core.errors import HttpError

MAX_SINGLE_PATCH = 128 * 1024 * 1024
DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024


def calculate_file_hash(file_path: Path) -> str:
    hash_obj = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def upload_with_retry(client, table_name, record_id, column_name, file_path, max_retries=3):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    chunk_size = None if path.stat().st_size <= MAX_SINGLE_PATCH else DEFAULT_CHUNK_SIZE
    file_hash = calculate_file_hash(path)

    for attempt in range(max_retries):
        try:
            response = client.upload_file(
                table_name=table_name,
                record_id=record_id,
                file_column_name=column_name,
                file_path=path,
                chunk_size=chunk_size,
            )
            return {"response": response, "sha256": file_hash}
        except HttpError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

Why: The code validates the path, chooses single PATCH or chunking at `128 MB`, computes integrity metadata, retries only SDK HTTP failures, and preserves exact SDK parameter names.

**Bad:**

```python
def upload(client, path):
    return client.upload_file("account", "account-guid", "new_file", path)
```

Why: Positional arguments obscure the Dataverse contract, there is no size decision, validation, chunk size, retry, audit log, or integrity signal.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `Path` for file inputs and convert early. | Path operations, size checks, suffix checks, and cleanup stay platform-safe. |
| Use named `client.upload_file` arguments: `table_name`, `record_id`, `file_column_name`, `file_path`, and `chunk_size`. | Dataverse file operations remain self-documenting and resistant to argument-order mistakes. |
| Use single PATCH below or at `128 MB`; use chunked upload above `128 MB`. | The upload path matches Dataverse file-column behavior and avoids request-size failures. |
| Default chunking to `4 MB` and increase to `8 MB` only for timeout troubleshooting. | Chunk sizes balance reliability and request overhead. |
| Validate existence, max size, allowed extension, disk buffer, and hash when the workflow depends on file integrity. | Bad input and local-environment failures surface before remote mutation. |
| Use `HttpError` retry with bounded exponential backoff. | Transient failures are retried without hiding persistent failures. |
| Return structured batch results with success and failure lists. | Multi-file operations stay observable and retryable. |
| Create metadata records before upload and update status after upload. | Dataverse records remain queryable and status reflects the file operation. |
| Use `IntEnum` for option-set values such as document, media, and report status. | Magic integers get meaningful names without changing the Dataverse payload. |
| Clean up generated report files after upload when they are intermediate artifacts. | Local workspaces do not accumulate stale generated data. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `DataverseClient` with a credential object and an environment URL. | Hardcode real secrets, tenant IDs, or production URLs in examples or source. |
| Upload with named SDK arguments. | Rely on positional `upload_file` calls. |
| Compute `file_size = file_path.stat().st_size` before choosing upload strategy. | Treat all files as the same size class. |
| Keep `ALLOWED_EXTENSIONS` explicit and compare lowercase suffixes. | Accept arbitrary file extensions silently. |
| Catch `HttpError` for retryable upload failures. | Catch all exceptions and continue as if upload succeeded. |
| Log `SUCCESS` and `FAILED` audit records with context. | Print only a success message and lose failure details. |
| Compare local SHA-256 to `new_filehash` when integrity metadata exists. | Assume upload integrity without verification when corruption is suspected. |
| Use `client.get(..., top=5000)` page iteration for exports. | Assume a single response contains all Dataverse records. |
| Set `ReportStatus.COMPLETED` or `ReportStatus.FAILED` after report upload. | Leave records stuck in `ReportStatus.PROCESSING`. |

## Checklist Before Opening a PR

- [ ] File uploads use `Path` and named `client.upload_file` parameters.
- [ ] Files at or below `128 MB` use single upload; larger files use chunking with an intentional `chunk_size`.
- [ ] Upload wrappers validate existence, max size, allowed extension, and disk space when those constraints apply.
- [ ] Integrity-sensitive uploads calculate or compare SHA-256 hashes and preserve `new_filehash` metadata where used.
- [ ] Batch uploads return structured `success` and `failed` results.
- [ ] Retry logic catches `HttpError`, uses bounded exponential backoff, and re-raises after the final attempt.
- [ ] Metadata records are created before file upload and status fields are updated after success or failure.
- [ ] Audit logs include table, record ID, file name, file size, status, and error context.
- [ ] Generated backup or report files are created under an intentional project path and cleaned up when temporary.
- [ ] No real Dataverse secrets, tenant IDs, client IDs, client secrets, or production organization URLs are committed.

## References

- PowerPlatform Dataverse Python file upload example: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/main/examples/advanced/file_upload.py
- Dataverse file column documentation: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/file-column-data
