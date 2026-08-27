---
name: qdrant-model-migration
description: >-
  Plan zero-downtime embedding model migrations in Qdrant with aliases, re-embedding, side-by-side
  collections, hybrid dense/sparse search, and bulk upload tuning. Use when switching embedding
  models, changing vector dimensions or providers, upgrading to hybrid search, re-embedding data,
  or A/B testing models.
---

<!-- Generated from harness/github-copilot/plugins/qdrant-development/skills/qdrant-model-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Qdrant model migration

Choose a safe Qdrant collection migration strategy when embedding vectors change, because vectors from different models are incompatible and named vectors must be defined when a collection is created.

## When to invoke

- "How do I switch embedding models in Qdrant without downtime?"
- "Can I use two embedding models at once?"
- "Migrate this collection from dense to hybrid search."
- "Re-embed my Qdrant data after changing providers."
- "A/B test old and new vectors in Qdrant."

## Core constraints

| Constraint | Consequence |
| --- | --- |
| Vectors from different models are incompatible. | Do not mix old and new embeddings in the same vector field. |
| You cannot add new named vector fields to an existing collection. | Create a new collection for model replacement or side-by-side fields. |
| Sparse vectors cannot be added to a dense-only collection after creation. | Dense-to-hybrid migration requires collection recreation. |
| Alias swap only redirects queries. | Payloads and vectors must be migrated or re-uploaded separately. |
| Large multi-vectors such as ColBERT can degrade all queries when co-located. | Put large vectors on disk or separate them for long migrations. |

## Strategy map

| Situation | Strategy | Key steps |
| --- | --- | --- |
| Production must stay available | Zero-downtime alias swap | Create new collection, re-embed in background, query through alias, atomically switch alias, verify, then delete old collection. |
| A/B testing or both models live | Side-by-side collection | Create a new collection with old and new named vectors defined upfront, migrate old vectors, backfill new vectors with `UpdateVectors`, query with `using: "old_model"` and `using: "new_model"`. |
| Dense to hybrid search | Recreate with dense and sparse/BM25 configs | Create collection with both dense and sparse vectors, re-embed all data, migrate payloads, swap alias. |
| Re-embedding is bottleneck | Batched idempotent migration | Scroll old collection with `with_vectors=False`, embed batches, upsert into the new collection with `update_mode: insert`, parallelize cautiously. |
| Future migrations anticipated | Predefine named vectors | Include likely vector fields at collection creation time even if some are backfilled later. |

## Re-embedding decision

| Change | Re-embed? | Notes |
| --- | --- | --- |
| OpenAI to Cohere, CLIP to BGE, or other provider/architecture switch | Yes | Vector spaces are incompatible. |
| Dimension count changes across different models | Yes | New collection needs the new vector size. |
| Adding sparse vectors to a dense-only collection | Yes | Recreate and generate sparse vectors. |
| Matryoshka lower-dimensional output | Maybe avoid full re-embedding | Use a `dimensions` parameter, learn a linear transformation from sample data, accept recall loss; most useful for 100M+ datasets. |
| Quantization change such as binary to scalar | No full re-embedding | Qdrant re-quantizes automatically. |
| Qdrant Cloud inference model switch | Usually pipeline config change | The model configuration changes, not necessarily the ingestion code path. |

## Migration procedures

### Zero downtime with alias swap

1. Create a new collection with the new model dimensions and distance metric.
2. Re-embed all source data into the new collection in the background.
3. Point the application at a collection alias instead of a direct collection name.
4. Atomically switch the alias to the new collection.
5. Verify search quality and latency.
6. Delete the old collection only after rollback is no longer needed.

### Side-by-side models

1. Create a new collection with both old and new vector fields defined upfront.
2. Migrate data from the old collection and preserve existing vectors in the old named field.
3. Backfill new embeddings incrementally using `UpdateVectors`.
4. Compare quality by querying with `using: "old_model"` versus `using: "new_model"`.
5. Swap the alias to the new collection when satisfied.

Use the same side-by-side shape for multi-modal experiments that combine dense and sparse vectors. You MUST still create the target collection before adding those named vectors.

### Large dataset tuning

- Use `update_mode: insert` for safe idempotent migration when supported.
- Upload in parallel batches of 64-256 points per request with 2-4 parallel streams.
- Disable HNSW during bulk load by setting `indexing_threshold_kb` very high, then restore it after ingestion.
- Expect days for 400GB+ datasets.
- For small datasets under 25MB, re-indexing from source is faster than using a migration tool.

## Gotchas

- **Do not delete the old collection before verification**: alias rollback is only possible while the old collection still exists.
- **Do not forget the application embedder**: queries must switch to the new embedding model when the alias points at the new vector space.
- **Payloads are not copied by aliases**: migrate payloads explicitly.
- **Chunk-level sparse vectors behave differently**: BM25 and TF-IDF quality can shift, especially for non-English text without stop-word removal.
- **ColBERT can dominate I/O**: users have reported millions-of-points latency dropping from 13s to 2s after removing co-located ColBERT vectors.

## Output template

```markdown
## Qdrant model migration plan

**Status:** planned | needs data | blocked
**Current collection:** `<name>`
**Target strategy:** zero-downtime alias swap | side-by-side | dense-to-hybrid | re-index from source

### Compatibility
| Check | Result | Evidence |
| --- | --- | --- |
| Model/provider changed | yes/no | <details> |
| Dimensions changed | yes/no | <old -> new> |
| Named vectors required | yes/no | <fields> |
| Sparse vectors added | yes/no | <dense/sparse config> |

### Steps
1. <collection creation or alias step>
2. <re-embedding/backfill step>
3. <verification and rollback step>

### Risks
- <payload migration, latency, ColBERT, BM25, or rollback risk>
```

## Quality gate

- [ ] The plan states whether re-embedding is required and why.
- [ ] The plan creates a new collection for model replacement, named-vector additions, or dense-to-hybrid migration.
- [ ] Alias use includes payload migration, verification, rollback, and delayed old-collection deletion.
- [ ] Side-by-side plans define both vector fields at collection creation and use `UpdateVectors` for backfill.
- [ ] Large migrations include batch size, parallel stream, and `indexing_threshold_kb` guidance.
- [ ] Search quality is verified before the alias switch is considered final.

## References

- [Collection aliases](https://qdrant.tech/documentation/manage-data/collections/?s=collection-aliases)
- [Switch collection](https://qdrant.tech/documentation/manage-data/collections/?s=switch-collection)
- [Collection with multiple vectors](https://qdrant.tech/documentation/manage-data/collections/?s=collection-with-multiple-vectors)
- [Update vectors](https://qdrant.tech/documentation/manage-data/points/?s=update-vectors)
- [Update mode](https://qdrant.tech/documentation/manage-data/points/?s=update-mode)
- [Quantization](https://qdrant.tech/documentation/manage-data/quantization/)
- [Bulk upload](https://qdrant.tech/documentation/tutorials-develop/bulk-upload/)
- [Inference docs](https://qdrant.tech/documentation/inference/)
