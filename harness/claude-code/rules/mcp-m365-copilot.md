---
paths:
  - "**/{*mcp*,*agent*,*plugin*,declarativeAgent.json,ai-plugin.json,mcp.json,manifest.json}"
---

<!-- Generated from harness/github-copilot/instructions/mcp-m365-copilot.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces conventions for MCP-based Microsoft 365 Copilot declarative agents, API plugins, adaptive cards, authentication, testing, deployment, and governance.

# MCP M365 Copilot Conventions — Declarative Agents and Plugins

These instructions apply to Microsoft 365 Copilot declarative agent, API plugin, MCP server configuration, and Teams app manifest files matched by the `applyTo` globs. They are authoritative for MCP-first agent design, `declarativeAgent.json`, `ai-plugin.json`, `mcp.json`, adaptive card response semantics, authentication, local testing, deployment readiness, performance, security, and governance in those files; organization policy, product documentation, and security primitives win when they impose stricter requirements.

## MCP-First Agent Design

Build Microsoft 365 Copilot agents around Model Context Protocol servers and declarative configuration.

| Principle | Convention |
| --- | --- |
| Model Context Protocol first | Import tools from MCP server endpoints and let MCP handle schema discovery and function generation |
| Declarative over imperative | Put behavior in `declarativeAgent.json`, tools and response semantics in `ai-plugin.json`, and server connection metadata in `mcp.json` |
| Least privilege | Import only necessary tools, group related tools from the same server, and test each tool individually before combining them |
| User-centered output | Provide clear conversation starters and adaptive cards that render well in Chat, Teams, and Outlook |

Use point-and-click tool selection in Agents Toolkit when it is available. Avoid hand-writing tool definitions that duplicate MCP metadata unless the platform requires generated plugin artifacts.

## Project Files and Responsibilities

Keep the standard package layout recognizable so Teams Toolkit and Microsoft 365 Agents Toolkit can provision, deploy, and sideload consistently.

```text
project-root/
├── appPackage/
│   ├── manifest.json
│   ├── declarativeAgent.json
│   ├── ai-plugin.json
│   ├── color.png
│   └── outline.png
├── .vscode/
│   └── mcp.json
├── .env.local
└── teamsapp.yml
```

| File | Owns |
| --- | --- |
| `appPackage/manifest.json` | Teams app manifest, app identity, icons, and package metadata |
| `appPackage/declarativeAgent.json` | Agent name, description, instructions, conversation starters, and capabilities |
| `appPackage/ai-plugin.json` | Imported MCP tools, function definitions, response semantics, `data_path`, `properties`, static adaptive card templates, and template selection |
| `.vscode/mcp.json` | MCP server URL, server metadata endpoint, and authentication reference |
| `.env.local` | OAuth client credentials, API keys, secrets, and environment-specific config; add it to `.gitignore` and never commit it |
| `teamsapp.yml` | Teams Toolkit provisioning and deployment configuration |

## Authentication and Server Configuration

Use OAuth 2.0 or Microsoft Entra ID SSO for authenticated tools. Validate that every MCP server uses HTTPS, reliable uptime, secure endpoints, and well-structured response data.

| Scenario | Required fields and examples |
| --- | --- |
| OAuth 2.0 static registration | `type: OAuthPluginVault`, `reference_id: YOUR_AUTH_ID`, `client_id`, `client_secret`, `authorization_url: https://github.com/login/oauth/authorize`, `token_url: https://github.com/login/oauth/access_token`, `scope: repo read:user` |
| SSO with Microsoft Entra ID | `type: OAuthPluginVault`, `reference_id: sso_auth`, `authorization_url: https://login.microsoftonline.com/common/oauth2/v2.0/authorize`, `token_url: https://login.microsoftonline.com/common/oauth2/v2.0/token`, `scope: User.Read` |
| Multi-tool agents | Configure `mcpServers` entries such as `github` at `https://github-mcp.example.com` and `jira` at `https://jira-mcp.example.com`, then import only the tools the agent needs |

Keep OAuth scopes minimal, use separate credentials for development and production, rotate credentials regularly, and test the authentication flow outside Copilot before organizational deployment. Authenticated actions follow this path: the user triggers a tool, OAuth redirects for consent, the access token is stored in the plugin vault, and subsequent requests use the stored token.

## Response Semantics and Adaptive Cards

Use response semantics to extract the smallest useful payload from MCP responses and render it in static, responsive cards.

| Concern | Convention |
| --- | --- |
| Data extraction | Use JSONPath such as `data_path: $.items[*]` to select relevant items |
| Field mapping | Map `properties` such as `title: $.name`, `subtitle: $.description`, and `url: $.html_url` |
| Template selection | Use `template_selector: $.templateType` only when responses genuinely require dynamic templates |
| Static templates | Prefer static templates in `ai-plugin.json` when responses share one shape |
| Card layout | Use a single-column layout, `stretch` or `auto` widths, small images, and simple scannable content |
| Card elements | Use `TextBlock` for titles and descriptions, `FactSet` for key-value metadata, `Image` for icons or thumbnails, `Container` for grouping, and `ActionSet` for buttons |

Adaptive card template language may use conditionals like `${if(status == 'active', ' Active', ' Inactive')}`, data binding like `${title}`, number formatting like `${formatNumber(score, 0)}`, and conditional rendering with `$when: ${count(items) > 0}`. Test cards across Chat, Teams, and Outlook because host rendering differences affect layout.

## Testing, Deployment, and Governance

Local testing follows the Teams Toolkit loop: Provision, Deploy, sideload to Teams, test at `https://m365.cloud.microsoft/chat`, then iterate and redeploy. Organization deployment requires IT admin approval in the Microsoft 365 admin center and assignment to all users or selected users and groups. Agent Store submission goes through Partner Center validation and requires a rigorous security review before public availability.

Govern deployed agents through admin controls and monitoring. Agents can be blocked, deployed to specific users or groups, or published organization-wide. Track usage and adoption, error rates and performance, user feedback and satisfaction, security incidents, configuration change history, access logs for sensitive operations, deployment approval records, and compliance attestations.

## Error Handling, Performance, and Privacy

Provide clear agent messages for MCP server errors, fall back to alternative tools only when an equivalent safe tool exists, log errors for debugging without sensitive data, and guide the user to retry or choose another path. For authentication failures, check `.env.local`, verify scopes, test consent and token refresh, and ensure credentials match the configured `reference_id`. For response parsing failures, validate JSONPath expressions, handle missing or null data, provide defaults, and test varied API responses.

Optimize performance by importing only necessary tools, avoiding redundant tools from multiple servers, measuring each tool's response time, filtering data through `data_path`, limiting result sets, using pagination for large datasets, and keeping adaptive cards lightweight. MCP servers may cache where appropriate; consider cache invalidation for time-sensitive data and remember that Microsoft 365 may cache agent responses.

Protect privacy by requesting minimum scopes, avoiding sensitive user data in logs, reviewing data residency requirements, following compliance policies such as GDPR, verifying that each MCP server is trusted, checking the server privacy policy, and testing for injection vulnerabilities.


## Preserved Plugin Vocabulary

Keep compatibility vocabulary from existing Microsoft 365 Copilot examples when rewriting plugin configuration.

| Vocabulary | Convention |
| --- | --- |
| `CRITICAL`, `NEVER`, `over-scoping`, and `auto-generated` | Use all-caps only for genuinely critical constraints such as secret handling; avoid over-scoping tools and preserve auto-generated function definitions from MCP metadata. |
| `github_client_id` and `github_client_secret` | Treat these as illustrative OAuth placeholder names only; actual secrets belong in `.env.local`, environment variables, or vault references. |
| `dev/prod` | Keep separate dev/prod credentials and deployments. |
| `end-to-end`, `follow-up`, and `re-deploy` | Test auth end-to-end, include follow-up card actions only when useful, and re-deploy after configuration changes. |
| `users/groups` | Organization deployment may target all users/groups or selected users/groups through admin controls. |
| `DevBlogs` | The Microsoft 365 DevBlogs article remains an authoritative external reference for MCP declarative agent patterns. |

## Good / Bad Examples

The examples below illustrate scoped response extraction and safe authentication metadata.

**Good:**

```json
{
  "data_path": "$.items[*]",
  "properties": {
    "title": "$.name",
    "subtitle": "$.description",
    "url": "$.html_url"
  }
}
```

Why: The plugin extracts only the list items the card needs and maps stable fields for predictable rendering.

**Bad:**

```json
{
  "data_path": "$",
  "properties": {
    "title": "$.*"
  }
}
```

Why: The plugin exposes an oversized response shape, makes card rendering unpredictable, and increases token and privacy risk.

## Conventions

| Rule | Rationale |
|---|---|
| Import tools from MCP server endpoints instead of manual definitions | MCP discovery keeps schemas and functions aligned with the server |
| Keep behavior declarative in `declarativeAgent.json`, `ai-plugin.json`, and `mcp.json` | Agents Toolkit and Copilot can validate, package, and govern the agent |
| Select only necessary tools and scopes | Least privilege reduces token usage, consent friction, and data exposure |
| Store credentials in `.env.local`, environment variables, or vault-backed references and add `.env.local` to `.gitignore` | Secrets must not be committed |
| Use OAuth 2.0 or SSO with HTTPS MCP endpoints | Authentication and transport stay compatible with organizational governance |
| Use `data_path`, `properties`, static adaptive card templates, and lightweight layouts | Responses remain fast, predictable, and readable across hubs |
| Test each MCP tool, authentication flow, adaptive card, response semantic, and error path before deployment | Agent failures are easier to isolate before organizational rollout |
| Maintain deployment approvals, access logs, change history, and compliance attestations | Admins can audit and govern business agents |

## Do / Do Not

| Do | Do not |
|---|---|
| Configure MCP servers in `mcp.json` and import tools through Agents Toolkit | Hand-author duplicate tool schemas when MCP discovery can supply them |
| Use `OAuthPluginVault`, `YOUR_AUTH_ID`, OAuth URLs, token URLs, and least-privilege scopes | Store client secrets in `ai-plugin.json`, `manifest.json`, or source control |
| Use static adaptive card templates for stable response shapes | Add dynamic templates when one static shape is sufficient |
| Test in Chat, Teams, Outlook, and https://m365.cloud.microsoft/chat | Assume one host's rendering represents every Microsoft 365 hub |
| Limit result sets and paginate large responses | Send full upstream payloads to Copilot or cards |
| Log operational errors without sensitive user data | Log access tokens, secrets, or private business data |
| Use Microsoft 365 admin center or Partner Center deployment flows as appropriate | Bypass approval and compliance review for organizational agents |

## Checklist Before Opening a PR

- [ ] `declarativeAgent.json`, `ai-plugin.json`, `mcp.json`, `manifest.json`, icons, `.env.local`, and `teamsapp.yml` responsibilities remain separated.
- [ ] MCP tools are imported from secure server endpoints and only necessary tools are selected.
- [ ] OAuth 2.0 or SSO configuration uses HTTPS authorization and token URLs, minimal scopes, and a stable `reference_id`.
- [ ] `.env.local` is ignored and no API keys, OAuth client secrets, tokens, or environment-specific secrets are committed.
- [ ] Response semantics use correct JSONPath `data_path`, `properties`, and template selection only where needed.
- [ ] Adaptive cards use responsive single-column layouts and render correctly in Chat, Teams, and Outlook.
- [ ] Each MCP tool, authentication flow, error path, and varied API response has been tested before deployment.
- [ ] Organization deployment or Agent Store submission has the required approval, security review, and compliance evidence.
- [ ] Monitoring, audit logs, change history, and deployment records are updated for governed agents.

## References

- Build Declarative Agents with MCP: https://devblogs.microsoft.com/microsoft365dev/build-declarative-agents-for-microsoft-365-copilot-with-mcp/
- Build MCP Plugins: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/build-mcp-plugins
- API Plugin Adaptive Cards: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-plugin-adaptive-cards
- Manage Copilot Agents: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-copilot-agents-integrated-apps
- Microsoft 365 Copilot Chat test hub: https://m365.cloud.microsoft/chat
