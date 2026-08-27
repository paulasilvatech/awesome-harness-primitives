---
name: aws-cloudwatch-investigation
description: >-
  Investigate AWS production incidents with CloudWatch Logs Insights, Metrics, Alarms, CloudTrail
  correlation, blast-radius narrowing, metric math, and incident timelines. Use when the user asks
  to debug CloudWatch alarms, query Logs Insights, correlate alarms to deployments, find Lambda
  cold starts, OOMs, timeouts, throttling, or reconstruct an AWS incident timeline.
---

<!-- Generated from harness/github-copilot/skills/aws-cloudwatch-investigation/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AWS CloudWatch investigation

Take an AWS incident signal, transform it into scoped CloudWatch Logs, Metrics, Alarm, and CloudTrail evidence, and return a timeline, blast-radius conclusion, likely root event, and next validation steps.

## When to invoke

- "Investigate this CloudWatch alarm."
- "Write Logs Insights queries for this error spike."
- "Did a deployment cause this AWS incident?"
- "Narrow the blast radius for these Lambda failures."
- "Build an incident timeline from CloudWatch and CloudTrail."

## Prerequisites and context

- The user must provide or authorize access to the AWS account, region, log groups, alarm names, service namespace, and incident window.
- Prefer read-only investigation. Do not change alarms, dashboards, retention, Lambda memory, ECS services, or infrastructure unless separately asked.
- Use event timestamps, not ingestion timestamps, when comparing CloudWatch Logs, CloudWatch Metrics, CloudWatch Alarms, CloudTrail, and AWS Health.

## Logs Insights query patterns

| Situation | Query |
| --- | --- |
| Error spike detection | `fields @timestamp, @message, @logStream\n| filter @message like /(?i)(error|exception|fatal|critical)/\n| stats count(*) as errorCount by bin(5m), @logStream\n| sort errorCount desc\n| limit 20` |
| P99 latency by operation | `fields @timestamp, @duration, operation\n| filter ispresent(@duration)\n| stats avg(@duration) as avgMs, pct(@duration, 50) as p50Ms, pct(@duration, 95) as p95Ms, pct(@duration, 99) as p99Ms, count(*) as invocations by operation\n| sort p99Ms desc\n| limit 15` |
| Lambda cold starts | `fields @timestamp, @duration, @initDuration, @memorySize, @maxMemoryUsed\n| filter ispresent(@initDuration)\n| stats count(*) as coldStarts, avg(@initDuration) as avgInitMs, max(@initDuration) as maxInitMs, avg(@duration) as avgDurationMs by bin(5m)\n| sort @timestamp desc` |
| OOM events | `fields @timestamp, @message, @logStream, @memorySize, @maxMemoryUsed\n| filter @message like /Runtime exited|out of memory|OOMKilled|Cannot allocate memory|MemoryError/\n| stats count(*) as oomEvents by @logStream, bin(10m)\n| sort oomEvents desc\n| limit 10` |
| Memory trend before OOM | `fields @timestamp, @maxMemoryUsed, @memorySize\n| filter ispresent(@maxMemoryUsed)\n| stats max(@maxMemoryUsed / @memorySize * 100) as peakMemPct, avg(@maxMemoryUsed / @memorySize * 100) as avgMemPct by bin(5m)\n| sort @timestamp desc` |
| Timeout detection | `fields @timestamp, @duration, @logStream, @requestId\n| filter @message like /Task timed out/ or @duration > 28000\n| stats count(*) as timeouts by @logStream, bin(5m)\n| sort timeouts desc` |
| First error timeline | `fields @timestamp, @message\n| filter @message like /ERROR|WARN|timeout|refused|denied/\n| stats earliest(@timestamp) as firstSeen, latest(@timestamp) as lastSeen, count(*) as occurrences by @message\n| sort firstSeen asc\n| limit 20` |

## Deployment correlation

Use the alarm transition timestamp as the anchor. Query CloudTrail for deployment-related events in `[alarm_time - 30min, alarm_time]`:

```sql
SELECT eventTime, eventName, userIdentity.arn, requestParameters
FROM <event-data-store-id>
WHERE eventTime > '<alarm_time_minus_30m>'
  AND eventTime < '<alarm_time>'
  AND eventName IN (
    'UpdateFunctionCode', 'UpdateFunctionConfiguration',
    'UpdateService', 'CreateDeployment', 'RegisterTaskDefinition',
    'CreateChangeSet', 'ExecuteChangeSet',
    'StartPipelineExecution', 'PutImage'
  )
ORDER BY eventTime DESC
```

| Correlation strength | Evidence |
| --- | --- |
| Strong | Same service/resource, completed within 15 minutes before alarm, CI/CD actor such as an assumed GitHub Actions deploy role, and alarm was `OK` in the previous deployment cycle. |
| Medium | Same account or service but partial resource match, nearby timing, or ambiguous actor. |
| Weak | Only temporal proximity, human hotfix, missing prior healthy cycle, or simultaneous environmental changes. |
| Not correlated | No deploy/config/image/change-set event before the first symptom. |

Strengthen the correlation by checking canary or synthetic monitor failures, scaling events, config changes, and whether any other environmental change happened in the same window.

## Blast-radius decision tree

```
START
  |
  v
[1] ACCOUNT — Which account(s) show the alarm?
  |  - Multi-account: suspect shared service such as SSO, networking, or deployment pipeline
  |  - Single account: proceed to Region
  v
[2] REGION — Which region(s) are affected?
  |  - Multi-region: suspect global service such as IAM, Route53, or S3 global behavior
  |  - Single-region: proceed to Service
  v
[3] SERVICE — Which service namespace shows degradation?
  |  - Multiple services: suspect VPC, NAT, DNS, IAM, shared database, cache, or external API
  |  - Single service: proceed to Operation
  v
[4] OPERATION — Which API action, function, stage, resource, method, ECS service, or task definition is failing?
  |  - All operations: suspect service-level throttling or quota
  |  - Specific operation: proceed to Resource
  v
[5] RESOURCE — Which Function ARN, Task ID, DB instance identifier, or other resource instance is the investigation target?
```

When multiple services are affected, investigate in this order: VPC/Networking (`NAT Gateway ErrorPortAllocation`, packet drops, DNS), IAM/STS (`ThrottlingException` on `AssumeRole`, token vending latency), downstream dependency, shared deployment pipeline, then AWS Health Dashboard and Service Health.

## Metric math patterns

| Signal | MetricDataQueries pattern |
| --- | --- |
| Error rate percentage | `errors = AWS/Lambda Errors Sum`, `invocations = AWS/Lambda Invocations Sum`, `error_rate = errors / invocations * 100`, label `Error Rate %`. |
| Latency anomaly | `current_p99 = AWS/Lambda Duration p99` for current window, `baseline_p99 = AWS/Lambda Duration p99` for same window last week, `anomaly_ratio = current_p99 / baseline_p99`, label `Latency vs Baseline (ratio > 2 = anomaly)`. |
| Throttling pressure | Sum `lambda_throttles`, `api_gw_429s` from `AWS/ApiGateway 4XXError`, and `dynamo_throttles` from `AWS/DynamoDB ThrottledRequests` into `throttle_pressure`. |
| Concurrent execution headroom | `concurrent = AWS/Lambda ConcurrentExecutions Maximum`, `headroom = 1000 - concurrent`, label `Remaining Concurrency (account limit 1000)`. |

Replace `TARGET`, `FunctionName`, `ApiName`, and `TableName` with the scoped resource. Treat `1000` as a default example account concurrency limit; use the account's actual quota when known.

## Incident timeline reconstruction

Collect timestamped evidence and sort by event time:

| Source | Query or API | Yields |
| --- | --- | --- |
| CloudWatch Alarms | Alarm history API | State transition times |
| CloudWatch Metrics | `GetMetricData` with 1-minute period | First anomaly datapoint |
| CloudWatch Logs | Logs Insights with `earliest(@timestamp)` | First error occurrence |
| CloudTrail | `LookupEvents` or CloudTrail Lake | Deployment and configuration events |
| AWS Health | `DescribeEvents` | AWS-side incidents |

Root event rule: walk backward from the first symptom to the most recent deploy, config change, scaling event, quota pressure, or external dependency shift that can explain all later symptoms.

## Gotchas

- CloudWatch metric timestamps are end-of-period; a 1-minute datapoint at `14:05` covers `14:04-14:05`.
- CloudTrail can have up to 15-minute delivery delay; use `eventTime`, not ingestion time.
- Log group timestamps depend on agent or SDK flush interval; allow 30-60 seconds of clock skew.
- Alarm state changes include evaluation delay: `periods x evaluation periods`; the anomaly often started earlier.

## Source compatibility terms

Retain these CloudWatch incident terms in investigations and reports: `5/min`, `ALARM`, `AWS/ECS`, `Deployment/change`, `IAM/STS**`, `STRONG`, `StartTime/EndTime`, `VPC/Networking**`, `agent/SDK`, `alarm-to-deployment`, `assumed-role`, `assumed-role/github-actions-deploy/session`, `built-in`, `canary/synthetic`, `github-actions-deploy`, `multi-region`, `payment-processor`, `payments-api`, `service/task`, `single-region`, `stage/resource/method`, `us-east-1`, `EndTime`, `MetricName`, `MetricStat`, `PaymentProcessorErrors`, and `StartTime`.

## Output template

```markdown
## CloudWatch investigation — <alarm, service, or incident>

**Status:** investigating | likely cause found | inconclusive | blocked
**Window:** <start> to <end> UTC
**Scope:** account=<id>, region=<region>, service=<namespace>, resource=<resource>

### Findings
| Time | Source | Evidence | Interpretation |
| --- | --- | --- | --- |
| `<timestamp>` | CloudTrail | `<eventName by actor>` | `<deploy/config/change candidate>` |
| `<timestamp>` | Logs Insights | `<query result>` | `<first symptom or dominant error>` |

### Blast radius
- Account: <single | multiple>
- Region: <single | multiple>
- Service: <single | multiple>
- Operation/resource: <specific target>

### Correlation
**Deployment correlation:** strong | medium | weak | none
**Root event:** <earliest plausible change or unknown>
**Confidence:** high | medium | low

### Queries used
- `<Logs Insights or MetricDataQueries summary>`

### Next checks
- <one concrete validation or mitigation step>
```

## Quality gate

- [ ] Alarm transition time, first symptom time, and investigation window are explicit.
- [ ] Logs, metrics, alarms, CloudTrail, and AWS Health are considered or explicitly marked unavailable.
- [ ] Blast radius is narrowed in account → region → service → operation → resource order.
- [ ] Deployment correlation uses same resource, timing, actor, and prior-health evidence.
- [ ] Metric math names the namespace, metric, dimensions, period, statistic, and expression.
- [ ] Timeline entries use event timestamps and account for metric period, CloudTrail delay, log skew, and alarm evaluation delay.
