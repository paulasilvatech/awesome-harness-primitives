---
name: msgraph-sdk
description: >-
  Integrate Microsoft Graph SDK in .NET, TypeScript/JavaScript, or Python applications using
  correct authentication, permissions, SDK clients, pagination, batching, delta queries, change
  notifications, throttling, and Microsoft 365 resource paths. Use when accessing users, mail,
  calendar, Teams, OneDrive, SharePoint, groups, search, or other Microsoft 365 data through
  Graph.
---

<!-- Generated from harness/github-copilot/plugins/microsoft-365-data-platform/skills/msgraph-sdk/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Microsoft Graph SDK

Implement Microsoft Graph access with the current language SDK, the right authentication flow, least-privilege permissions, pagination, retry handling, and resource-specific patterns.

## When to invoke

- "Add Microsoft Graph SDK to this app."
- "Call Graph to read users, mail, calendar, Teams, files, or SharePoint data."
- "Choose the right Graph authentication flow for this service."
- "Handle Graph paging, throttling, batching, or delta sync."
- "Fix Microsoft Graph 403, 429, subscription, or permission issues."

## Progressive disclosure and bundled resources

| Reference | Use when |
| --- | --- |
| `references/dotnet.md` | Project contains `.cs`, `.csproj`, `.sln`, or user asks for C#/.NET. |
| `references/typescript.md` | Project contains `package.json`, `.ts`, `.js`, or user asks for Node.js/browser. |
| `references/python.md` | Project contains `.py`, `pyproject.toml`, `requirements.txt`, or user asks for Python. |

Read the language reference before writing SDK-specific code.

## Language and documentation selection

1. Determine the target language from files or user request.
2. If multiple languages are present, match the files being edited or ask the user.
3. Ground implementation in current Microsoft Graph SDK docs and version-specific samples rather than memory.
4. Use Graph Explorer to test paths and permissions before coding when feasible.

## Authentication decision table

| Scenario | Flow |
| --- | --- |
| Background service or daemon with no user | Client credentials, app-only permissions. |
| Agent or API acting for a signed-in user | On-Behalf-Of (OBO), delegated permissions. |
| Azure Function, Container App, VM, or Azure-hosted service | Managed Identity, usually through `DefaultAzureCredential`. |
| CLI tool or local dev script | Device code or interactive browser. |
| Browser-only single-page app | Authorization code + PKCE. |

Never use client credentials when a user context is required. Prefer `DefaultAzureCredential` in Azure-hosted apps. Never hardcode secrets; use environment variables, Azure Key Vault, Secret Manager, or managed identity.

## Core SDK patterns

| Concern | Rule |
| --- | --- |
| Client lifetime | Construct `GraphServiceClient` once and reuse it. |
| Credentials | Pass an Azure Identity credential or language-specific auth provider; do not hand-roll raw HTTP auth. |
| Async calls | Always `await` SDK calls. |
| Projection | Use `$select` to limit returned fields. |
| Filtering | Use `$filter` server-side instead of in-memory filtering. |
| Expansion | Use `$expand` for small related resources. |
| Pagination | Check `@odata.nextLink` and use the SDK `PageIterator`; set `$top` when useful. |
| Batching | Use `$batch` for up to 20 independent Graph calls; match responses by request `id`. |
| Delta sync | Store `@odata.deltaLink` durably and reuse it for incremental changes. |
| Webhooks | Create `POST /subscriptions`, echo `validationToken` as plain text with HTTP 200, and renew before `expirationDateTime`. |
| Throttling | Handle HTTP 429 by honoring `Retry-After`; avoid uncontrolled fan-out. |

## Advanced Graph patterns

| Pattern | Use when | Critical detail |
| --- | --- | --- |
| Delta queries | Sync users, groups, messages, calendar events, Teams channels, and supported resources incrementally. | First call such as `GET /users/delta` returns all items plus `@odata.deltaLink`; subsequent calls use the link. |
| Change notifications | Need near-real-time updates. | Notification URL must be HTTPS; handle lifecycle notifications with `notificationUrl` and `lifecycleNotificationUrl`. |
| Resource data notifications | High-volume scenarios need changed resource payloads. | Requires additional encryption setup. |
| Retry middleware | Production workloads may hit 429. | Enable SDK retry middleware or implement exact `Retry-After` waits. |
| Least privilege | Avoid broad permissions. | Use https://learn.microsoft.com/graph/permissions-reference and admin consent only when required. |

## Common resource paths

| Goal | Resource path |
| --- | --- |
| Get signed-in user's profile | `GET /me` |
| List user's mailbox messages | `GET /me/messages` |
| Send an email | `POST /me/sendMail` |
| List calendar events | `GET /me/events` |
| Get user's OneDrive root | `GET /me/drive/root/children` |
| List Teams the user is in | `GET /me/joinedTeams` |
| Post a Teams channel message | `POST /teams/{id}/channels/{id}/messages` |
| List SharePoint site lists | `GET /sites/{siteId}/lists` |
| Search across M365 | `POST /search/query` |
| List all users in tenant | `GET /users` |
| Get group members | `GET /groups/{id}/members` |

Use the SDK fluent API equivalent, for example `client.Users[userId].Messages.GetAsync(...)` in .NET where appropriate.

## Procedure

1. Identify target language and read the matching `references/` file.
2. Select auth flow from the scenario table and confirm application versus delegated permissions.
3. Check Microsoft Graph overview, Graph Explorer, and permissions reference for current endpoint and scope requirements.
4. Implement a reused `GraphServiceClient` with the language-specific SDK package.
5. Add `$select`, `$filter`, pagination, and retry handling from the start.
6. For dashboards, consider batching; for synchronization, prefer delta queries; for event-driven workloads, use change notifications.
7. Validate 403, 429, subscription, and paging behavior with concrete evidence.

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `built-in`
- `deltaLink`
- `high-call-count`
- `high-volume`
- `mail/calendar`
- `users/groups`

## Output template

```markdown
## Microsoft Graph SDK result

**Status:** implemented | planned | blocked
**Language:** .NET | TypeScript/JavaScript | Python
**Auth flow:** client credentials | OBO | managed identity | device code | interactive browser | auth code + PKCE

### Permissions
| Operation | Permission | Type | Consent |
| --- | --- | --- | --- |
| `<Graph path>` | `<scope>` | Application/Delegated | <admin/user> |

### Implementation notes
- Client: `GraphServiceClient` reused: <yes/no>
- Pagination: <PageIterator/nextLink handling>
- Throttling: <Retry-After or middleware>
- Validation: <Graph Explorer/test result>
```

## Quality gate

- [ ] Target language and matching bundled reference were used.
- [ ] Auth flow matches user-context versus app-only requirements.
- [ ] Permissions are least-privilege and checked against the Microsoft permissions reference.
- [ ] `GraphServiceClient` is constructed once and reused.
- [ ] Collection reads handle `@odata.nextLink` or `PageIterator`.
- [ ] HTTP 429 handling honors `Retry-After`.
- [ ] No secret is hardcoded.
- [ ] Graph paths, SDK calls, and current docs were verified.

## References

- [Microsoft Graph overview](https://learn.microsoft.com/graph/overview)
- [Graph Explorer](https://developer.microsoft.com/graph/graph-explorer)
- [Graph permissions reference](https://learn.microsoft.com/graph/permissions-reference)
