---
name: playwright-automation-fill-in-form
description: >-
  Automate filling and reviewing a Microsoft Forms response with Playwright MCP. Use this skill
  when the user asks to open a form, fill specific fields, upload an image, or prepare but not
  submit a Playwright-driven form response.
---

<!-- Generated from harness/github-copilot/plugins/testing-automation/skills/playwright-automation-fill-in-form/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Playwright form automation

Fill the target Microsoft Forms page with the requested show, date, time, topic, and upload image, then stop before submission so the human can review the populated form.

## When to invoke

- "Use Playwright MCP to fill in this Microsoft Form."
- "Open the form and enter the show details, but do not submit it."
- "Upload an image into a form field with Playwright."
- "Prepare a form response and ask me to review before submitting."

## Prerequisites and context

- Use Playwright MCP browser automation, not direct HTTP requests, because the task depends on visible form controls and file upload widgets.
- Navigate to `https://forms.microsoft.com/url-of-my-form` unless the user supplies a different Microsoft Forms URL.
- Use the image path `/Users/myuserName/Downloads/my-image.png` for the upload field unless the user provides a replacement file.
- The final action is review-only: DO NOT SUBMIT THE FORM.

## Form field map

| Field label or intent | Value to enter | Verification |
| --- | --- | --- |
| Show | `playwright live` | The selected or typed show value is visible in the form. |
| Date | `15 July` | The date control displays the intended day and month. |
| Time | `1:00 AM` | The time control displays `1:00 AM`, not `1:00 PM` or a 24-hour conversion error. |
| Topic | `Playwright Live - Latest updates on Playwright MCP + Live Demo` | The full topic text is present without truncation. |
| Upload image | `/Users/myuserName/Downloads/my-image.png` | The upload control shows the file name or successful attachment state. |

## Procedure

1. Open the form URL in the browser and wait until the form controls are visible.
2. Fill each field from the field map. Prefer label-based selectors or accessibility snapshots over brittle CSS positions.
3. Upload the image through the native file chooser or upload control.
4. Review every populated value in the page state after filling.
5. Stop before any submit, send, finish, or final confirmation button. Ask for a review of the form before submitting it.

## Gotchas

- **Do not submit**: the required deliverable is a populated draft, not a completed response.
- **Preserve the upload path exactly**: `/Users/myuserName/Downloads/my-image.png` is a task-specific input and must not be shortened to a file name.
- **Confirm time semantics**: `1:00 AM` is an overnight time; many controls default to PM or current time.
- **Use browser-observed state**: report values from the rendered form, not only the automation script's intended inputs.

## Output template

```markdown
## Form fill review

**Status:** ready for review | blocked
**URL:** `https://forms.microsoft.com/url-of-my-form`

| Field | Expected value | Observed value | Status |
| --- | --- | --- | --- |
| Show | `playwright live` | `<observed>` | pass/fail |
| Date | `15 July` | `<observed>` | pass/fail |
| Time | `1:00 AM` | `<observed>` | pass/fail |
| Topic | `Playwright Live - Latest updates on Playwright MCP + Live Demo` | `<observed>` | pass/fail |
| Upload image | `/Users/myuserName/Downloads/my-image.png` | `<observed>` | pass/fail |

**Submission:** not submitted; awaiting human review.
```

## Quality gate

- [ ] The browser navigated to `https://forms.microsoft.com/url-of-my-form` or the user-supplied replacement URL.
- [ ] Show, Date, Time, Topic, and Upload image were filled with the exact requested values.
- [ ] The uploaded file path `/Users/myuserName/Downloads/my-image.png` was used or a missing-file blocker was reported.
- [ ] The form was not submitted.
- [ ] The response asks for a review of the form before submitting it.
