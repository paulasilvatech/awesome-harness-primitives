# Session Store on Azure Managed Redis

Short term agent memory is the working state of a single conversation or task run. Redis is a natural backing store for it in custom runtimes (Azure AI Foundry Agent Service manages threads for you).

## What to store

- Recent conversation turns kept verbatim for continuity.
- A running summary of older turns (compacted to save context budget).
- Tool results that the current task still needs.
- Run metadata: status, step counter, and a correlation id for tracing.

## Patterns

- **Key shape.** `t:{tenant}:u:{user}:session:{sessionId}` with a hash or stream for turns. Always namespace by tenant and user.
- **Time to live.** Set an expiry on idle sessions so memory does not accumulate. Refresh on activity.
- **Compaction.** When turn count or token estimate passes a threshold, summarize older turns into the running summary and trim the verbatim tail.
- **Concurrency.** Use optimistic concurrency (a version field) if multiple workers can touch one session.

## Why Redis here

- Sub-millisecond reads keep the agent loop fast.
- Native expiry handles session lifecycle without a sweeper.
- The same cluster can also host the semantic cache and vector memory, reducing moving parts.

## Sources

- [Azure Managed Redis](https://learn.microsoft.com/azure/redis/)
- [Azure AI Foundry Agent Service threads](https://learn.microsoft.com/azure/ai-foundry/agents/)
