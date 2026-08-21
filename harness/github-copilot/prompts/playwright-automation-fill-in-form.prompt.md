---
name: 'playwright-automation-fill-in-form'
description: 'Fill a specified web form with Playwright MCP and pause for review before submission.'
agent: 'agent'
tools: ['playwright']
---

# /playwright-automation-fill-in-form

## Objective

Automate filling a specified Microsoft Forms web form with Playwright MCP using the provided show, date, time, topic, and image upload values, then stop for human review before any submission.

## When to Invoke

Use this prompt when the task is to navigate to a web form, fill known fields, optionally upload a file, and pause for review without submitting the form.

## Preconditions

- Playwright MCP is available through the configured `playwright` tool.
- The browser can navigate to `https://forms.microsoft.com/url-of-my-form`.
- The upload file path `/Users/myuserName/Downloads/my-image.png` exists or the user can provide a replacement.
- The user understands that the form must not be submitted automatically.

## Inputs the Team Must Provide

- Form URL — default `https://forms.microsoft.com/url-of-my-form`.
- Field values: Show, Date, Time, Topic, and Upload image.
- Any authentication or access step required to reach the form.
- Ask the user for anything that is missing, especially credentials or a missing upload file.

## What I Will Do

- Navigate to the Microsoft Forms URL with Playwright MCP.
- Fill Show with `playwright live`.
- Fill Date with `15 July`.
- Fill Time with `1:00 AM`.
- Fill Topic with `Playwright Live - Latest updates on Playwright MCP + Live Demo`.
- Upload image from `/Users/myuserName/Downloads/my-image.png`.
- Pause and ask for review before submission.

## What I Will NOT Do

- Submit the form.
- Click final confirmation, send, publish, or submit controls.
- Invent missing form values or upload a different file without user approval.
- Bypass authentication, CAPTCHA, consent, or access controls.
- Continue past the review pause.

## Output Format

Return this concise status report after filling the form:

```markdown
### Playwright Form Fill Result

### Form
- URL: `https://forms.microsoft.com/url-of-my-form`

### Filled Values
- Show: `playwright live`
- Date: `15 July`
- Time: `1:00 AM`
- Topic: `Playwright Live - Latest updates on Playwright MCP + Live Demo`
- Upload image: `/Users/myuserName/Downloads/my-image.png`

### Review Status
- Submission paused: `yes`
- User review requested: `yes`

### Blockers
- `<missing file, access issue, or none>`
```

## Definition of Done

- [ ] The form page is open at `https://forms.microsoft.com/url-of-my-form`.
- [ ] Show, Date, Time, Topic, and Upload image fields are filled with the requested values.
- [ ] The form has not been submitted.
- [ ] A review pause is requested before any submission action.
- [ ] Any access, upload, or field-matching blocker is reported.

## Prompt Body

Follow these steps in order. The safety boundary is strict: do not submit the form.

**Step 1 — Open the form.** Use Playwright MCP to navigate to `https://forms.microsoft.com/url-of-my-form`. If authentication or access is required, stop and ask for the missing step.

**Step 2 — Fill the fields.** Fill in the form with these details: Show `playwright live`; Date `15 July`; Time `1:00 AM`; Topic `Playwright Live - Latest updates on Playwright MCP + Live Demo`; Upload image `/Users/myuserName/Downloads/my-image.png`.

**Step 3 — Verify visible values.** Check that each field contains the requested value and that the upload control shows the selected image file when the form provides a visible confirmation.

**Step 4 — Pause before submission.** DO NOT SUBMIT THE FORM. Ask for a review of the form before submitting it. Do not click submit, final send, or any equivalent control.

**Step 5 — Report status.** Return the form URL, filled values, review status, and any blocker. Keep the response concise.

## Invocation Example

```
/playwright-automation-fill-in-form url=https://forms.microsoft.com/url-of-my-form
```
