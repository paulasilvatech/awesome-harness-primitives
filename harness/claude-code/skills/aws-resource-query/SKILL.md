---
name: aws-resource-query
description: >-
  Answer natural-language questions about AWS resources by running strictly read-only AWS CLI
  queries. Use when asking about EC2, S3, RDS, Lambda, ECS, EKS, Secrets Manager, IAM, VPC,
  networking, messaging, `aws lambda list-event-source-mappings --query
  'EventSourceMappings[].[FunctionArn,EventSourceArn,State,BatchSize]' --output table`, or
  current-state inventory.
---

<!-- Generated from harness/github-copilot/skills/aws-resource-query/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AWS resource query

Translate resource inventory questions into read-only AWS CLI commands, confirm account and region context, format concise tables, and refuse create/modify/delete actions. This is the intent-to-command bridge for each `service/query`.

## When to invoke

- "List my EC2 instances in us-east-1."
- "Show Lambda event source mappings and batch sizes."
- "Which S3 buckets exist in this account?"
- "Find RDS databases by tag."
- "Query AWS resources without changing anything."

## Safety contract

STRICTLY READ ONLY. Use ONLY these AWS CLI command families:

| Allowed command family | Examples |
| --- | --- |
| Describe | `aws <service> describe-*` |
| List | `aws <service> list-*` |
| Get | `aws <service> get-*` |
| Identity | `aws sts get-caller-identity` |
| Configuration | `aws configure get` |
| Tags | `aws resourcegroupstaggingapi get-resources` |
| Cost Explorer | `aws ce get-*` |
| Support | `aws support describe-*` |

NEVER run mutating commands, including `create-*`, `run-*`, `start-*`, `stop-*`, `reboot-*`, `delete-*`, `terminate-*`, `put-*`, `update-*`, `modify-*`, `attach-*`, `detach-*`, `send-*`, `publish-*`, `invoke-*`, or `execute-*`.

If the user's query implies a write action, respond exactly with this pattern:

```markdown
This skill is read-only. I can show you the current state of [resource], but I cannot [create/modify/delete] it. Would you like to see what currently exists?
```

## Procedure

1. Parse intent: target service, resource type, filters, detail level, and region.
2. Confirm account and default region:
   - `aws sts get-caller-identity --query '{Account:Account,UserId:UserId}'`
   - `aws configure get region`
3. Append `--region <region>` to every command when the user specifies a region.
4. Read `references/intent-command-mapping.md` when translating service/resource intent to AWS CLI commands.
5. Run only allowed read-only commands.
6. Format list results with `--output table`; use `--output json` only for explicitly requested deep detail.
7. Use `--query` to extract relevant fields and avoid dumping raw JSON.
8. For large result sets over 20 items, show a count first and offer filters.

## Common query patterns

| User intent | Read-only command pattern |
| --- | --- |
| Confirm identity | `aws sts get-caller-identity --query '{Account:Account,UserId:UserId}'` |
| Check default region | `aws configure get region` |
| Lambda event source mappings | `aws lambda list-event-source-mappings --query 'EventSourceMappings[].[FunctionArn,EventSourceArn,State,BatchSize]' --output table` |
| Tag-based inventory | `aws resourcegroupstaggingapi get-resources --query '<fields>' --output table` |
| Cost data | `aws ce get-* --query '<fields>' --output table` |
| Support metadata | `aws support describe-* --query '<fields>' --output table` |

Services covered include EC2, S3, RDS, Lambda, ECS, EKS, Secrets Manager, IAM, VPC, networking, messaging, and more when the command remains read-only.

## Progressive disclosure and bundled resources

- `references/intent-command-mapping.md`: open this when mapping natural-language AWS resource questions to service-specific CLI commands.

## Output formatting rules

| Rule | Implementation |
| --- | --- |
| Table first | Use `--output table` for list results. |
| JSON only on request | Use `--output json` only for deep detail the user explicitly asks for. |
| Query fields | Always include `--query` to select relevant fields. |
| Large results | If more than 20 items are likely or returned, show count and offer filters. |
| Empty results | Explain likely causes: wrong region, no resources, or insufficient permissions. |
| Drill-down | Offer a next filter, such as state, type, tag, or resource ID. |

## Troubleshooting

| Error | Likely cause | Response |
| --- | --- | --- |
| `AccessDenied` | Caller lacks permission. | "You don't have permission to list [resource]. Required: `<service>:<Action>`." |
| `NoCredentialProviders` | AWS credentials are missing. | "Run `aws configure` or set `AWS_PROFILE`." |
| Empty result | Region, filters, or account do not contain the resource. | "No [resources] found in [region]. Check another region?" |
| Invalid identifier | Name or ID does not match an existing resource. | "Could not find '[name]'. Check the name or provide the resource ID." |

## Output template

```markdown
## AWS resource query result

**Status:** complete | read-only refusal | blocked
**Account:** `<account or not checked>`
**Region:** `<region or default>`
**Question:** <user intent>

| Resource | Key fields | Notes |
| --- | --- | --- |
| `<id/name>` | `<selected --query fields>` | <state, tags, or caveat> |

### Commands run
- `<aws read-only command with --query and --output table>`

### Next filter
- <state, type, tag, resource ID, or none>
```

## Quality gate

- [ ] Every command is read-only and belongs to an allowed command family.
- [ ] Mutating verbs such as `create-*`, `delete-*`, `update-*`, `modify-*`, `invoke-*`, and `execute-*` were refused.
- [ ] Account and region were checked or the inability to check them was reported.
- [ ] User-specified regions were applied with `--region <region>`.
- [ ] List output uses `--output table` and a focused `--query`.
- [ ] Large, empty, or permission-denied results are explained with next-step filters or required permissions.
