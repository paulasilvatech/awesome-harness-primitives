---
name: qdrant-search-quality
description: >-
  Diagnose and improve Qdrant search relevance by separating embedding, payload, index, and
  query-strategy causes. Use when users report bad search results, wrong results, low precision,
  low recall, irrelevant matches, missing expected results, quantization regressions, model
  changes, data growth, or ask whether to use hybrid search, reranking, relevance feedback, or a
  different embedding model.
allowed-tools: Read, Grep, Glob
---

<!-- Generated from harness/github-copilot/plugins/qdrant-development/skills/qdrant-search-quality/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Qdrant search quality

Diagnose poor Qdrant relevance by isolating whether the failure comes from embeddings, chunking, payload filters, index settings, quantization, or query strategy, then recommend concrete tuning and validation steps.

## When to invoke

- "Search results are bad in Qdrant."
- "Qdrant returns wrong results and misses expected results."
- "Should I use hybrid search or reranking?"
- "Quality dropped after quantization, model change, or data growth."
- "How do I improve low precision or low recall?"

## Relevance fault isolation

Most quality issues come from the model or data, not from Qdrant itself. Inspect how chunks are passed to Qdrant before tuning parameters; splitting mid-sentence can drop quality 30-40%.

| Suspect | Evidence | Check | Corrective action |
| --- | --- | --- | --- |
| Embedding model | Semantically close items are far apart even with filters off. | Compare nearest neighbors for known good query-document pairs. | Use a domain-appropriate model, keep query and document encoders compatible, and re-embed all points after model changes. |
| Chunking | Expected answer is split across chunks or a chunk starts mid-sentence. | Inspect stored text around missing results. | Chunk by semantic boundaries, preserve titles and context, and avoid mid-sentence splits. |
| Payload filters | Relevant points disappear only when filters are enabled. | Run the same query with filters removed, then add one filter at a time. | Fix payload names, types, and filter operators; verify indexed payload fields for high-cardinality filters. |
| HNSW recall | Exact search finds expected points but approximate search does not. | Compare approximate search with exact search using the Search API. | Increase `ef`, review `m`, and validate recall before changing embeddings. |
| Quantization | Recall drops after enabling scalar or binary quantization. | Compare quantized search to unquantized or rescored search. | Enable rescoring or reduce compression aggressiveness for quality-critical collections. |
| Query formulation | Short or ambiguous queries return broad matches. | Test expanded, rewritten, or field-aware queries. | Add query rewriting, hybrid retrieval, metadata boosts, or reranking. |

Start by testing with exact search to isolate the problem. Preserve and consult the Qdrant Search API documentation at https://qdrant.tech/documentation/search/search/?s=search-api.

## Tuning levers

| Lever | Improves | Cost | Use when |
| --- | --- | --- | --- |
| `limit` increase before reranking | Recall before final selection | More candidate processing | Reranker has too few good candidates. |
| `score_threshold` | Precision | Can hide relevant low-score results | Users complain about irrelevant matches, not missing results. |
| HNSW `ef` | Recall | More CPU and latency | Exact search beats approximate search. |
| HNSW `m` | Graph connectivity and recall | More memory and indexing time | Building a new collection or accepting reindex cost. |
| Payload index | Filter latency and correctness at scale | More index storage | Filters are common and selective. |
| Quantization rescoring | Quality after compression | More vector reads | Quantized search has near-miss candidates. |
| Hybrid dense+sparse retrieval | Lexical exactness plus semantic recall | More indexing and fusion logic | Queries include product names, codes, rare terms, or exact phrases. |
| Cross-encoder reranking | Final ordering precision | Highest per-query latency | Top candidates contain the answer but order is poor. |

## Strategy selection

| User symptom | Prefer | Avoid |
| --- | --- | --- |
| "Expected document is missing" | Increase candidate count, exact-search comparison, chunk audit, HNSW `ef` tuning. | Tight `score_threshold` before recall is proven. |
| "Top result is unrelated" | Reranking, better query text, metadata constraints, domain embeddings. | Blindly raising `limit`, which may only expose more bad results. |
| "Names or IDs do not match" | Hybrid search with sparse vectors or keyword payload filters. | Pure dense retrieval for exact identifiers. |
| "Quality degraded after re-embedding" | Verify vector dimensionality, collection vector name, normalized input text, and full reindex. | Mixing embeddings from old and new models in one vector space. |
| "Quality degraded after growth" | Re-check HNSW settings, payload indexes, chunk distribution, and evaluation set coverage. | Assuming Qdrant changed without measuring data drift. |

## Bundled deep dives

- `diagnosis/SKILL.md`: isolate embedding, Qdrant configuration, HNSW, chunking, and quantization causes.
- `search-strategies/SKILL.md`: apply hybrid search, reranking, relevance feedback, and exploration APIs after diagnosis identifies strategy limits.

## Gotchas

- **Do not tune blindly**: always compare exact search, approximate search, filters, and candidate text before changing production parameters.
- **Do not mix embedding spaces**: a model change requires consistent re-embedding of query and document vectors.
- **Do not judge from one query**: build a small labeled set with expected hits, negatives, and edge cases.
- **Do not optimize average score alone**: inspect precision@k, recall@k, and whether expected documents appear before reranking.

## Output template

```markdown
## Qdrant search quality diagnosis

**Status:** diagnosed | needs data | blocked
**Primary suspected cause:** embedding model | chunking | payload filters | HNSW recall | quantization | query strategy

| Check | Evidence | Result | Next action |
| --- | --- | --- | --- |
| Exact Search API comparison | `<query and collection>` | pass/fail | `<action>` |
| Chunk inspection | `<point ids or payload fields>` | pass/fail | `<action>` |
| Filter isolation | `<filters tested>` | pass/fail | `<action>` |
| Strategy test | `<hybrid/rerank/threshold test>` | pass/fail | `<action>` |

**Recommendation:** <specific configuration, data, model, or query-strategy change>
**Validation metric:** <precision@k, recall@k, nDCG, or labeled-query result>
```

## Quality gate

- [ ] Exact search was used or explicitly recommended to isolate approximate-index effects.
- [ ] Chunking quality, including mid-sentence splits, was inspected or requested.
- [ ] Embedding model compatibility and re-embedding requirements were checked.
- [ ] Payload filters and indexed payload fields were separated from vector recall issues.
- [ ] Any HNSW, quantization, hybrid, reranking, or threshold recommendation names the quality metric it should improve.
- [ ] The final recommendation distinguishes low precision from low recall.

## References

- [Qdrant Search API](https://qdrant.tech/documentation/search/search/?s=search-api)
