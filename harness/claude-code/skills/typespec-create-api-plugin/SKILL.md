---
name: typespec-create-api-plugin
description: >-
  Generate TypeSpec API plugins for Microsoft 365 Copilot with REST operations, authentication,
  confirmations, Adaptive Cards, and response instructions. Use when asked to create a TypeSpec
  API plugin, define main.tsp and actions.tsp, model API operations, add @useAuth, or build
  Adaptive Card responses for Microsoft 365 Copilot agents.
---

<!-- Generated from harness/github-copilot/skills/typespec-create-api-plugin/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# TypeSpec API plugin creation

Create a complete Microsoft 365 Copilot API plugin from API requirements by producing `main.tsp`, `actions.tsp`, optional `cards/card.json`, and implementation notes for operations, authentication, confirmations, and response shaping.

## When to invoke

- "Create a TypeSpec API plugin for this REST API."
- "Generate main.tsp and actions.tsp for a Microsoft 365 Copilot agent."
- "Add API key or OAuth2 auth to a TypeSpec action plugin."
- "Return API results with an Adaptive Card."
- "Model these CRUD operations as Copilot plugin actions."

## Inputs

Use the user's API description as the source of truth. Capture API base URL, purpose, operations, request and response schema, authentication method, destructive operations that need confirmation, and whether responses need Adaptive Cards.

## TypeSpec file map

| File | Required content |
| --- | --- |
| `main.tsp` | Imports `@typespec/http`, `@typespec/openapi3`, `@microsoft/typespec-m365-copilot`, and `./actions.tsp`; defines `@agent`, `@instructions`, namespace, and operation references. |
| `actions.tsp` | Imports `@typespec/http` and `@microsoft/typespec-m365-copilot`; defines `@service`, `@actions`, `@server("[API_BASE_URL]", "[API Name]")`, optional `@useAuth`, REST operations, and models. |
| `cards/card.json` | Optional Adaptive Card template referenced by `@card` when rich visual responses are required. |

Use these skeletons as the minimum shape:

```typescript
// main.tsp
import "@typespec/http";
import "@typespec/openapi3";
import "@microsoft/typespec-m365-copilot";
import "./actions.tsp";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;
using TypeSpec.M365.Copilot.Actions;

@agent({ name: "[Agent Name]", description: "[Description]" })
@instructions("""
  [Instructions for using the API operations]
""")
namespace [AgentName] {
  op operation1 is [APINamespace].operationName;
}
```

```typescript
// actions.tsp
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Actions;

@service
@actions(#{
  nameForHuman: "[API Display Name]",
  descriptionForModel: "[Model description]",
  descriptionForHuman: "[User description]"
})
@server("[API_BASE_URL]", "[API Name]")
@useAuth([AuthType])
namespace [APINamespace] {
  @route("[/path]")
  @get
  @action
  op operationName(@path param1: string, @query param2?: string): ResponseModel;

  model ResponseModel {
    // Response structure
  }
}
```

## Authentication patterns

| API requirement | TypeSpec pattern |
| --- | --- |
| Public API | Omit `@useAuth`; do not create placeholder auth models. |
| API key in header | `@useAuth(ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">)` |
| OAuth2 authorization code | `@useAuth(OAuth2Auth<[{ type: OAuth2FlowType.authorizationCode; authorizationUrl: "https://oauth.example.com/authorize"; tokenUrl: "https://oauth.example.com/token"; refreshUrl: "https://oauth.example.com/token"; scopes: ["read", "write"]; }]>)` |
| Registered auth reference | Define `@authReferenceId("registration-id-here") model Auth is ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">` and call `@useAuth(Auth)`. |

## Operation design rules

| Area | Rule |
| --- | --- |
| Operation names | Use clear action-oriented names such as `listProjects` or `createTicket`. |
| Models | Define TypeScript-like request and response models instead of anonymous blobs. |
| HTTP methods | Use `@get`, `@post`, `@patch`, and `@delete` to match the API contract. |
| Routes | Use RESTful paths with `@route`; bind variables with `@path`, `@query`, `@header`, and `@body`. |
| Descriptions | Fill `nameForHuman`, `descriptionForModel`, and `descriptionForHuman` with concrete language for model understanding. |
| Confirmations | Add confirmation dialogs for `delete`, critical `update`, payment, or irreversible operations. |
| Cards | Use `@card` for rich visual responses with multiple data items. |

## Capability decorators

```typescript
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "Confirm Action",
    body: """
    Are you sure you want to perform this action?
      * **Parameter**: {{ function.parameters.paramName }}
    """
  }
})
```

```typescript
@card(#{
  dataPath: "$.items",
  title: "$.title",
  url: "$.link",
  file: "cards/card.json"
})
```

```typescript
@reasoning("""
  Consider user's context when calling this operation.
  Prioritize recent items over older ones.
""")
@responding("""
  Present results in a clear table format with columns: ID, Title, Status.
  Include a summary count at the end.
""")
```

## Procedure

1. Ask or infer the API base URL, API purpose, required CRUD operations, authentication method, confirmation needs, and Adaptive Card needs.
2. Generate `main.tsp` with the agent definition and operation references.
3. Generate `actions.tsp` with service metadata, server, auth, routes, parameters, and request/response models.
4. Add `cards/card.json` only when the response design uses `@card`.
5. Review the generated TypeSpec for concrete names, no unresolved placeholders except user-approved placeholders, and correct auth decorators.

## Gotchas

- **Do not leave `[API_BASE_URL]` unresolved in final code** unless the user explicitly asks for a template.
- **Do not add `@useAuth` for public APIs**; placeholder auth breaks plugin setup.
- **Do not skip confirmations on destructive operations**; deletion and critical updates need `@capabilities` confirmation.
- **Do not model response bodies as untyped `object` when fields are known**; TypeSpec models improve action planning and OpenAPI output.

## Output template

```markdown
## TypeSpec API plugin

**Status:** complete | needs input | blocked
**Agent:** <agent name>
**API base URL:** <base URL or unresolved placeholder>

### Files
- `main.tsp`: <summary>
- `actions.tsp`: <summary>
- `cards/card.json`: <created | not needed>

### Operations
| Operation | Method | Route | Auth | Confirmation | Response |
| --- | --- | --- | --- | --- | --- |
| `<operationName>` | `<GET|POST|PATCH|DELETE>` | `<route>` | `<auth>` | `<yes|no>` | `<model/card>` |

### Validation
- Placeholder review: <pass|fail and evidence>
- Auth mapping: <pass|fail and evidence>
- Adaptive Card mapping: <pass|not applicable and evidence>
```

## Quality gate

- [ ] `main.tsp` imports required TypeSpec and Microsoft 365 Copilot libraries and references operations from `actions.tsp`.
- [ ] `actions.tsp` defines `@service`, `@actions`, `@server`, operations, models, and only the needed `@useAuth` pattern.
- [ ] Every operation has an HTTP verb, `@route`, parameter decorators, and a typed response model.
- [ ] Destructive operations include an Adaptive Card confirmation.
- [ ] `@card`, `@reasoning`, and `@responding` are used only when they add concrete behavior.
- [ ] Any remaining placeholder such as `[AgentName]` or `[API_BASE_URL]` is intentional and reported.
