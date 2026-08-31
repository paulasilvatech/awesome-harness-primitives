---
name: foundry-claude-api
description: >-
  Designs, implements, reviews, and migrates Claude API integrations using
  official Anthropic SDKs or Claude models in Microsoft Foundry. Use when work
  involves Claude, Anthropic, Opus, Sonnet, Haiku, Messages API, tool use,
  streaming, caching, model migration, or Foundry-hosted Claude clients.
license: Complete terms in LICENSE.txt
---

# Foundry Claude API

Build Claude integrations from current first-party documentation and the
project's selected hosting surface. Keep direct Anthropic API, Microsoft
Foundry, Amazon Bedrock, and Google Vertex contracts separate.

## When to invoke

- Add or review Claude API requests, streaming, tools, caching, or files.
- Select or migrate a Claude model or Anthropic SDK version.
- Configure Claude Code or an SDK client for Microsoft Foundry.
- Audit Claude prompts, tool descriptions, token use, or provider compatibility.
- Diagnose Claude authentication, tool-call, streaming, refusal, or limit errors.

## Procedure

1. Identify the provider and language.
   - Use the provider named by the user or repository.
   - If another provider is explicit, use that provider's skill instead.
   - Keep provider-neutral code provider-neutral unless the user approves a
     Claude-specific dependency.
2. Verify current behavior.
   - Read `shared/live-sources.md` and fetch only the relevant official source.
   - Do not quote a model, version, price, context limit, feature, beta header,
     or SDK method from memory or cached vendor text when currentness matters.
3. Choose the narrowest supported client.
   - Prefer the official SDK for the repository language.
   - Use raw HTTP only when requested, when the language lacks a supported SDK,
     or when the project is intentionally HTTP-based.
   - Do not use OpenAI-compatible shims for Anthropic protocol behavior.
4. Apply provider-specific identity.
   - Direct Anthropic integrations use an approved credential provider outside
     source control.
   - Microsoft Foundry workloads prefer Microsoft Entra ID and
     `DefaultAzureCredential`; hosted Azure workloads use Managed Identity.
   - Keep account local authentication disabled when required by platform
     policy and never log credentials or bearer tokens.
5. Implement and validate.
   - Copy exact imports, classes, request fields, and feature support from the
     selected language and provider documentation.
   - Use streaming for long-running requests and handle terminal/error states.
   - Validate tool schemas, tool-result pairing, retries, cancellation,
     redaction, response sizes, and provider feature limitations.
6. Handle specialized workflows.
   - Model migration: read `shared/model-migration.md` and confirm scope before
     editing.
   - Prompt audit: read `shared/prompt-audit.md` and report findings before
     applying unrequested edits.
   - Token counting: read `shared/token-counting.md`; do not substitute another
     provider's tokenizer.
   - Managed agents: read `shared/managed-agents-overview.md` first and verify
     provider availability before choosing that surface.

## Microsoft Foundry criteria

- Use the Foundry resource endpoint and exact approved deployment name.
- For Claude Code, use `CLAUDE_CODE_USE_FOUNDRY=1` and a Foundry resource or
  `/anthropic` base URL; pin approved deployment aliases.
- When no Foundry key or explicit bearer-token variable is set, verify the
  default Azure credential chain resolves the intended managed identity.
- Distinguish Hosted on Azure from Hosted on Anthropic using current catalog
  and live deployment evidence.
- Verify feature availability for the exact hosting option. Do not assume
  server-side tools, MCP connectors, Agent Skills, structured outputs, or Files
  API are supported by a Hosted on Azure deployment.
- Claude Code uses the Anthropic-compatible route, not a model-router
  OpenAI-compatible route.

## Security criteria

- Treat prompts, retrieved content, MCP results, and tool results as untrusted.
- Keep authorization and approval outside model instructions.
- Use strict schemas, explicit tool allowlists, finite limits, and bounded
  retries.
- Require human approval for destructive, deployment, identity, or policy
  changes.
- Redact prompts, tool arguments, credentials, and personal data according to
  the application policy before logging or tracing.

## Output template

```markdown
# Claude API result

**Status:** completed | blocked
**Provider:** Anthropic | Microsoft Foundry | Bedrock | Vertex
**Language:** <language or not applicable>
**Model/deployment:** <verified ID or blocked>
**Summary:** <one-sentence outcome>

### Implementation
- Files changed: <paths or none>
- Client surface: <SDK class/API>
- Identity: <credential mechanism without secret values>
- Features: <streaming/tools/caching/etc.>

### Validation evidence
- Official sources checked: <URLs and date>
- Build/tests: <commands and results>
- Provider compatibility: <pass/fail/blocked>
- Security checks: <summary>
```

## Limits

- Do not use this skill when another model provider is explicitly selected.
- Do not invent models, versions, prices, limits, SDK APIs, or provider parity.
- Do not deploy models, accept Marketplace terms, or mutate cloud resources
  without explicit approval and the repository's protected deployment gates.
- Do not treat a catalog listing as proof of subscription quota or live access.
- Do not use the archived vendor guide as fresher evidence than official docs.

## Progressive disclosure and bundled resources

- `references/README.md`: package reference index and freshness rule.
- `shared/live-sources.md`: first-party documentation and SDK repositories.
- `shared/platform-availability.md`: provider-specific feature availability.
- `shared/models.md`: model discovery and capability fields.
- `shared/model-migration.md`: model migration and breaking changes.
- `shared/prompt-audit.md`: prompt and tool-description audit workflow.
- `shared/prompt-caching.md`: cache design and diagnostics.
- `shared/tool-use-concepts.md`: tool-use and agent-loop contracts.
- `shared/error-codes.md`: typed error handling.
- `shared/token-counting.md`: Claude token counting.
- `shared/managed-agents-overview.md`: managed-agent reading guide.
- `shared/vendor-guide.md`: archived comprehensive vendor guide; use only as a
  navigation aid and revalidate volatile claims.
- `<language>/claude-api/`: language-specific SDK examples where present.
- `curl/`: raw HTTP examples.

Read only the files required by the provider, language, and feature.

## Quality gate

- [ ] Provider and language are evidenced from the request or repository.
- [ ] Current first-party documentation supports each volatile claim.
- [ ] Exact SDK imports, methods, request fields, and model/deployment names are
      verified.
- [ ] Authentication uses an approved credential provider and exposes no secret.
- [ ] Provider and hosting-option feature limitations are enforced.
- [ ] Tools, streams, retries, cancellation, errors, and redaction are tested as
      applicable.
- [ ] Model or SDK migrations preserve scope and include focused validation.
- [ ] The response follows `## Output template` exactly.
- [ ] Every referenced bundled resource exists.
