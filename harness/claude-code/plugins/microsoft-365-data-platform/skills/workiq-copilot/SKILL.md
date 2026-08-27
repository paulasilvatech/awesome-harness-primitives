---
name: workiq-copilot
description: >-
  Use the WorkIQ `CLI/MCP` server to query Microsoft 365 work data such as emails, meetings,
  documents, Teams messages, people, and projects for live organizational context. Use when the
  user asks for agenda summaries, follow-ups, document lookup, stakeholder or project context,
  blockers, recommendations, or Microsoft 365 work intelligence.
---

<!-- Generated from harness/github-copilot/plugins/microsoft-365-data-platform/skills/workiq-copilot/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# WorkIQ for GitHub GitHub Copilot CLI

Query Microsoft 365 work data through WorkIQ Public Preview, then synthesize concise, privacy-aware summaries and recommendations from emails, `meetings/documents`, Teams messages, `People/Projects**`, people, and project context.

## When to invoke

- "Summarize my emails from Sarah about the budget."
- "What are my upcoming meetings this week?"
- "Find recent documents about Q4 planning."
- "Summarize Teams messages in the Engineering channel today."
- "Who is working on Project Alpha and what are the blockers?"

## Prerequisites and context

- Preferred access path: GitHub Copilot CLI plugin marketplace package `workiq@copilot-plugins`.
- Standalone access path: `@microsoft/workiq` CLI or `workiq mcp` MCP stdio server.
- Tenant admin consent may be required for EULA and Microsoft 365 permissions. Non-admins must ask their tenant admin to approve access using the Tenant Administrator Enablement Guide.
- Be ready for browser device login on first use or when tokens expire.

## Setup and access

| Path | Commands | Use when |
| --- | --- | --- |
| GitHub Copilot CLI plugin | `copilot`, `/plugin marketplace add github/copilot-plugins`, `/plugin install workiq@copilot-plugins`, then restart GitHub Copilot CLI. | The user wants WorkIQ integrated into GitHub Copilot CLI. |
| Standalone CLI | `npm install -g @microsoft/workiq` | Repeated local terminal usage is expected. |
| One-off CLI | `npx -y @microsoft/workiq mcp` | Temporary MCP server use without global install. |
| MCP server | `workiq mcp` | Another `agent/workflow` needs direct tool access. |

Pre-flight checks:

- Run `Get-Command workiq` to ensure the binary is available.
- Accept the EULA once with `workiq accept-eula`.
- Confirm tenant targeting with `-t <tenant-id>` when default `common` is not correct.
- Complete browser login before assuming a command is hung.

## Core workflow

1. Clarify intent: agenda, action items, document lookup, people search, risk summary, or recommendation.
2. Craft a narrow prompt with timeframe, source, person, channel, meeting, or project name.
3. Run `workiq ask --question "<prompt>"` or shorthand `workiq ask -q "<prompt>"`; add `-t <tenant>` when needed.
4. Wait for streaming output to complete before issuing another request.
5. Summarize and redact: call out priorities, blockers, conflicts, and optional next steps without dumping raw confidential snippets.
6. Offer focused follow-ups such as blocking time, drafting a note, requesting a recording, or running a deeper query.

## Command reference and prompt patterns

| Command | Purpose |
| --- | --- |
| `workiq --help` | Show global options. |
| `workiq version` | Display installed version. |
| `workiq accept-eula` | Accept the license on first use. |
| `workiq ask` | Start interactive mode. |
| `workiq ask --question "..."` | Ask a specific question. |
| `workiq ask -q "..."` | Shorthand question form. |
| `workiq ask -t <tenant> -q "..."` | Target a specific tenant. |
| `workiq mcp` | Start the MCP stdio server. |

| Intent | Prompt pattern |
| --- | --- |
| Agenda | "What's on my calendar tomorrow?" |
| Action items and `conflicts/tasks` | "Summarize follow-ups from today's customer sync." |
| Documents | "List PowerPoints about Contoso FY26 roadmap." |
| Communications | "What did my manager say about the deadline?" |
| Insights | "What blockers came up in the last three meetings?" |
| Planning | "Suggest focus blocks for Tuesday afternoon." |

Supported data includes emails, meetings, documents, Teams messages, people, and projects.

## Response rules

- Keep summaries to 2-3 sentences unless the user asks for detail.
- Call out load, priorities, blockers, conflicts, and next steps.
- Refer to meetings and documents generically unless the user explicitly needs links.
- Do not expose attendee lists, confidential snippets, or raw message content unless specifically requested and appropriate.
- Log which commands were run, for example: "Asked WorkIQ for agenda + conflicts".
- Map suggestions to concrete offers: block `focus/overflow` time, draft a `reschedule/decline`, request a recording, capture action items, or run a scoped follow-up query.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Missing CLI | `workiq` is not installed or not on `PATH`. | Install with npm or fix `PATH`; notify the user if unavailable. |
| `Consent/auth` error | Tenant admin consent missing or device login incomplete. | Ask for admin grant or complete browser login, then rerun. |
| `Long/incomplete` output | Prompt too broad or streaming not finished. | Wait for completion or `re-run` with a narrower `day/project/person` scope. |
| Command hanging | Browser login pending or process stuck. | Cancel the specific running command, confirm login, restart GitHub Copilot CLI if needed, then retry. |
| Wrong tenant data | Default `common` tenant selected. | Use `workiq ask -t <tenant> -q "..."`. |

## Output template

```markdown
## WorkIQ result

**Status:** complete | needs auth | blocked
**Question:** <prompt sent to WorkIQ>
**Sources requested:** email | meetings | documents | Teams | people | projects
**Command:** `<workiq command>`

### Summary
<2-3 sentence synthesis>

### Signals
- <priority, blocker, conflict, or follow-up>

### Suggested next actions
- <offer or action>
```

## Quality gate

- [ ] WorkIQ access path and tenant context are verified before relying on results.
- [ ] The prompt includes a timeframe, source, person, project, or topic to reduce noise.
- [ ] Streaming output completed before summarization.
- [ ] The final response is concise and privacy-aware.
- [ ] Commands run are recorded in the output.
- [ ] Follow-up offers are actionable.
- [ ] The output follows `## Output template` exactly.
