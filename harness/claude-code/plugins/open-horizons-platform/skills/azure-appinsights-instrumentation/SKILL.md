---
name: azure-appinsights-instrumentation
description: >-
  Instrument Azure-hosted web apps with Azure Application Insights telemetry by choosing
  auto-instrumentation or code instrumentation for ASP.NET Core, Node.js, or Python. Use when the
  user wants to enable telemetry, observe app health, create an App Insights resource, or wire
  instrumentation into a webapp.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/azure-appinsights-instrumentation/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure AppInsights instrumentation

Identify the app stack and Azure hosting model, create or reuse Application Insights infrastructure, and add the minimum code or platform configuration needed for useful telemetry, preferring auto-instrument paths when they fit.

## When to invoke

- "Enable Application Insights for this webapp."
- "Instrument my ASP.NET Core app with App Insights."
- "Add telemetry to a Node.js or Python app hosted in Azure."
- "Create the App Insights resource and wire the connection string."

## Prerequisites and context

- The workspace app should be an ASP.NET Core app, a Node.js app, or a Python web app.
- The hosting target should be known: Azure App Service as code, Azure App Service as container, Azure Container Apps, local development, or another Azure host.
- Azure resource creation requires an authenticated Azure CLI or existing Bicep deployment workflow.
- Prefer the same resource group as the hosted app unless the user's resource organization requires a different one.

## Procedure

1. Inspect source files to infer the programming language, application framework, and hosting tuple.
2. Ask for or infer the Azure hosting model before choosing instrumentation. In non-interactive execution, state the assumption and choose the safest documented path.
3. Prefer Azure App Service auto-instrumentation for C# ASP.NET Core hosted in Azure App Service; use `references/AUTO.md`.
4. If auto-instrumentation does not fit, create or update the Application Insights resource through existing Bicep or Azure CLI.
5. Modify application code using the stack-specific guide: `references/ASPNETCORE.md`, `references/NODEJS.md`, or `references/PYTHON.md`.
6. Validate that configuration uses the Application Insights connection string or the platform-supported setting and that telemetry can be emitted without hardcoded secrets.

## Instrumentation decision table

| App and hosting | Preferred path | Files to consult |
| --- | --- | --- |
| ASP.NET Core on Azure App Service | Auto-instrument first. | `references/AUTO.md` |
| ASP.NET Core requiring code instrumentation | Add SDK/configuration in app startup. | `references/ASPNETCORE.md` |
| Node.js web app | Add Node.js Application Insights initialization as early as possible in process startup. | `references/NODEJS.md` |
| Python web app | Add Python instrumentation appropriate to the framework and startup path. | `references/PYTHON.md` |
| Existing Bicep infrastructure | Add the App Insights resource to the template. | `examples/appinsights.bicep` |
| No IaC available | Use Azure CLI commands from the script as a model. | `scripts/appinsights.ps1` |

## Infrastructure rules

- Add Application Insights to existing Bicep when the workspace already contains Bicep templates.
- Use Azure CLI from `scripts/appinsights.ps1` when no infrastructure-as-code path exists.
- Do not hardcode instrumentation keys, connection strings, subscription IDs, tenant IDs, or secrets in source code.
- Store runtime configuration in Azure app settings, environment variables, or the repository's existing secret mechanism.
- Instrument useful telemetry: request/dependency tracking, exceptions, logs/traces, and custom events only when they answer an operational question.

## Progressive disclosure and bundled resources

- `references/AUTO.md`: Azure App Service auto-instrumentation guidance.
- `references/ASPNETCORE.md`: ASP.NET Core code changes.
- `references/NODEJS.md`: Node.js JavaScript/TypeScript code changes.
- `references/PYTHON.md`: Python web app code changes.
- `examples/appinsights.bicep`: Bicep resource example.
- `scripts/appinsights.ps1`: Azure CLI command model for creating the resource.

## Output template

```markdown
## Application Insights instrumentation result

**Status:** instrumented | recommendation only | blocked
**App stack:** `<language, framework, hosting>`
**Instrumentation path:** auto-instrumentation | ASP.NET Core SDK | Node.js SDK | Python SDK | infrastructure only

| Change | File/resource | Evidence |
| --- | --- | --- |
| `<resource created or code updated>` | `<path or Azure resource>` | `<setting, package, or snippet>` |

### Configuration
- Application Insights resource group: `<resource group or assumed target>`
- Connection setting location: `<app setting/env var/IaC output>`

### Validation
- Telemetry startup path checked: <yes/no>
- Secret hardcoding avoided: <yes/no>
```

## Quality gate

- [ ] The app's language, framework, and hosting model were identified or an assumption was explicitly stated.
- [ ] Auto-instrumentation was considered before code instrumentation for ASP.NET Core on Azure App Service.
- [ ] Existing Bicep was preferred over ad hoc CLI resource creation when present.
- [ ] The Application Insights connection string or equivalent setting is configured outside source code.
- [ ] The stack-specific bundled reference was used before changing code.
- [ ] The result explains how telemetry can be validated after deployment.
