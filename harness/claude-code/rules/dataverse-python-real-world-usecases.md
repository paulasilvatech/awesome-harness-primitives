---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-real-world-usecases.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for real-world Python Dataverse SDK migration, synchronization, data quality, enrichment, reporting, workflow automation, and scheduled jobs.

# Dataverse SDK for Python Conventions — Real-World Automation Use Cases

These instructions apply to Python code that uses the PowerPlatform Dataverse client for migration, synchronization, reporting, enrichment, bulk workflow, or scheduled automation. They are authoritative for Dataverse client setup, table operations, paging, batching, reconciliation, data-quality checks, export shape, Azure Functions scheduling, and error handling in matched Python files; stricter project security, identity, data-retention, and deployment instructions win when they define narrower production constraints.

## Client Setup, Authentication, and Configuration

Create Dataverse clients through `DataverseClient` with `DefaultAzureCredential` and keep organization URLs explicit at the boundary of the application. Use `DataverseConfig` for SDK configuration instead of global toggles.

```python
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()
cfg.logging_enable = False

client = DataverseClient(
    base_url="https://myorg.crm.dynamics.com",
    credential=DefaultAzureCredential(),
    config=cfg,
)
```

Use `DataverseError` for SDK failures, Python `logging` for durable operational logs, and `print` only in local scripts or sample utilities. Do not embed real API keys; placeholders such as `your-api-key` and masked headers such as `Authorization: ******` must stay placeholders.

## Migration and Reconciliation

Model migrations as extract, transform, load, and reconcile. Preserve source identifiers in Dataverse so every migrated record can be traced back to the source system.

```
Legacy System → Staging Database → Dataverse
    (Extract)    (Transform)        (Load)
```

| Stage | Convention |
| --- | --- |
| Extract | Use `pd.read_sql(query, legacy_db_connection)` or an equivalent source adapter. |
| Transform | Map source columns such as `company_name`, `phone`, `website`, `annual_revenue`, `employees`, and `legacy_id` to Dataverse payload fields. |
| Field limits | Enforce field constraints during transform, for example `name` sliced to 100 characters. |
| Reconciliation | Store `new_sourcecompanyid` and `new_importsequencenumber` so source rows can be merged with Dataverse IDs. |
| Batch size | Default to conservative batches such as `batch_size=200`; tune deliberately, for example `batch_size=300`, when throttling and payload size are understood. |
| Throttling | Add short pauses such as `time.sleep(0.5)` between batches when the API or tenant is rate-sensitive. |
| Metrics | Report `total_source`, `migrated`, `failed`, and `success_rate`. |

Use `client.create("account", batch)` for batch creation, extend `success_records` with returned IDs, extend `failed_records` with failed payloads, and calculate success rates from reconciled records rather than from attempted sends alone.

## Data Quality and Deduplication

Build quality agents that page through data, compute deterministic match keys, and make merge operations explicit.

| Operation | Convention |
| --- | --- |
| Duplicate search | Use `client.get(table_name, select=match_fields, top=10000)` and compare normalized values from fields such as `name` and `emailaddress1`. |
| Duplicate record shape | Return `original`, `duplicate`, and `fields_matched` so reviewers know why records matched. |
| Merge | Read the duplicate, copy only missing mapped fields to the primary, call `client.update(table_name, primary_id, updates)`, then call `client.delete(table_name, duplicate_id)` only when merge confidence is high. |
| Quality report | Include `table`, `total_records`, `null_values`, `duplicates`, and `completeness_score`. |
| Completeness | Calculate per-field `null_count` and percentage completeness before deriving an average completeness score. |

Guard merge utilities against undefined variables and accidental deletes: load both the primary and duplicate records before comparing fields, and do not delete the duplicate if the primary update fails.

## Enrichment and External Integrations

Keep enrichment idempotent by selecting only records missing enrichment fields, limiting each run, and catching per-record failures.

| Scenario | Dataverse pattern |
| --- | --- |
| Account industry enrichment | Query `account` with `select=["accountid", "name", "websiteurl"]`, `filter="new_industrydata eq null"`, and `top=500`; update `new_industrydata`. |
| Contact social profile enrichment | Query `contact` with `select=["contactid", "fullname", "emailaddress1"]`, `filter="new_linkedinurl eq null"`, and `top=500`; update `new_linkedinurl` and `new_twitterhandle`. |
| External API calls | Use `requests.get` with `params` and masked `Authorization`; handle non-200 responses by returning `None` or `{}` as appropriate. |

Do not let one failed enrichment stop the whole run. Log failures with enough context, such as the account `name` or contact `fullname`, without logging secrets.

## Reporting and Export

Export reports by paging Dataverse records into lists, converting to `pandas` DataFrames, and writing stable output files.

| Report | Convention |
| --- | --- |
| Sales summary | Export `account` fields `accountid`, `name`, `revenue`, `numberofemployees`, `createdon`, and `modifiedon` where `statecode eq 0`, ordered by `revenue desc`. |
| Opportunity export | Export `opportunity` fields `opportunityid`, `name`, `estimatedvalue`, `statuscode`, `parentaccountid`, and `createdon`. |
| Excel sheets | Use `pd.ExcelWriter(output_file)` with sheets named `Accounts`, `Opportunities`, and `Summary`. |
| Summary metrics | Include `Total Accounts`, `Total Opportunities`, `Total Revenue`, and `Export Date`. |
| Activity log | Export `activitypointer` fields `activityid`, `subject`, `activitytypecode`, `createdon`, and `ownerid` for recent records to `activity_log_%Y%m%d.csv`. |
| Time windows | Use timezone-aware timestamps such as `pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=days_back)`. |

Use `to_excel(..., index=False)` and `to_csv(..., index=False)` so reports are clean for business users.

## Bulk Workflow Automation

Represent Dataverse option-set values with explicit enums when the code owns the mapping.

```python
from enum import IntEnum

class AccountStatus(IntEnum):
    PROSPECT = 1
    ACTIVE = 2
    CLOSED = 3
```

For inactive-account workflows, query active `account` records with fields such as `accountid` and `name`, filter by `modifiedon lt ... and statecode eq 0`, collect IDs, and bulk update `statecode` to `AccountStatus.CLOSED`. For opportunity workflows, query `opportunityid` and `estimatedvalue`, ignore closed records with `statuscode ne 7`, compute stage IDs such as `1` for Qualification, `2` for Proposal, and `3` for Proposal Review, then call `client.update("opportunity", ids, updates)`.

## Scheduled Azure Functions Jobs

Scheduled jobs should be small wrappers around reusable classes, not copies of migration logic. In Azure Functions, keep the timer entry point in `function_app.py`, use `func.FunctionApp()`, decorate with `@app.schedule_trigger(schedule="0 0 * * *")` for daily midnight jobs, accept `func.TimerRequest`, check `timer.past_due`, and delegate to a reusable function such as `main(timer)`.

Use `logging.info` for start, completion, and reconciliation metrics, `logging.error` for failure, and re-raise exceptions so the platform records failed executions.

## Starter Application Shape

A reusable Dataverse application class should keep client creation private and expose narrow table methods.

| Method | Convention |
| --- | --- |
| `_create_client` | Build `DataverseClient` with `base_url`, `DefaultAzureCredential`, and optional `DataverseConfig`. |
| `create_account` | Send `payload = {"name": name}` plus optional `telephone1`; return the first ID from `client.create("account", payload)`. |
| `get_accounts` | Use `filter`, `select=["accountid", "name", "telephone1", "createdon"]`, `orderby=["createdon desc"]`, and `top`. |
| `update_account` | Call `client.update("account", account_id, kwargs)` and log the updated identifier. |
| Main guard | Keep sample usage under `if __name__ == "__main__":`. |

## Identifier Inventory

Preserve these table names, fields, classes, methods, and placeholders when compressing examples: `AccountStatus`, `ACTIVE`, `CLOSED`, `DataEnrichmentAgent`, `DataMigrationPipeline`, `DataQualityAgent`, `DataverseApp`, `DataverseClient`, `DataverseConfig`, `DataverseError`, `DefaultAzureCredential`, `FunctionApp`, `IntEnum`, `PROSPECT`, `ReportExporter`, `TimerRequest`, `account`, `accountid`, `activity_log_%Y%m%d.csv`, `activityid`, `activitypointer`, `activitytypecode`, `annual_revenue`, `api_key`, `base_url`, `batch_size`, `client.create`, `client.delete`, `client.get`, `client.update`, `company_name`, `completeness_score`, `createdon`, `days_back`, `days_no_activity`, `duplicate_id`, `emailaddress1`, `estimatedvalue`, `external_api_key`, `failed_records`, `filter`, `from_date`, `fullname`, `generate_quality_report`, `get_accounts`, `legacy_connection`, `legacy_db_connection`, `legacy_id`, `logging_enable`, `mark_accounts_as_inactive_if_no_activity`, `match_fields`, `modifiedon`, `new_importsequencenumber`, `new_industrydata`, `new_linkedinurl`, `new_sourcecompanyid`, `new_twitterhandle`, `null_count`, `numberofemployees`, `opportunity`, `opportunityid`, `orderby`, `org_url`, `output_file`, `parentaccountid`, `pd.DataFrame`, `pd.ExcelWriter`, `pd.read_sql`, `primary_id`, `reconcile_migration`, `sales_report.xlsx`, `schedule_trigger`, `scheduled_migration_job.py`, `select`, `source_data`, `statecode`, `statuscode`, `success_records`, `telephone1`, `top`, `total_source`, `transform_accounts`, `update_opportunity_status_based_on_amount`, `websiteurl`, and `your-api-key`.

Additional preserved vocabulary from the baseline: `FROM`, `INFO`, `SELECT`, `accounts_to_deactivate`, `all_accounts`, `all_fields`, `https://api.example.com/industry`, `https://api.example.com/social`, `api.example.com/industry`, `api.example.com/social`, `avg_completeness`, `created_accounts`, `created_df`, `df_accounts`, `df_opportunities`, `enrich_accounts_with_industry_data`, `enrich_contacts_with_social_profiles`, `enriched_count`, `export_activity_log`, `export_sales_summary`, `extract_from_legacy`, `filter_expr`, `find_potential_duplicates`, `inactive_accounts`, `left_on`, `load_to_dataverse`, `merge_records`, `migration_job`, `report_file`, `right_on`, `sheet_name`, `source_field`, `status_code`, `target_field`, `usr/bin/env`, `BulkWorkflow`.

## Good / Bad Examples

The examples below illustrate safe batch migration with source reconciliation.

**Good:**

```python
try:
    ids = client.create("account", batch)
    success_records.extend(ids)
    time.sleep(0.5)
except DataverseError as exc:
    failed_records.extend(batch)
    logger.error("Dataverse batch failed: %s", exc.message)
```

Why: The batch records successes, captures failed payloads for retry, throttles conservatively, and logs through a durable logger.

**Bad:**

```python
ids = client.create("account", payloads)
print(ids)
```

Why: The whole migration is sent as one unbounded operation, failures cannot be reconciled to source rows, and operational logs are not durable.

## Conventions

| Rule | Rationale |
| --- | --- |
| Authenticate `DataverseClient` with `DefaultAzureCredential` and explicit `base_url` | Runtime identity and target tenant stay clear. |
| Preserve source IDs such as `new_sourcecompanyid` and `new_importsequencenumber` during migration | Reconciliation, retry, and audit remain possible. |
| Batch Dataverse writes and track `success_records` and `failed_records` | Large migrations survive partial failures. |
| Page `client.get` results before DataFrame or merge work | Large tables do not disappear behind a single partial response. |
| Merge duplicates only after explicit field mapping and successful primary update | Deduplication does not destroy recoverable data. |
| Select only records missing enrichment values | Repeated enrichment jobs remain idempotent. |
| Use timezone-aware timestamps for report windows | Exports are reproducible across hosts. |
| Keep Azure Functions timer triggers as wrappers around reusable classes | Scheduled jobs stay testable outside Azure Functions. |
| Catch `DataverseError` separately from generic exceptions | SDK failures preserve useful message details. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `DefaultAzureCredential` and approved environment identity | Hard-code passwords, tokens, or real API keys. |
| Transform fields before loading, including length and type conversions | Send raw legacy rows directly to Dataverse. |
| Use `top`, `select`, `filter`, and `orderby` intentionally | Query entire tables without bounding or shaping results. |
| Store reconciliation fields for migrated rows | Depend on names alone to match migrated records. |
| Use `pd.ExcelWriter` and named sheets for business reports | Dump ambiguous CSVs when multi-sheet reporting is required. |
| Use `IntEnum` for owned option-set mappings | Scatter unexplained magic status values through workflows. |
| Re-raise scheduled-job exceptions after logging | Swallow Azure Functions failures and make monitoring inaccurate. |
| Keep external API authorization masked in examples | Commit live `Authorization` headers or API keys. |

## Checklist Before Opening a PR

- [ ] Dataverse clients use `DataverseClient`, `DefaultAzureCredential`, explicit `base_url`, and optional `DataverseConfig`.
- [ ] Migration payloads preserve source identifiers and enforce known Dataverse field constraints.
- [ ] Create, update, and delete operations are batched or bounded and track successes and failures.
- [ ] Queries use explicit `select`, `filter`, `orderby`, and `top` where applicable.
- [ ] Deduplication code loads required records, checks merge confidence, and avoids deleting when update fails.
- [ ] Enrichment code is idempotent and handles per-record external API failures.
- [ ] Reports use stable sheet names or file names and timezone-aware date filters.
- [ ] Azure Functions timer jobs log start, completion, and failure, then re-raise failures.
- [ ] No real API keys, tokens, or unmasked authorization headers are present.

## References

- Dataverse Data Migration: https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/data-migration/workflow-complex-data-migration
- Working with Data (SDK): https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data
- SDK Examples on GitHub: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/tree/main/examples
- Placeholder industry enrichment endpoint from examples: https://api.example.com/industry
- Placeholder social enrichment endpoint from examples: https://api.example.com/social
