# Memory

Separate two kinds of memory. Mixing them causes both cost blowups and forgetfulness.

## Short term memory (thread state)

The working context of a single conversation or task run: recent turns, tool results, scratchpad.

- Lives with the agent run. In Azure AI Foundry Agent Service this is the **thread**; the service persists messages and run state.
- Bounded by the context window. Compact it (summarize older turns) before it overflows. See context-curation.md.
- Fast and ephemeral. A session store in Azure Managed Redis is a good backing for custom runtimes (see `azure-managed-redis-cache`).

## Long term memory (durable)

Facts, preferences, and prior outcomes that should survive across sessions.

- **Semantic memory.** Embedded facts and documents in a vector store, retrieved by similarity. Backed by Azure Managed Redis vector search, Azure AI Search, or Cosmos DB.
- **Episodic memory.** Summaries of past sessions or task outcomes, retrieved when a similar situation recurs.
- **Profile memory.** Structured user or tenant preferences, stored as key value or a small document.

## Write and read policy

- **Write path.** Decide what is worth remembering. Do not persist every turn. Summarize and extract durable facts at session end or on explicit save.
- **Read path.** On a new task, retrieve relevant long term memory and inject a budgeted slice into context. Rank and trim.
- **Isolation.** Always scope memory keys by tenant and user. Never let one tenant retrieve another tenant's memory.
- **Lifecycle.** Set retention and a forget path for privacy and correctness. Support deletion requests.

## Service mapping (this workspace)

| Need | Service |
| --- | --- |
| Session and short term state | Azure Managed Redis (session store) |
| Semantic and vector memory | Azure Managed Redis vector search, or Azure AI Search |
| Structured profile | Cosmos DB or Redis hash |
| Managed thread state | Azure AI Foundry Agent Service threads |

## Sources

- [Azure AI Foundry Agent Service threads](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Azure Managed Redis](https://learn.microsoft.com/azure/redis/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
