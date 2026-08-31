---
name: "azure-role-selector"
description: >-
  Select the least-privilege Azure RBAC role for an identity, compare built-in and custom role options, and produce assignment commands or Bicep snippets. Use this skill when the user asks which Azure role to assign for permissions, scopes, identities, data-plane access, control-plane access, custom roles, or access requirements.
allowed-tools: [Azure MCP/documentation, Azure MCP/bicepschema, Azure MCP/extension_cli_generate, Azure MCP/get_bestpractices]
---

# Azure role selector

Select the minimal Azure RBAC role that grants the requested actions at the narrowest safe scope, then return the matching built-in or custom role option with Azure CLI assignment commands and a Bicep role assignment snippet.

## When to invoke

- "Which Azure RBAC role should I assign for this identity?"
- "Find the least-privilege role for these Azure permissions."
- "Generate an az role assignment command for this service principal."
- "Should this use a built-in role or a custom role?"
- "Provide a Bicep snippet for this role assignment."

## Prerequisites and context

- Use `Azure MCP/documentation` to find minimal built-in role definitions and confirm `Actions`, `NotActions`, `DataActions`, and `NotDataActions`.
- Use `Azure MCP/extension_cli_generate` to generate Azure CLI commands and to create a custom role definition when no built-in role matches the required permissions.
- Use `Azure MCP/bicepschema` and `Azure MCP/get_bestpractices` to produce Bicep role assignment snippets and current Azure best-practice guidance.
- Require the identity, scope, and permissions. If any are missing, infer only when the repository or user request provides clear evidence; otherwise state the missing input.

## Inputs to resolve

| Input | Required detail | Examples |
| --- | --- | --- |
| Identity | Principal type and object/principal ID or resolvable name | user, group, service principal, managed identity |
| Scope | Narrowest resource boundary that needs access | management group, subscription, resource group, storage account, Key Vault |
| Permissions | Operations the identity must perform | read metrics, restart web app, pull image, read blobs, manage secrets |
| Plane | Control plane or data plane | `Actions` for ARM management; `DataActions` for data access |
| Duration | Permanent, temporary, or Privileged Identity Management workflow | standing assignment, eligible assignment, break-glass |

## Selection criteria

| Decision | Rule |
| --- | --- |
| Least privilege | Choose the narrowest built-in role whose allowed operations cover the required actions without broad unrelated permissions. |
| Scope minimization | Assign at the resource scope when possible; move to resource group, subscription, or management group only when the required operation spans that scope. |
| Built-in before custom | Prefer a built-in role when it matches cleanly. Create a custom role only when built-ins are too broad or miss required operations. |
| Control plane vs data plane | Do not confuse ARM management with data access. For example, managing a storage account is different from reading blobs. |
| Wildcards | Treat `*`, broad `Microsoft.Authorization/*`, and owner-like roles as high risk unless the request explicitly requires administration. |
| Deny exclusions | Check `NotActions` and `NotDataActions`; an apparent match is invalid if exclusions remove a required operation. |

## Role matching workflow

1. Normalize the user's requested access into Azure operation names where possible.
2. Determine the target scope and whether each permission is control-plane `Actions` or data-plane `DataActions`.
3. Query Azure role documentation with `Azure MCP/documentation` and compare candidate built-in roles.
4. Select the least-privilege built-in role when one covers the requested permissions.
5. If no built-in role matches, use `Azure MCP/extension_cli_generate` to produce a custom role definition containing only the required `Actions` or `DataActions`.
6. Generate an assignment command with `Azure MCP/extension_cli_generate`.
7. Generate a Bicep snippet with `Azure MCP/bicepschema` and validate it against `Azure MCP/get_bestpractices`.

## Common Azure RBAC distinctions

| Request pattern | Check carefully |
| --- | --- |
| "Read a resource" | Reader may cover management metadata but not data-plane contents such as blobs, secrets, queues, or database rows. |
| "Deploy resources" | Contributor can create resources but cannot grant access; role assignment requires `Microsoft.Authorization/roleAssignments/write`. |
| "Manage access" | User Access Administrator grants role assignment management without full Owner permissions. |
| "Use Key Vault" | Separate secret, key, and certificate data operations from vault management operations. |
| "Use Storage" | Separate storage account management from blob, queue, table, or file data access roles. |
| "Pull container images" | Registry pull is narrower than contributor permissions on the registry. |
| "Managed identity access" | The consuming identity needs permissions at the target resource; the app host may also need permission to use or attach the identity. |

## Assignment artifacts

| Artifact | Include | Notes |
| --- | --- | --- |
| Azure CLI command | `az role assignment create --assignee <principal> --role "<role-name-or-id>" --scope <scope>` | Prefer role ID for custom roles or ambiguous names. |
| Custom role JSON | `Name`, `IsCustom`, `Description`, `Actions`, `NotActions`, `DataActions`, `NotDataActions`, `AssignableScopes` | Include only when no suitable built-in role exists. |
| Bicep snippet | `Microsoft.Authorization/roleAssignments` with deterministic `guid()` name | Role assignment name must be stable for the same principal, role, and scope. |
| Explanation | Why the selected role is least privilege and which broader roles were rejected | Mention major excluded permissions and risk. |

## Gotchas

- **Reader is not data reader**: many Azure services require data-plane roles even when the identity can view the resource in the portal.
- **Contributor cannot assign roles**: access management needs role assignment permissions, commonly via Owner or User Access Administrator.
- **Scope inheritance is powerful**: subscription-scope assignments flow to every child resource; prefer the smallest scope that satisfies the requirement.
- **Custom roles need assignable scopes**: a custom role cannot be assigned outside its `AssignableScopes`.
- **Role names can be ambiguous**: use role definition IDs when generating durable automation.

## Open Horizons integration

- Scope role selection to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons least-privilege, managed-identity, Azure scope, and evidence boundaries.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

````markdown
## Azure role selection

**Status:** built-in selected | custom role required | blocked
**Identity:** <principal type and identifier>
**Scope:** `<scope>`
**Plane:** control plane | data plane | both

### Recommendation
| Role | Type | Why it matches | Broader roles rejected |
| --- | --- | --- | --- |
| `<role name or custom role name>` | built-in/custom | <required permissions covered> | <roles and reason> |

### Assignment command
```bash
az role assignment create --assignee <principal-id> --role "<role-name-or-id>" --scope <scope>
```

### Bicep
```bicep
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(<scope-id>, '<principal-id>', '<role-definition-id>')
  scope: <scope-symbol>
  properties: {
    principalId: '<principal-id>'
    roleDefinitionId: '<role-definition-resource-id>'
    principalType: '<User|Group|ServicePrincipal|ForeignGroup|Device>'
  }
}
```

### Custom role definition
<include only when no built-in role matches>
````

## Quality gate

- [ ] The identity, scope, and required permissions are stated or listed as blockers.
- [ ] `Azure MCP/documentation` was used to compare built-in role definitions.
- [ ] The selected role is the least-privilege match and broader roles are explicitly rejected.
- [ ] Control-plane `Actions` and data-plane `DataActions` are not confused.
- [ ] `NotActions` and `NotDataActions` do not exclude required permissions.
- [ ] `Azure MCP/extension_cli_generate` was used for assignment commands and custom role definitions when needed.
- [ ] `Azure MCP/bicepschema` and `Azure MCP/get_bestpractices` were used for the Bicep snippet.
- [ ] The CLI command and Bicep snippet use the narrowest safe scope.
