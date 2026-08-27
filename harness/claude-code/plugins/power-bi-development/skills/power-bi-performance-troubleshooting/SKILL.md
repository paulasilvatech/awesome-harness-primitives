---
name: power-bi-performance-troubleshooting
description: >-
  Diagnose and resolve Power BI performance issues across semantic models, reports, DAX, refresh,
  DirectQuery, gateways, and Fabric or Premium capacity. Use this skill when asked to troubleshoot
  slow Power BI reports, page loading, visual interactions, query execution, model refresh,
  capacity pressure, or gateway bottlenecks.
---

<!-- Generated from harness/github-copilot/plugins/power-bi-development/skills/power-bi-performance-troubleshooting/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power BI performance troubleshooting

Turn reported Power BI symptoms and available metrics into a scoped diagnosis, ranked root causes, concrete fixes, and before/after validation evidence.

## When to invoke

- "Troubleshoot this slow Power BI report."
- "Why is this Power BI page taking more than 10 seconds to load?"
- "Diagnose DAX and model performance bottlenecks."
- "Find why our refresh or DirectQuery queries are timing out."
- "Analyze Fabric capacity, gateway, or Premium performance pressure."

## Source evidence

Use the symptoms, affected reports/models, current performance metrics, environment and configuration details, previous troubleshooting attempts, business requirements, and constraints. If the user has no metrics, collect a baseline first rather than guessing.

## Targets and symptoms

| Metric or symptom | Target or threshold | Investigate first |
| --- | --- | --- |
| Page load times | Target `<10 seconds`; alert when `>15 seconds` | Performance Analyzer, visual count, default filters, slow DAX |
| Visual interaction response | Target `<3 seconds` | Cross-filtering, slicers, custom visuals, high-cardinality filters |
| Query execution times | Target `<30 seconds`; alert when `>45 seconds` | DAX Studio, Storage engine vs. formula engine, DirectQuery source plans |
| Capacity CPU | Investigate when `>70% sustained`; alert when `>80% for >10 minutes` | Fabric Capacity Metrics App, query volume, concurrency, workload mix |
| Memory utilization | Alert when `>90%` or memory pressure warnings appear | Model size, high-cardinality columns, refresh overlap, capacity scale |
| Model refresh duration | Varies by model size; compare against baseline | Incremental refresh, source performance, gateway, transformations |
| User impact | All users vs. specific users; specific times vs. consistently | Capacity, geography, network, permissions, report-specific design |

Use `Report/model` as the shorthand label when the evidence spans both artifacts, and call out slow-loading pages separately from slow interactions.

## Procedure

1. Classify the issue: model loading/refresh performance, report page loading performance, visual interaction responsiveness, query execution speed, capacity resource constraints, or data source connectivity issues.
2. Scope the blast radius: all users vs. specific users, specific times vs. consistently, specific reports vs. all reports, certain data filters vs. all scenarios.
3. Collect the baseline: page load times, visual interaction response, query execution times, model refresh duration, memory and CPU utilization, and concurrent user load.
4. Diagnose from the closest layer to the symptom: report visuals, DAX, model architecture, storage mode, data source, gateway, network, then capacity.
5. Apply the lowest-risk fixes first, measure again, and escalate to advanced model redesign, aggregation, or infrastructure scaling only when evidence supports it.
6. Document root cause, changes, before/after metrics, validation, monitoring, and follow-up recommendations.

For by-step reproduction notes, list the exact interactions that cause the slowdown before proposing fixes.

## Diagnostic criteria

### Model performance

- [ ] Model size and complexity, relationship design and cardinality, and storage mode configuration (`Import`, `DirectQuery`, `Composite`) are reviewed.
- [ ] Legacy shorthand `Import/DirectQuery/Composite` is expanded into specific storage-mode evidence.
- [ ] Data types, compression efficiency, calculated columns vs. measures, and Date table implementation are checked.
- [ ] Common issues are flagged: unnecessary columns/rows, many-to-many relationships, bidirectional filters, high-cardinality text columns, excessive calculated columns, missing or improper Date tables, and poor data type selections.

### DAX performance

- [ ] Measures avoid repeated calculations by using `VAR` and `RETURN` where values are reused.
- [ ] `DIVIDE` is used for safe division and error handling instead of manual fragile division.
- [ ] Context transition overhead, iterator function optimization, filter context complexity, nested `CALCULATE`, inefficient time intelligence, and `FILTER()` used as a filter argument are reviewed.

```dax
Sales Growth =
VAR CurrentMonth = [Total Sales]
VAR PreviousMonth = CALCULATE([Total Sales], PREVIOUSMONTH('Date'[Date]))
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth)
```

### Report design

- [ ] Pages target 6-8 visuals maximum unless evidence shows acceptable performance.
- [ ] Drill-through, bookmarks, default filters, slicer design, cross-filtering configuration, visual interactions, custom visuals, and mobile layout are reviewed.
- [ ] High-cardinality slicers and resource competition from too many visuals are treated as likely bottlenecks.

### Infrastructure and capacity

- [ ] Capacity utilization, query volume, workload distribution, network bandwidth, data source performance, gateway configuration, concurrent user patterns, and geographic distribution are reviewed.
- [ ] Fabric Capacity Metrics App or Premium Capacity Monitoring evidence is used for CPU, memory, refresh, user activity, and query queuing trends.
- [ ] Gateway optimization considers dedicated gateway clusters, load balancing configuration, connection optimization, and performance monitoring.

## Tools and techniques

| Tool | Use it to | Evidence to capture |
| --- | --- | --- |
| Performance Analyzer | Record visual refresh times and identify slowest visuals or operations | Duration by visual, DAX query vs. visual rendering time, exported results |
| DAX Studio | Analyze advanced DAX behavior | Total duration, formula engine duration, storage engine duration, scan count, memory usage patterns, query execution plans, server timings |
| Fabric Capacity Metrics App | Diagnose shared resource pressure | CPU and memory utilization trends, query volume and patterns, refresh performance, user activity, resource bottlenecks |
| Premium Capacity Monitoring | Assess capacity history | Threshold alerts, historical trend analysis, workload distribution |

## Fix patterns

| Area | Immediate fixes | Advanced solutions |
| --- | --- | --- |
| Model | Remove unused columns and tables; optimize data types; replace calculated columns with measures; implement star schema relationships; use incremental refresh | Pre-aggregation, aggregation tables, compression optimization, complete redesign |
| Report | Reduce visuals to 6-8 per page; apply filters early; disable unnecessary cross-filtering; use drill-through and bookmarks | Restructure pages, optimize custom visuals, load test realistic concurrent users |
| DirectQuery | Maximize query folding, add database indexes, reduce cross-source relationships | Aggregation table implementation, connection pooling configuration, strategic Composite models |
| Capacity | Reschedule refreshes, reduce query concurrency, monitor thresholds | Vertical scaling, horizontal workload distribution, geographic optimization, load balancing |

## Troubleshooting workflows

| Workflow | Timebox | Checklist |
| --- | --- | --- |
| Quick Win Checklist | 30 minutes | Check Performance Analyzer; reduce visuals; apply default filters; disable unnecessary cross-filtering; check missing relationships causing cross-joins; verify storage modes; optimize top 3 slowest DAX measures |
| Comprehensive Analysis | 2-4 hours | Review model architecture; optimize DAX with variables and efficient patterns; restructure report design; analyze data source performance; assess capacity; review user access patterns; test mobile; load test concurrent users |
| Strategic Optimization | 1-2 weeks | Redesign data model if necessary; implement aggregations; plan infrastructure scaling; set monitoring and alerting; train users on efficient usage; establish performance governance and continuous optimization |

## Monitoring cadence

| Frequency | Actions |
| --- | --- |
| Weekly | Review performance dashboards, capacity utilization trends, slow-running queries, user feedback, and issues |
| Monthly | Run comprehensive performance analysis, model optimization review, capacity planning, and user training needs assessment |
| Quarterly | Perform strategic performance review, technology update assessment, scaling requirements review, and governance updates |

## Output template

```markdown
## Power BI performance troubleshooting report — <report/model>

**Status:** diagnosed | partially diagnosed | blocked
**Symptom:** <page load, visual interaction, query, refresh, capacity, gateway, or source issue>
**Scope:** <users/reports/times/filters affected>

### Baseline
| Metric | Current | Target | Evidence |
| --- | --- | --- | --- |
| Page load time | <value> | <10 seconds | <Performance Analyzer/export/user timing> |
| Visual response | <value> | <3 seconds | <evidence> |
| Query execution | <value> | <30 seconds | <DAX Studio/source evidence> |
| Capacity CPU/memory | <value> | <threshold> | <Fabric/Premium evidence> |

### Findings
| # | Layer | Root cause | Evidence | Fix | Expected impact |
| --- | --- | --- | --- | --- | --- |
| 1 | DAX | <issue> | <measure/timing> | <change> | <impact> |
| 2 | Model | <issue> | <metadata/timing> | <change> | <impact> |

### Resolution documentation
- **Changes implemented:** <optimization changes>
- **Before/after metrics:** <measured improvement>
- **Validation and testing completed:** <checks>
- **Monitoring setup:** <ongoing health checks>
- **Follow-up recommendations:** <next steps>
```

## Quality gate

- [ ] Issue classification, scope assessment, and baseline metrics are stated before root cause claims.
- [ ] Performance Analyzer, DAX Studio, Fabric Capacity Metrics App, Premium Capacity Monitoring, or equivalent evidence is cited when available.
- [ ] Findings distinguish model, DAX, report, data source, gateway, network, and capacity causes.
- [ ] Recommendations include immediate fixes and escalation criteria for advanced solutions.
- [ ] Before/after performance metrics and monitoring follow-up are documented.
- [ ] The output follows `## Output template` exactly.
