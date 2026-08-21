---
name: arize-annotation
description: >-
  Create, inspect, update, and use Arize annotation configs and annotation queues, then bulk-apply human labels to spans with the Python SDK. Use when asked for "annotation config", "annotation queue", "label schema", "human feedback", "bulk annotate spans", "update_annotations", "labeling queue", "annotate record", or "human review".
metadata:
  author: arize
  compatibility: "Requires the ax CLI and a configured Arize profile."
  version: "1.0"
---

# Arize annotation

Create and manage Arize annotation configs and queues, then transform human review labels into CLI queue annotations or Python SDK span updates.

## When to invoke

- "Create an Arize annotation config for correctness labels."
- "Set up an annotation queue for human review."
- "Bulk annotate spans with update_annotations."
- "Annotate a queue record with a score and reviewer notes."
- "Troubleshoot ax annotation-configs or annotation-queues."

## Prerequisites and context

- Proceed directly with the requested `ax` command. Do not check versions, environment variables, or profiles upfront.
- `SPACE` means a space name such as `my-workspace` or a base64 space ID such as `U3BhY2U6...`; `--space` and `ARIZE_SPACE` accept either. Find spaces with `ax spaces list`.
- Use `ax profiles show` only after an authorization or profile error.
- Never read `.env` files or search the filesystem for credentials. Use `ax profiles` for Arize credentials and `ax ai-integrations` for LLM provider keys.
- If the user needs an API key, direct them to https://app.arize.com/admin > API Keys.

## Progressive disclosure and bundled resources

- `references/ax-setup.md`: use when `ax` is missing or the installed version is incompatible.
- `references/ax-profiles.md`: use when profile creation, update, or credential persistence is required.

Read these references only when the matching error or setup request occurs.

## Annotation concepts

This skill covers `ax annotation-configs`, `ax annotation-queues`, CRUD operations, `create/update` flows, and bulk span writes with `spans.update_annotations`. Config types are `categorical`, `continuous`, and `freeform`; freeform captures open-ended text, continuous uses Min/Max score bounds, and categorical values may use `{"label": str, "score": number}` pairs. Common config names include `Correctness` and `Helpfulness`; use `maximize` when higher is better.


| Concept | Purpose | Key fields or surfaces |
| --- | --- | --- |
| Annotation config | Label schema for one human feedback dimension. | Name, type, values, min/max score, optimization direction. |
| Categorical config | Reviewer picks a fixed label. | `correct` / `incorrect`, `helpful` / `unhelpful`, `safe` / `unsafe`, `relevant` / `irrelevant`, `pass` / `fail`. |
| Continuous config | Reviewer enters a numeric score. | `--min-score`, `--max-score`, `--optimization-direction maximize` or `minimize`. |
| Freeform config | Reviewer enters text feedback. | Name, space, and `--type freeform`. |
| Annotation queue | Routes spans, dataset examples, experiment runs, or records to reviewers. | Config IDs, annotator emails, instructions, assignment method. |
| Project spans | Programmatic annotation target. | Python SDK `ArizeClient.spans.update_annotations`. |
| Dataset examples and experiment outputs | Human-labeling surfaces in the UI. | Configs must already exist in the space. |

Always create or confirm the relevant annotation config before expecting labels to persist on spans, dataset examples, experiment-related records, or annotation queue items.

## Annotation config commands

| Task | Command |
| --- | --- |
| List configs | `ax annotation-configs list --space SPACE` |
| List JSON | `ax annotation-configs list --space SPACE -o json` |
| List with limit | `ax annotation-configs list --space SPACE --limit 20` |
| Get by ID | `ax annotation-configs get NAME_OR_ID` |
| Get by name | `ax annotation-configs get NAME_OR_ID --space SPACE` |
| Get JSON | `ax annotation-configs get NAME_OR_ID -o json` |
| Delete | `ax annotation-configs delete NAME_OR_ID` |
| Delete by name | `ax annotation-configs delete NAME_OR_ID --space SPACE` |
| Delete without confirmation | `ax annotation-configs delete NAME_OR_ID --force` |

Create a categorical config:

```bash
ax annotation-configs create \
  --name "Correctness" \
  --space SPACE \
  --type categorical \
  --value correct \
  --value incorrect \
  --optimization-direction maximize
```

Create a continuous config:

```bash
ax annotation-configs create \
  --name "Quality Score" \
  --space SPACE \
  --type continuous \
  --min-score 0 \
  --max-score 10 \
  --optimization-direction maximize
```

Create a freeform config:

```bash
ax annotation-configs create \
  --name "Reviewer Notes" \
  --space SPACE \
  --type freeform
```

Deletion is irreversible. Any annotation queue associations to the deleted config are also removed in the product; queues may remain and need association repair in the Arize UI.

## Annotation queue commands

| Task | Command |
| --- | --- |
| List queues | `ax annotation-queues list --space SPACE` |
| List queues JSON | `ax annotation-queues list --space SPACE -o json` |
| Get queue | `ax annotation-queues get NAME_OR_ID --space SPACE` |
| Get queue JSON | `ax annotation-queues get NAME_OR_ID --space SPACE -o json` |
| Update name | `ax annotation-queues update NAME_OR_ID --space SPACE --name "New Name"` |
| Update instructions | `ax annotation-queues update NAME_OR_ID --space SPACE --instructions "Updated instructions"` |
| Delete queue | `ax annotation-queues delete NAME_OR_ID --space SPACE` |
| Delete queue without confirmation | `ax annotation-queues delete NAME_OR_ID --space SPACE --force` |
| List records | `ax annotation-queues list-records NAME_OR_ID --space SPACE` |
| List records JSON | `ax annotation-queues list-records NAME_OR_ID --space SPACE --limit 50 -o json` |
| Assign record | `ax annotation-queues assign-record NAME_OR_ID RECORD_ID --space SPACE` |
| Delete records | `ax annotation-queues delete-records NAME_OR_ID --space SPACE` |

Create a queue with at least one `--annotation-config-id`:

```bash
ax annotation-queues create \
  --name "Correctness Review" \
  --space SPACE \
  --annotation-config-id CONFIG_ID \
  --annotator-email reviewer@example.com \
  --instructions "Label each response as correct or incorrect." \
  --assignment-method all
```

Use `--assignment-method random` instead of `all` when each item should go to one reviewer. Repeat `--annotation-config-id` and `--annotator-email` to attach multiple configs or reviewers.

List flags fully replace existing values when provided. Pass all desired values, not only the new ones:

```bash
ax annotation-queues update NAME_OR_ID --space SPACE \
  --annotation-config-id CONFIG_ID_A \
  --annotation-config-id CONFIG_ID_B
```

Submit annotations to queue records. Annotations are upserted by config name; supply at least one of `--score`, `--label`, or `--text`:

```bash
ax annotation-queues annotate-record NAME_OR_ID RECORD_ID \
  --annotation-name "Correctness" \
  --label "correct" \
  --space SPACE

ax annotation-queues annotate-record NAME_OR_ID RECORD_ID \
  --annotation-name "Quality Score" \
  --score 8.5 \
  --text "Response was accurate but slightly verbose." \
  --space SPACE
```

## Python SDK span annotations

Use the Python SDK to bulk-apply annotations to project spans when labels already exist in a review export or external labeling tool.

```python
import os
import pandas as pd
from arize import ArizeClient

client = ArizeClient(api_key=os.environ["ARIZE_API_KEY"])

annotations_df = pd.DataFrame([
    {
        "context.span_id": "span_001",
        "annotation.Correctness.label": "correct",
        "annotation.Correctness.updated_by": "reviewer@example.com",
    },
    {
        "context.span_id": "span_002",
        "annotation.Correctness.label": "incorrect",
        "annotation.Correctness.updated_by": "reviewer@example.com",
    },
])

response = client.spans.update_annotations(
    space_id=os.environ["ARIZE_SPACE"],
    project_name="your-project",
    dataframe=annotations_df,
    validate=True,
)
```

DataFrame schema:

| Column | Required | Description |
| --- | --- | --- |
| `context.span_id` | yes | The span to annotate. |
| `annotation.<name>.label` | one of | Categorical or freeform label. |
| `annotation.<name>.score` | one of | Numeric score. |
| `annotation.<name>.updated_by` | no | Annotator identifier, email, or name. |
| `annotation.<name>.updated_at` | no | Timestamp in milliseconds since epoch. |
| `annotation.notes` | no | Freeform notes on the span. |

Annotations apply only to spans within 31 days prior to submission.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `ax: command not found` or `command not found` | CLI absent. | Read `references/ax-setup.md`. |
| Version error | CLI incompatible. | Read `references/ax-setup.md`. |
| `401 Unauthorized` | API key lacks access or profile is wrong. | Run `ax profiles show`; update via `references/ax-profiles.md`; API keys are at https://app.arize.com/admin > API Keys. |
| Space unknown | Name or ID is wrong. | Run `ax spaces list` and select by name or ask the user. |
| `Annotation config not found` | Config absent or wrong space. | Run `ax annotation-configs list --space SPACE` or `ax annotation-configs get NAME_OR_ID --space SPACE`. |
| `409 Conflict on create` | Config name already exists. | Use a different name or get the existing config ID. |
| Queue not found | Wrong queue name, ID, or space. | Run `ax annotation-queues list --space SPACE`. |
| Record not appearing in queue | Queue/config association issue. | Confirm the config exists with `ax annotation-configs list --space SPACE`. |
| Span SDK errors or missing spans | Bad `project_name`, `space_id`, span ID, or age window. | Confirm identifiers and use `arize-trace` to export spans. |

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `arize-trace` | skill | Export spans to find span IDs and time ranges. |
| `arize-dataset` | skill | Find dataset IDs and example IDs. |
| `arize-evaluator` | skill | Pair automated LLM-as-judge with human annotation. |
| `arize-experiment` | skill | Work with experiments tied to datasets and evaluation workflows. |
| `arize-link` | skill | Build deep links to annotation configs and queues in the Arize UI. |

## Gotchas

- **List updates fully replace values**: queue `--annotation-config-id` and `--annotator-email` updates must include every desired value, not just the delta.
- **Annotation configs are the label schema**: create configs before applying labels to spans, queues, dataset examples, or experiment records.
- **`and/or` surfaces are real**: human annotations may apply through the UI and/or the SDK depending on the target surface.

## Output template

```markdown
## Arize annotation result

**Status:** completed | blocked | needs input
**Space:** <SPACE or ARIZE_SPACE value used>
**Target:** annotation config | annotation queue | queue record | project spans

| Action | Command or API | Result |
| --- | --- | --- |
| <action> | `<ax command or ArizeClient.spans.update_annotations>` | <created/updated/listed/deleted/annotated> |

### Identifiers
- Config: <NAME_OR_ID or CONFIG_ID>
- Queue: <NAME_OR_ID>
- Record: <RECORD_ID>
- Project: <project_name>

### Validation
- <command or SDK validation>: pass/fail with evidence
```

## Quality gate

- [ ] The command uses `--space SPACE` or the SDK uses `ARIZE_SPACE` where required.
- [ ] Annotation configs exist before queue creation or span annotation.
- [ ] Queue updates that pass list flags include the full desired replacement list.
- [ ] `annotate-record` supplies at least one of `--score`, `--label`, or `--text`.
- [ ] SDK span annotation uses `context.span_id` and at least one `annotation.<name>.label` or `annotation.<name>.score` column.
- [ ] No `.env` file or filesystem credential search was performed.
- [ ] Setup/profile references were read only when the matching error or task required them.
