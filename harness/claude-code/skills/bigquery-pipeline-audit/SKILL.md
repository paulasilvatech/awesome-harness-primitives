---
name: bigquery-pipeline-audit
description: >-
  Audit Python and BigQuery pipeline scripts for cost exposure, dry-run safety, bounded backfills,
  query pruning, idempotent writes, and observability. Use this skill when reviewing client.query,
  load_table_from_*, extract_table, copy_table, DDL/DML query jobs, external API calls, LLM calls,
  or storage writes before production use.
---

<!-- Generated from harness/github-copilot/skills/bigquery-pipeline-audit/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# BigQuery pipeline audit

Review a Python + BigQuery pipeline, inventory every billable or external side effect, and return a risk-ranked production-readiness report with exact functions, line locations, and minimal fixes.

## When to invoke

- "Audit this BigQuery pipeline before it runs in production."
- "Check this Python script for BigQuery cost and rerun safety."
- "Review these client.query and load_table_from_* calls."
- "Find runaway backfill, DDL/DML, extract_table, or copy_table risks."
- "Is this BigQuery job loop safe and observable?"

## Cost exposure

Locate every BigQuery job trigger and every external side effect. Treat `client.query`, `load_table_from_*`, `extract_table`, `copy_table`, DDL/DML via query, external APIs, LLM calls, and storage writes as billable or mutating operations.

| Check | Required evidence | Fail condition | Minimal fix |
| --- | --- | --- | --- |
| Job inventory | Function name, line, job type, SQL or table scope | Any BigQuery job trigger is missing from the report | Add a complete trigger table before judging risk. |
| Loop and retry context | Whether the call is inside a loop, retry block, async gather, or callback | Worst-case count cannot be bounded | Compute `dates x entities x retries x concurrent tasks`. |
| Query scan cap | `QueryJobConfig.maximum_bytes_billed` on every `client.query` | Missing `maximum_bytes_billed` | Add a conservative cap and surface cap failures. |
| Non-query job cap | Load, extract, and copy job scope is bounded and counted against `MAX_JOBS` | Unlimited table list, date list, or file list | Enforce `MAX_JOBS` before submitting jobs. |
| Duplicate work | Same SQL and params run more than once in one run | Repeated identical queries | Hash SQL plus params and cache into a temp table. |

Flag immediately when any BigQuery query runs once per date or once per entity in a loop, worst-case BigQuery job count exceeds 20, or `maximum_bytes_billed` is missing on any `client.query` call.

## Execution modes

Verify a `--mode` flag exists with at least `dry_run` and `execute` options.

| Mode rule | Required behavior |
| --- | --- |
| `dry_run` | Print the plan and estimated scope with zero billed BigQuery execution, zero external API calls, zero LLM calls, and zero storage writes. BigQuery dry-run estimation through job config is allowed. |
| `execute` | Perform side effects only after mode is explicit. |
| Production confirmation | Require `--env=prod --confirm` for production execution. |
| Safe default | Production must not be the default environment. |

If the flags are missing, propose a minimal `argparse` patch with safe defaults instead of redesigning the CLI.

## Backfill and loop design

Hard fail when the script runs one BigQuery query per date or per entity in a loop. Date-range backfills must use one of these patterns:

| Pattern | Use when | Required guard |
| --- | --- | --- |
| Set-based query | The date range can be represented in SQL | Use `GENERATE_DATE_ARRAY` and one partition-pruned join. |
| Staging table | The date/entity list comes from Python or an API | Load all keys once, then run one join query. |
| Explicit chunks | The source enforces batch limits | Set a hard `MAX_CHUNKS` cap and stop when exceeded. |

Default date ranges should be bounded, usually no more than 14 days without an `--override`. A crash in the middle of a run must be safe to rerun without double-writing. Backdated simulations must read time-consistent data using `FOR SYSTEM_TIME AS OF`, partitioned as-of tables, or dated snapshot tables; flag any read from a `latest` or unversioned table in backdated mode.

## Query safety and scan size

For each query, check the SQL shape before reviewing style.

| Risk | Bad pattern | Required correction |
| --- | --- | --- |
| Partition pruning disabled | `DATE(ts)`, `CAST(partition_col AS ...)`, or a function around the partition column | Filter the raw partition column directly. |
| Unbounded projection | `SELECT *` | Select only columns used downstream. |
| Join explosion | Many-to-many keys or unscoped joins | Prove uniqueness, pre-aggregate, or add join predicates. |
| Full-scan expensive functions | `REGEXP`, `JSON_EXTRACT`, or UDFs before partition filtering | Filter partitions first, then apply expensive expressions. |

Provide a concrete SQL fix for every failing query.

## Safe writes and idempotency

Identify every write operation and flag plain `INSERT` or append with no deduplication logic.

| Write pattern | Acceptable when | Required key rule |
| --- | --- | --- |
| `MERGE` | A deterministic business key exists | Key examples: `entity_id + date + model_version`. |
| Staging table then swap or merge | The run needs isolation or validation before publish | Stage table is scoped to the run and cleaned up. |
| Append-only plus dedupe view | Historical writes are intentional | Use `QUALIFY ROW_NUMBER() OVER (PARTITION BY <key>) = 1`. |

Check whether reruns create duplicate rows, whether `WRITE_TRUNCATE` or `WRITE_APPEND` is intentional and documented, and whether `run_id` is incorrectly part of the uniqueness key. Store `run_id` as metadata unless multi-run history is explicitly required.

## Observability

Failures must raise and abort; no silent `except: pass` and no warn-only failure path for a mutating operation. Each BigQuery job log should include job ID, bytes processed or billed when available, slot milliseconds, and duration. The run summary must include `run_id, env, mode, date_range, tables written, total BQ jobs, total bytes`, and `run_id` must be present on every log line.

If `run_id` is missing, propose this one-line fix:

```python
run_id = run_id or datetime.utcnow().strftime('%Y%m%dT%H%M%S')
```

## Criteria

### Blocking failures

- [ ] Any `client.query` call lacks `QueryJobConfig.maximum_bytes_billed`.
- [ ] Worst-case BigQuery job count is greater than 20 or cannot be calculated.
- [ ] A backfill runs one query per date or one query per entity.
- [ ] Production can execute without `--env=prod --confirm`.
- [ ] A rerun can double-write records or corrupt final tables.

### Review completeness

- [ ] Every BigQuery job trigger and external call is listed with function and line evidence.
- [ ] Every query has partition, projection, join, and expensive-operation checks.
- [ ] Every write operation has an idempotency strategy and dedup key.
- [ ] Every failure path and end-of-run summary is observable through logs or metrics.

## Audit vocabulary

Preserve these review labels from the source checklist when reporting: `COST EXPOSURE`, `DRY RUN AND EXECUTION MODES`, `BACKFILL AND LOOP DESIGN`, `QUERY SAFETY AND SCAN SIZE`, `SAFE WRITES AND IDEMPOTENCY`, and `OBSERVABILITY`. Use the terms `date-range`, `set-based`, `mid-run`, `re-run`, and `many-to-many` exactly when they describe the risk. Include SQL evidence such as `CAST(...)` when a partition filter blocks pruning.

## Output template

```markdown
## BigQuery pipeline audit - <file or module>

**Verdict:** PASS | FAIL
**Scope reviewed:** <files, functions, and entry points>

### A. Cost exposure
| Trigger | Location | Loop/retry context | Worst-case count | Cap present | Finding |
| --- | --- | --- | --- | --- | --- |
| `<client.query or job>` | `<function:line>` | `<context>` | `<count>` | `<yes/no>` | `<risk>` |

### B. Dry run and execution modes
<pass/fail with evidence and minimal argparse patch if needed>

### C. Backfill and loop design
<pass/fail with backfill pattern, MAX_CHUNKS/MAX_JOBS evidence, and rerun safety>

### D. Query safety and scan size
| Query | Evidence | Risk | SQL fix |
| --- | --- | --- | --- |

### E. Safe writes and idempotency
| Write | Disposition | Dedup key | Rerun outcome | Recommendation |
| --- | --- | --- | --- | --- |

### F. Observability
<job ID, bytes, slot milliseconds, duration, run_id, and run summary findings>

### Patch list
1. `<highest-risk minimal patch with exact function>`
2. `<next patch>`

### Top 3 cost risks
1. `<rough estimate, for example 90 dates x 3 retries = 270 BigQuery jobs>`
```

## Quality gate

- [ ] The report states `PASS` or `FAIL` with section-specific reasons for A through F.
- [ ] Every billable BigQuery operation and external call has exact location evidence.
- [ ] The worst-case job count calculation is explicit and compares against 20, `MAX_JOBS`, and `MAX_CHUNKS` where present.
- [ ] Missing `maximum_bytes_billed`, unsafe production defaults, and row-by-row backfills are treated as blocking failures.
- [ ] Every SQL recommendation preserves partition pruning and avoids `SELECT *`.
- [ ] Every write recommendation names a deterministic deduplication key and explains `run_id` usage.
- [ ] The patch list is ordered by production risk and avoids broad rewrites.
