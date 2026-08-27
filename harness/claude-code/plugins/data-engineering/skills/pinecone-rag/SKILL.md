---
name: pinecone-rag
description: >-
  Build production RAG pipelines and persistent agent memory with Pinecone as the vector database
  backend. Use this skill when indexing documents for semantic search, building
  retrieval-augmented generation, storing agent memory across sessions, implementing hybrid
  search, designing namespace isolation for multi-tenant agents, creating embedding pipelines, or
  scaling a searchable knowledge base beyond local storage.
license: Apache-2.0
metadata:
  compatibility: "pinecone>=6.0.0, Python 3.10+"
---

<!-- Generated from harness/github-copilot/plugins/data-engineering/skills/pinecone-rag/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Pinecone RAG and agent memory

Use this skill to choose a Pinecone index, embed and upsert content in batches, select dense or hybrid retrieval, wire a RAG answer or agent memory loop, and validate end-to-end retrieval quality.

## When to invoke

- "Build a RAG pipeline with Pinecone."
- "Index documents for semantic search or a searchable knowledge base."
- "Store persistent agent memory across sessions."
- "Implement hybrid search with Pinecone and BM25."
- "Design namespace isolation for multi-tenant agents or users."

## Prerequisites and context

- Python 3.10+ and `pinecone>=6.0.0`.
- Pinecone API key available as `PINECONE_API_KEY` or through the user's existing secret mechanism.
- An embedding provider such as OpenAI, Voyage, or a local model; the embedding dimension must match the Pinecone index exactly.
- Do not use this skill for local-only vector stores such as FAISS or Chroma, pgvector-only designs, pure keyword search, or another explicit vector DB such as Weaviate or Qdrant.

## Procedure

1. Classify the use case before code: document RAG, agent memory, or both.
2. Choose the index type and dimension before any upsert; recreating an index is often required after a dimension mistake.
3. Embed content in batches and upsert vectors with original text stored in metadata.
4. Choose dense, hybrid, and metadata-filtered retrieval based on corpus needs.
5. Wire document RAG or agent memory namespace patterns.
6. Run a smoke test that covers index → upsert → query → LLM response or recall.

If the user has not said whether the task is document retrieval, agent memory, or both, ask: "Is this for document retrieval, agent memory, or both?"

## Index configuration

Use serverless for most workloads and pod-based indexes only when consistent high-throughput production requirements justify them.

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="PINECONE_API_KEY")

if "my-index" not in pc.list_indexes().names():
    pc.create_index(
        name="my-index",
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index("my-index")
```

```python
from pinecone import PodSpec

pc.create_index(
    name="my-index-prod",
    dimension=1536,
    metric="cosine",
    spec=PodSpec(environment="us-east1-gcp", pod_type="p1.x1")
)
```

| Model | Dimension |
| --- | --- |
| `text-embedding-3-small` | 1536 |
| `text-embedding-3-large` | 3072 |
| `voyage-3` / `voyage-multimodal-3` | 1024 |
| `BAAI/bge-large-en-v1.5` | 1024 |
| `intfloat/multilingual-e5-large` for Arabic, Malay, Chinese | 1024 |

Checkpoint: index exists, dimension matches the embedding model, and `index.describe_index_stats()` returns without error.

## Embedding and upsert pipeline

Always batch upserts; never upsert one vector at a time. Store the original text in metadata so retrieval does not require a second lookup.

```python
from openai import OpenAI

client = OpenAI()

def embed(texts: list[str]) -> list[list[float]]:
    res = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [r.embedding for r in res.data]

def upsert_docs(index, docs: list[dict], namespace: str = "default"):
    """docs = [{"id": "...", "text": "...", "metadata": {...}}]"""
    BATCH = 100
    for i in range(0, len(docs), BATCH):
        batch = docs[i:i + BATCH]
        vecs = [
            {
                "id": d["id"],
                "values": emb,
                "metadata": {**d.get("metadata", {}), "text": d["text"]}
            }
            for d, emb in zip(batch, embed([d["text"] for d in batch]))
        ]
        index.upsert(vectors=vecs, namespace=namespace)
```

Checkpoint: `index.describe_index_stats()` shows vector count greater than 0 in the target namespace.

## Retrieval strategies

Use dense semantic search for most cases.

```python
def search(index, query: str, top_k: int = 5, namespace: str = "default",
           filter: dict = None) -> list[dict]:
    [q_emb] = embed([query])
    results = index.query(
        vector=q_emb, top_k=top_k, namespace=namespace,
        include_metadata=True, filter=filter
    )
    return [{"text": m.metadata["text"], "score": m.score, "id": m.id}
            for m in results.matches]
```

Use hybrid search when exact terminology matters: legal citations, medical codes, product SKUs, and API method names.

```python
from pinecone_text.sparse import BM25Encoder

bm25 = BM25Encoder().default()
bm25.fit([d["text"] for d in docs])

def hybrid_search(index, query: str, top_k: int = 5, alpha: float = 0.7):
    """alpha=1.0 is pure dense; alpha=0.0 is pure sparse."""
    dense = [v * alpha for v in embed([query])[0]]
    sparse_raw = bm25.encode_queries(query)
    sparse = {
        "indices": sparse_raw["indices"],
        "values": [v * (1 - alpha) for v in sparse_raw["values"]]
    }
    return index.query(vector=dense, sparse_vector=sparse,
                       top_k=top_k, include_metadata=True).matches
```

Use metadata filtering to scope results before semantic ranking.

```python
results = index.query(vector=emb, filter={"source": {"$eq": "confluence"}})

results = index.query(vector=emb, filter={
    "$and": [
        {"category": {"$eq": "engineering"}},
        {"language": {"$in": ["en", "ar"]}}
    ]
})
```

Checkpoint: a test query returns relevant results with scores greater than 0.7 for clearly matching content.

## RAG and memory patterns

Document RAG uses retrieved chunks as grounded context and refuses answers not present in the context.

```python
def rag_answer(index, question: str, namespace: str = "default",
               model: str = "gpt-4o-mini") -> str:
    hits = search(index, question, top_k=5, namespace=namespace)
    context = "\n\n".join(h["text"] for h in hits)

    return client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided context. "
                    "If the answer isn't in the context, say so.\n\n"
                    f"Context:\n{context}"
                )
            },
            {"role": "user", "content": question}
        ]
    ).choices[0].message.content
```

Agent memory uses namespaces to isolate each agent's or user's memories. A namespace per agent prevents memory bleed across users or sessions.

```python
import time, hashlib

def remember(index, agent_id: str, content: str,
             memory_type: str = "fact"):
    """Store a memory for an agent."""
    mem_id = hashlib.md5(
        f"{agent_id}{content}{time.time()}".encode()
    ).hexdigest()
    [emb] = embed([content])
    index.upsert(
        vectors=[{
            "id": mem_id,
            "values": emb,
            "metadata": {
                "text": content,
                "type": memory_type,
                "timestamp": time.time(),
                "agent_id": agent_id
            }
        }],
        namespace=f"agent_{agent_id}"
    )

def recall(index, agent_id: str, query: str,
           top_k: int = 5) -> list[str]:
    """Recall relevant memories for an agent."""
    return [h["text"] for h in
            search(index, query, top_k=top_k,
                   namespace=f"agent_{agent_id}")]

def forget(index, agent_id: str):
    """Wipe all memories for an agent (e.g., on user request)."""
    index.delete(delete_all=True, namespace=f"agent_{agent_id}")
```

Run an end-to-end smoke test before integrating into the larger system.

```python
upsert_docs(index, [
    {"id": "t1", "text": "Pinecone is a vector database for semantic search."},
    {"id": "t2", "text": "RAG combines retrieval with language model generation."},
])

hits = search(index, "What is Pinecone?")
assert hits[0]["score"] > 0.7, f"Expected high similarity, got {hits[0]['score']}"
print("Smoke test passed:", hits[0]["text"])
```

## Gotchas

- **Dimension mismatch breaks upserts**: verify `len(embed(["test"])[0])` matches the index dimension before the first upsert.
- **Missing text in metadata causes slow retrieval**: if `"text"` is absent, the app needs a second lookup for actual content.
- **Single-vector upserts are inefficient**: batch in chunks of 100.
- **No namespace strategy leaks data**: choose one namespace per user, tenant, or agent before storing production data.
- **BM25 needs representative data**: fit on at least a few hundred documents when possible.

## Limits

Use a different approach when the dataset fits in memory and latency does not matter, when the user wants FAISS or Chroma, when PostgreSQL plus pgvector is the preferred architecture, when sub-5ms p99 latency forbids external API calls, when the request is pure keyword search, or when the user explicitly wants Weaviate, Qdrant, or another vector database.


## Pinecone vocabulary

Preserve user trigger and architecture terms from existing requests: `ALWAYS`, `USE`, `THIS`, `SKILL`, `re-creating`, `to-end`, `cross-tenant`, and `user/agent`. Treat them as clues for Pinecone RAG, namespace isolation, and end-to-end validation.

## Output template

```markdown
### Pinecone RAG result

**Status:** complete | needs changes | blocked
**Use case:** document RAG | agent memory | both
**Index:** `<index name>`
**Dimension / metric:** `<dimension>` / `<metric>`
**Namespace strategy:** `<namespace per tenant/user/agent/default>`

| Component | Decision | Evidence |
| --- | --- | --- |
| Embedding model | `<model>` | dimension `<value>` matches index |
| Upsert batch size | `<size>` | vector count `<count>` |
| Retrieval | dense | hybrid | metadata-filtered | `<why>` |
| Text metadata | present | missing | `<field name>` |

**Smoke test**
- `index.describe_index_stats()`: pass | fail
- Query: `<test query>`
- Top score: `<score>`
- Result snippet: `<text>`

**Implementation notes**
- <files changed or code to add>
```

## Quality gate

- [ ] The use case is classified as document RAG, agent memory, or both.
- [ ] The Pinecone index dimension exactly matches the embedding model.
- [ ] `index.describe_index_stats()` succeeds before and after upsert.
- [ ] Upserts are batched and include original `text` in metadata.
- [ ] Namespace isolation is explicit for multi-tenant users, agents, or sessions.
- [ ] Dense, hybrid, and metadata-filtered retrieval decisions are justified.
- [ ] A smoke test verifies index, upsert, query, and RAG answer or memory recall.
- [ ] Local-only vector store, pgvector-only, pure keyword, and non-Pinecone requests are handed off instead of forced into Pinecone.
