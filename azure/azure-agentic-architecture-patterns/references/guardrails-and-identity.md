# Guardrails and Identity

Agentic systems take actions, so identity and guardrails are not optional. Design them in from the start.

## Identity

- **Agent identity.** Give each agent a first-class identity with Microsoft Entra Agent ID, so its actions are attributable and governable like a user or service principal. Route to the `entra-agent-id` skill.
- **Managed identity.** Authenticate to Azure services with managed identity and `DefaultAzureCredential`, never with embedded keys. Some tenant policies force `disableLocalAuth=true`, so design for AAD from day one.
- **App registration.** For agents that call Microsoft Graph or protected APIs, register the app and request least-privilege scopes. Route to the `entra-app-registration` skill.
- **Least privilege.** Scope each tool and each backend to the minimum role. Separate read and write paths.

## Content and prompt guardrails

- **Azure AI Content Safety.** Screen inputs and outputs for harmful content, with severity thresholds per category.
- **Prompt Shields.** Detect prompt injection and jailbreak attempts, including indirect injection from retrieved documents and tool outputs.
- **Groundedness checks.** Verify that answers are supported by provided context; flag ungrounded claims.
- **Human in the loop.** Require approval for high-impact or irreversible tool actions.

## Network and data posture

- Private networking (private endpoints, VNet integration) where data sensitivity requires it. Note that some resources, such as the Developer tier of API Management, cannot be created with public access disabled; create enabled and harden after.
- Encrypt in transit and at rest. Scope cache and memory keys by tenant to prevent cross-tenant leakage.
- Classify data and keep regulated data inside approved boundaries.

## Checklist

- Every agent has an Entra Agent ID and a managed identity.
- No shared secrets in code or config.
- Content Safety and Prompt Shields on the input and output paths.
- High-impact tools gated by approval.
- Tenant isolation enforced in cache, memory, and retrieval keys.
- Audit log for prompts, tool calls, and identities.

## Sources

- [Microsoft Entra Agent ID](https://learn.microsoft.com/entra/)
- [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Azure Well-Architected security for AI](https://learn.microsoft.com/azure/well-architected/ai/)
