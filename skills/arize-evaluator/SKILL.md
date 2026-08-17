---
name: "arize-evaluator"
description: >-
  Handles LLM-as-judge evaluation workflows on Arize including creating/updating evaluators, running
  evaluations on spans or experiments, managing tasks, trigger-run operations, column mapping, and
  continuous monitoring. Use when the user mentions create evaluator, LLM judge, hallucination,
  faithfulness, correctness, relevance, run eval, score spans, score experiment, trigger-run, column
  mapping, continuous monitoring, or improve evaluator prompt.
metadata:
  author: "arize"
  compatibility: "Requires the ax CLI and a configured Arize profile with an AI integration."
  version: "1.0"
---
# Arize Evaluator Skill

> **`SPACE`** — All `--space` flags and the `ARIZE_SPACE` env var accept a space **name** (e.g., `my-workspace`) or a base64 space **ID** (e.g., `U3BhY2U6...`). Find yours with `ax spaces list`.

This skill covers designing, creating, and running **LLM-as-judge evaluators** on Arize. An evaluator defines the judge; a **task** is how you run it against real data.

---

## Prerequisites

Proceed directly with the task — run the `ax` command you need. Do NOT check versions, env vars, or profiles upfront.

If an `ax` command fails, troubleshoot based on the error:
- `command not found` or version error → see references/ax-setup.md
- `401 Unauthorized` / missing API key → run `ax profiles show` to inspect the current profile. If the profile is missing or the API key is wrong, follow references/ax-profiles.md to create/update it. If the user doesn't have their key, direct them to https://app.arize.com/admin > API Keys
- Space unknown → run `ax spaces list` to pick by name, or ask the user
- LLM provider call fails (missing OPENAI_API_KEY / ANTHROPIC_API_KEY) → run `ax ai-integrations list --space SPACE` to check for platform-managed credentials. If none exist, ask the user to provide the key or create an integration via the **arize-ai-provider-integration** skill
- **Security:** Never read `.env` files or search the filesystem for credentials. Use `ax profiles` for Arize credentials and `ax ai-integrations` for LLM provider keys. If credentials are not available through these channels, ask the user.
- **CRITICAL — Never fabricate evaluation results:** If an evaluation task fails, is cancelled, or produces no scores, report the failure clearly and explain what went wrong. Do NOT perform a "manual evaluation," invent quality scores, estimate percentages, or present any agent-generated analysis as if it came from the Arize evaluation system. Instead suggest: (1) fix the identified issue and retry, (2) try running from the Arize UI, (3) verify integration credentials with `ax ai-integrations list`, (4) contact support at https://arize.com/support

---

## Concepts

### What is an Evaluator?

An **evaluator** is an LLM-as-judge definition. It contains:

| Field | Description |
|-------|-------------|
| **Template** | The judge prompt. Uses `{variable}` placeholders (e.g. `{input}`, `{output}`, `{context}`) that get filled in at run time via a task's column mappings. |
| **Classification choices** | The set of allowed output labels (e.g. `factual` / `hallucinated`). Binary is the default and most common. Each choice can optionally carry a numeric score. |
| **AI Integration** | Stored LLM provider credentials (OpenAI, Anthropic, Bedrock, etc.) the evaluator uses to call the judge model. |
| **Model** | The specific judge model (e.g. `gpt-4o`, `claude-sonnet-4-5`). |
| **Invocation params** | Optional JSON of model settings like `{"temperature": 0}`. Low temperature is recommended for reproducibility. |
| **Optimization direction** | Whether higher scores are better (`maximize`) or worse (`minimize`). Sets how the UI renders trends. |
| **Data granularity** | Whether the evaluator runs at the **span**, **trace**, or **session** level. Most evaluators run at the span level. |

Evaluators are **versioned** — every prompt or model change creates a new immutable version. The most recent version is active.

### What is a Task?

A **task** is how you run one or more evaluators against real data. Tasks are attached to a **project** (live traces/spans) or a **dataset** (experiment runs). A task contains:

| Field | Description |
|-------|-------------|
| **Evaluators** | List of evaluators to run. You can run multiple in one task. |
| **Column mappings** | Maps each evaluator's template variables to actual field paths on spans or experiment runs (e.g. `"input" → "attributes.input.value"`). This is what makes evaluators portable across projects and experiments. |
| **Query filter** | SQL-style expression to select which spans/runs to evaluate (e.g. `"span_kind = 'LLM'"`). Optional but important for precision. |
| **Continuous** | For project tasks: whether to automatically score new spans as they arrive. |
| **Sampling rate** | For continuous project tasks: fraction of new spans to evaluate (0–1). |

---

## Data Granularity

The `--data-granularity` flag controls what unit of data the evaluator scores. It defaults to `span` and only applies to **project tasks** (not dataset/experiment tasks — those evaluate experiment runs directly).

| Level | What it evaluates | Use for | Result column prefix |
|-------|-------------------|---------|---------------------|
| `span` (default) | Individual spans | Q&A correctness, hallucination, relevance | `eval.{name}.label` / `.score` / `.explanation` |
| `trace` | All spans in a trace, grouped by `context.trace_id` | Agent trajectory, task correctness — anything that needs the full call chain | `trace_eval.{name}.label` / `.score` / `.explanation` |
| `session` | All traces in a session, grouped by `attributes.session.id` and ordered by start time | Multi-turn coherence, overall tone, conversation quality | `session_eval.{name}.label` / `.score` / `.explanation` |

### How trace and session aggregation works

For **trace** granularity, spans sharing the same `context.trace_id` are grouped together. Column values used by the evaluator template are comma-joined into a single string (each value truncated to 100K characters) before being passed to the judge model.

For **session** granularity, the same trace-level grouping happens first, then traces are ordered by `start_time` and grouped by `attributes.session.id`. Session-level values are capped at 100K characters total.

### The `{conversation}` template variable

At session granularity, `{conversation}` is a special template variable that renders as a JSON array of `{input, output}` turns across all traces in the session, built from `attributes.input.value` / `attributes.llm.input_messages` (input side) and `attributes.output.value` / `attributes.llm.output_messages` (output side).

At span or trace granularity, `{conversation}` is treated as a regular template variable and resolved via column mappings like any other.

### Multi-evaluator tasks

A task can contain evaluators at different granularities. At runtime the system uses the **highest** granularity (session > trace > span) for data fetching and automatically **splits into one child run per evaluator**. Per-evaluator `query_filter` in the task's evaluators JSON further narrows which spans are included (e.g., only tool-call spans within a session).

---

## Bundled Resources

- [Arize evaluator CRUD, workflows, and troubleshooting](references/evaluator-crud-workflows.md) — For GraphQL CRUD calls, project/experiment evaluator setup, or error diagnosis, open this detailed evaluator reference.

## Best Practices for Template Design

### 1. Use generic, portable variable names

Use `{input}`, `{output}`, and `{context}` — not names tied to a specific project or span attribute (e.g. do not use `{attributes_input_value}`). The evaluator itself stays abstract; the **task's `column_mappings`** is where you wire it to the actual fields in a specific project or experiment. This lets the same evaluator run across multiple projects and experiments without modification.

### 2. Default to binary labels

Use exactly two clear string labels (e.g. `hallucinated` / `factual`, `correct` / `incorrect`, `pass` / `fail`). Binary labels are:
- Easiest for the judge model to produce consistently
- Most common in the industry
- Simplest to interpret in dashboards

If the user insists on more than two choices, that's fine — but recommend binary first and explain the tradeoff (more labels → more ambiguity → lower inter-rater reliability).

### 3. Be explicit about what the model must return

The template must tell the judge model to respond with **only** the label string — nothing else. The label strings in the prompt must **exactly match** the labels in `--classification-choices` (same spelling, same casing).

Good:
```
Respond with exactly one of these labels: hallucinated, factual
```

Bad (too open-ended):
```
Is this hallucinated? Answer yes or no.
```

### 4. Keep temperature low

Pass `--invocation-params '{"temperature": 0}'` for reproducible scoring. Higher temperatures introduce noise into evaluation results.

### 5. Use `--include-explanations` for debugging

During initial setup, always include explanations so you can verify the judge is reasoning correctly before trusting the labels at scale.

### 6. Pass the template in single quotes in bash

Single quotes prevent the shell from interpolating `{variable}` placeholders. Double quotes will cause issues:

```bash
# Correct
--template 'Judge this: {input} → {output}'

# Wrong — shell may interpret { } or fail
--template "Judge this: {input} → {output}"
```

### 7. Always set `--classification-choices` to match your template labels

The labels in `--classification-choices` must exactly match the labels referenced in `--template` (same spelling, same casing). Omitting `--classification-choices` causes task runs to fail with "missing rails and classification choices."

---

## Related Skills

- **arize-ai-provider-integration**: Full CRUD for LLM provider integrations (create, update, delete credentials)
- **arize-trace**: Export spans to discover column paths and time ranges
- **arize-experiment**: Create experiments and export runs for experiment column mappings
- **arize-dataset**: Export dataset examples to find input fields when runs omit them
- **arize-link**: Deep links to evaluators and tasks in the Arize UI

---

## Save Credentials for Future Use

See references/ax-profiles.md § Save Credentials for Future Use.
