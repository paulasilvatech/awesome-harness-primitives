---
name: azure-ai
description: >-
  Build on Azure AI services including AI Search, Speech, Azure OpenAI, and Document Intelligence,
  covering keyword, vector, hybrid, and semantic search, speech-to-text, text-to-speech,
  transcription, and OCR. Use when the user asks about AI Search, query search, vector search,
  hybrid search, semantic search, speech-to-text, text-to-speech, transcription, OCR, or
  converting text to speech.
allowed-tools: >-
  mcp__com_microsoft_azure__documentation, mcp__com_microsoft_azure__foundry,
  mcp__com_microsoft_azure__search
license: MIT
metadata:
  author: Microsoft
  version: 1.2.1
---

<!-- Generated from harness/github-copilot/plugins/azure-ai-foundry/skills/azure-ai/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure AI Services

## When to invoke

- "Add vector or hybrid search to my app with Azure AI Search."
- "Transcribe this audio or convert text to speech."
- "Extract fields from these documents with Document Intelligence."
- "Which Azure AI service should I use for semantic search?"

## Services

| Service | Use When | MCP Tools | CLI |
|---------|----------|-----------|-----|
| AI Search | Full-text, vector, hybrid search | `azure__search` | `az search` |
| Speech | Speech-to-text, text-to-speech | `azure__speech` | - |
| OpenAI | GPT models, embeddings, DALL-E | - | `az cognitiveservices` |
| Document Intelligence | Form extraction, OCR | - | - |

## MCP Server (Preferred)

When Azure MCP is enabled:

### AI Search
- `azure__search` with command `search_index_list` - List search indexes
- `azure__search` with command `search_index_get` - Get index details
- `azure__search` with command `search_query` - Query search index

### Speech
- `azure__speech` with command `speech_transcribe` - Speech to text
- `azure__speech` with command `speech_synthesize` - Text to speech

**If Azure MCP is not enabled:** Run `/azure:setup` or enable via `/mcp`.

## AI Search Capabilities

| Feature | Description |
|---------|-------------|
| Full-text search | Linguistic analysis, stemming |
| Vector search | Semantic similarity with embeddings |
| Hybrid search | Combined keyword + vector |
| AI enrichment | Entity extraction, OCR, sentiment |

## Speech Capabilities

| Feature | Description |
|---------|-------------|
| Speech-to-text | Real-time and batch transcription |
| Text-to-speech | Neural voices, SSML support |
| Speaker diarization | Identify who spoke when |
| Custom models | Domain-specific vocabulary |

## SDK Quick References

For programmatic access to these services, see the condensed SDK guides:

- **AI Search**: [Python](references/sdk/azure-search-documents-py.md) | [TypeScript](references/sdk/azure-search-documents-ts.md) | [.NET](references/sdk/azure-search-documents-dotnet.md)
- **OpenAI**: [.NET](references/sdk/azure-ai-openai-dotnet.md)
- **Vision**: [Python](references/sdk/azure-ai-vision-imageanalysis-py.md) | [Java](references/sdk/azure-ai-vision-imageanalysis-java.md)
- **Transcription**: [Python](references/sdk/azure-ai-transcription-py.md)
- **Translation**: [Python](references/sdk/azure-ai-translation-text-py.md) | [TypeScript](references/sdk/azure-ai-translation-ts.md)
- **Document Intelligence**: [.NET](references/sdk/azure-ai-document-intelligence-dotnet.md) | [TypeScript](references/sdk/azure-ai-document-intelligence-ts.md)
- **Content Safety**: [Python](references/sdk/azure-ai-contentsafety-py.md) | [TypeScript](references/sdk/azure-ai-contentsafety-ts.md) | [Java](references/sdk/azure-ai-contentsafety-java.md)

## Service Details

For deep documentation on specific services:

- AI Search indexing and queries -> [Azure AI Search documentation](https://learn.microsoft.com/azure/search/search-what-is-azure-search)
- Speech transcription patterns -> [Azure AI Speech documentation](https://learn.microsoft.com/azure/ai-services/speech-service/overview)

## Output template

```markdown
## Azure AI service result

**Status:** designed | implemented | blocked
**Summary:** <one sentence covering scope and outcome>

### Details
Chosen service, index or model configuration, and calling code changes.

### Validation
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] The selected service matches the retrieval, speech, or extraction need.
- [ ] Keys are replaced by managed identity or Entra auth wherever supported.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was performed and its evidence is shown.
- [ ] Irreversible Azure actions were confirmed with the user first.
