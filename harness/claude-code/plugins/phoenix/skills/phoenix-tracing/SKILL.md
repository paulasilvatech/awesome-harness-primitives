---
name: phoenix-tracing
description: >-
  Instrument Python and TypeScript LLM applications with Phoenix AI observability using
  OpenInference semantic conventions, arize-phoenix-otel, @arizeai/phoenix-otel, spans, sessions,
  metadata, annotations, and production masking. Use when setting up Phoenix tracing, creating
  custom spans, adding OpenInference attributes, or deploying tracing to production.
license: Apache-2.0
metadata:
  author: "oss@arize.com"
  compatibility: >-
    Requires Phoenix server. Python skills need arize-phoenix-otel; TypeScript skills need
    @arizeai/phoenix-otel.
  languages: Python, TypeScript
  version: 1.0.0
---

<!-- Generated from harness/github-copilot/plugins/phoenix/skills/phoenix-tracing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Phoenix tracing

Instrument LLM applications for Phoenix with OpenInference traces, spans, attributes, projects, sessions, metadata, annotations, and production-safe export settings.

## When to invoke

- "Set up Phoenix tracing for this Python LLM app."
- "Add OpenInference spans to this TypeScript agent."
- "Create custom spans for LLM operations."
- "Add Phoenix session or project tracking."
- "Deploy Phoenix tracing to production with masking."

## Prerequisites and context

- A Phoenix server must be available.
- Python projects need `arize-phoenix-otel`.
- TypeScript projects need `@arizeai/phoenix-otel` and may also use `@arizeai/phoenix-client`; Python client work may use `arize-phoenix-client`.
- Follow OpenInference semantic conventions from the bundled span and fundamentals references.

## Reference map

| Priority | Category | Description | Prefix |
| --- | --- | --- | --- |
| 1 | Setup | Installation and endpoint configuration | `setup-*` |
| 2 | Instrumentation | Auto and manual tracing | `instrumentation-*` |
| 3 | Span Types | 9 span kinds with attributes | `span-*` |
| 4 | Organization | Projects and sessions | `projects-*`, `sessions-*` |
| 5 | Enrichment | Custom metadata | `metadata-*` |
| 6 | Production | Batch processing and masking | `production-*` |
| 7 | Feedback | Annotations and evaluation | `annotations-*` |

## Procedure

1. Identify language: Python or TypeScript.
2. Read `references/setup-python.md` or `references/setup-typescript.md` first.
3. Choose auto instrumentation for supported frameworks, or manual instrumentation for custom LLM, chain, retriever, tool, agent, embedding, reranker, guardrail, or evaluator operations.
4. Read the relevant `span-<type>.md` file for required attributes before writing spans.
5. Add project and session grouping when traces must be filtered by application or conversation.
6. Add metadata and annotations only when the workflow needs enrichment, feedback, or evaluation.
7. For production, read `production-python.md` or `production-typescript.md` for batching, masking, and deployment settings before enabling export broadly.

## Navigation patterns

```text
references/setup-*              # Installation and configuration
references/instrumentation-*    # Auto and manual tracing
references/span-*               # Span type specifications
references/sessions-*           # Session tracking
references/production-*         # Production deployment
references/fundamentals-*       # Core concepts
references/attributes-*         # Attribute specifications
references/*-python.md          # Python implementations
references/*-typescript.md      # TypeScript implementations
```

Common workflows:

| Workflow | Reading order |
| --- | --- |
| Quick Start | START HERE: `setup-{lang}` → `instrumentation-auto-{lang}` → check Phoenix for OpenAI, LangChain, or other supported frameworks. |
| Custom Spans | `setup-{lang}` → `instrumentation-manual-{lang}` → `span-{type}`. |
| Session Tracking | `sessions-{lang}` for conversation grouping patterns. |
| Production | `production-{lang}` for batching, masking, and deployment. |

## Span categories

| Span reference | Use for |
| --- | --- |
| `span-llm.md` | LLM API calls, model, tokens, messages, and cost. |
| `span-chain.md` | Multi-step workflows and pipelines. |
| `span-retriever.md` | Document retrieval, documents, and scores. |
| `span-tool.md` | Function/API calls, names, and parameters. |
| `span-agent.md` | Multi-step reasoning agents. |
| `span-embedding.md` | Vector generation. |
| `span-reranker.md` | Document re-ranking. |
| `span-guardrail.md` | Safety checks. |
| `span-evaluator.md` | LLM evaluation. |

## Progressive disclosure and bundled resources

- `references/setup-python.md` and `references/setup-typescript.md`: install and configure tracing.
- `references/instrumentation-auto-python.md`, `references/instrumentation-auto-typescript.md`, `references/instrumentation-manual-python.md`, and `references/instrumentation-manual-typescript.md`: tracing implementation patterns.
- `references/span-llm.md`, `references/span-chain.md`, `references/span-retriever.md`, `references/span-tool.md`, `references/span-agent.md`, `references/span-embedding.md`, `references/span-reranker.md`, `references/span-guardrail.md`, and `references/span-evaluator.md`: full attribute schemas.
- `references/projects-python.md`, `references/projects-typescript.md`, `references/sessions-python.md`, and `references/sessions-typescript.md`: grouping traces by application and conversation.
- `references/metadata-python.md`, `references/metadata-typescript.md`, `references/production-python.md`, `references/production-typescript.md`, `references/annotations-overview.md`, `references/annotations-python.md`, and `references/annotations-typescript.md`: enrichment, masking, batching, and feedback.
- `references/fundamentals-overview.md`, `references/fundamentals-required-attributes.md`, `references/fundamentals-universal-attributes.md`, and `references/fundamentals-flattening.md`: traces, spans, attributes, common attributes such as `user.id` and `session.id`, and JSON flattening rules.

## Output template

```markdown
## Phoenix tracing plan — <application or workflow>

**Status:** implemented | plan only | blocked
**Language:** Python | TypeScript
**Instrumentation:** auto | manual | mixed
**Phoenix endpoint:** `<endpoint or unknown>`

| Trace area | Reference used | Span kind or attribute set | Implementation note |
| --- | --- | --- | --- |
| Setup | `references/setup-<lang>.md` | <endpoint/project> | <change or instruction> |
| Operation | `references/span-<type>.md` | <span kind> | <attributes added> |
| Production | `references/production-<lang>.md` | masking/batching | <setting or blocker> |

### Validation
- Phoenix trace visible: pass | fail | not checked
- Required OpenInference attributes present: pass | fail | not checked
```

## Quality gate

- [ ] CRITICAL production masking and batching guidance was checked before broad deployment.
- [ ] Setup reference for the project language was read before instrumentation.
- [ ] Auto versus manual instrumentation was chosen based on the framework and operation.
- [ ] Each custom span maps to a documented OpenInference span kind.
- [ ] Required attributes from `fundamentals-required-attributes.md` and the relevant `span-*` file are present.
- [ ] `user.id`, `session.id`, project, metadata, and annotations are added only when useful and privacy-safe.
- [ ] Production deployments account for batching and PII masking.
- [ ] The result names the Phoenix server endpoint or states why it is unknown.

## References

- [Phoenix Documentation](https://docs.arize.com/phoenix)
- [OpenInference Spec](https://github.com/Arize-ai/openinference/tree/main/spec)
- [Python OTEL Package](https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing)
- [Python Client Package](https://arize.com/docs/phoenix)
- [TypeScript Packages](https://arize-ai.github.io/phoenix/)
