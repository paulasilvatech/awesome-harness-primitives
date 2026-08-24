---
name: "foundry-agent-sync"
description: >-
  Create, register, deploy, update, and synchronize prompt-based Azure AI Foundry agents from a local JSON manifest using the Agent Service REST API. Use when users ask to sync Foundry agents, create agents in Foundry, push agents, update agent instructions, scaffold a foundry-agents.json manifest, or add sync scripts.
---

# Foundry agent sync

Synchronize prompt-based agents from a local manifest into Azure AI Foundry by creating or updating server-side agents through named REST calls, then verify they are available in the Foundry project.

## When to invoke

- "Create an agent in Foundry from this manifest."
- "Sync Foundry agents."
- "Deploy, register, or push agents to Foundry."
- "Update Foundry agent instructions."
- "Scaffold a foundry agent manifest and sync script."

## Prerequisites and context

| Requirement | Details |
| --- | --- |
| Foundry project | Azure AI Foundry project with a deployed model such as `gpt-5-4`. |
| Auth | Azure CLI `az` authenticated to the subscription. |
| Role | **Azure AI User** or higher on the Foundry project resource. |
| Endpoint | Foundry project endpoint from Azure Portal → AI Foundry project → Overview → Endpoint, or `az resource show`. |
| Subscription ID | `az account show --query id -o tsv`. |
| Model deployment name | The model deployment in the project, for example `gpt-5-4`. |

This skill creates agents inside AI Foundry server-side. It does not scaffold local agent code or container images.

## Manifest contract

Look for `foundry-agents.json` at `infra/foundry-agents.json`, `foundry-agents.json`, or `.foundry/agents.json`. If none exists, ask what agents are needed and scaffold one.

```json
[
  {
    "useCaseId": "alert-triage",
    "description": "Short description of what this agent does.",
    "baseInstruction": "You are an assistant that... <system prompt for the agent>"
  }
]
```

| Field | Required | Rule |
| --- | --- | --- |
| `useCaseId` | Yes | Kebab-case identifier; used in `{prefix}-{useCaseId}`. |
| `description` | Yes | Human-readable description stored as metadata. |
| `baseInstruction` | Yes | System prompt / base instructions for the agent. |

## Procedure

1. Locate or scaffold the manifest.
2. Locate `infra/scripts/sync-foundry-agents.ps1` or `foundry-agent-sync.sh`; scaffold the PowerShell script when missing and adapt `$AgentNamePrefix`, `$ModelName`, and `$ManifestPath`.
3. Collect Foundry project endpoint, subscription ID, model deployment name, and agent name prefix. Default model can be `gpt-5-4`; default prefix can be repo name in kebab-case.
4. Authenticate and sync with a token for `https://ai.azure.com/`.
5. Verify by listing agents from the project endpoint.

Run the PowerShell sync like this:

```powershell
.\infra\scripts\sync-foundry-agents.ps1 `
  -SubscriptionId '<sub-id>' `
  -ProjectEndpoint '<endpoint>' `
  -ModelName '<model>' `
  -AgentNamePrefix '<prefix>'
```

## Sync implementation details

| Concern | Required detail |
| --- | --- |
| Script path | Canonical path is `infra/scripts/sync-foundry-agents.ps1`, adapted to repository layout. |
| Parameters | `$SubscriptionId`, `$ProjectEndpoint`, `$ManifestPath`, `$ModelName`, `$AgentNamePrefix`, `$ApiVersion = '2025-11-15-preview'`. |
| Token | `az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv`. |
| Create/update body | `definition.kind = 'prompt'`, `definition.model = $ModelName`, `definition.instructions = $instructions`, `description = $def.description`, `metadata.useCaseId = $def.useCaseId`, `metadata.managedBy = 'foundry-agent-sync'`. |
| Create/update URI | `$ProjectEndpoint.TrimEnd('/') + '/agents/' + $agentName + '?api-version=' + $ApiVersion`. |
| Result handling | Capture `$resp.version`, `$resp.latest_version`, `$resp.id`, or `unknown`; print `Synced $agentName ($version)`. |
| Secret handling | Never print the bearer token; use redacted headers in examples such as `Authorization = "******"`. |

For automated Bicep deployment, use `loadJsonContent('foundry-agents.json')`, create a User-Assigned Managed Identity with the Azure AI User role, and create a `Microsoft.Resources/deploymentScripts` resource of kind `AzureCLI` that uses `loadTextContent`, the managed identity, endpoint, definitions, and model environment variables. Gate the script behind `deployFoundryAgents`.

For bash in `Microsoft.Resources/deploymentScripts`, authenticate with `az login --identity --username "$CLIENT_ID"`, acquire the token with `az account get-access-token --resource https://ai.azure.com/`, iterate definitions from `FOUNDRY_AGENT_DEFINITIONS`, and POST each agent to `{endpoint}/agents/{name}?api-version=2025-11-15-preview`.

## REST API reference

| Operation | Method | URL |
| --- | --- | --- |
| Create/update agent | POST | `{projectEndpoint}/agents/{agentName}?api-version=2025-11-15-preview` |
| List agents | GET | `{projectEndpoint}/agents?api-version=2025-11-15-preview` |
| Get agent | GET | `{projectEndpoint}/agents/{agentName}?api-version=2025-11-15-preview` |
| Delete agent | DELETE | `{projectEndpoint}/agents/{agentName}?api-version=2025-11-15-preview` |

Payload:

```json
{
  "definition": {
    "kind": "prompt",
    "model": "<deployed-model-name>",
    "instructions": "<system prompt>"
  },
  "description": "<agent description>",
  "metadata": {
    "useCaseId": "<use-case-id>",
    "managedBy": "foundry-agent-sync"
  }
}
```

## Troubleshooting

| Symptom | Cause | Resolution |
| --- | --- | --- |
| `401 Unauthorized` | Token expired or wrong audience. | Re-run `az account get-access-token --resource https://ai.azure.com/`. |
| `403 Forbidden` | Missing Azure AI User role. | Assign the role on the Foundry project scope. |
| `404 Not Found` | Wrong project endpoint. | Verify the endpoint includes `/api/projects/{projectName}`. |
| Model not found | Model is not deployed in the project. | Deploy the model in the AI Foundry portal first. |
| Empty definitions | Manifest path is wrong. | Check `-ManifestPath` points to the JSON file. |

## Script and API vocabulary

The local scaffold boundary is the `microsoft-foundry` skill's `create` sub-skill; this skill syncs server-side agents. Preserve `sync-foundry-agents.ps1`, `project-endpoint`, `endpoint/agents`, Create/Update semantics, opt in/out. gates, and `application/json` content type.

PowerShell implementations commonly use `$ErrorActionPreference`, `Get-Content | ConvertFrom-Json`, `ConvertFrom`, `ConvertTo-Json`, `ConvertTo`, `Invoke-RestMethod`, `RestMethod`, `-ContentType 'application/json'`, and `Format-Table -AutoSize`.

## Output template

```markdown
## Foundry agent sync result

**Status:** synced | scaffolded | blocked
**Endpoint:** `<project endpoint>`
**Manifest:** `<manifest path>`

### Agents
| Agent | useCaseId | Version | Action |
| --- | --- | --- | --- |
| `<prefix>-<useCaseId>` | `<useCaseId>` | `<version or unknown>` | created | updated | verified |

### Commands
- `az account set --subscription <subscription>`
- `az account get-access-token --resource https://ai.azure.com/`
- `<sync script command>`

### Validation
- List agents: <pass/fail and evidence>
```

## Quality gate

- [ ] Manifest exists or was scaffolded with `useCaseId`, `description`, and `baseInstruction`.
- [ ] Endpoint, subscription ID, model deployment name, and agent name prefix are known.
- [ ] Token audience is `https://ai.azure.com/` and the token is not printed.
- [ ] Agent names are built from `{prefix}-{useCaseId}`.
- [ ] REST calls use `api-version=2025-11-15-preview`.
- [ ] Sync is idempotent create/update by named POST.
- [ ] Verification lists agents after sync or reports the blocker.
