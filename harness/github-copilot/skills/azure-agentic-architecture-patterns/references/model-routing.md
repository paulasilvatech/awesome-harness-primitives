# Model Routing

Match each task to the cheapest model that meets the quality bar. A fixed entitlement or budget is spent fastest by sending easy work to expensive models.

## Tiers

Group models into classes and route by task difficulty. Indicative classes (verify exact prices and context limits on the model card and Microsoft Learn before quoting):

| Class | Use for | Notes |
| --- | --- | --- |
| mini / small | classification, routing, extraction, short answers, tool argument filling | cheapest, fastest, highest volume |
| standard | general reasoning, drafting, summarization, most agent steps | the default workhorse |
| premium | hard reasoning, long context synthesis, code review | reserve for steps that fail at standard |
| frontier | the hardest planning, multi-step proofs, ambiguous tasks | smallest share of traffic, highest unit cost |

The spread between classes can be very large per million tokens, so even small shifts of traffic from premium to mini move cost materially. Compute the blended cost from the actual mix; do not assume a flat rate.

## Routing strategies

- **Static rules.** Route by task type or by a classifier label. Cheapest to operate, predictable.
- **Cascade / fallback.** Try a small model first, escalate to a larger one only when a confidence or validation check fails. Saves cost on the easy majority.
- **Model router service.** Use a hosted router (for example the Azure AI Foundry model router, or GitHub Models for prototyping) that selects a model per request. Verify availability and behavior on Microsoft Learn.
- **Semantic routing.** Embed the request and route by similarity to labeled exemplars. Pairs well with a vector store.

## Design checklist

- Define task classes and the quality bar for each.
- Choose a primary model per class plus a fallback for availability.
- Add a validation or confidence gate before escalating tiers.
- Centralize routing behind the AI gateway (see `apim-ai-gateway`) so load balancing, retries, and token limits apply uniformly.
- Track per-class token share and blended cost (see evaluation-observability-cost.md).

## Sources

- [Azure AI Foundry model catalog and router](https://learn.microsoft.com/azure/ai-foundry/)
- [GitHub Models](https://docs.github.com/github-models)
- [Azure API Management for AI](https://learn.microsoft.com/azure/api-management/)
