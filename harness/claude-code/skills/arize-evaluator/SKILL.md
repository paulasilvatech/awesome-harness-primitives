---
name: arize-evaluator
description: >-
  Create, update, and run Arize LLM-as-judge evaluators and tasks for spans, traces, sessions,
  projects, datasets, and experiments. Use when the user mentions create evaluator, LLM judge,
  hallucination, faithfulness, correctness, relevance, run eval, score spans, score experiment,
  trigger-run, column mapping, continuous monitoring, or evaluator prompt improvement.
metadata:
  author: arize
  compatibility: Requires the ax CLI and a configured Arize profile with an AI integration.
  version: 1.0
---

<!-- Generated from harness/github-copilot/skills/arize-evaluator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Arize evaluator

Design evaluator prompts, create or update Arize evaluators, map task columns, run evaluations, and troubleshoot `ax` failures without fabricating results or reading local credential files.

## When to invoke

- "Create an Arize LLM judge evaluator."
- "Run a hallucination eval on spans."
- "Score this experiment for correctness."
- "Fix evaluator column mapping."
- "Set up continuous monitoring with trigger-run."

## Prerequisites and context

Proceed directly with the needed `ax` command; do not check versions, environment variables, or profiles up front. If an `ax` command fails, react to the error.

| Symptom | Resolution |
| --- | --- |
| `command not found` or version error | Read `references/ax-setup.md`. |
| `401 Unauthorized` or missing API key | Run `ax profiles show`. If the profile is missing or wrong, use `references/ax-profiles.md`; if the user lacks a key, direct them to https://app.arize.com/admin > API Keys. |
| Space unknown | Run `ax spaces list` and select by name, or ask the user. |
| LLM provider call fails because `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is missing | Run `ax ai-integrations list --space SPACE` to check platform-managed credentials. If none exist, ask for a key or use the `arize-ai-provider-integration` skill. |

Security rule: never read `.env` files or search the filesystem for credentials. Use `ax profiles` for Arize credentials and `ax ai-integrations` for LLM provider keys. If credentials are unavailable through those channels, ask the user.

`SPACE`, `--space`, and `ARIZE_SPACE` accept either a space name such as `my-workspace` or a base64 space ID such as `U3BhY2U6...`; find values with `ax spaces list`.

## Evaluator model

| Field | Meaning |
| --- | --- |
| Template | Judge prompt with `{variable}` placeholders such as `{input}`, `{output}`, `{context}`, or `{conversation}`. |
| Classification choices | Allowed labels such as `factual` / `hallucinated`, `correct` / `incorrect`, or `pass` / `fail`; each may carry a numeric score. |
| AI Integration | Stored LLM provider credentials used by the evaluator. |
| Model | Judge model such as `gpt-4o` or `claude-sonnet-4-5`. |
| Invocation params | JSON model settings such as `{"temperature": 0}`. |
| Optimization direction | `maximize` when higher scores are better, `minimize` when lower scores are better. |
| Data granularity | `span`, `trace`, or `session`; most evaluators default to `span`. |

Evaluators are versioned. Every prompt or model change creates a new immutable version, and the newest version is active.

## Task model and granularity

| Task field | Meaning |
| --- | --- |
| Evaluators | One or more evaluators to run. |
| Column mappings | Maps template variables to span or run fields, such as `input` → `attributes.input.value`. |
| Query filter | SQL-style expression such as `span_kind = 'LLM'` to choose spans or runs. |
| Continuous | Project task option that scores new spans as they arrive. |
| Sampling rate | Continuous task fraction from 0 to 1. |

| Granularity | What it evaluates | Use for | Result column prefix |
| --- | --- | --- | --- |
| `span` | Individual spans | Q&A correctness, hallucination, relevance | `eval.{name}.label`, `eval.{name}.score`, `eval.{name}.explanation` |
| `trace` | Spans grouped by `context.trace_id` | Agent trajectory and full call-chain task correctness | `trace_eval.{name}.label`, `trace_eval.{name}.score`, `trace_eval.{name}.explanation` |
| `session` | Traces grouped by `attributes.session.id` and ordered by `start_time` | Multi-turn coherence, tone, and conversation quality | `session_eval.{name}.label`, `session_eval.{name}.score`, `session_eval.{name}.explanation` |

For trace granularity, values are grouped by `context.trace_id` and comma-joined, with each value truncated to 100K characters. For session granularity, trace-level grouping happens first, then traces are ordered by `start_time` and grouped by `attributes.session.id`; session-level values are capped at 100K characters total. At session granularity, `{conversation}` renders as a JSON array of `{input, output}` turns from `attributes.input.value` / `attributes.llm.input_messages` and `attributes.output.value` / `attributes.llm.output_messages`. At span or trace granularity, `{conversation}` is resolved like any other mapped variable.

Multi-evaluator tasks may contain different granularities. Runtime uses the highest granularity, session > trace > span, and splits into one child run per evaluator. Per-evaluator `query_filter` in the task evaluators JSON narrows included spans, such as only tool-call spans within a session.

## Template design rules

| Rule | Requirement |
| --- | --- |
| Portable variables | Use `{input}`, `{output}`, and `{context}`, not project-specific names such as `{attributes_input_value}`. Wire actual paths in `column_mappings`. |
| Binary first | Prefer two labels such as `hallucinated` / `factual` because more labels increase ambiguity and lower inter-rater reliability. |
| Exact label output | Prompt the judge to respond with only one label string, and ensure labels exactly match `--classification-choices` by spelling and casing. |
| Low temperature | Use `--invocation-params '{"temperature": 0}'` for reproducible scoring. |
| Explanations during setup | Use `--include-explanations` while debugging judge behavior. |
| Shell quoting | Pass templates in single quotes, for example `--template 'Judge this: {input} → {output}'`; double quotes can cause shell interpolation. |
| Classification choices | Always set `--classification-choices`; omitting it can fail with "missing rails and classification choices." |

## Limits

Never fabricate evaluation results. If a task fails, is cancelled, or produces no scores, report the failure and explain what happened. Do not perform a manual evaluation, invent quality scores, estimate percentages, or present agent analysis as Arize evaluation output. Recommend fixing the issue and retrying, trying the Arize UI, verifying credentials with `ax ai-integrations list`, or contacting `https://arize.com/support`.

## Progressive disclosure and bundled resources

- `references/evaluator-crud-workflows.md`: GraphQL CRUD calls, project and experiment evaluator setup, trigger-run operations, task management, column mapping, continuous monitoring, and troubleshooting.
- `references/ax-setup.md`: `ax` install and version remediation.
- `references/ax-profiles.md`: profile creation and update workflow.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `arize-ai-provider-integration` | skill | Creating, updating, or deleting LLM provider credentials. |
| `arize-trace` | skill | Exporting spans to discover column paths and time ranges. |
| `arize-experiment` | skill | Creating experiments and exporting runs for experiment column mappings. |
| `arize-dataset` | skill | Exporting dataset examples to find input fields when runs omit them. |
| `arize-link` | skill | Creating deep links to evaluators and tasks in the Arize UI. |

<!-- Baseline technical terms preserved for loss check: `"input" → "attributes.input.value"`, `"span_kind = 'LLM'"`, `--data-granularity`, `--template`, `.explanation`, `.score`, `CRITICAL`, `agent-generated`, `create/update`, `creating/updating`, `data-granularity`, `dataset/experiment`, `open-ended`, `project/experiment`, `spans/runs`, `traces/spans` -->

## Output template

```markdown
### Arize evaluator result

**Status:** created | updated | run complete | failed | blocked
**Space:** `<SPACE or ARIZE_SPACE>`
**Evaluator:** `<name/id/version>`
**Task:** `<task id or n/a>`
**Granularity:** span | trace | session

| Step | Command | Result |
| --- | --- | --- |
| <step> | `ax ...` | <output summary> |

### Column mappings
| Template variable | Data field |
| --- | --- |
| `{input}` | `<field path>` |
| `{output}` | `<field path>` |

### Evaluation results
- <actual Arize result, task status, or failure reason; never fabricated>
```

## Quality gate

- [ ] The task proceeded with the needed `ax` command before speculative prechecks.
- [ ] `SPACE` / `--space` / `ARIZE_SPACE` was resolved by name or base64 ID.
- [ ] Credentials were checked only through `ax profiles` or `ax ai-integrations`; no `.env` files were read.
- [ ] Template labels exactly match `--classification-choices`.
- [ ] `--invocation-params '{"temperature": 0}'` is used unless a different temperature is justified.
- [ ] Column mappings connect every template variable to real span, trace, session, project, dataset, or experiment fields.
- [ ] Results reported are actual Arize outputs; failures are not converted into manual scores.

## References

- [Arize admin API keys](https://app.arize.com/admin)
- [Arize support](https://arize.com/support)
