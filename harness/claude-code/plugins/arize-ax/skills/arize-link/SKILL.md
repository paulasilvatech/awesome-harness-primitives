---
name: arize-link
description: >-
  Generate Arize UI deep links for traces, spans, sessions, datasets, labeling queues, evaluators,
  and annotation configs using base64 org and space IDs, resource IDs, and trace/session time
  windows. Use when the user wants to link to, open, share, or debug an Arize trace, span,
  session, dataset, queue, evaluator, or annotation config.
metadata:
  author: arize
  version: 1.0
---

<!-- Generated from harness/github-copilot/plugins/arize-ax/skills/arize-link/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Arize link

Build clickable Arize UI URLs from exported IDs, logs, or existing browser URLs by validating base64 path IDs, selecting the right resource template, and preserving or computing trace time windows.

## When to invoke

- "Create an Arize link for this trace ID."
- "Open this span in Arize."
- "Give me a URL for this dataset."
- "Link to the labeling queue."
- "Share the evaluator version in Arize."

## Inputs

| Resource | Required inputs | Optional inputs |
| --- | --- | --- |
| Trace | `org_id`, `space_id`, `project_id`, `trace_id`, `startA`, `endA` | `span_id`, `base_url` |
| Span | `org_id`, `space_id`, `project_id`, `trace_id`, `span_id`, `startA`, `endA` | `base_url` |
| Session | `org_id`, `space_id`, `project_id`, `session_id`, `startA`, `endA` | `base_url` |
| Dataset | `org_id`, `space_id`, `dataset_id` | `selectedTab=examples|experiments`, `base_url` |
| Queue list | `org_id`, `space_id` | `base_url` |
| Specific queue | `org_id`, `space_id`, `queue_id` | `base_url` |
| Evaluator | `org_id`, `space_id`, `evaluator_id` | `version`, `base_url` |
| Annotation configs | `org_id`, `space_id` | `base_url` |

Default `base_url` is `https://app.arize.com`; override it only for on-prem deployments.

## ID validation

All path IDs must be base64-encoded with characters `A-Za-z0-9+/=`. Raw numeric IDs produce valid-looking URLs that 404. If the user provides a number, ask them to copy the ID directly from an Arize browser URL such as `https://app.arize.com/organizations/{org_id}/spaces/{space_id}/…`. If a raw internal ID is available, such as `Organization:1:abC1`, base64-encode it before inserting it into the URL.

## URL templates

| Resource | Template |
| --- | --- |
| Trace | `{base_url}/organizations/{org_id}/spaces/{space_id}/projects/{project_id}?selectedTraceId={trace_id}&queryFilterA=&selectedTab=llmTracing&timeZoneA=America%2FLos_Angeles&startA={start_ms}&endA={end_ms}&envA=tracing&modelType=generative_llm` |
| Span highlight | Append `&selectedSpanId={span_id}` to the trace URL. |
| Session | `{base_url}/organizations/{org_id}/spaces/{space_id}/projects/{project_id}?selectedSessionId={session_id}&queryFilterA=&selectedTab=llmTracing&timeZoneA=America%2FLos_Angeles&startA={start_ms}&endA={end_ms}&envA=tracing&modelType=generative_llm` |
| Dataset examples | `{base_url}/organizations/{org_id}/spaces/{space_id}/datasets/{dataset_id}?selectedTab=examples` |
| Dataset experiments | `{base_url}/organizations/{org_id}/spaces/{space_id}/datasets/{dataset_id}?selectedTab=experiments` |
| Queue list | `{base_url}/organizations/{org_id}/spaces/{space_id}/queues` |
| Specific queue | `{base_url}/organizations/{org_id}/spaces/{space_id}/queues/{queue_id}` |
| Evaluator latest | `{base_url}/organizations/{org_id}/spaces/{space_id}/evaluators/{evaluator_id}` |
| Evaluator version | `{base_url}/organizations/{org_id}/spaces/{space_id}/evaluators/{evaluator_id}?version={version_url_encoded}` |
| Annotation configs | `{base_url}/organizations/{org_id}/spaces/{space_id}/annotation-configs` |

URL-encode `version`; for example, a trailing `=` becomes `%3D`.

## Time range rules

`startA` and `endA` are required epoch milliseconds for trace, span, and session links. Omitting them defaults to the last 7 days and can show "no recent data" when the trace falls outside that window.

| Priority | Source | Rule |
| --- | --- | --- |
| 1 | User-provided URL | Extract and reuse `startA` and `endA` directly. |
| 2 | Span `start_time` | Pad by ±1 day, or ±1 hour for a tighter window. |
| 3 | Fallback | Use last 90 days: `now - 90d` to `now`. |

Prefer tight windows because 90-day windows load slowly.

## Procedure

1. Gather IDs from the user, exported trace data, logs, or an existing Arize URL.
2. Validate `org_id`, `space_id`, and other path IDs as base64.
3. Determine `startA` and `endA` for trace/span/session links using the priority order.
4. Select the resource template and URL-encode query values such as evaluator `version`.
5. Present a clickable Markdown link.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| "No data" or empty view | Trace outside time window | Widen `startA`/`endA`: ±1h -> ±1d -> 90d. |
| 404 | Wrong ID or non-base64 ID | Re-check `org_id`, `space_id`, and `project_id` from the browser URL. |
| Span not highlighted | `span_id` belongs to a different trace | Verify `span_id` against exported span data. |
| `org_id` unknown | `ax` CLI does not expose it | Ask the user to copy it from `https://app.arize.com/organizations/{org_id}/spaces/{space_id}/…`. |

## Progressive disclosure and bundled resources

- `references/EXAMPLES.md`: concrete URLs for every supported Arize link type.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `arize-trace` | skill | You need to export spans to obtain `trace_id`, `span_id`, or `start_time` before linking. |

The trace/span path uses `trace/span` inputs. `selectedTab` accepts `examples` or `experiments`. Evaluator versions may appear as `?version=…`. Treat missing time range as `CRITICAL`. Preserve the raw-ID note: `). If you have a raw internal ID (e.g. `.

## Output template

```markdown
## Arize link result

**Status:** linked | blocked
**Resource:** `trace | span | session | dataset | queue | evaluator | annotation-configs`

[Open in Arize](<generated URL>)

### Inputs used
- `org_id`: `<base64 id>`
- `space_id`: `<base64 id>`
- Resource ID: `<id>`
- Time range: `<startA>-<endA or not required>`
```

## Quality gate

- [ ] `org_id` and `space_id` are base64 path IDs, not raw numeric IDs.
- [ ] The selected URL template matches the requested resource.
- [ ] Trace, span, and session links include `startA` and `endA` in epoch milliseconds.
- [ ] Existing `startA` and `endA` values from a user-provided URL were preserved when available.
- [ ] Evaluator `version` was URL-encoded when present.
- [ ] The final answer includes a clickable Markdown link.

## References

- [Arize application](https://app.arize.com)
