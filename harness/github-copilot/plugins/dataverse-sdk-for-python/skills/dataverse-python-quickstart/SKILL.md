---
name: "dataverse-python-quickstart"
description: >-
  Generate concise Microsoft Dataverse SDK for Python preview setup, authentication, CRUD, bulk create/update, paging, and optional File column upload snippets using official patterns. Use when the user asks for Dataverse Python quickstart code, SDK setup, InteractiveBrowserCredential, retrieve-multiple paging, or basic CRUD examples.
---

# Dataverse Python quickstart

Generate concise quickstart snippets for Microsoft Dataverse SDK for Python (preview), covering installation, `DataverseClient` setup with `InteractiveBrowserCredential`, CRUD, bulk operations, retrieve-multiple paging, and optional File column upload.

## When to invoke

- "Show a Dataverse Python SDK quickstart."
- "Create a DataverseClient with InteractiveBrowserCredential."
- "Generate CRUD examples for Microsoft Dataverse in Python."
- "Show bulk create, bulk update, and paging with Dataverse Python."
- "Optionally demonstrate File column upload."

## Quickstart scope

| Area | Include | Rule |
| --- | --- | --- |
| Install | `pip install PowerPlatform-Dataverse-Client` | Use the official package name exactly. |
| Authentication | `InteractiveBrowserCredential` | Good for local quickstarts; do not imply it is the only production credential. |
| Client | `DataverseClient` | Show environment-specific URL configuration without hardcoded secrets. |
| CRUD | Single-record create, retrieve, update, delete | Keep examples minimal and use logical table/column names. |
| Bulk create | Multiple records | Show collection-style input and capture created IDs. |
| Bulk update | Broadcast and 1:1 patterns | Distinguish one update applied to many records from per-record updates. |
| Retrieve multiple | `top`, `page_size` paging | Show deterministic paging and result iteration. |
| File column | Optional upload | Include only when user asks or the entity has a File column scenario. |

## Snippet rules

- Keep code aligned with official examples and avoid unannounced preview features.
- Use placeholders such as `<org-url>`, `<table-logical-name>`, and `<column-logical-name>` where the user has not provided environment details.
- Use logical Dataverse names, not display names.
- Keep snippets short enough for a quickstart; use the `dataverse-python-advanced-patterns` skill for advanced retries, metadata, pandas, and production hardening.

## Output template

````markdown
## Dataverse Python quickstart

**Status:** generated | needs environment details | blocked
**Package:** `PowerPlatform-Dataverse-Client`

### Install
```bash
pip install PowerPlatform-Dataverse-Client
```

### Code
```python
from azure.identity import InteractiveBrowserCredential
from dataverse import DataverseClient

credential = InteractiveBrowserCredential()
client = DataverseClient("<org-url>", credential=credential)

# CRUD single-record operations
# Bulk create
# Bulk update: broadcast and 1:1
# Retrieve multiple with top and page_size
# Optional File column upload
```

### Placeholders to replace
| Placeholder | Meaning |
| --- | --- |
| `<org-url>` | Dataverse environment URL |
| `<table-logical-name>` | Dataverse table logical name |
| `<column-logical-name>` | Dataverse column logical name |
````

## Quality gate

- [ ] Installation uses `pip install PowerPlatform-Dataverse-Client` exactly.
- [ ] Authentication uses `InteractiveBrowserCredential` for the quickstart.
- [ ] Client setup uses `DataverseClient` without hardcoded secrets.
- [ ] CRUD single-record operations are shown.
- [ ] Bulk create and bulk update are shown, including broadcast and 1:1 update patterns.
- [ ] Retrieve-multiple paging demonstrates `top` and `page_size`.
- [ ] File upload to a File column is included only when appropriate.
- [ ] Preview features are not introduced unless the user explicitly asks and the official examples support them.
