---
name: plugin-analytics-instrumentation
description: >-
  Instrument Backstage frontend plugins with meaningful Analytics API events and tests while
  avoiding duplicate BUI navigation events or UI noise. Use when adding or reviewing captureEvent,
  AnalyticsContext, event taxonomy, noTrack overrides, or analytics behavior.
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: eeac444a9aba7c107525d2a726851e907418c181
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/skills/plugin-analytics-instrumentation/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage plugin analytics instrumentation

Capture semantic plugin-owned outcomes and user intent, not every interaction or component
lifecycle event.

## When to invoke

- "Add analytics events to this Backstage plugin."
- "Review captureEvent usage."
- "Test AnalyticsContext behavior."
- "Avoid duplicate events from Backstage UI components."

## Procedure

1. Confirm frontend mode, installed Analytics API and BUI versions, and the questions the events
   must answer.
2. Read [the pinned upstream procedure](references/upstream/SKILL.md).
3. Inventory existing analytics context, built-in BUI events, manual events, and tests.
4. Define stable action, subject, and context fields for semantic plugin-owned behavior.
5. Prefer BUI components' built-in navigation instrumentation.
6. Use `noTrack` only when replacing a built-in event with a more meaningful event.
7. Avoid lifecycle, hover, generic tab, duplicate click, and field-by-field form noise.
8. Add tests for event presence, payload, context, and non-duplication.
9. Validate that event values contain no secrets, tokens, or sensitive user data.

## Output template

```markdown
## Plugin analytics result

| User intent | Action | Subject | Context | Test |
| --- | --- | --- | --- | --- |

### Removed or avoided events
- <event and reason>
```

## Quality gate

- [ ] Every event answers a named product or operational question.
- [ ] BUI built-in events are reused rather than duplicated.
- [ ] Action, subject, and context remain independently queryable.
- [ ] Event payloads contain no secrets or sensitive user data.
- [ ] Tests cover event capture and non-capture cases.
- [ ] Lifecycle and low-value UI noise are not instrumented.
