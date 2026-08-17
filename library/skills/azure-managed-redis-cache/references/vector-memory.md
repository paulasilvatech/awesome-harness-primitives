# Vector Memory on Azure Managed Redis

Redis vector search stores embeddings and retrieves them by similarity, which makes it a fast backend for long term agent memory and for the retrieval step of RAG.

## Index design

- **Schema.** Define a vector field (dimension matches your embedding model), plus filter fields (tenant, user, type, timestamp, source) and a text field for the original content.
- **Algorithm.** Choose HNSW for low-latency approximate search at scale, or flat for exact search on small sets.
- **Distance.** Cosine is typical for normalized text embeddings. Match it to how the embedding model was trained.

## Memory types on one index

- **Semantic memory.** Facts and documents, retrieved by query similarity.
- **Episodic memory.** Session summaries, tagged by time and outcome, retrieved when a similar situation recurs.
- Use filter fields to separate types and to enforce tenant isolation in the query itself.

## Read and write policy

- **Write.** Extract durable facts and summaries at session end or on explicit save. Do not embed every turn.
- **Read.** Retrieve top candidates, rerank, and inject a budgeted slice into context (see context curation in `agentic-architecture-patterns`).
- **Isolation.** Always include a tenant and user filter in the query. Never run an unfiltered nearest-neighbor search across tenants.
- **Lifecycle.** Set retention and support deletion for privacy and correctness.

## When to use Redis vs Azure AI Search

- **Redis** for the lowest-latency hot memory and when you already run Redis for cache and session.
- **Azure AI Search** for large corpora, hybrid (vector plus keyword) retrieval, and built-in semantic ranking.
- Many designs use both: Redis for hot session memory and semantic cache, AI Search for the document corpus.

## Sources

- [Azure Managed Redis vector search](https://learn.microsoft.com/azure/redis/redis-vector-search)
- [RedisVL vector queries](https://redis.io/docs/latest/integrate/redisvl/)
- [Azure AI Search vector search](https://learn.microsoft.com/azure/search/vector-search-overview)
