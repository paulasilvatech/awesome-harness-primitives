---
name: microsoft-code-reference
description: >-
  Look up official Microsoft API references, SDK signatures, packages, and working code samples before writing or fixing Azure SDK, .NET, Microsoft Graph, or Microsoft API code. Use when verifying method names, overloads, parameters, authentication patterns, package names, deprecations, RBAC errors, or suspected hallucinated Microsoft SDK calls.
metadata:
  compatibility: "Works best with Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp). Can also use the mslearn CLI as a fallback."
---

# Microsoft code reference

Verify Microsoft SDK and API code against Microsoft Learn reference pages and official samples so generated code uses real packages, methods, overloads, authentication patterns, and current SDK versions instead of plausible but hallucinated APIs.

## When to invoke

- "Check whether this Azure SDK method actually exists."
- "Find an official Microsoft sample for uploading a blob with managed identity."
- "Verify the parameters for this .NET or Microsoft Graph call."
- "Troubleshoot this Azure SDK method-not-found or 403 error."
- "Migrate this old CloudBlobClient code to the current SDK pattern."

## Prerequisites and context

- Prefer the Microsoft Learn MCP server when tools such as `microsoft_docs_search`, `microsoft_code_sample_search`, and `microsoft_docs_fetch` are available.
- If the MCP server is absent, use the `mslearn` CLI fallback through `npx @microsoft/learn-cli` or an installed `mslearn` command from Bash, PowerShell, or another shell.
- Include the language, SDK namespace, package, and service name in queries whenever known.
- Treat official docs and official code samples as higher authority than blog posts, Stack Overflow, or model memory.

## Lookup workflow

Use exact quoted queries when necessary: `"BlobClient UploadAsync Azure.Storage.Blobs"`, `"DefaultAzureCredential troubleshooting"`, `"[ClassName] methods [Namespace]"`, `"[TypeName] NuGet package namespace"`, `"[ClassName] [MethodName] overloads"`, `"[OldType] migration v12"`, and `"[ServiceName] RBAC permissions"`.


| Need | Preferred tool | Query example | Completion rule |
| --- | --- | --- | --- |
| API `method/class` or `class/interface` lookup | `microsoft_docs_search` | `BlobClient UploadAsync Azure.Storage.Blobs` | Confirm the member exists in the target SDK version. |
| Working code sample | `microsoft_code_sample_search` | `query: "upload blob managed identity", language: "python"` | Compare setup, client construction, auth, and call pattern. |
| Full API reference | `microsoft_docs_fetch` | Fetch the URL returned by search. | Read overloads, parameter types, return type, exceptions, and remarks. |
| Package discovery | `microsoft_docs_search` | `Azure Blob Storage NuGet package` or `azure-storage-blob pip package` | Confirm package name and namespace/import. |

For complex API usage, complete all three validation steps: search the method or package, fetch the full reference for `overloads/complex` parameter details, and find a `known-good` working sample. For simple lookups, a precise search result may be sufficient.

## Query patterns

Use exact type, member, and namespace names when possible:

```text
BlobClient UploadAsync Azure.Storage.Blobs
GraphServiceClient Users Microsoft.Graph
DefaultAzureCredential class Azure.Identity
Azure Blob Storage NuGet package
azure-storage-blob pip package
```

When the SDK version may be wrong, query both old and new types. Example: compare v11 `CloudBlobClient` with v12 `BlobServiceClient` before writing migration code.

## Error troubleshooting

| Symptom | Query | What to verify |
| --- | --- | --- |
| Method not found | `[ClassName] methods [Namespace]` | The method exists on that type and SDK version. |
| Type not found | `[TypeName] NuGet package namespace` | Correct package, namespace/import, and major SDK line. |
| Wrong signature | `[ClassName] [MethodName] overloads` then fetch full page | Parameter order, async suffix, return type, cancellation token, options object. |
| Deprecated warning | `[OldType] migration v12` | Replacement type and migration caveats. |
| Authentication failure | `DefaultAzureCredential troubleshooting` | Credential chain, tenant, environment variables, managed identity availability. |
| `403 Forbidden` | `[ServiceName] RBAC permissions` | Required data-plane role and scope, not just control-plane contributor. |

Always verify when a method name seems too convenient, such as `UploadFile` instead of the actual SDK method `Upload` or `UploadAsync`, when mixing SDK major versions, or when package names do not follow conventions such as `Azure.*` for .NET and `azure-*` for Python.

## CLI fallback

Run the Learn CLI directly when MCP tools are unavailable:

```sh
npx @microsoft/learn-cli search "BlobClient UploadAsync Azure.Storage.Blobs"
npm install -g @microsoft/learn-cli
mslearn search "BlobClient UploadAsync Azure.Storage.Blobs"
mslearn code-search "upload file to blob storage" --language csharp
mslearn fetch "<learn-url>"
```

| MCP tool | CLI command |
| --- | --- |
| `microsoft_docs_search(query: "...")` | `mslearn search "..."` |
| `microsoft_code_sample_search(query: "...", language: "...")` | `mslearn code-search "..." --language ...` |
| `microsoft_docs_fetch(url: "...")` | `mslearn fetch "..."` |

Pass `--json` for `JSON` to `search` or `code-search` when downstream processing needs raw structured output.

## Gotchas

- **Do not trust model memory for overloads**: Microsoft SDKs often use options types, response wrappers, and async overloads that look similar but differ by language.
- **Data-plane RBAC is separate**: Azure Contributor does not automatically grant blob, queue, key vault secret, or Service Bus data operations.
- **Samples show `initialization/setup` context**: copy client construction and authentication shape, not just the final method call.
- **Version lines matter**: v11 Azure Storage types such as `CloudBlobClient` do not mix with v12 clients such as `BlobServiceClient`.

## Output template

````markdown
## Microsoft code reference result

**Status:** verified | correction needed | blocked
**Service/SDK:** <service, package, language, version if known>
**Docs checked:** <search result URLs or "MCP/CLI result titles">

| Item | Verified API or package | Evidence | Code guidance |
| --- | --- | --- | --- |
| Method | `<Type.Member>` | <official reference/sample> | <use this signature or replacement> |

### Corrected pattern
```<language>
<minimal code pattern or corrected call>
```
````

## Quality gate

- [ ] Official Microsoft Learn reference or sample evidence was checked before writing or correcting SDK code.
- [ ] Method names, overloads, parameter types, package names, and namespaces/imports are verified.
- [ ] SDK major versions are not mixed unless the migration plan explicitly handles it.
- [ ] Authentication and RBAC guidance distinguishes control-plane and data-plane permissions.
- [ ] CLI fallback commands are used only when MCP tools are unavailable.
- [ ] The output follows `## Output template` exactly.

## References

- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp)
