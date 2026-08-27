---
name: frontend-conversational-ui
description: >-
  Design and verify chat, copilot, assistant, streaming, citations, tool activity, attachments,
  multimodal input, conversation history, retry, stop, and accessible live-update behavior. Use
  this skill when frontend work includes conversational or generated-content interfaces.
---

<!-- Generated from harness/github-copilot/plugins/frontend-experience/skills/frontend-conversational-ui/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend conversational UI

Define a complete, trustworthy conversational experience rather than a message list plus text input.

## When to invoke

- "Design a professional chat or copilot interface."
- "Implement streaming responses with stop, retry, and citations."
- "Review assistant tool states, attachments, and errors."
- "Make this chat accessible during live updates."
- "Test conversation history, reconnect, and partial output."

## Conversation contract

Read [references/conversation-patterns.md](references/conversation-patterns.md). Define:

- new, existing, loading, streaming, completed, stopped, failed, retried, edited, and deleted states as applicable;
- composer empty, multiline, attachment, recording, disabled, offline, and sending states;
- identity and semantics for user content, assistant output, tool results, quoted content, citations, and system status;
- history, title, rename, archive, search, retention, and privacy behavior when in scope;
- focus, keyboard, selection, copy, code, tables, links, and long-content behavior.

## Streaming and tools

Read [references/streaming-and-tool-states.md](references/streaming-and-tool-states.md).

Expose pending, approval, running, partial, completed, failed, cancelled, retryable, and unavailable tool states when applicable. Preserve partial output and explain retry consequences after disconnects.

Do not execute, render, or trust generated HTML, links, files, citations, commands, or code blindly.

## Accessibility and safety

Read [references/chat-accessibility.md](references/chat-accessibility.md).

- Keep focus stable as messages append or panels expand.
- Announce meaningful changes without interrupting every streamed token.
- Provide a non-streaming or reduced-update reading path when frequent updates create a barrier.
- Preserve input after errors and make destructive history or retention actions confirmable.
- Expose citations, code blocks, tables, attachments, and actions semantically.
- Allow reading, selection, copying, and navigation while output streams.

Use [assets/streaming-chat-review.md](assets/streaming-chat-review.md) and [assets/human-review-checklist.md](assets/human-review-checklist.md).

## Limits

- Do not invent model capabilities, tool permissions, data-use policy, retention, citation truth, or privacy guarantees.
- Do not present generated output as trusted or executable by default.
- Do not use typing animation that blocks selection, reading, or accessibility.
- Do not claim screen-reader or reconnect behavior without runtime evidence.

## Output template

```markdown
## Conversational UI result
**Status:** ready | needs revision | blocked

### State model
| Actor/component | State | Trigger | Visible behavior | Recovery |
| --- | --- | --- | --- | --- |

### Trust and accessibility
| Boundary | Treatment | Evidence required |
| --- | --- | --- |

### Runtime scenarios
| Scenario | Expected behavior | Result/evidence |
| --- | --- | --- |
```

## Quality gate

- [ ] Conversation, composer, streaming, tool, citation, attachment, history, and failure states are covered when applicable.
- [ ] Stop, cancel, retry, edit, reconnect, duplicate event, ordering, and partial-output behavior comes from evidence.
- [ ] User, assistant, tool, quoted, cited, and system content remain distinguishable.
- [ ] Focus, announcements, keyboard, reading, selection, code, tables, and reduced-update behavior are defined.
- [ ] Generated and remote content is treated as untrusted.
- [ ] The human review checklist has no unresolved blocked item.
