---
name: "dataverse-python-production-code"
description: >-
  Generate production-ready Python 3.10+ code for the PowerPlatform-Dataverse-Client SDK with DataverseError handling, singleton client management, retry with exponential backoff for 429/timeout failures, OData optimization, audit logging, type hints, docstrings, configuration handling, and usage examples. Use when asked for Dataverse Python code, SDK examples, or system instructions.
---

# Dataverse Python production code

Generate production-ready Python for the PowerPlatform-Dataverse-Client SDK by using typed service classes, singleton client management, Dataverse exception handling, retryable transient errors, server-side OData filtering, and structured logging instead of throwaway snippets.

## When to invoke

- "Generate production Python for Dataverse."
- "Write PowerPlatform-Dataverse-Client SDK code with retries."
- "Show Dataverse error handling and logging patterns."
- "Create a singleton Dataverse client service."
- "Optimize this Dataverse query with OData select and filter."

## Code generation criteria

| Area | Required rule |
| --- | --- |
| Python version | Code must be syntactically correct Python 3.10+. |
| Imports | Order stdlib, third-party, then local imports. |
| Error handling | Catch `DataverseError`, `ValidationError`, `MetadataError`, and `HttpError` with try-except blocks where appropriate. |
| Retry | Retry transient `429` or timeout errors with exponential backoff; default `max_retries=3`. |
| Client management | Use a singleton service class so connection management is centralized. |
| OData | Filter on the server, select only needed columns, use lowercase logical names, and apply `orderby`, `top`, and `expand` when appropriate. |
| Logging | Use `logger`, not `print()`, with enough context for audit trails and debugging. |
| Types and docs | Include type hints and docstrings for all public functions. |
| Configuration | Keep secrets, URLs, and credentials in configuration; do not hardcode them. |
| Style | Follow PEP 8 and Microsoft best practices from official examples. |

## Error handling pattern

```python
from PowerPlatform.Dataverse.core.errors import (
    DataverseError, ValidationError, MetadataError, HttpError
)
import logging
import time

logger = logging.getLogger(__name__)

def operation_with_retry(max_retries=3):
    """Function with retry logic."""
    for attempt in range(max_retries):
        try:
            # Operation code
            pass
        except HttpError as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                raise
            backoff = 2 ** attempt
            logger.warning(f"Attempt {attempt + 1} failed. Retrying in {backoff}s")
            time.sleep(backoff)
```

## Client management pattern

```python
class DataverseService:
    _instance = None
    _client = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, org_url, credential):
        if self._client is None:
            self._client = DataverseClient(org_url, credential)
    
    @property
    def client(self):
        return self._client
```

## Logging pattern

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f"Created {count} records")
logger.warning(f"Record {id} not found")
logger.error(f"Operation failed: {error}")
```

## OData optimization rules

| Rule | Reason |
| --- | --- |
| Always include `select` | Avoid transferring unused columns. |
| Use `filter` on server | Do not fetch broad records and filter in Python. |
| Use lowercase logical names | Dataverse logical names are lowercase and differ from display names. |
| Use `orderby` and `top` | Make pagination and result order deterministic. |
| Use `expand` for related records when available | Avoid manual follow-up calls when supported. |
| Log query intent, not secrets | Audit behavior without leaking tokens or PII. |

## User request processing

When generating code, include these sections:

1. Imports with all required modules.
2. Configuration section with `constants/enums`.
3. Main implementation with proper error handling.
4. Docstrings explaining parameters and return values.
5. Type hints for all functions.
6. Usage example showing how to call the code.
7. Error scenarios with exception handling.
8. Logging statements for debugging.

## Output template

````markdown
## Dataverse Python implementation

**Status:** generated | needs details | blocked
**SDK:** `PowerPlatform-Dataverse-Client`
**Python:** `3.10+`

### Code
```python
from PowerPlatform.Dataverse.core.errors import DataverseError, ValidationError, MetadataError, HttpError

# stdlib imports, configuration, logging, singleton DataverseService,
# OData-optimized operation, retry handling, usage example
```

### Error scenarios
| Scenario | Exception | Handling |
| --- | --- | --- |
| Validation failure | `ValidationError` | fail fast with clear message |
| Metadata issue | `MetadataError` | log and raise |
| HTTP 429/timeout | `HttpError` | retry with exponential backoff |
| Other Dataverse failure | `DataverseError` | log with context and raise |

### OData query choices
- `select`: <columns>
- `filter`: <server-side filter>
- `orderby`: <ordering>
- `top`: <limit>
- `expand`: <related records if used>
````

## Quality gate

- [ ] Code is valid Python 3.10+ and follows PEP 8.
- [ ] API calls are inside try/except blocks using `DataverseError`, `ValidationError`, `MetadataError`, and `HttpError` where applicable.
- [ ] Retry logic with exponential backoff covers transient `429` and timeout errors.
- [ ] Client creation follows the singleton `DataverseService` pattern.
- [ ] OData queries use `select`, server-side `filter`, lowercase logical names, and `orderby`/`top`/`expand` when appropriate.
- [ ] All public functions include type hints and docstrings.
- [ ] Logging uses `logger` and never `print()` for operational messages.
- [ ] Secrets, URLs, and credentials are configuration-driven, not hardcoded.
- [ ] The answer includes imports, configuration, main implementation, usage example, error scenarios, and logging statements.
