---
name: dataverse-python-usecase-builder
description: >-
  Generate complete Python solutions for Microsoft Dataverse SDK business use cases, including
  architecture, table design, CRUD, batch, query, file, scheduled, or real-time patterns. Use this
  skill when the user describes a Dataverse business need and asks for production-ready Python
  code, PowerPlatform-Dataverse-Client guidance, or Dataverse solution architecture.
---

<!-- Generated from harness/github-copilot/plugins/dataverse-sdk-for-python/skills/dataverse-python-usecase-builder/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Dataverse Python use case builder

Transform a Dataverse business need into a production-ready Python architecture with table design, pattern selection, SDK code, performance guidance, error handling, monitoring, and tests.

## When to invoke

- "Build a Python Dataverse solution for this use case."
- "Design tables and code for a Dataverse document workflow."
- "Generate PowerPlatform-Dataverse-Client SDK code for bulk sync."
- "Create a Dataverse scheduled job in Python."
- "Recommend Dataverse architecture for this business process."

## Prerequisites and context

- Target Python 3.10+ and PEP 8 style.
- Use `PowerPlatform.Dataverse.client.DataverseClient`, `PowerPlatform.Dataverse.core.config.DataverseConfig`, and `azure.identity.ClientSecretCredential` when authentication is needed.
- Use Dataverse table logical names, relationship names, choice values, and file columns supplied by the user or discovered from metadata. Do not invent production schema names without labeling them as proposed.

## Procedure

1. Analyze requirements: operations, data volume, frequency, performance, error tolerance, and audit needs.
2. Design the data model: tables, columns, relationships, lookups, files, and option sets.
3. Select the implementation pattern from the pattern table.
4. Generate complete Python code with configuration, service class, operations, error handling, logging, and usage examples.
5. Add optimization recommendations for the expected volume and latency.
6. Document monitoring, metrics, test strategy, and recovery behavior.

## Requirement analysis questions

| Area | Ask or infer |
| --- | --- |
| Operations | Create, Read, Update, Delete, Bulk, Query, file upload, or delete. |
| Volume | Record count, file sizes, page sizes, and batch sizes. |
| Frequency | One-time, batch, real-time, scheduled, daily, weekly, monthly. |
| Performance | Response time, throughput, timeout tolerance. |
| Error tolerance | Retry strategy, idempotency, partial success handling, resume behavior. |
| Audit | Logging, history, compliance, privacy, user activity tracking. |

## Data model design

Use proposed schema blocks like this when the real schema is not provided:

```python
tables = {
    "account": {
        "custom_fields": ["new_documentcount", "new_lastdocumentdate"]
    },
    "new_document": {
        "primary_key": "new_documentid",
        "columns": {
            "new_name": "string",
            "new_documenttype": "enum",
            "new_parentaccount": "lookup(account)",
            "new_uploadedby": "lookup(user)",
            "new_uploadeddate": "datetime",
            "new_documentfile": "file"
        }
    }
}
```

## Pattern selection

| Pattern | Use when | Examples |
| --- | --- | --- |
| Transactional CRUD Operations | Single record creation/update, immediate consistency, relationships, lookups. | Order management, invoice creation. |
| Batch Processing | Bulk create/update/delete, performance priority, partial failure acceptable. | Data migration, daily sync. |
| Query & Analytics | Complex filtering, aggregation, pagination, optimized reads. | Reporting, dashboards. |
| File Management | Document upload/storage, chunked transfers, audit trail. | Contract management, media library. |
| Scheduled Jobs | Recurring operations, external synchronization, resumable cleanup. | Nightly syncs, cleanup tasks. |
| Real-time Integration | Event-driven low-latency processing with status tracking. | Order processing, approval workflows. |

## Implementation skeleton

```python
import logging
from enum import IntEnum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig
from PowerPlatform.Dataverse.core.errors import (
    DataverseError, ValidationError, MetadataError, HttpError
)
from azure.identity import ClientSecretCredential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Status(IntEnum):
    DRAFT = 1
    ACTIVE = 2
    ARCHIVED = 3

class DataverseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        config = DataverseConfig()
        credential = ClientSecretCredential(
            tenant_id=config.tenant_id,
            client_id=config.client_id,
            client_secret=config.client_secret,
        )
        self.client = DataverseClient(config=config, credential=credential)
```

Include CRUD, bulk, query, file, or scheduled methods after this skeleton based on the selected pattern.

## Optimization rules

| Scenario | Pattern |
| --- | --- |
| High-volume create/update | Use batch operations: `client.create("table", [record1, record2, record3])`; avoid one network call per row. |
| Bulk load | Chunk input and track successful IDs: `client.create("table", [record] * 1000)`. |
| Complex query | Use `filter`, `select`, `orderby`, and `top=500`; process pages instead of materializing all results. |
| Large file transfer | Use chunked upload with `chunk_size=4 * 1024 * 1024` for 4 MB chunks. |
| Recovery | Store checkpoints, retry transient `HttpError`, and treat validation failures as data-quality records. |

```python
for page in client.get(
    "table",
    filter="status eq 1",
    select=["id", "name", "amount"],
    orderby="name",
    top=500
):
    pass

client.upload_file(
    table_name="table",
    record_id=id,
    file_column_name="new_file",
    file_path=path,
    chunk_size=4 * 1024 * 1024
)
```

## Use case categories

| Category | Typical cases |
| --- | --- |
| Customer Relationship Management | Lead management, account hierarchy, contact tracking, opportunity pipeline, activity history. |
| Document Management | Storage and retrieval, version control, access control, audit trails, compliance tracking. |
| Data Integration | ETL, data synchronization, external system integration, migration, backup/restore. |
| Business Process | Order management, approval workflows, project tracking, inventory, resource allocation. |
| Reporting & Analytics | Aggregation, historical analysis, KPI tracking, dashboard data, export functionality. |
| Compliance & Audit | Change tracking, user activity logging, governance, retention policies, privacy management. |

## Dataverse implementation labels

Use these labels when structuring generated code and architecture notes: `Backup/restore`, `CLASS`, `CONFIGURATION`, `CONSTANTS`, `ENUMS`, `ERROR`, `EXAMPLE`, `HANDLING`, `OPERATIONS`, `PATTERN`, `RECOVERY`, `SERVICE`, `SETUP`, `SINGLETON`, `SPECIFIC`, `USAGE`, `Upload/store`, and `relationships/lookups`.

## Output template

```markdown
## Dataverse Python solution - <use case>

**Status:** complete | needs details | blocked
**Pattern:** Transactional CRUD Operations | Batch Processing | Query & Analytics | File Management | Scheduled Jobs | Real-time Integration

### Architecture overview
<2-3 sentence design summary>

### Data model
| Table | Relationship | Key columns | Notes |
| --- | --- | --- | --- |
| `<logical name>` | `<relationship>` | `<columns>` | `<constraints>` |

### Implementation code
```python
<complete Python 3.10+ code>
```

### Usage instructions
1. <configuration step>
2. <run command or entry point>

### Performance notes
- <throughput, batch, paging, or chunking guidance>

### Error handling
| Failure | Recovery |
| --- | --- |
| `<failure>` | `<retry, skip, compensate, or alert>` |

### Monitoring
- <metric to track>

### Testing
- <unit or integration test pattern>
```

## Quality gate

- [ ] The solution states operations, volume, frequency, performance, error tolerance, and audit assumptions.
- [ ] Proposed table and column names are labeled when not user-provided.
- [ ] Code includes all imports, type hints, logging, and Dataverse error handling.
- [ ] The selected pattern matches the use case category and volume.
- [ ] Bulk, paging, or chunking is used for high-volume records or files.
- [ ] Usage, monitoring, and testing guidance are included.
