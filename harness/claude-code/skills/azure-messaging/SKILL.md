---
name: azure-messaging
description: >-
  Troubleshoot and resolve issues with the Azure Messaging SDKs for Event Hubs and Service Bus,
  covering connection failures, authentication errors, message processing problems, and SDK
  configuration. Use when the user hits an Event Hubs or Service Bus SDK error, AMQP or connection
  failure, event processor host issue, lost or expired message lock, lock renewal problem, send
  timeout, disconnected receiver, checkpoint or offset issue, dead-letter or session error,
  duplicate events, or needs SDK logging enabled in .NET, Java, Python, or JavaScript.
license: MIT
metadata:
  author: Microsoft
  version: 1.2.1
---

<!-- Generated from harness/github-copilot/skills/azure-messaging/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Messaging SDK Troubleshooting

## Quick Reference

| Property | Value |
|----------|-------|
| **Services** | Azure Event Hubs, Azure Service Bus |
| **MCP Tools** | `mcp_azure_mcp_eventhubs`, `mcp_azure_mcp_servicebus` |
| **Best For** | Diagnosing SDK connection, auth, and message processing issues |

## When to invoke

- SDK connection failures, auth errors, or AMQP link errors
- Idle timeout, connection inactivity, or slow reconnection after disconnect
- AMQP link detach or detach-forced errors
- Message lock lost, message lock expired, lock renewal failures, or batch lock timeouts
- Session lock lost, session lock expired, or session receiver errors
- Event processor or message handler stops processing
- Duplicate events or checkpoint offset resets
- SDK configuration questions (retry, prefetch, batch size, receive batch behavior)

## MCP Tools

| Tool | Command | Use |
|------|---------|-----|
| `mcp_azure_mcp_eventhubs` | Namespace/hub ops | List namespaces, hubs, consumer groups |
| `mcp_azure_mcp_servicebus` | Queue/topic ops | List namespaces, queues, topics, subscriptions |
| `mcp_azure_mcp_monitor` | `logs_query` | Query diagnostic logs with KQL |
| `mcp_azure_mcp_resourcehealth` | `get` | Check service health status |
| `mcp_azure_mcp_documentation` | Doc search | Search Microsoft Learn for troubleshooting docs |

## Diagnosis Workflow

1. **Identify the SDK and version** — Check the prompt for SDK and version clues; if not stated, proceed with diagnosis and ask later if needed
2. **Check resource health** — Use `mcp_azure_mcp_resourcehealth` to verify the namespace is healthy
3. **Review the error message** — Match against language-specific troubleshooting guide
4. **Look up documentation** — Use `mcp_azure_mcp_documentation` to search Microsoft Learn for the error or topic
5. **Check configuration** — Verify connection string, entity name, consumer group
6. **Recommend fix** — Apply remediation, citing documentation found


## Troubleshooting Guides

Connectivity, SDK, and auth troubleshooting guides are located in the azure-diagnostics skill under `troubleshooting/messaging/`.

## References

- Use `mcp_azure_mcp_documentation` to search Microsoft Learn for latest guidance.

## Output template

```markdown
## Messaging troubleshooting result

**Status:** resolved | mitigated | inconclusive
**Summary:** <one sentence covering scope and outcome>

### Details
Error signature, root cause, and the SDK or configuration fix.

### Validation
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] The diagnosis matches the observed SDK error and client version.
- [ ] The fix names the specific SDK setting or code change.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was performed and its evidence is shown.
- [ ] Irreversible Azure actions were confirmed with the user first.
