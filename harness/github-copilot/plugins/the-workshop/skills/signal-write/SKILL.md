---
name: signal-write
description: >-
  Emit structured agent signals as JSON files under desk .signals directories and journal markers for dashboard consumption. Use when a desk needs hands-up or blocked operator attention, work is done and ready for review, significant progress needs a checkpoint, two desks disagree, or a TA reports partnership coordination quality.
---

# Agent signal writing

Write concise machine-readable signal JSON and a persistent journal marker when a desk state changes in a way the operator or dashboard should see.

## When to invoke

- "Signal hands-up because two desks disagree."
- "Mark this desk blocked."
- "Emit done for review."
- "Write a checkpoint signal."
- "Report partnership quality for the TA."

## Signal semantics

| Signal | Meaning | Use when |
| --- | --- | --- |
| `hands-up` | Escalation for disagreement between desks. | Two desks cannot settle a decision against external facts. |
| `blocked` | Escalation for missing input. | The desk cannot proceed because of access, ambiguous scope, or a decision only the operator can make. |
| `done` | Execution completion. | Work is complete and artifacts are on the bench for review. |
| `checkpoint` | Execution progress marker. | Significant progress matters to the operator, but work continues. |
| `partnership` | TA coordination quality report. | The room coordinator reports intent, confidence, accuracy, and completeness. |

Self-assessment scores reflect coordination, not code accuracy: `intent`, `confidence`, `accuracy`, and `completeness` each use a 0–5 scale. A 3/5 is acceptable; all 5/5 scores are suspicious unless evidence supports them.

## Procedure

1. Choose the desk directory and create `desks/<desk-name>/.signals/<timestamp>.json` with an ISO 8601 UTC timestamp.
2. Write the JSON signal using the mapping table below. This is the primary dashboard input.
3. Append a short journal marker for persistence:

```markdown
## <date> — [signal:<type>] <summary>
- <key details>
```

4. Keep signals short, factual, and actionable. Do not signal routine progress.

## JSON schema and mapping

Execution, escalation, and partnership signal shape:

```json
{
  "signal_type": "execution",
  "subtype": "checkpoint",
  "timestamp": "2026-07-19T21:30:00Z",
  "run_id": "<optional; set to pair this with an outcome signal>",
  "agent_name": "<desk-name>",
  "self_assessment": {
    "intent": 4,
    "confidence": 5,
    "accuracy": 4,
    "completeness": 3
  },
  "patterns": {
    "what_worked": "description of what went well",
    "what_was_hard": "description of challenges",
    "skill_gap": "areas for improvement"
  },
  "escalation": {
    "reason": null,
    "blocked_on": null,
    "recommendation": null
  }
}
```

| Signal | `signal_type` | `subtype` |
| --- | --- | --- |
| `hands-up` | `"escalation"` | `"hands-up"` |
| `blocked` | `"escalation"` | `"blocked"` |
| `done` | `"execution"` | `"done"` |
| `checkpoint` | `"execution"` | `"checkpoint"` |
| `partnership` | `"partnership"` | `"partnership"` |

The signals-dashboard canvas extension reads `subtype` when present and falls back to `signal_type` for display. Consumers should prefer `subtype` for the specific state. The dashboard orders by `timestamp` and falls back to file mtime only when absent; git clone/checkout resets mtimes, so mtime alone is not a dependable clock.

## Outcome signals

Outcome signals calibrate self-assessment with realized quality and are usually emitted by a `reviewer/evaluator`. Write them to the same `.signals/` directory.

```json
{
  "signal_type": "outcome",
  "run_id": "<same run_id as the signal it rates>",
  "agent_name": "<reviewer name>",
  "quality_rating": 4,
  "effort_to_merge": "minimal",
  "issues_found": ["optional short strings"],
  "timestamp": "2026-07-19T22:00:00Z"
}
```

| Field | Rule |
| --- | --- |
| `run_id` | Correlates an outcome with the execution/partnership signal; if absent, the dashboard falls back to the nearest outcome emitted shortly after the latest signal. |
| `quality_rating` | Realized quality on a 0–5 scale; compared to self-assessed `confidence` for the honesty gap. |
| `effort_to_merge` | Use `"minimal"`, `"moderate"`, or `"significant"`. |
| `issues_found` | Optional array of short issue strings. |

## Principles

- Signals are structured, not chatty.
- `hands-up` is not failure; it means the system caught a disagreement one frame alone would have missed.
- `blocked` means truly blocked, not merely preferring input. If a reasonable default exists, proceed and note it.
- Do not signal routine progress; signals are for state changes that affect the room.
- Self-assessment should be honest, not optimistic.

## Gotchas

- **Do not omit `subtype`**; dashboard consumers use it for the precise state.
- **Do not rely on file mtime**; always include an ISO 8601 UTC `timestamp`.
- **Do not emit outcome signals from the same desk being rated** unless the workflow explicitly requires self-review.

## Output template

```markdown
## Signal write result

**Status:** written | blocked
**Signal:** `<hands-up|blocked|done|checkpoint|partnership|outcome>`
**JSON file:** `desks/<desk-name>/.signals/<timestamp>.json`
**Journal entry:** `<journal path or not written>`

### Payload summary
- `signal_type`: `<value>`
- `subtype`: `<value>`
- `run_id`: `<value or none>`
- `timestamp`: `<UTC timestamp>`

### Validation
- JSON parse: <pass|fail>
- Dashboard fields: <pass|fail>
- Journal marker: <pass|fail>
```

## Quality gate

- [ ] JSON signal is written under `desks/<desk-name>/.signals/` with a timestamped filename.
- [ ] `signal_type` and `subtype` match the mapping table.
- [ ] `timestamp` is ISO 8601 UTC.
- [ ] Escalation fields explain `reason`, `blocked_on`, and `recommendation` when applicable.
- [ ] Outcome signals use matching `run_id` when rating a specific signal.
- [ ] A journal marker is appended with `[signal:<type>]`.
