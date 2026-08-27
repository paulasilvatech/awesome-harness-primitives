---
name: frontend-form-interactions
description: >-
  Design and verify forms, validation, search, filters, settings, uploads, checkout, onboarding,
  destructive actions, and multi-step data-entry workflows with preserved input and recoverable
  async behavior. Use this skill when frontend work collects, validates, or submits user data.
---

<!-- Generated from harness/github-copilot/plugins/frontend-experience/skills/frontend-form-interactions/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend form interactions

Make data entry understandable, efficient, accessible, and recoverable across client validation, server validation, authentication, network failures, and device constraints.

## When to invoke

- "Design a complex form with validation and recovery."
- "Implement onboarding, checkout, search filters, or settings."
- "Map server errors to fields without losing user input."
- "Review an upload or multi-step workflow."
- "Test autofill, mobile keyboards, duplicate submission, and retries."

## Input contract

For each field or action, record:

- purpose and why sensitive information is requested;
- visible label, instructions, examples, format, required status, and access;
- native input type, autocomplete token, input mode, and password-manager behavior;
- client and server validation timing, error shape, and cross-field rules;
- persistence, draft, back navigation, cancellation, and retry behavior;
- submitted data, idempotency, progress, confirmation, and destructive consequences.

Read [references/data-entry-patterns.md](references/data-entry-patterns.md).

## Validation and errors

Read [references/validation-and-errors.md](references/validation-and-errors.md).

- Validate at a useful time without error noise before the user can respond.
- Link field errors programmatically and add a summary for complex workflows.
- Map known server validation safely to fields while retaining a workflow-level message for unknown or cross-field failures.
- Preserve input and state after recoverable failure.
- Distinguish invalid, unauthorized, forbidden, conflict, rate limit, timeout, unavailable, offline, and unexpected errors.

## Async submission

Read [references/async-submission.md](references/async-submission.md).

Prevent accidental duplicates while communicating pending, progress, cancellation, retry, rollback, and confirmation. Use idempotency or conflict behavior defined by the backend contract; do not invent it.

## Criteria

- Visible labels remain present; placeholders are hints only.
- Native controls and semantics are preferred before custom widgets.
- Password paste, managers, and autofill remain enabled unless an approved security requirement says otherwise.
- Multi-step flows expose progress, saved state, safe backward navigation, and interruption behavior.
- Mobile virtual keyboards, viewport changes, safe areas, and touch targets do not hide active fields or actions.
- Test international names and addresses, locale-specific numbers, long text, paste, autofill, uploads, expiry, network failure, and retry where applicable.

Use [assets/complex-data-entry-review.md](assets/complex-data-entry-review.md) and [assets/human-review-checklist.md](assets/human-review-checklist.md).

## Limits

- Do not invent validation, data retention, security, compliance, or idempotency rules.
- Do not clear input after a recoverable error.
- Do not disable paste or password managers by default.
- Do not make a custom date picker, combobox, editor, drag control, or signature pad without accessible keyboard and fallback behavior.

## Output template

```markdown
## Form interaction result
**Status:** ready | needs revision | blocked

### Field and action contract
| Field/action | Purpose | Input semantics | Validation | Persistence/recovery |
| --- | --- | --- | --- | --- |

### State map
| State | Trigger | Visible behavior | Focus/announcement | Recovery |
| --- | --- | --- | --- | --- |

### Validation evidence
- <automated or manual check>
```

## Quality gate

- [ ] Labels, instructions, input purpose, native semantics, and access requirements are explicit.
- [ ] Client, server, cross-field, unknown, and workflow errors have defined behavior.
- [ ] Input, draft, progress, backward navigation, cancellation, retry, and duplicate-submission behavior is preserved when applicable.
- [ ] Autofill, paste, password managers, localization, mobile keyboards, uploads, and long content are covered by risk.
- [ ] Focus, announcements, summaries, and custom-widget keyboard behavior are defined.
- [ ] The human review checklist has no unresolved blocked item.
