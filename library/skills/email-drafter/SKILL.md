---
name: email-drafter
description: >-
  Draft and review professional emails that match the user's established writing style by analyzing recipient context, tone, greeting, structure, sign-off, and language patterns when WorkIQ is available, then saving markdown drafts. Use this skill when the user asks to draft email, write email, compose email, reply email, follow-up email, proposal email, analyze email tone, or perform context-aware email review.
---

# Email drafter

Draft context-aware professional emails by gathering recipient and purpose, matching the user's prior communication style when available, producing an editable draft, and saving the final version as Markdown.

## When to invoke

- "Draft an email to Sarah about the project timeline."
- "Write a follow-up email to the customer regarding migration questions."
- "Reply to John's email and suggest we add monitoring."
- "Compose a proposal email for the training initiative."
- "Analyze my email tone with the Acme team."

## Prerequisites and context

WorkIQ MCP access to Microsoft 365 / Outlook is recommended for tone analysis and recipient history. If WorkIQ is unavailable or no prior correspondence exists, use sensible professional defaults and note that tone was inferred.

Never send email. Produce drafts only for the user to review and send manually.

## Context gathering

Collect enough context before drafting:

| Context | Required | Notes |
| --- | --- | --- |
| Recipient(s) | Yes | Names, roles, and whether internal or external. |
| Purpose | Yes | Proposal, follow-up, technical guidance, introduction, status update, reply, or other. |
| Key points | Yes | Facts, asks, decisions, dates, and attachments to mention. |
| Relationship context | Recommended | Use WorkIQ for prior history when available. |
| Source email | Required for replies | Preserve the thread's core question and requested action. |

If the user provides all of this upfront, proceed directly. Otherwise ask at most three clarifying questions.

## Tone analysis

When WorkIQ is available, pull 3-5 recent sent emails to the same recipient or similar recipients. Extract these patterns:

| Pattern | What to infer |
| --- | --- |
| Greeting style | Formal `Dear`, standard `Hello`, casual `Hi`, or direct with no greeting. |
| Structure | Short paragraphs, bullet lists, numbered steps, or hybrid. |
| Sign-off | Closing phrase and name format. |
| Formality | Professional, friendly-professional, or casual. |
| Language | English by default, or the language used with this recipient. |
| Relationship memory | Prior project, customer concern, decision, or follow-up owed. |

Respect privacy: do not include sensitive information from unrelated threads.

## Drafting rules

| Element | Rule |
| --- | --- |
| Greeting | Match discovered style. Default to `Hello [FirstName],` for external recipients and `Hi [FirstName],` for internal recipients. For multiple recipients, use `Hello [Name1], [Name2],`. |
| Opening | Get to the point quickly and include relevant prior context such as "Following our recent conversation about..." when useful. |
| Body | Use simple paragraphs for 1-2 points; use bullets or numbered lists for proposals, multi-point updates, and technical guidance. |
| Tone | Be direct, concise, friendly, and professional; avoid filler. |
| Help offer | Use offers such as "Happy to discuss further" or "Let me know if you need anything" only when appropriate. |
| Sign-off | Match the user's pattern. Default to `Best regards,` followed by the user's first name on the next line. |
| Language | Match recipient history or the user's request; otherwise default to English. |

## Saving drafts

Save the final draft, after user-requested edits, under `outputs/<year>/<month>/` with a descriptive filename such as `2026-03-26-email-acme-followup.md`. Use the current date for `<year>` and `<month>`.

## Procedure

1. Gather recipient, purpose, key points, and source email if replying.
2. Use WorkIQ for prior recipient context and 3-5 recent sent examples when available.
3. Infer greeting, structure, sign-off, formality, and language.
4. Draft the email and include a brief note on the style applied.
5. Apply user edits until the draft is satisfactory.
6. Save the final Markdown draft to `outputs/<year>/<month>/`.

## Gotchas

- **Never send emails**: stop at a saved draft.
- **Do not overfit unrelated correspondence**: only use relevant recipient or similar-recipient patterns.
- **Do not leak unrelated sensitive details**: prior email context informs style, not content unless directly relevant.
- **Do not ask unlimited questions**: ask at most three clarifying questions, then draft with stated assumptions.

Report the applied `tone/style` when presenting a draft.

## Output template

```markdown
## Email draft result

**Status:** drafted | revised | saved | blocked
**Recipient(s):** `<names>`
**Purpose:** `<purpose>`
**Tone source:** `WorkIQ recipient history | WorkIQ similar recipients | professional defaults`

### Draft
Subject: <subject line>

<email body>

### Style notes
- Greeting: `<matched/default>`
- Structure: `<paragraphs/bullets/numbered>`
- Sign-off: `<matched/default>`
- Language: `<language>`

### Saved file
`outputs/<year>/<month>/<filename>.md`
```

## Quality gate

- [ ] Recipient, purpose, and key points were collected or reasonable assumptions were stated.
- [ ] WorkIQ was used for prior context when available; otherwise professional defaults were disclosed.
- [ ] Greeting, structure, sign-off, formality, and language match evidence or defaults.
- [ ] The draft is concise, professional, and context-aware.
- [ ] No unrelated sensitive information from prior email threads is included.
- [ ] The email was not sent.
- [ ] Final drafts are saved under `outputs/<year>/<month>/` with a descriptive filename when the workflow reaches final form.
