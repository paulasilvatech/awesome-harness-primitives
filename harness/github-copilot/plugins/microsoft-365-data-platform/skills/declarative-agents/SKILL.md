---
name: declarative-agents
description: >-
  Build, validate, and optimize Microsoft 365 Copilot declarative agents with v1.5 schema, TypeSpec, Microsoft 365 Agents Toolkit, capabilities, conversation starters, localization, and Agents Playground testing. Use when the user asks for Microsoft 365 declarative agents development, manifest design, TypeSpec migration, or validation.
---

# Microsoft 365 declarative agents

Create, validate, or optimize Microsoft 365 Copilot declarative agents by choosing the right workflow, enforcing v1.5 schema limits, using TypeSpec when helpful, and integrating Microsoft 365 Agents Toolkit and Agents Playground.

## When to invoke

- "Create a Microsoft 365 Copilot declarative agent."
- "Validate this declarative agent manifest."
- "Convert this agent JSON to TypeSpec."
- "Choose capabilities for an enterprise declarative agent."
- "Optimize conversation starters and instructions for a Microsoft 365 agent."

## Workflow selection

| Workflow | Best for | Outcome |
| --- | --- | --- |
| Basic Agent Creation | New developers, simple agents, quick prototypes. | Planned purpose, selected capabilities, JSON manifest or TypeSpec, testing setup. |
| Advanced Enterprise Agent Design | Complex enterprise scenarios, production deployment, advanced features. | Enterprise architecture, capability interactions, behavior overrides, localization, lifecycle plan. |
| Validation & Optimization | Existing agents, troubleshooting, performance optimization. | Schema compliance findings, limit fixes, capability audit, TypeSpec migration plan, test protocol. |

## Basic agent creation

1. Define agent purpose, target users, core tasks, and success criteria.
2. Select capabilities from the available capability catalog, respecting the maximum of 5.
3. Generate a compliant JSON manifest with required fields and constraints.
4. Offer a TypeSpec alternative for type-safe definitions that compile to JSON.
5. Configure Agents Playground for local testing.
6. Use Microsoft 365 Agents Toolkit for development, debugging, and environment management.

## Advanced enterprise design

| Area | Required decisions |
| --- | --- |
| Requirements | Tenant model, target users, compliance boundaries, data access, audit needs. |
| Capabilities | Interactions between WebSearch, Microsoft Graph, SharePoint, connectors, and business data. |
| Behavior overrides | Response style, refusal boundaries, escalation, and specialized behaviors. |
| Localization | Languages, resource files, conversation starter translations, fallback language. |
| Conversation starters | Up to 4 high-value entry points aligned to user tasks. |
| Deployment | Development, staging, production environments; versioning and lifecycle. |
| Monitoring | Usage analytics, quality signals, failure modes, performance optimization. |

## Validation rules

| Item | Limit or rule |
| --- | --- |
| Schema | Use Microsoft 365 declarative agent JSON Schema v1.5. |
| `name` | Maximum 100 characters. |
| `description` | Maximum 1000 characters. |
| `instructions` | Maximum 8000 characters. |
| `conversation_starters` | Maximum 4. |
| `capabilities` | Maximum 5. |
| Required fields | Validate required field presence and type correctness. |
| Environment placeholders | Support `${AGENT_NAME}`, `${AGENT_DESCRIPTION}`, and `${AGENT_INSTRUCTIONS}` where the toolchain resolves them. |

## Capability catalog

Choose no more than 5 capabilities.

| Capability | Use when |
| --- | --- |
| WebSearch | Internet search functionality. |
| OneDriveAndSharePoint | File and content access. |
| GraphConnectors | Enterprise data integration. |
| MicrosoftGraph | Microsoft 365 service integration. |
| TeamsAndOutlook | Communication platform access. |
| PowerPlatform | Power Apps and Power Automate integration. |
| BusinessDataProcessing | Enterprise data analysis. |
| WordAndExcel | Document and spreadsheet manipulation. |
| CopilotForMicrosoft365 | Advanced Copilot features. |
| EnterpriseApplications | Third-party system integration. |
| CustomConnectors | Custom API and service integration. |

## Microsoft 365 Agents Toolkit and TypeSpec

| Feature | Use |
| --- | --- |
| VS Code extension | `teamsdevapp.ms-teams-vscode-extension` for Microsoft 365 Agents Toolkit integration. |
| TypeSpec | Type-safe agent definitions that compile to JSON. |
| Local debugging | Agents Playground validation and behavior testing. |
| Environment management | Development, staging, and production configurations. |
| Lifecycle management | Creation, testing, deployment, monitoring, and version updates. |

```typespec
model MyAgent {
  name: string;
  description: string;
  instructions: string;
  capabilities: AgentCapability[];
  conversation_starters?: ConversationStarter[];
}
```

```json
{
  "name": "${AGENT_NAME}",
  "description": "${AGENT_DESCRIPTION}",
  "instructions": "${AGENT_INSTRUCTIONS}"
}
```

## Criteria

- [ ] The chosen workflow matches the user's maturity: basic, advanced, or validation.
- [ ] Capability count is 5 or fewer and each capability maps to a user task.
- [ ] Conversation starter count is 4 or fewer and each starter is task-oriented.
- [ ] `name`, `description`, and `instructions` respect 100, 1000, and 8000 character limits.
- [ ] TypeSpec and JSON outputs stay equivalent when both are produced.
- [ ] Agents Playground testing is included for local validation.
- [ ] Enterprise designs address tenant, compliance, localization, lifecycle, and monitoring concerns.

## Gotchas

- **Do not start with all capabilities**: overbroad capability selection weakens behavior and can violate the max-5 limit.
- **Do not exceed character limits**: long instructions silently damage validation and usability.
- **Do not create generic conversation starters**: starters should be specific user tasks, not marketing copy.
- **Do not skip local testing**: schema-valid manifests can still behave poorly in Agents Playground.

## Output template

```markdown
## Declarative agent result

**Status:** ready | needs changes | blocked
**Workflow:** Basic Agent Creation | Advanced Enterprise Agent Design | Validation & Optimization
**Agent name:** `<name>`

| Area | Decision or finding | Evidence |
| --- | --- | --- |
| Purpose | <agent purpose> | <user requirement> |
| Capabilities | <selected capabilities> | <count <= 5> |
| Conversation starters | <starters> | <count <= 4> |
| Schema | v1.5 compliant | pass | fail |
| Testing | Agents Playground | pass | fail | not run |

### Artifacts
- `<manifest path or TypeSpec path>`

### Validation
- `name` <= 100: pass | fail
- `description` <= 1000: pass | fail
- `instructions` <= 8000: pass | fail
```

## Quality gate

- [ ] The response states which workflow was used and why.
- [ ] Manifest or TypeSpec content follows Microsoft 365 declarative agent v1.5 constraints.
- [ ] Capability selection uses no more than 5 capabilities from the catalog.
- [ ] Conversation starters use no more than 4 entries.
- [ ] `AGENT_NAME`, `AGENT_DESCRIPTION`, and `AGENT_INSTRUCTIONS` placeholders are preserved when environment substitution is intended.
- [ ] Microsoft 365 Agents Toolkit and Agents Playground validation steps are included when building or debugging.
- [ ] Validation findings include concrete fixes instead of generic advice.
