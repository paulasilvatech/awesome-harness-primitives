---
name: arize-experiment
description: >-
  Create, run, export, compare, delete, and troubleshoot Arize experiments with the ax CLI,
  including real model inference, run files, evaluations, result analysis, and dataset-linked
  experiment workflows. Use this skill when the user asks to create experiment, run experiment,
  compare models, evaluate AI, benchmark prompts, A/B test models, export experiment results,
  measure accuracy, or inspect experiment runs in Arize.
metadata:
  author: arize
  compatibility: Requires the ax CLI and a configured Arize profile.
  version: 1.0
---

<!-- Generated from harness/github-copilot/skills/arize-experiment/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Arize experiment

Create and analyze Arize experiments by exporting dataset examples, calling the real model API for every example, creating `runs.json`, loading it with `ax experiments create`, and comparing exported evaluations without fabricating outputs or scores.

## When to invoke

- "Create an Arize experiment for this dataset."
- "Run this prompt against a dataset and upload results to Arize."
- "Compare two model experiments."
- "Export experiment runs and analyze correctness scores."
- "Troubleshoot an ax experiments error."

## Prerequisites and context

Proceed directly with the needed `ax` command. Do not check versions, environment variables, or profiles upfront. If a command fails, troubleshoot from the error.

| Context | Rule |
| --- | --- |
| `SPACE` | All `--space` flags and `ARIZE_SPACE` accept a space name such as `my-workspace` or a base64 space ID such as `U3BhY2U6...`; find spaces with `ax spaces list`. |
| Credentials | Never read `.env` files or search the filesystem for credentials. Use `ax profiles` for Arize credentials and `ax ai-integrations` for LLM provider keys. If credentials are absent, ask the user. |
| API keys | For `401 Unauthorized`, run `ax profiles show`; if missing or wrong, use `references/ax-profiles.md`. If the user needs a key, direct them to https://app.arize.com/admin > API Keys. |
| Setup failure | For `command not found` or version errors, use `references/ax-setup.md`. |
| Space unknown | Run `ax spaces list` and choose by name, or ask the user. |
| Project unclear | Ask the user, or run `ax projects list -o json --limit 100` and present options. |
| Model calls | Must call the real model API specified by the user for every dataset example. Never fabricate, simulate, or hardcode model outputs, latencies, labels, scores, or explanations. Stop if SDKs, credentials, or network access are missing. |

## Core concepts

| Term | Meaning |
| --- | --- |
| Experiment | A named evaluation run tied to a dataset and specific dataset version. |
| Experiment Run | One dataset example's result: model output, optional evaluations, and optional metadata. |
| Dataset | Versioned collection of examples; every experiment is tied to a dataset version. |
| Evaluation | Named metric such as `correctness` or `relevance` with optional `label`, `score`, and `explanation`. |

Typical flow: export a dataset → process each example with a real model → collect outputs and evaluations → create an experiment with the runs.

## Experiment commands

| Task | Command |
| --- | --- |
| List experiments | `ax experiments list` |
| Filter by dataset | `ax experiments list --dataset DATASET_NAME --space SPACE --limit 20` |
| Paginate | `ax experiments list --cursor CURSOR_TOKEN` |
| JSON list | `ax experiments list -o json` |
| Get by ID | `ax experiments get NAME_OR_ID -o json` |
| Get by name | `ax experiments get NAME_OR_ID --dataset DATASET_NAME --space SPACE` |
| Export default REST | `ax experiments export EXPERIMENT_NAME --dataset DATASET_NAME --space SPACE` |
| Export all with Flight | `ax experiments export EXPERIMENT_NAME --dataset DATASET_NAME --space SPACE --all` |
| Export to directory | `ax experiments export EXPERIMENT_NAME --dataset DATASET_NAME --space SPACE --output-dir ./results` |
| Export to stdout | `ax experiments export EXPERIMENT_NAME --dataset DATASET_NAME --space SPACE --stdout` |
| Inspect first run | `ax experiments export EXPERIMENT_NAME --dataset DATASET_NAME --space SPACE --stdout | jq '.[0]'` |
| Create from JSON | `ax experiments create --name "gpt-4o-baseline" --dataset DATASET_NAME --space SPACE --file runs.json` |
| Create from CSV | `ax experiments create --name "claude-test" --dataset DATASET_NAME --space SPACE --file runs.csv` |
| Create from stdin | `echo '[{"example_id":"ex_001","output":"Paris"}]' | ax experiments create --name "my-experiment" --dataset DATASET_NAME --space SPACE --file -` |
| Delete | `ax experiments delete NAME_OR_ID` |
| Delete by name | `ax experiments delete NAME_OR_ID --dataset DATASET_NAME --space SPACE` |
| Force delete | `ax experiments delete NAME_OR_ID --force` |

### Command flags and fields

| Command | Important flags |
| --- | --- |
| `ax experiments list` | `--dataset`, `--limit, -l` default `15` max `100`, `--cursor`, `-o, --output` (`table`, `json`, `csv`, `parquet`, or file path), `-p, --profile` default `default`. |
| `ax experiments get` | Positional `NAME_OR_ID`; `--dataset` required when using experiment name instead of ID; `--space` required when using dataset name instead of ID; `-o, --output`; `-p, --profile`. |
| `ax experiments export` | Positional `NAME_OR_ID`; `--dataset`; `--space`; `--all`; `--output-dir` default `.`; `--stdout`; `-p, --profile`. |
| `ax experiments create` | `--name, -n`; `--dataset`; `--space, -s`; `--file, -f` as `CSV`, `JSON`, `JSONL`, or `Parquet`; `-o, --output`; `-p, --profile`. |
| `ax experiments delete` | Positional `NAME_OR_ID`; `--dataset`; `--space`; `--force, -f`; `-p, --profile`. |

`ax experiments get` returns `id`, `name`, `dataset_id`, `dataset_version_id`, `experiment_traces_project_id`, `created_at`, and `updated_at`.

## Run file schema

Each run must correspond to one dataset example. Required columns are `example_id` and `output`; additional columns pass through as `additionalProperties`.

```json
{
  "example_id": "ex_001",
  "output": "The answer is 4.",
  "evaluations": {
    "correctness": { "label": "correct", "score": 1.0 },
    "relevance": { "score": 0.95, "explanation": "Directly answers the question" }
  },
  "metadata": {
    "model": "gpt-4o",
    "temperature": 0.7,
    "latency_ms": 1234
  }
}
```

Evaluation fields are optional, but at least one of `label`, `score`, or `explanation` should be present per evaluation. Useful labels include `correct`, `incorrect`, and `partial`; scores are typically `0.0` to `1.0`.

## Procedure

1. Find and inspect the dataset:

```bash
ax datasets list --space SPACE
ax datasets export DATASET_NAME --space SPACE --stdout | jq 'length'
ax datasets export DATASET_NAME --space SPACE
```

2. Export examples and inspect the JSON to identify the input field, such as `input`, `question`, or `prompt`.
3. Write an inference script that reads examples from stdin, calls the requested provider for every example, records `latency_ms`, and emits a JSON array of runs to stdout.

```bash
ax datasets export DATASET_NAME --space SPACE --stdout | python3 infer.py > runs.json
```

Provider SDK environment variables commonly used by the script include `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `CUSTOM_BASE_URL`, `CUSTOM_API_KEY`, and `CUSTOM_MODEL`. A custom OpenAI-compatible endpoint may use `https://my-proxy.example.com/v1`; use it for Azure OpenAI, NVIDIA NIM, local Ollama, or a test integration proxy. Use `MODEL_NAME` in metadata for the selected model.

4. Verify the run file before upload:

```bash
python3 -c "import json; runs=json.load(open('runs.json')); print(f'{len(runs)} runs'); print(json.dumps(runs[0], indent=2))"
```

5. Create and verify the experiment:

```bash
ax experiments create --name "gpt-4o-baseline" --dataset DATASET_NAME --space SPACE --file runs.json
ax experiments get "gpt-4o-baseline" --dataset DATASET_NAME --space SPACE
```

## Export and comparison analysis

REST export is lower friction, uses standard HTTPS, and returns up to 500 runs per page. Flight export with `--all` uses Arrow Flight over gRPC+TLS at `flight.arize.com:443` and is required for experiments with more than 500 runs. If REST returns exactly 500 runs, treat it as likely truncated and re-run with `--all`.

```bash
ax experiments export "experiment-a" --dataset DATASET_NAME --space SPACE --stdout > a.json
ax experiments export "experiment-b" --dataset DATASET_NAME --space SPACE --stdout > b.json
jq '[.[] | .evaluations.correctness.score] | add / length' a.json
jq '[.[] | .evaluations.correctness.score] | add / length' b.json
jq '[.[] | .evaluations.correctness.label] | group_by(.) | map({label: .[0], count: length})' a.json
jq 'length' a.json
```

Find differing examples and regressions:

```bash
jq -s '.[0] as $a | .[1][] | . as $run |
  {
    example_id: $run.example_id,
    b_score: $run.evaluations.correctness.score,
    a_score: ($a[] | select(.example_id == $run.example_id) | .evaluations.correctness.score)
  }' a.json b.json

jq -s '
  [.[0][] | select(.evaluations.correctness.label == "correct")] as $passed_a |
  [.[1][] | select(.evaluations.correctness.label != "correct") |
    select(.example_id as $id | $passed_a | any(.example_id == $id))
  ]
' a.json b.json
```

Score comparisons are most reliable with at least 30 examples per evaluator. With fewer examples, treat deltas as directional; a 5% difference on `n=10` may be noise. Always report sample size alongside scores.

## Troubleshooting

| Problem | Resolution |
| --- | --- |
| `ax: command not found` | Read `references/ax-setup.md`. |
| Version error | Read `references/ax-setup.md`. |
| `401 Unauthorized` | Inspect `ax profiles show`; fix profile with `references/ax-profiles.md`; direct the user to https://app.arize.com/admin > API Keys if they need a key. |
| `No profile found` | Create a profile with `references/ax-profiles.md`. |
| Space unknown | Run `ax spaces list`; choose by name where possible. |
| Project unclear | Ask the user or run `ax projects list -o json --limit 100`. |
| `Experiment not found` | Verify with `ax experiments list --space SPACE` and include `--dataset DATASET_NAME` when using a name. |
| `Dataset not found` | Check `ax datasets list`; the linked dataset may have been deleted. |
| `Invalid runs file` | Ensure each run has `example_id` and `output`. |
| `example_id mismatch` | Export the dataset and match run `example_id` values to dataset example IDs. |
| `No runs found` | Verify the experiment has runs with `ax experiments get`. |
| REST export exactly 500 runs | Re-run `ax experiments export ... --all`. |
| Missing model SDK or key | Stop and state the missing SDK, credential, or network access; do not fabricate outputs. |

## Progressive disclosure and bundled resources

- `references/ax-setup.md`: install and version troubleshooting for `ax`.
- `references/ax-profiles.md`: profile creation, update, inspection, and saved credentials.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `arize-dataset` | skill | The dataset must be created or exported before the experiment can run. |
| `arize-prompt-optimization` | skill | Experiment results should drive prompt improvements. |
| `arize-trace` | skill | Failing experiment runs need span-level trace inspection. |
| `arize-link` | skill | The user needs clickable UI links to traces from experiment runs. |

## Technical index

Preserve these Arize command placeholders, API names, and schema terms when editing or reporting: `CRUD`, `CRITICAL`, `MUST`, `CALL`, `REAL`, `MODEL`, `HERE`, `--stdout`, `--file -`, `Arrow/Flight`, `auto-escalation`, `host/port`, `create/update`, `custom`, `dataset/version`, `model/system`, `pass/fail/partial`, `evaluations`, `metadata`, `metric_name`, `run_001`, `experiment_abc123_20260305_141500`, `experiment_abc123_20260305_141500/runs.json`, `infer.py`, `user_input`, `output_text`, `base_url`, `api_key`, `max_tokens`, `anthropic`, `google-genai`, `generate_content`, `claude-sonnet-4-6`, `pip install openai`, `ax ai-integrations create`, `ax datasets export --stdout`, `ax experiments list --dataset DATASET_NAME --space SPACE`, `jq 'length' a.json`, and `references/ax-profiles.md.`

## Output template

```markdown
## Arize experiment result

**Status:** created | exported | compared | deleted | blocked
**Space:** `<SPACE or ARIZE_SPACE>`
**Dataset:** `<DATASET_NAME>`
**Experiment(s):** `<EXPERIMENT_NAME or NAME_OR_ID>`

### Commands run
- `<ax command>`

### Run file
| Field | Value |
| --- | --- |
| Runs | `<count>` |
| Required fields | `example_id`, `output` |
| Evaluations | `<names or none>` |
| Metadata | `<keys or none>` |

### Results
| Metric | Experiment A | Experiment B | Delta | Sample size |
| --- | --- | --- | --- | --- |
| `correctness.score` | `<value>` | `<value>` | `<delta>` | `<n>` |

### Validation
- Real model API called for every example: <yes/no/evidence>
- Upload or export verified: <command and result>
- Truncation checked: <REST count or --all used>
```

## Quality gate

- [ ] `SPACE`, `DATASET_NAME`, and `EXPERIMENT_NAME` or `NAME_OR_ID` are resolved before create, get, export, compare, or delete.
- [ ] No `.env` files or credential searches were used; `ax profiles` or `ax ai-integrations` handled credentials.
- [ ] Every generated run has `example_id` and `output`; evaluations contain `label`, `score`, or `explanation` when present.
- [ ] Real model APIs were called for every dataset example; no output, latency, label, score, or explanation was fabricated.
- [ ] REST exports returning exactly 500 runs were re-run with `--all`.
- [ ] Comparisons report sample size and treat fewer than 30 examples as directional.
- [ ] The final response includes commands run, result location or experiment ID, and any blocked credential or SDK requirement.

## References

- [Arize API keys](https://app.arize.com/admin)
