---
name: aws-resource-health-diagnose
description: >-
  Diagnose AWS resource health with AWS CLI, CloudWatch metrics, CloudWatch Logs Insights,
  Performance Insights, CloudTrail correlation, severity classification, root cause analysis, and
  remediation plans. Use when the user asks for AWS resource health, issue diagnosis, CloudWatch
  troubleshooting, or remediation for EC2, Lambda, RDS, ECS, ALB, DynamoDB, SQS, or API Gateway.
---

<!-- Generated from harness/github-copilot/plugins/aws-cloud-development/skills/aws-resource-health-diagnose/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AWS resource health diagnosis

Identify a target AWS resource, collect service-specific status, CloudWatch metrics, logs, and related events, classify issues by severity and root cause, then produce immediate, short-term, and long-term remediation steps with validation.

## When to invoke

- "Diagnose this AWS Lambda health issue."
- "Check why this RDS instance is slow."
- "Analyze CloudWatch logs and metrics for this resource."
- "Create a remediation plan for an unhealthy ECS service."
- "Troubleshoot AWS resource health for EC2, ALB, SQS, or DynamoDB."

## Prerequisites and context

- AWS CLI must be configured and authenticated.
- The target resource must be identified by name, type, and optionally region/account.
- CloudWatch logs and metrics should be enabled; if not, report the limitation and recommend enablement.
- Fetch `https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/` when current monitoring guidance is needed.

## Resource discovery

Use the appropriate AWS CLI command for the resource type:

```bash
aws ec2 describe-instances --filters "Name=tag:Name,Values=<name>"
aws lambda get-function --function-name <name>
aws rds describe-db-instances --db-instance-identifier <name>
aws ecs describe-services --cluster <cluster> --services <name>
aws elbv2 describe-load-balancers --names <name>
aws dynamodb describe-table --table-name <name>
aws sqs get-queue-attributes --queue-url <url> --attribute-names All
aws apigatewayv2 get-apis
```

If multiple matches exist, ask for the specific region, account, cluster, queue URL, or resource identifier.

## Health indicators

| Service | Key indicators |
| --- | --- |
| Lambda | Error rate, throttle rate, duration P99, concurrent executions, cold starts. |
| RDS | CPU utilization, FreeStorageSpace, DatabaseConnections, ReadLatency, WriteLatency, Performance Insights DB load. |
| ECS | Running vs desired count, pending count, task stop reason, service status. |
| ALB | TargetResponseTime, HTTPCode_ELB_5XX_Count, UnHealthyHostCount. |
| SQS | ApproximateNumberOfMessagesNotVisible, ApproximateAgeOfOldestMessage. |
| DynamoDB | ConsumedReadCapacityUnits, ThrottledRequests, SuccessfulRequestLatency. |
| EC2 | Instance status checks, CPU, memory if agent-enabled, disk, network, system events. |

Service checks:

```bash
aws ec2 describe-instance-status --instance-ids <id>
aws rds describe-db-instances --db-instance-identifier <name> --query 'DBInstances[0].DBInstanceStatus'
aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Errors --dimensions Name=FunctionName,Value=<name> --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 3600 --statistics Sum
aws ecs describe-services --cluster <cluster> --services <name> --query 'services[0].[status,runningCount,desiredCount,pendingCount]'
```

## Logs and metrics analysis

Find log groups, run CloudWatch Logs Insights, and retrieve results:

```bash
aws logs describe-log-groups --log-group-name-prefix /aws/<service>/<name>
aws logs start-query --log-group-name /aws/lambda/<name> --start-time $(date -u -d '24 hours ago' +%s) --end-time $(date -u +%s) --query-string 'filter @message like /ERROR/ | stats count(*) as errorCount by bin(1h)'
aws logs get-query-results --query-id <id>
aws logs start-query --log-group-name /aws/lambda/<name> --start-time $(date -u -d '24 hours ago' +%s) --end-time $(date -u +%s) --query-string 'filter @type = "REPORT" | filter @initDuration > 0 | stats count() as coldStarts by bin(1h)'
aws pi get-resource-metrics --service-type RDS --identifier db:<identifier> --metric-queries '[{"Metric":"db.load.avg"}]' --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period-in-seconds 3600
```

Look for recurring error patterns, correlation with deployments or CloudTrail events, performance trends, dependency failures, and saturation signals.

## Severity and root cause

| Severity | Definition |
| --- | --- |
| Critical | Service unavailable, data loss, or security incident. |
| High | Performance degradation, intermittent failures, or error rates `>5%`. |
| Medium | Warnings, suboptimal configuration, or minor performance issue. |
| Low | Informational alert or optimization opportunity. |

| Root cause category | Examples |
| --- | --- |
| Configuration Issues | Wrong settings, missing env vars, IAM permission denials. |
| Resource Constraints | CPU, memory, disk, Lambda throttling, RDS connection exhaustion. |
| Network Issues | Security group rules, VPC routing, DNS, NACLs. |
| Application Issues | Code bugs, memory leaks, unhandled exceptions, slow queries. |
| Dependency Issues | Downstream timeouts, SQS/SNS failures, external API limits. |
| Security Issues | KMS key issues, certificate expiration. |

## Remediation planning

Immediate actions apply only to Critical issues and should include rollback/validation. Examples:

```bash
aws lambda put-reserved-concurrency --function-name <name> --reserved-concurrent-executions 100
aws rds reboot-db-instance --db-instance-identifier <name>
```

Short-term fixes include configuration adjustments, right-sizing, CloudWatch alarms, and IAM corrections. Long-term improvements include resilience architecture, preventive monitoring, and AWS Health Dashboard notifications via EventBridge.

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| Resource Not Found | Ask for resource name, type, region, account, cluster, or queue URL. |
| Authentication Issues | Guide through `aws configure`. |
| Insufficient Permissions | List required IAM actions such as `logs:*`, `cloudwatch:*`, and `pi:*`. |
| No Logs Available | Recommend enabling CloudWatch logging for the resource type. |
| Query Timeouts | Use shorter time windows. |

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `CPU/memory/disk`
- `Healthy/Warning/Critical`
- `High/Medium`
- `High/Medium/Low`
- `ReadLatency/WriteLatency`
- `name/region`
- `region/account`

## Output template

```markdown
## AWS resource health assessment

**Status:** Healthy | Warning | Critical | blocked
**Resource:** <name> (<type>)
**Region/account:** <region> | <account id>

| Issue | Severity | Evidence | Root cause category | Remediation phase |
| --- | --- | --- | --- | --- |
| <issue> | Critical/High/Medium/Low | <metric/log/status evidence> | <category> | Immediate/Short-term/Long-term |

### Remediation plan
#### Immediate actions
- <command, rollback, validation>

#### Short-term fixes
- <configuration, alarm, IAM, or sizing change>

#### Long-term improvements
- <architecture, monitoring, EventBridge, or resilience change>

### Validation
- <metric, log query, CLI check, or alarm state to confirm recovery>
```

## Quality gate

- [ ] Target resource identity, type, region, and account were resolved or reported as blocked.
- [ ] Service-specific health metrics and status checks were collected.
- [ ] CloudWatch logs were queried or missing logs were documented.
- [ ] Major issues have severity, evidence, and root cause category.
- [ ] Remediation is split into immediate, short-term, and long-term actions when applicable.
- [ ] AWS CLI commands include validation and rollback considerations for risky changes.
- [ ] Monitoring recommendations include CloudWatch alarms or AWS Health Dashboard/EventBridge where relevant.

## References

- [Amazon CloudWatch monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/)
