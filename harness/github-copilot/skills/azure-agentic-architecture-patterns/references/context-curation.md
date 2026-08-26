# Context Curation

The context window is a scarce, paid resource. Curation decides what enters it, in what order, and how much. Good curation beats a bigger model for most retrieval tasks.

## The budget

Set an explicit token budget for each call and allocate it:

- System prompt and tool schemas (stable, cacheable, keep first).
- Retrieved knowledge (RAG results, ranked and trimmed).
- Conversation history (compacted).
- The current user input.

Reserve headroom for the response. Never let history grow unbounded.

## RAG pipeline

1. **Ingest.** Chunk sources with overlap that respects structure (headings, code blocks). Store embeddings in a vector store.
2. **Retrieve.** Embed the query and fetch top candidates. Consider hybrid retrieval (vector plus keyword) for recall.
3. **Rerank.** Apply a reranker or a cross-encoder to order candidates by true relevance, then keep the top few.
4. **Assemble.** Insert the kept chunks with citations, within budget.
5. **Ground.** Instruct the model to answer only from provided context and to say when it cannot.

## History compaction

- Summarize older turns into a running summary once history passes a threshold.
- Keep the last few turns verbatim for continuity.
- Drop tool outputs that are no longer needed, or replace them with a short reference.

## Quality levers

- **Chunking** quality usually matters more than model size for retrieval accuracy.
- **Reranking** removes the near-miss noise that vector search alone returns.
- **Citations** make answers auditable and let you evaluate grounding.
- **Hybrid search** improves recall on names, codes, and rare terms.

## Service mapping

| Step | Service |
| --- | --- |
| Vector store | Azure Managed Redis vector search, Azure AI Search |
| Hybrid and semantic ranking | Azure AI Search |
| Embeddings and rerank models | Azure AI Foundry model catalog |

## Sources

- [Retrieval augmented generation on Azure AI Search](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure Managed Redis vector search](https://learn.microsoft.com/azure/redis/)
