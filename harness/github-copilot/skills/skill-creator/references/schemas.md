# Eval Schemas

The exact JSON shapes the skill-creator evaluation subsystem reads and writes. The viewer (`eval-viewer/generate_review.py`) and the aggregation script depend on these field names, so match them precisely.

## evals/evals.json

The test cases for a skill. Write the prompts first; add the `assertions` array in the grading step.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "assertions": [
        "The output is a valid .docx file",
        "The chart has labeled axes"
      ]
    }
  ]
}
```

- `id`: stable integer per eval.
- `prompt`: the realistic user request.
- `expected_output`: short description of a correct result.
- `files`: optional input file paths provided to the run.
- `assertions`: testable checks, added before grading. Prefer programmatically checkable statements.

## timing.json (per run)

Captured from the subagent task notification at completion. This is the only chance to record it.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## grading.json (per run)

One entry per assertion. The viewer requires exactly these field names.

```json
{
  "run_id": "eval-0-with_skill",
  "expectations": [
    { "text": "The output is a valid .docx file", "passed": true, "evidence": "file opens, OOXML valid" },
    { "text": "The chart has labeled axes", "passed": false, "evidence": "y-axis has no title" }
  ]
}
```

- Use `text`, `passed`, `evidence`. Do not use `name`, `met`, or `details`.

## benchmark.json (per iteration)

Optional benchmark summary. Produce this manually or with a project-specific aggregation script when quantitative grading is useful. The viewer's Benchmark tab reads this shape when a benchmark file is provided.

```json
{
  "skill_name": "example-skill",
  "configurations": [
    {
      "name": "with_skill",
      "pass_rate": { "mean": 0.86, "stddev": 0.05 },
      "time_seconds": { "mean": 23.3, "stddev": 2.1 },
      "tokens": { "mean": 84852, "stddev": 4200 },
      "per_eval": [
        { "id": 1, "pass_rate": 1.0, "time_seconds": 22.0, "tokens": 80000 }
      ]
    },
    {
      "name": "without_skill",
      "pass_rate": { "mean": 0.62, "stddev": 0.08 },
      "time_seconds": { "mean": 18.0, "stddev": 1.7 },
      "tokens": { "mean": 60000, "stddev": 3500 },
      "per_eval": [
        { "id": 1, "pass_rate": 0.66, "time_seconds": 17.0, "tokens": 58000 }
      ]
    }
  ],
  "delta": { "pass_rate": 0.24, "time_seconds": 5.3, "tokens": 24852 }
}
```

- List each `with_skill` configuration before its baseline counterpart.

## feedback.json (written by the viewer)

```json
{
  "reviews": [
    { "run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "2026-06-04T12:00:00Z" },
    { "run_id": "eval-1-with_skill", "feedback": "", "timestamp": "2026-06-04T12:01:00Z" }
  ],
  "status": "complete"
}
```

- Empty `feedback` means the user was satisfied with that run.

## eval_set.json (description optimization)

The trigger-eval set produced by `assets/eval_review.html`.

```json
[
  { "query": "the user prompt", "should_trigger": true },
  { "query": "a near-miss prompt", "should_trigger": false }
]
```

- Aim for 8 to 10 should-trigger and 8 to 10 should-not-trigger queries, with realistic phrasing and tricky near-misses.
