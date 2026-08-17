---
applyTo: "**/*.json,**/*.ts,**/*.tsp,**/manifest.json,**/agent.json,**/declarative-agent.json"
description: "Enforces Microsoft 365 Copilot declarative agent conventions for schema v1.5 manifests, TypeSpec models, capabilities, toolkit workflows, testing, deployment, monitoring, and security."
---

# Microsoft 365 Declarative Agent Conventions — Schema v1.5 Manifests

These instructions apply to Microsoft 365 Copilot declarative agent manifests, TypeScript helpers, TypeSpec definitions, and related JSON files. They are authoritative for schema v1.5 structure, character limits, capability selection, Microsoft 365 Agents Toolkit integration, TypeSpec compilation, testing, deployment lifecycle, monitoring, and security in matched files; tenant governance, organizational compliance policy, and official schema validation win where they impose stricter requirements.

## Schema v1.5 Manifest Contract

Use the Microsoft 365 declarative agent schema exactly for agent manifests.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json",
  "version": "v1.5",
  "name": "string (max 100 characters)",
  "description": "string (max 1000 characters)",
  "instructions": "string (max 8000 characters)",
  "capabilities": ["array (max 5 items)"],
  "conversation_starters": ["array (max 4 items, optional)"]
}
```

| Property | Constraint | Convention |
| --- | --- | --- |
| `$schema` | Required | Use `https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json`. |
| `version` | Required | Use `v1.5` for the schema covered by this file. |
| `name` | Required, 1 to 100 characters | Keep the name concise and user-facing. |
| `description` | Required, 1 to 1000 characters | State the agent's purpose and scope. |
| `instructions` | Required, 1 to 8000 characters | Give direct behavior guidance with compliance boundaries. |
| `capabilities` | Required, 1 to 5 items | Declare only capabilities needed by the agent. |
| `conversation_starters` | Optional, max 4 items | Keep each starter focused and useful. |

## Capabilities and Enterprise Boundaries

Select capabilities incrementally and test every combination.

| Capability | Use when |
| --- | --- |
| `WebSearch` | Internet search and real-time information access are required. |
| `OneDriveAndSharePoint` | File access, document search, or content management is required. |
| `GraphConnectors` | Enterprise data from third-party systems is integrated through Graph connectors. |
| `MicrosoftGraph` | Microsoft 365 services and data access is required. |
| `TeamsAndOutlook` | Teams chat, meetings, or email integration is required. |
| `CopilotForMicrosoft365` | Advanced Microsoft 365 Copilot features and workflows are required. |
| `PowerPlatform` | Power Apps, Power Automate, or Power BI integration is required. |
| `BusinessDataProcessing` | Advanced data analysis and processing is required. |
| `WordAndExcel` | Document creation, editing, or analysis is required. |
| `EnterpriseApplications` | Third-party business system integration is required. |
| `CustomConnectors` | Custom API or service integration is required. |

Start with one or two core capabilities, add more only from user feedback or validated requirements, and evaluate compliance implications before enabling enterprise data access.

## TypeSpec and Toolkit Integration

Use Microsoft 365 Agents Toolkit and TypeSpec when they improve repeatability.

- Install the VS Code extension `teamsdevapp.ms-teams-vscode-extension` for Microsoft 365 Agents Toolkit workflows.
- Use TypeSpec with `import "@typespec/json-schema";`, `using TypeSpec.JsonSchema;`, `@jsonSchema("/schemas/declarative-agent/v1.5/schema.json")`, and `namespace DeclarativeAgent;` when maintaining schema-first definitions.
- Model `Agent` with `$schema`, `version`, `name`, `description`, `instructions`, `capabilities`, and optional `conversation_starters`.
- Preserve TypeSpec constraints such as `@minLength(1)`, `@maxLength(100)`, `@maxLength(1000)`, `@maxLength(8000)`, `@minItems(1)`, and `@maxItems(5)` / `@maxItems(4)`.
- Represent capabilities with `union AgentCapability` and conversation starters with `model ConversationStarter` and `text` limited to 100 characters.
- Compile TypeSpec manifests with `tsp compile agent.tsp --emit=@typespec/json-schema`.

## Environment Configuration and Lifecycle

Keep development and production values explicit and environment-specific.

| Environment | Convention |
| --- | --- |
| Development | Use placeholders such as `${DEV_AGENT_NAME}`, `${AGENT_DESCRIPTION}`, `${AGENT_INSTRUCTIONS}`, and `${REQUIRED_CAPABILITIES}` for local iteration. |
| Production | Use `${PROD_AGENT_NAME}`, `${AGENT_DESCRIPTION}`, `${AGENT_INSTRUCTIONS}`, and `${PRODUCTION_CAPABILITIES}` for promoted manifests. |
| Version management | Include semantic application metadata such as `1.2.0`, `20241208.1`, and `environment: production` when the schema or packaging supports it. |
| Promotion | Move from TypeSpec definition to JSON compilation, local testing, validation, staging deployment, and production release without changing schema constraints. |

## Validation and Testing

Validate both schema shape and agent behavior.

- Fetch the v1.5 schema and validate manifests with a JSON schema validator before deployment.
- Use helper checks equivalent to `validateName`, `validateDescription`, and `validateInstructions` to enforce length constraints in TypeScript code.
- Test locally with `npm install -g @microsoft/agents-playground` and `agents-playground start --manifest=./agent.json` when Agents Playground is part of the workflow.
- Cover capability validation, conversation flow, invalid inputs, edge cases, response time, and reliability.
- Use TypeSpec compiler diagnostics, Agents Playground debugging, Microsoft 365 Agents Toolkit logs, and schema validation utilities for troubleshooting.

## Advanced Behavior, Localization, and Observability

Add advanced manifest features only when the target platform supports them.

| Area | Convention |
| --- | --- |
| Behavior overrides | Use `behavior_overrides`, `response_tone`, `max_response_length`, and `citation_requirements` only when supported and tested. |
| Localization | Use localized values such as `en-US`, `es-ES`, and `fr-FR` only in schema locations that support object-valued localization. |
| Monitoring | Track response time per capability, conversation starter engagement, error rates, failure patterns, and capability utilization statistics. |
| Logging | Use structured fields such as `timestamp`, `agentName`, `version`, `userId`, `capability`, `responseTime`, and `success`, while respecting privacy policy. |

## Security and Compliance

Treat enterprise data access as a security boundary.

- Validate all inputs and outputs.
- Implement appropriate access controls for enterprise capabilities.
- Use rate limiting and abuse prevention where the hosting model supports it.
- Monitor suspicious activity patterns and perform regular security audits and updates.
- Ensure data handling complies with GDPR, CCPA, and organizational policies.

## Good / Bad Examples

The examples below illustrate a minimal schema-valid manifest.

**Good:**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json",
  "version": "v1.5",
  "name": "Research Assistant",
  "description": "Helps employees search approved enterprise and web sources.",
  "instructions": "Answer with concise source-aware guidance and respect tenant data boundaries.",
  "capabilities": ["WebSearch", "MicrosoftGraph"],
  "conversation_starters": [{ "text": "Find related project documents" }]
}
```

Why: The manifest uses the correct schema, version, required fields, bounded capabilities, and a focused starter.

**Bad:**

```json
{
  "name": "Agent",
  "description": "Does everything",
  "instructions": "Help users",
  "capabilities": ["WebSearch", "OneDriveAndSharePoint", "GraphConnectors", "MicrosoftGraph", "TeamsAndOutlook", "PowerPlatform"]
}
```

Why: The manifest omits `$schema` and `version`, overstates scope, and exceeds the five-capability limit.

## Compatibility Vocabulary

Retain `production-ready` as the quality bar and `MyAgent` only as an illustrative placeholder name in logging examples.

## Conventions

| Rule | Rationale |
|---|---|
| Use schema `v1.5` and the official `$schema` URL | Validation and tooling depend on the declared schema contract |
| Enforce name, description, instructions, capabilities, and conversation starter limits | Over-limit manifests fail validation or degrade usability |
| Start with the smallest capability set that satisfies requirements | Enterprise permissions and performance costs grow with each capability |
| Compile TypeSpec with `tsp compile agent.tsp --emit=@typespec/json-schema` when TypeSpec is the source | Generated JSON stays aligned with the model constraints |
| Test with Agents Playground, toolkit logs, and schema validators | Schema validity does not prove conversational behavior |
| Apply privacy, access control, rate limiting, and audit conventions to enterprise data | Declarative agents can expose sensitive Microsoft 365 information |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `${DEV_AGENT_NAME}` and `${PROD_AGENT_NAME}` to separate environments | Reuse development names or capabilities in production by accident |
| Keep `conversation_starters` to four focused options or fewer | Add generic starters that do not exercise the agent's value |
| Validate `validateName`, `validateDescription`, and `validateInstructions` logic in helpers | Trust UI text lengths without automated checks |
| Use `GraphConnectors`, `MicrosoftGraph`, or `OneDriveAndSharePoint` only with governance approval | Enable broad enterprise data capabilities by default |
| Log operational metrics without unnecessary sensitive content | Put user secrets or confidential prompts into analytics logs |

## Checklist Before Opening a PR

- [ ] `$schema` is `https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json` and `version` is `v1.5`.
- [ ] `name`, `description`, and `instructions` are present and within 100, 1000, and 8000 characters.
- [ ] `capabilities` contains one to five justified values.
- [ ] `conversation_starters` has no more than four focused entries.
- [ ] TypeSpec constraints and generated JSON remain synchronized when `.tsp` files are used.
- [ ] Development and production placeholders or values are separated.
- [ ] Agents Playground, schema validation, or equivalent toolkit validation covers declared capabilities and conversation flow.
- [ ] Security, privacy, compliance, rate limiting, and monitoring requirements are satisfied for enterprise data access.

## References

- Microsoft 365 declarative agent schema v1.5: https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json
