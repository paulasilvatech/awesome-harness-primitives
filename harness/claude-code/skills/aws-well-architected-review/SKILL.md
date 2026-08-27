---
name: aws-well-architected-review
description: >-
  Review AWS workloads against the AWS Well-Architected Framework across Operational Excellence,
  Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability. Use when
  the user asks for an AWS well-architected review, IaC architecture assessment, WAF findings,
  risk classification, or GitHub issue remediation plan.
---

<!-- Generated from harness/github-copilot/skills/aws-well-architected-review/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AWS Well-Architected review

Review repository IaC and available AWS infrastructure evidence against the six AWS Well-Architected Framework pillars, classify risks, summarize remediation, and prepare GitHub issue-ready findings.

## When to invoke

- "Run an AWS Well-Architected review."
- "Review this Terraform stack against WAF pillars."
- "Find AWS architecture risks and create remediation issues."
- "Assess our CDK app for security, reliability, and cost."
- "Generate Well-Architected findings for this workload."

## Prerequisites and context

- AWS CLI must be configured and authenticated for live infrastructure checks.
- IaC should be present as Terraform, CloudFormation, CDK, or SAM. If none exists, review live resources only and report the gap.
- GitHub issue creation requires an authenticated GitHub tool or `gh`; otherwise output issue-ready Markdown.
- Fetch `https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html` and relevant lenses when current best practices are needed.

## Discovery

Scan for IaC and architecture evidence:

| IaC type | File patterns |
| --- | --- |
| Terraform | `**/*.tf` |
| CloudFormation/SAM | `**/*.yaml`, `**/*.json` templates |
| CDK | `lib/**/*.ts`, `bin/**/*.ts`, `cdk.json` |

Identify compute, data, networking, security, and observability services. Generate a Mermaid architecture diagram for the EPIC issue when enough relationships are known.

## Pillar criteria

### Operational Excellence

- [ ] All infrastructure is defined as IaC; no unmanaged manual console changes.
- [ ] Consistent tagging strategy exists across resources.
- [ ] CloudWatch alarms cover key metrics.
- [ ] Automated deployment pipeline exists; no manual deployments.
- [ ] CloudTrail is enabled for audit logging.
- [ ] Runbooks or operational documentation are present.

### Security

- [ ] IAM roles use least privilege; no `*` actions without justification.
- [ ] No hardcoded credentials appear in IaC or code.
- [ ] Secrets are managed in Secrets Manager or SSM Parameter Store.
- [ ] S3 buckets block public access and enable server-side encryption.
- [ ] Sensitive resources are in private subnets.
- [ ] Security groups restrict inbound access to required ports and CIDRs.
- [ ] KMS encryption is enabled for RDS, EBS, S3, SQS, DynamoDB, and other sensitive stores.
- [ ] SSL/TLS is enforced on endpoints, including `enforceSSL: true` where applicable.
- [ ] GuardDuty is enabled; validate with `aws guardduty list-detectors`.
- [ ] AWS WAF protects public APIs and CloudFront distributions.
- [ ] MFA delete is enabled for critical S3 buckets when operationally feasible.

### Reliability

- [ ] Production databases use Multi-AZ or equivalent regional resilience.
- [ ] DynamoDB Global Tables are used when global active-active data is required.
- [ ] Auto Scaling policies exist for EC2 and ECS where load varies.
- [ ] S3 versioning and lifecycle policies are configured.
- [ ] RDS automated backups have an appropriate retention period.
- [ ] DynamoDB Point-in-Time Recovery (PITR) is enabled for critical tables.
- [ ] Dead Letter Queues (DLQ) exist for Lambda, SQS, and SNS failure paths.
- [ ] Route 53 health checks support DNS failover where needed.
- [ ] Lambda reserved concurrency prevents noisy-neighbor throttling.

### Performance Efficiency

- [ ] Lambda memory, EC2 instance type, and RDS class are right-sized.
- [ ] Graviton or ARM is used where compatible, including Lambda `arm64` and EC2 Graviton.
- [ ] Caching exists where repeated reads justify it: ElastiCache, DAX, CloudFront, or API Gateway caching.
- [ ] CloudFront serves global static content.
- [ ] Aurora Serverless or DynamoDB On-Demand is considered for variable load.
- [ ] Lambda Provisioned Concurrency is used for latency-critical synchronous paths.

### Cost Optimization

- [ ] EC2 Reserved Instances or Savings Plans cover steady-state workloads.
- [ ] S3 lifecycle policies move data to cheaper tiers.
- [ ] Lambda `arm64` is used when compatible for cost reduction.
- [ ] VPC Endpoints for S3 and DynamoDB avoid unnecessary NAT Gateway charges.
- [ ] `gp2` EBS volumes are migrated to `gp3` when compatible.
- [ ] Development and test environments have auto-shutdown schedules.
- [ ] AWS Budgets and Cost Anomaly Detection are configured.
- [ ] Unattached EBS volumes and idle EC2 instances are identified.

### Sustainability

- [ ] Graviton or ARM instances are selected where available.
- [ ] Serverless or managed services are preferred over always-on EC2 when suitable.
- [ ] S3 lifecycle policies reduce unnecessary long-term storage.
- [ ] Auto Scaling avoids over-provisioning.
- [ ] Region selection considers AWS renewable energy commitments.

## Risk classification

| Risk | Use when |
| --- | --- |
| High Risk | Security vulnerability, single point of failure, no backup/recovery, or likely production outage. |
| Medium Risk | Reliability weakness, cost inefficiency, or performance concern that should be addressed soon. |
| Low Risk | Best-practice deviation or minor optimization opportunity. |

## Issue templates

Individual issue title: `[WAF-<PILLAR>] [Brief Finding] — [Risk Level]`. Label with `well-architected` and the pillar name such as `security` or `reliability`.

```markdown
## Well-Architected Finding: <Brief Title>

**Pillar**: <Name> | **Risk Level**: <High/Medium/Low> | **Effort**: <Low/Medium/High>

### Description
<finding and why it matters>

### Remediation
**IaC Fix** (preferred):
```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
```

**AWS CLI fallback**:
```bash
aws s3api put-bucket-encryption --bucket <name> --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'
```

### AWS Reference
- <WAF best practice link>
- <AWS documentation link>

### Validation
- [ ] Change implemented in IaC and deployed
- [ ] AWS Config rule passes when applicable
- [ ] Security Hub finding resolved when applicable

**Well-Architected Question**: <question>
```

EPIC issue title: `[EPIC] AWS Well-Architected Review — X findings across 6 pillars`. Label with `well-architected` and `epic`. Include executive summary, pillar/risk table, Mermaid diagram, prioritized High -> Medium -> Low checklist, and success criteria.

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| No IaC Files Found | Limit review to live AWS CLI discovery and note the IaC gap. |
| Insufficient AWS Permissions | List required read-only permissions for the services being reviewed. |
| GitHub Creation Failure | Output every finding as formatted Markdown for manual issue creation. |

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `Development/test`
- `EC2/ECS`
- `Graviton/ARM`
- `S3/DynamoDB`
- `Serverless/managed`
- `least-privilege`
- `ports/CIDRs`
- `public-facing`

## Output template

```markdown
## AWS Well-Architected review summary

**Status:** reviewed | issue-ready | blocked
**Scope:** <IaC files and/or live resources>

| Pillar | High | Medium | Low | Top finding |
| --- | --- | --- | --- | --- |
| Operational Excellence | <n> | <n> | <n> | <finding> |
| Security | <n> | <n> | <n> | <finding> |
| Reliability | <n> | <n> | <n> | <finding> |
| Performance Efficiency | <n> | <n> | <n> | <finding> |
| Cost Optimization | <n> | <n> | <n> | <finding> |
| Sustainability | <n> | <n> | <n> | <finding> |

### Issues
- <issue title or issue URL>

### Validation
- <commands, files, and evidence reviewed>
```

## Quality gate

- [ ] All six WAF pillars were reviewed.
- [ ] IaC files and live infrastructure evidence are named, or the absence of either is reported.
- [ ] Every finding has a pillar, risk level, evidence, remediation, and validation step.
- [ ] High Risk findings identify immediate impact and owner-ready next action.
- [ ] Issue-ready Markdown is produced when GitHub issue creation is not available.
- [ ] AWS documentation references are included for findings.

## References

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
