---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-testing-debugging.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces testing and debugging conventions for Python Dataverse SDK code, including mocks, integration tests, coverage, performance checks, and diagnostics.

# Dataverse Python Testing Conventions — SDK Diagnostics

These instructions apply to Python tests, fixtures, and diagnostics for Dataverse SDK code matched by `**/*.py`. They are authoritative for pytest structure, mocked `DataverseClient` tests, integration-test isolation, coverage, logging, performance checks, and debugging practices around `PowerPlatform.Dataverse`; official pytest, `unittest.mock`, Azure Functions testing, and Dataverse SDK documentation win where they define stricter API behavior.

## Testing Overview

### Testing Pyramid for Dataverse SDK

```
         Integration Tests  <- Test with real Dataverse
              /\
             /  \
            /Unit Tests (Mocked)\
           /____________________\
          < Framework Tests
```

---

## Unit Testing with Mocking

### Test Environment Dependencies

```bash
# Install test dependencies
pip install pytest pytest-cov unittest-mock
```

### Mock DataverseClient

```python
# tests/test_operations.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from PowerPlatform.Dataverse.client import DataverseClient

@pytest.fixture
def mock_client():
    """Provide mocked DataverseClient."""
    client = Mock(spec=DataverseClient)
    return client

def test_create_account(mock_client):
    """Test account creation with mocked client."""
    
    # Setup mock response
    mock_client.create.return_value = ["id-123"]
    
    # Call function
    from my_app import create_account
    result = create_account(mock_client, {"name": "Acme"})
    
    # Verify
    assert result == "id-123"
    mock_client.create.assert_called_once_with("account", {"name": "Acme"})

def test_create_account_error(mock_client):
    """Test error handling in account creation."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    # Setup mock to raise error
    mock_client.create.side_effect = DataverseError(
        message="Account exists",
        code="validation_error",
        status_code=400
    )
    
    # Verify error is raised
    from my_app import create_account
    with pytest.raises(DataverseError):
        create_account(mock_client, {"name": "Acme"})
```

### Test Data Structures

```python
# tests/fixtures.py
import pytest

@pytest.fixture
def sample_account():
    """Sample account record for testing."""
    return {
        "accountid": "id-123",
        "name": "Acme Inc",
        "telephone1": "555-0100",
        "statecode": 0,
        "createdon": "2025-01-01T00:00:00Z"
    }

@pytest.fixture
def sample_accounts(sample_account):
    """Multiple sample accounts."""
    return [
        sample_account,
        {**sample_account, "accountid": "id-124", "name": "Fabrikam"},
        {**sample_account, "accountid": "id-125", "name": "Contoso"},
    ]

# Usage in tests
def test_process_accounts(mock_client, sample_accounts):
    mock_client.get.return_value = iter([sample_accounts])
    # Test processing
```

---

## Mocking Common Patterns

### Mock Get with Pagination

```python
def test_pagination(mock_client, sample_accounts):
    """Test handling paginated results."""
    
    # Mock returns generator with pages
    mock_client.get.return_value = iter([
        sample_accounts[:2],  # Page 1
        sample_accounts[2:]   # Page 2
    ])
    
    from my_app import process_all_accounts
    result = process_all_accounts(mock_client)
    
    assert len(result) == 3  # All pages processed
```

### Mock Bulk Operations

```python
def test_bulk_create(mock_client):
    """Test bulk account creation."""
    
    payloads = [
        {"name": "Account 1"},
        {"name": "Account 2"},
    ]
    
    # Mock returns list of IDs
    mock_client.create.return_value = ["id-1", "id-2"]
    
    from my_app import create_accounts
    ids = create_accounts(mock_client, payloads)
    
    assert len(ids) == 2
    mock_client.create.assert_called_once_with("account", payloads)
```

### Mock Errors

```python
def test_rate_limiting_retry(mock_client):
    """Test retry logic on rate limiting."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    # Mock fails then succeeds
    error = DataverseError(
        message="Too many requests",
        code="http_error",
        status_code=429,
        is_transient=True
    )
    mock_client.create.side_effect = [error, ["id-123"]]
    
    from my_app import create_with_retry
    result = create_with_retry(mock_client, "account", {})
    
    assert result == "id-123"
    assert mock_client.create.call_count == 2  # Retried
```

---

## Integration Testing

### Local Development Testing

```python
# tests/test_integration.py
import pytest
from azure.identity import InteractiveBrowserCredential
from PowerPlatform.Dataverse.client import DataverseClient

@pytest.fixture
def dataverse_client():
    """Real client for integration testing."""
    client = DataverseClient(
        base_url="https://<your-org>.crm.dynamics.com",
        credential=InteractiveBrowserCredential()
    )
    return client

@pytest.mark.integration
def test_create_and_retrieve_account(dataverse_client):
    """Test creating and retrieving account (against real Dataverse)."""
    
    # Create
    account_id = dataverse_client.create("account", {
        "name": "Test Account"
    })[0]
    
    # Retrieve
    account = dataverse_client.get("account", account_id)
    
    # Verify
    assert account["name"] == "Test Account"
    
    # Cleanup
    dataverse_client.delete("account", account_id)
```

### Test Isolation

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="function")
def test_account(dataverse_client):
    """Create test account, cleanup after test."""
    
    account_id = dataverse_client.create("account", {
        "name": "Test Account"
    })[0]
    
    yield account_id
    
    # Cleanup
    try:
        dataverse_client.delete("account", account_id)
    except:
        pass  # Already deleted

# Usage
def test_update_account(dataverse_client, test_account):
    """Test updating account."""
    dataverse_client.update("account", test_account, {"telephone1": "555-0100"})
    
    account = dataverse_client.get("account", test_account)
    assert account["telephone1"] == "555-0100"
```

---

## Pytest Configuration

### pytest.ini

```ini
[pytest]
# Skip integration tests by default
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    integration: marks tests as integration (run with -m integration)
    slow: marks tests as slow
    unit: marks tests as unit tests
```

### Run Tests

```bash
# Unit tests only
pytest

# Unit + integration
pytest -m "unit or integration"

# Integration only
pytest -m integration

# With coverage
pytest --cov=my_app tests/

# Specific test
pytest tests/test_operations.py::test_create_account
```

---

## Coverage Analysis

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=my_app --cov-report=html tests/

# View coverage
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Coverage Configuration (.coveragerc)

```ini
[run]
branch = True
source = my_app

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

---

## Debugging with Print and Logging

### Enable Debug Logging

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug.log')
    ]
)

# Enable SDK logging
logging.getLogger('PowerPlatform').setLevel(logging.DEBUG)
logging.getLogger('azure').setLevel(logging.DEBUG)

# In test
def test_with_logging(mock_client):
    logger = logging.getLogger(__name__)
    logger.debug("Starting test")
    
    result = my_function(mock_client)
    
    logger.debug(f"Result: {result}")
```

### Pytest Capturing Output

```bash
# Show print/logging output in tests
pytest -s tests/

# Capture and show on failure only
pytest --tb=short tests/
```

---

## Performance Testing

### Measure Operation Duration

```python
import pytest
import time

def test_bulk_create_performance(dataverse_client):
    """Test bulk create performance."""
    
    payloads = [{"name": f"Account {i}"} for i in range(1000)]
    
    start = time.time()
    ids = dataverse_client.create("account", payloads)
    duration = time.time() - start
    
    assert len(ids) == 1000
    assert duration < 10  # Should complete in under 10 seconds
    
    print(f"Created 1000 records in {duration:.2f}s ({1000/duration:.0f} records/s)")
```

### Pytest Benchmark Plugin

```bash
pip install pytest-benchmark
```

```python
def test_query_performance(benchmark, dataverse_client):
    """Benchmark query performance."""
    
    def get_accounts():
        return list(dataverse_client.get("account", top=100))
    
    result = benchmark(get_accounts)
    assert len(result) <= 100
```

---

## Common Testing Patterns

### Testing Retry Logic

```python
def test_retry_on_transient_error(mock_client):
    """Test retry on transient error."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    error = DataverseError(
        message="Timeout",
        code="http_error",
        status_code=408,
        is_transient=True
    )
    
    # Fail then succeed
    mock_client.create.side_effect = [error, ["id-123"]]
    
    from my_app import create_with_retry
    result = create_with_retry(mock_client, "account", {})
    
    assert result == "id-123"
```

### Testing Filter Building

```python
def test_filter_builder():
    """Test OData filter generation."""
    from my_app import build_account_filter
    
    # Test cases
    assert build_account_filter(status="active") == "statecode eq 0"
    assert build_account_filter(name="Acme") == "contains(name, 'Acme')"
    assert build_account_filter(status="active", name="Acme") \
        == "statecode eq 0 and contains(name, 'Acme')"
```

### Testing Error Handling

```python
def test_handles_missing_record(mock_client):
    """Test handling 404 errors."""
    from PowerPlatform.Dataverse.core.errors import DataverseError
    
    mock_client.get.side_effect = DataverseError(
        message="Not found",
        code="http_error",
        status_code=404
    )
    
    from my_app import get_account_safe
    result = get_account_safe(mock_client, "invalid-id")
    
    assert result is None  # Returns None instead of raising
```

---

## Debugging Checklist

| Issue | Debug Steps |
|-------|-------------|
| Test fails unexpectedly | Add `-s` flag to see print output |
| Mock not called | Check method name/parameters match exactly |
| Real API failing | Check credentials, URL, permissions |
| Rate limiting in tests | Add delays or use smaller batches |
| Data not found | Verify record created and not cleaned up |
| Assertion errors | Print actual vs expected values |

---

## Good / Bad Examples

The examples below illustrate a Dataverse unit test that isolates SDK behavior while preserving error semantics.

**Good:**

```python
from unittest.mock import Mock
import pytest
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.errors import DataverseError

def test_create_account_error():
    mock_client = Mock(spec=DataverseClient)
    mock_client.create.side_effect = DataverseError(
        message="Account exists",
        code="validation_error",
        status_code=400
    )

    with pytest.raises(DataverseError):
        create_account(mock_client, {"name": "Acme"})

    mock_client.create.assert_called_once_with("account", {"name": "Acme"})
```

Why: The test constrains the mock with `spec=DataverseClient`, preserves the SDK exception type, and verifies the exact entity name and payload.

**Bad:**

```python
def test_create_account_error():
    mock_client = Mock()
    mock_client.create.side_effect = Exception("failed")

    assert create_account(mock_client, {"name": "Acme"}) is None
```

Why: The unrestricted mock can accept misspelled SDK calls, the generic exception hides `DataverseError` fields such as `code`, `status_code`, and `is_transient`, and the assertion does not verify SDK behavior.

## Conventions

| Rule | Rationale |
|---|---|
| Install and use `pytest`, `pytest-cov`, and `unittest-mock` for local test work when the project does not already provide equivalent dependencies | Tests stay consistent with the documented pytest and mock patterns |
| Mock `DataverseClient` with `Mock(spec=DataverseClient)` and assert exact calls such as `create("account", {"name": "Acme"})` | Spec-bound mocks catch misspelled SDK methods and wrong parameters |
| Represent SDK failures with `PowerPlatform.Dataverse.core.errors.DataverseError` including `message`, `code`, `status_code`, and `is_transient` | Retry and error-handling tests exercise the same signals as production |
| Model paginated `get` calls as iterators of page lists | Application code that consumes pages is tested instead of a single happy path |
| Keep integration tests behind `@pytest.mark.integration` and run them explicitly with `pytest -m integration` | Real Dataverse calls require credentials, permissions, and cleanup |
| Use `InteractiveBrowserCredential` only for local integration fixtures and configure `DataverseClient(base_url="https://<your-org>.crm.dynamics.com", credential=...)` deliberately | Tests do not accidentally target the wrong tenant or environment |
| Create integration records in fixtures and clean them with `delete` in `yield` teardown | Test data does not pollute Dataverse environments |
| Configure `pytest.ini` with `testpaths`, `python_files`, `python_classes`, `python_functions`, and markers for `integration`, `slow`, and `unit` | Test discovery and marker selection are predictable |
| Use `.coveragerc` with `branch = True`, `source = my_app`, and `htmlcov` output for coverage analysis | Coverage reports focus on application code and keep generated output consistent |
| Enable `logging.DEBUG` for `PowerPlatform` and `azure` only while diagnosing failures | SDK and Azure logs are verbose and should not become default test noise |
| Use `pytest -s tests/` for live output and `pytest --tb=short tests/` for concise failure traces | Debug output is available without making normal runs noisy |
| Treat performance thresholds such as `duration < 10` for 1000 records as environment-sensitive examples, not universal SLAs | Dataverse throughput depends on tenant, network, throttling, and payload shape |
| Benchmark with `pytest-benchmark` only for repeatable local comparisons | Benchmarks are useful when they compare the same operation under similar conditions |
| Test OData filters such as `statecode eq 0`, `contains(name, 'Acme')`, and combined `and` clauses as strings | Query builders fail silently if filter syntax drifts |

## Do / Do Not

| Do | Do not |
|---|---|
| Keep fast unit tests mocked and deterministic | Call real Dataverse from default `pytest` runs |
| Mark real-environment tests with `@pytest.mark.integration` | Hide integration tests among normal unit tests |
| Mock `create`, `get`, `update`, and `delete` responses with SDK-shaped data | Return arbitrary objects that production code never receives |
| Test `DataverseError` status codes `400`, `408`, `429`, and `404` where behavior depends on them | Collapse all SDK failures into `Exception` |
| Verify cleanup in integration fixtures even when a test fails | Leave test accounts behind after `create` succeeds |
| Use `pytest --cov=my_app --cov-report=html tests/` for coverage reports | Treat coverage as a substitute for asserting SDK behavior |
| Print actual and expected values only while diagnosing an assertion | Commit noisy debugging output to stable tests |
| Add delays or smaller batches when rate limiting appears | Increase concurrency against Dataverse to force flaky tests through |

## Checklist Before Opening a PR

- [ ] Unit tests mock `DataverseClient` with a spec and assert exact SDK method names and parameters.
- [ ] SDK error paths use `DataverseError` with relevant `code`, `status_code`, and `is_transient` values.
- [ ] Pagination, bulk create, retry, missing-record, and OData filter behavior are covered where the application implements them.
- [ ] Integration tests are marked with `integration`, require explicit selection, and clean up created records.
- [ ] `pytest.ini` marker and discovery settings match the test suite.
- [ ] Coverage commands and `.coveragerc` settings target application code, not generated reports.
- [ ] Debug logging for `PowerPlatform` and `azure` is opt-in and does not leak credentials or tenant data.
- [ ] Performance assertions are justified for the target environment or written as benchmarks instead of brittle limits.

## References

- Pytest Documentation: https://docs.pytest.org/
- unittest.mock Reference: https://docs.python.org/3/harness/github-copilot/unittest.mock.html
- Azure Functions Testing: https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python#unit-testing
- Dataverse SDK Examples: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/tree/main/examples
