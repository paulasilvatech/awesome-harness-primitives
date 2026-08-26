---
name: azure-api-center
description: "Design Azure API Center as the enterprise inventory and governance plane for APIs, agent tools, OpenAPI definitions, environments, deployments, metadata, linting, and MCP server discovery. Use when building an API or tool catalog, enforcing API standards, registering MCP servers, or making approved tools discoverable to agent builders."
argument-hint: "what to govern, for example a central tool and MCP catalog for agent builders"
---

# Azure API Center

Design Azure API Center as the catalog and governance plane for APIs, tools, versions, definitions, environments, deployments, and MCP servers so agent builders discover approved capabilities instead of ungoverned endpoints.

## When to invoke

- "Create an API Center catalog for our agent tools."
- "Govern OpenAPI definitions and MCP servers for agent builders."
- "Design API standards and linting with Azure API Center."
- "Make backend APIs discoverable for an agentic platform."

## Inputs

Use `$ARGUMENTS` as the governance scenario: API families, tool types, MCP servers, environments, required metadata, linter standards, consumers, and discovery experience. If the current Azure API Center feature set matters, verify it before stating final design.

## Prerequisites and context

- Confirm current API Center capabilities, including MCP registration, linting rules, portal features, and extension support, on Microsoft Learn before committing a design.
- Do not assert a feature without a source when the platform capability is time-sensitive.
- Pair API Center with API Management only when runtime enforcement is in scope; API Center itself is the inventory and governance plane.

## Core concepts

| Concept | Purpose | Design questions |
| --- | --- | --- |
| API | Logical entry for a product, backend, tool, or capability. | Who owns it? What domain does it serve? |
| Version | Specific version of an API. | What is the lifecycle stage and compatibility policy? |
| Definition | Contract, typically an OpenAPI document. | Is it linted, complete, and linked to a version? |
| Environment | Runtime environment such as Azure API Management or a Kubernetes cluster. | Is it dev, staging, production, or sandbox? |
| Deployment | Runtime location where a version is available. | Which environment, gateway, base URL, and owner apply? |
| Metadata | Custom governance properties. | Which fields are required for compliance and reporting? |
| MCP server | Tool server agents can discover and call. | Is it approved, owned, documented, and secured? |

## Governance model

| Governance need | API Center mechanism | Minimum metadata |
| --- | --- | --- |
| Ownership | Required custom metadata | owner, team, support contact. |
| Data sensitivity | Required custom metadata and review workflow | classification, PII, retention, region. |
| Lifecycle | Version and metadata | stage, deprecation date, replacement API. |
| Security standards | Linter and required fields | auth type, scopes, network exposure. |
| Discoverability | Portal or VS Code extension | description, tags, domain, examples. |
| Agent tool reuse | OpenAPI or MCP registration | tool purpose, side effects, rate limits, safety notes. |

## Procedure

1. Model the catalog. Define metadata schema first: owner, classification, lifecycle stage, data sensitivity, cost center, support path, and allowed consumers.
2. Register APIs and tools. Import OpenAPI definitions for backend APIs and HTTP tools. Register MCP servers so agents can discover them through the governed catalog.
3. Link environments and deployments. Connect Azure API Management instances and other runtimes so API Center reflects where each API version actually runs.
4. Govern definitions. Apply the API Center linter and required metadata. Reject or flag definitions that miss security, naming, versioning, or documentation standards.
5. Publish discovery. Expose the API Center portal or VS Code extension to agent builders with filters for approved tools, environments, and lifecycle stage.
6. Connect runtime enforcement. Use APIM AI gateway for authentication, token limits, semantic cache, and load balancing when the cataloged API is used at runtime.

## Platform fit

```text
Backend APIs / Tools / MCP servers
        |  register definitions and metadata
   Azure API Center  (inventory + governance + discovery)
        |  reference governed APIs
   Azure API Management  (runtime AI gateway: authN, token limit, cache)
        |
   Agents (Foundry, Container Apps) select and call governed tools
```

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-aigateway` | skill | You need runtime enforcement, authN, token limits, cache, routing, and metrics. |
| `foundry-agent-blueprint` | skill | Agents need to consume cataloged APIs as OpenAPI or MCP tools. |
| `azure-agentic-architecture-patterns` | skill | You need architecture guidance for tools and MCP boundaries. |

## Gotchas

- **Catalogs fail without ownership**: require owner and support metadata before publishing an API or tool.
- **Discovery is not enforcement**: API Center does not replace API Management for runtime authentication or throttling.
- **Linting must run before registration is trusted**: imported OpenAPI alone does not guarantee secure or usable APIs.
- **MCP tool descriptions affect agent behavior**: document side effects, auth, and rate limits, not just endpoints.

## Output template

```markdown
## Azure API Center governance design

**Scope:** <APIs, tools, MCP servers, or platform>

| Catalog item | Definition source | Required metadata | Environment/deployment | Governance check |
| --- | --- | --- | --- | --- |
| <API or tool> | <OpenAPI, MCP, manual> | <owner, classification, lifecycle> | <dev/stage/prod runtime> | <linter/approval> |

### Discovery model
- Portal or extension: <audience and filters>
- Approved tool criteria: <criteria>

### Runtime handoff
- API Management/APIM AI gateway: <when used>
```

## Quality gate

- [ ] Current API Center capabilities are verified when feature specificity matters.
- [ ] API, Version, Definition, Environment, Deployment, Metadata, and MCP server concepts are mapped where relevant.
- [ ] Required metadata covers owner, classification, lifecycle, data sensitivity, and support path.
- [ ] OpenAPI definitions and MCP servers have governance checks before discovery.
- [ ] Runtime concerns are handed to API Management or `azure-aigateway` instead of overstating API Center.
- [ ] Agent builders have a clear discovery path for approved APIs and tools.

## References

- [Azure API Center](https://learn.microsoft.com/azure/api-center/)
- [Register APIs in API Center](https://learn.microsoft.com/azure/api-center/register-apis)
- [API governance and linting](https://learn.microsoft.com/azure/api-center/enable-api-analysis-linting)
- [API Center and API Management](https://learn.microsoft.com/azure/api-center/)
