---
name: arize-ai-provider-integration
description: >-
  Create, list, inspect, update, and delete Arize AI integrations that store LLM provider
  credentials for evaluators and Arize features. Use this skill when connecting OpenAI, Anthropic,
  Azure OpenAI, AWS Bedrock, Vertex AI, Gemini, NVIDIA NIM, or custom providers to Arize; managing
  AI integration credentials; listing integrations; rotating keys; deleting integrations; or
  finding integration IDs.
metadata:
  author: arize
  compatibility: Requires the ax CLI and a configured Arize profile.
  version: 1.0
---

<!-- Generated from harness/github-copilot/plugins/arize-ax/skills/arize-ai-provider-integration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Arize AI provider integrations

Use the `ax ai-integrations` CLI to manage account-scoped LLM provider credentials in Arize, then return the integration ID, provider, scoping, credential status, and any downstream evaluator impact.

## When to invoke

- "Create an Arize AI integration for OpenAI, Anthropic, Azure OpenAI, Bedrock, Vertex AI, Gemini, NVIDIA NIM, or a custom provider."
- "List or inspect Arize AI integrations in a space."
- "Rotate credentials or update model names for an Arize integration."
- "Delete an Arize LLM provider integration."
- "Find the integration ID to use with an evaluator."

## Prerequisites and context

Proceed directly with the needed `ax` command; do not check versions, env vars, or profiles upfront. If a command fails, troubleshoot from the error.

- Most `--space` flags and the `ARIZE_SPACE` env var accept a space name such as `my-workspace` or a base64 space ID such as `U3BhY2U6...`; find spaces with `ax spaces list`.
- `ai-integrations create` does not accept `--space` because AI integrations are account-scoped.
- Use `--space` with `list`, `get`, `update`, and `delete` when resolving by name or filtering visibility.
- Never read `.env` files or search the filesystem for credentials. Use `ax profiles` for Arize credentials and `ax ai-integrations` for LLM provider keys.
- If credentials are not available through these channels, ask the user.

## Concepts and fields

| Concept | Meaning |
| --- | --- |
| AI Integration | Stored LLM provider credentials registered in Arize; evaluators and other Arize features use them to call a judge model or LLM. |
| Provider | The LLM service backing the integration, such as `openAI`, `anthropic`, or `awsBedrock`. |
| Integration ID | Base64 global identifier such as `TGxtSW50ZWdyYXRpb246MTI6YUJjRA==`; required for evaluator creation and downstream commands. |
| Scoping | Visibility rules controlling which spaces or users can use an integration. |
| Auth type | Provider authentication method: `default`, `proxy_with_headers`, or `bearer_token`. |

| Response field | Description |
| --- | --- |
| `id` | Base64 integration ID; copy this for downstream commands. |
| `name` | Human-readable name. |
| `provider` | LLM provider enum. |
| `has_api_key` | `true` if credentials are stored. |
| `model_names` | Allowed model list, or `null` if all models are enabled. |
| `enable_default_models` | Whether default models for this provider are allowed. |
| `function_calling_enabled` | Whether tool/function calling is enabled. |
| `auth_type` | `default`, `proxy_with_headers`, or `bearer_token`. |

## List and inspect integrations

List all integrations accessible in a space:

```bash
ax ai-integrations list --space SPACE
```

Filter by name, using a case-insensitive substring match:

```bash
ax ai-integrations list --space SPACE --name "openai"
```

Paginate large result sets:

```bash
ax ai-integrations list --space SPACE --limit 20 -o json
ax ai-integrations list --space SPACE --limit 20 --cursor CURSOR_TOKEN -o json
```

| Flag | Description |
| --- | --- |
| `--space` | Space name or ID to filter integrations. |
| `--name` | Case-insensitive substring filter on integration name. |
| `--limit` | Max results from 1–100, default 15. |
| `--cursor` | Pagination token from a previous response. |
| `-o, --output` | Output format: `table` default or `json`. |

Get a specific integration:

```bash
ax ai-integrations get NAME_OR_ID
ax ai-integrations get NAME_OR_ID -o json
ax ai-integrations get NAME_OR_ID --space SPACE
```

Use `--space SPACE` when using a name instead of an ID.

## Create integrations

Before creating, list integrations first because the user may already have a suitable one:

```bash
ax ai-integrations list --space SPACE
```

If none exists, create with provider-specific flags.

| Provider | Command |
| --- | --- |
| `openAI` | `ax ai-integrations create --name "My OpenAI Integration" --provider openAI --api-key $OPENAI_API_KEY` |
| `anthropic` | `ax ai-integrations create --name "My Anthropic Integration" --provider anthropic --api-key $ANTHROPIC_API_KEY` |
| `azureOpenAI` | `ax ai-integrations create --name "My Azure OpenAI Integration" --provider azureOpenAI --api-key $AZURE_OPENAI_API_KEY --base-url "https://my-resource.openai.azure.com/"` |
| `awsBedrock` | `ax ai-integrations create --name "My Bedrock Integration" --provider awsBedrock --provider-metadata '{"role_arn": "arn:aws:iam::123456789012:role/ArizeBedrockRole"}'` |
| `vertexAI` | `ax ai-integrations create --name "My Vertex AI Integration" --provider vertexAI --provider-metadata '{"project_id": "my-gcp-project", "location": "us-central1"}'` |
| `gemini` | `ax ai-integrations create --name "My Gemini Integration" --provider gemini --api-key $GEMINI_API_KEY` |
| `nvidiaNim` | `ax ai-integrations create --name "My NVIDIA NIM Integration" --provider nvidiaNim --api-key $NVIDIA_API_KEY --base-url "https://integrate.api.nvidia.com/v1/models"` |
| `custom` | `ax ai-integrations create --name "My Custom Integration" --provider custom --base-url "https://my-llm-proxy.example.com/v1" --api-key $CUSTOM_LLM_API_KEY` |

| Optional flag | Description |
| --- | --- |
| `--model-name` | Allowed model name; repeat for multiple, for example `--model-name gpt-4o --model-name gpt-4o-mini`; omit to allow all models. |
| `--enable-default-models` | Enable the provider's default model list. |
| `--function-calling-enabled` | Enable tool/function calling support. |
| `--auth-type` | `default`, `proxy_with_headers`, or `bearer_token`. |
| `--headers` | Custom headers as JSON object or file path for proxy auth. |
| `--provider-metadata` | Provider-specific metadata as JSON object or file path. |

After creation, capture the integration ID such as `TGxtSW50ZWdyYXRpb246MTI6YUJjRA==`. If you missed it, retrieve it with `ax ai-integrations list --space SPACE -o json` or `ax ai-integrations get NAME_OR_ID`.

## Update and delete integrations

`update` is a partial update; omitted fields stay as-is. Add `--space SPACE` when using a name instead of ID. Any flag accepted by `create` can be passed to `update`.

```bash
ax ai-integrations update NAME_OR_ID --name "New Name"
ax ai-integrations update NAME_OR_ID --api-key $OPENAI_API_KEY
ax ai-integrations update NAME_OR_ID --model-name gpt-4o --model-name gpt-4o-mini
ax ai-integrations update NAME_OR_ID --base-url "https://new-endpoint.example.com/v1"
```

Deletion is permanent. Evaluators that reference the integration will no longer run.

```bash
ax ai-integrations delete NAME_OR_ID --force
ax ai-integrations delete NAME_OR_ID --space SPACE --force
```

Omit `--force` to get a confirmation prompt instead of deleting immediately.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `ax: command not found` or version error | Read `references/ax-setup.md`. |
| `401 Unauthorized` or missing API key | Run `ax profiles show` or `ax profiles show --expand`; if missing or wrong, read `references/ax-profiles.md`; direct users without a key to https://app.arize.com/admin > API Keys. |
| Space unknown | Run `ax spaces list` to pick by name, or ask the user. |
| No profile found | Set `ARIZE_API_KEY` or write `~/.arize/config.toml` using `references/ax-profiles.md`. |
| LLM provider call fails due to missing `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` | Run `ax ai-integrations list --space SPACE` to check for platform-managed credentials; if none exist, ask the user to provide the key or create an integration. |
| `Integration not found` | Verify with `ax ai-integrations list --space SPACE`. |
| `has_api_key: false` after create | Re-run `update` with the correct `--api-key` or `--provider-metadata`. |
| Evaluator runs fail with LLM errors | Check credentials with `ax ai-integrations get INT_ID`; rotate the API key if needed. |
| `provider` mismatch | Provider cannot be changed; delete and recreate with the correct provider. |

## Progressive disclosure and bundled resources

- `references/ax-setup.md`: install or fix the `ax` CLI when commands are unavailable or incompatible.
- `references/ax-profiles.md`: configure Arize profiles, `ARIZE_API_KEY`, and `~/.arize/config.toml` when authentication fails.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `arize-evaluator` | skill | Create LLM-as-judge evaluators that use an AI integration. |
| `arize-experiment` | skill | Run experiments that use evaluators backed by an AI integration. |


## Arize command vocabulary

Preserve exact placeholder forms when adapting commands: `--api-key <key>`, `--base-url <azure-endpoint>`, `--base-url <nim-endpoint>`, `--base-url <endpoint>`, `--provider-metadata '{"role_arn": "<arn>"}'`, `azure-endpoint`, `nim-endpoint`, `gcp-project`, `role-based`, `name/ID`, `create/update`, `re-run`, `command not found`, and `No profile found`.

## Output template

```markdown
### Arize AI integration result

**Status:** created | listed | updated | deleted | blocked
**Space:** `<SPACE or ARIZE_SPACE or not used>`
**Integration:** `<name or NAME_OR_ID>`
**Provider:** `openAI` | `anthropic` | `azureOpenAI` | `awsBedrock` | `vertexAI` | `gemini` | `nvidiaNim` | `custom`
**Integration ID:** `<id such as TGxtSW50ZWdyYXRpb246MTI6YUJjRA==>`

| Field | Value |
| --- | --- |
| `has_api_key` | `true` | `false` |
| `model_names` | `<list or null>` |
| `enable_default_models` | `<value>` |
| `function_calling_enabled` | `<value>` |
| `auth_type` | `default` | `proxy_with_headers` | `bearer_token` |

**Commands run**
- `<ax ai-integrations ...>`

**Notes**
- <downstream evaluator impact, credential rotation note, or blocker>
```

## Quality gate

- [ ] `ax ai-integrations list --space SPACE` is run before creating a new integration unless no space context exists.
- [ ] `create` is not called with `--space`.
- [ ] `--space SPACE` is supplied for `get`, `update`, or `delete` when resolving by name.
- [ ] Provider-specific required flags are present.
- [ ] Credentials are never read from `.env` or discovered by filesystem search.
- [ ] The integration ID is captured or retrieved after creation.
- [ ] Deletion impact on evaluators is stated before using `--force`.
- [ ] Troubleshooting uses `references/ax-setup.md` or `references/ax-profiles.md` only after a relevant command failure.

## References

- [Arize API Keys](https://app.arize.com/admin)
- [Azure OpenAI endpoint example](https://my-resource.openai.azure.com/)
- [NVIDIA NIM endpoint example](https://integrate.api.nvidia.com/v1/models)
- [Custom OpenAI-compatible endpoint example](https://my-llm-proxy.example.com/v1)
- [Updated endpoint example](https://new-endpoint.example.com/v1)
