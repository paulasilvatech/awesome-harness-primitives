# Evaluation, Observability, and Cost

You cannot govern what you do not measure. Instrument quality, behavior, and spend before scaling.

## Evaluation

- **Offline evals.** Build a test set of representative inputs with expected properties. Score with metrics for relevance, groundedness, coherence, safety, and task success. Azure AI Foundry provides an evaluation framework for these.
- **LLM as judge.** Use a strong model to grade outputs against a rubric where exact match does not apply. Calibrate the judge against human labels.
- **Regression gates.** Run evals in CI (GitHub Actions) so a prompt, model, or routing change that lowers quality fails the build.
- **Online evals.** Sample production traffic and score it continuously to catch drift.

## Observability

- **OpenTelemetry GenAI.** Emit traces and metrics using the GenAI semantic conventions: spans per model call and per tool call, with token counts, model name, latency, and outcome.
- **Distributed tracing.** Correlate a user request through routing, retrieval, tool calls, and model calls. Azure Monitor and Application Insights collect and visualize these.
- **Foundry tracing.** Use built-in tracing for agent runs to inspect the full chain of thoughts, tool calls, and messages.
- **Key signals.** Latency per step, token usage per model class, cache hit rate, tool error rate, guardrail triggers, and groundedness scores.

## Cost control

- **Attribute spend.** Tag usage by model class, tenant, and feature. Track blended cost from the real model mix, not a flat assumption.
- **Levers, in order of impact.** Prompt caching and semantic caching, routing easy work to smaller models, trimming context, and reducing retries. A fixed entitlement pool means cutting consumption cuts overage more than proportionally.
- **Budgets and alerts.** Set per-feature and per-tenant budgets with alerts before limits. Front models with the AI gateway to enforce token limits (see `apim-ai-gateway`).
- **Forecast.** Model the curve as adoption grows; do not assume today's mix holds.

## Checklist

- An eval set exists and runs in CI.
- Traces use OpenTelemetry GenAI conventions and reach App Insights.
- Dashboards show latency, token mix, cache hit rate, and guardrail triggers.
- Spend is attributed by model class and tenant, with budgets and alerts.

## Sources

- [Azure AI Foundry evaluation](https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Monitor generative AI applications](https://learn.microsoft.com/azure/ai-foundry/how-to/monitor-applications)
- [Azure Well-Architected cost optimization](https://learn.microsoft.com/azure/well-architected/cost-optimization/)
