---
name: brag-sheet
description: >-
  Turn vague work-history prompts into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, weekly updates, status reports, and accomplishments. Use when the user says "brag", "what did I do", "backfill my work history", "review prep", "what did I ship", "track my wins", or documenting engineering impact from Copilot CLI sessions, git commits, and GitHub PRs.
license: MIT
argument-hint: "Optional: time range (\"last 2 weeks\", \"this half\"), category (\"infrastructure\"), \"backfill\", or \"review prep\""
metadata:
  compatibility: "Cross-platform (Windows, macOS, Linux). Works with any GitHub Copilot CLI session. Optional: git, gh CLI."
  version: "1.1"
---

# Brag sheet

Turn scattered engineering activity into concise, evidence-backed impact entries by mining GitHub Copilot CLI sessions, git commits, and GitHub pull requests, then enforcing action → result → evidence.

## When to invoke

- "What did I do last week?"
- "Backfill my work history for this half."
- "Write impact statements for my performance review."
- "Summarize what I shipped from my PRs."
- "Help me prep a promo packet or weekly update."

## Inputs

Use `$ARGUMENTS` for the time range, category, mode, or scope. If it is ambiguous, confirm the range and source scope before scanning. Common modes are Capture, Backfill, and Review Pack.

## Limits

- Do not use this skill for project management, sprint planning, time tracking, or ticket creation.
- Do not fabricate metrics, team size, impact numbers, or shipped status.
- Do not save entries with `save_to_brag_sheet` unless that tool is confirmed available and the user approves the drafted entries.

## Modes

| User wants | Mode | Output |
| --- | --- | --- |
| Log one accomplishment | Capture | One impact-first entry. |
| "What did I do last week?" | Backfill | Entries grouped by week, mined from git, PRs, and sessions. |
| Prep for review or promo | Review Pack | Top impact themes plus STAR narratives. |

## Impact contract

Every entry must include all three parts:

```text
Did [action] → [result/impact] → [evidence]
```

If evidence is missing, write `(evidence needed)` and ask for proof. Never silently omit evidence.

| Do not write | Write instead |
| --- | --- |
| `Fixed a bug in auth` | `Fixed token refresh race condition → eliminated 401s affecting 12% of API calls → PR #247` |
| `Worked on dashboards` | `Built latency dashboard in Grafana → on-call detects P95 spikes in <2min → deployed to prod` |
| `saved 40% of eng time` when not provided | Ask for an estimate or keep the impact qualitative. |
| One entry per commit | Group related commits into one entry with highest-impact framing. |
| `The pipeline was improved` | `Built CI matrix → caught Windows-only bug before release` |
| Technology list only | State the outcome: `Migrated 4 services to IaC → deploy time 45min → 8min`. |

## Evidence ladder

| Strength | Evidence type | Example |
| --- | --- | --- |
| Best | Quantified metric | `Reduced P95 latency from 800ms to 120ms`. |
| Strong | PR, commit, or doc link | `PR #312, design doc in wiki`. |
| Good | Observable outcome | `Unblocked Team X`, `Resolved Sev2 incident Y`. |
| Acceptable | Qualitative plus context | `Reduced toil for on-call rotation — see updated runbook`. |
| Weak | Activity only | `Worked on auth`; reframe or mark `(evidence needed)`. |

Qualitative evidence with context beats fabricated numbers.

## Categories

| ID | Use for |
| --- | --- |
| `pr` | Merged PRs and shipped features. |
| `bugfix` | Bug fixes and incident patches. |
| `infrastructure` | Infrastructure, deployments, migrations. |
| `investigation` | Root cause analysis and debugging. |
| `collaboration` | Reviews, mentoring, design discussions. |
| `tooling` | Developer tools, scripts, automation. |
| `oncall` | Incident response and on-call wins. |
| `design` | Design docs and architecture decisions. |
| `documentation` | Docs, runbooks, guides. |

## Procedure

1. Confirm time range and scope. Do not assume "last week" without dates.
2. Check available tools and sources: `save_to_brag_sheet`, `git`, `gh`, and Copilot session logs.
3. For Backfill, scan all available sources before drafting entries.
4. Group related signals: same PR plus commits, multiple commits on same feature within 3 days, and Copilot sessions on the same repo and branch.
5. Draft entries using action → result → evidence and assign categories.
6. Show drafted entries before saving or finalizing.
7. For Review Pack, select the top 3-5 highest-impact items, organize by impact theme, and expand selected items using STAR.

## Backfill commands

```bash
git --version 2>/dev/null
gh --version 2>/dev/null
ls ~/.copilot/session-state/ 2>/dev/null
```

```bash
git log --author="$(git config user.email)" --since="2 weeks ago" \
  --pretty=format:'%h|%ad|%s' --date=short --no-merges
```

```bash
gh pr list --author @me --state merged --limit 20 \
  --json number,title,repository,mergedAt
```

For Copilot session history, read `~/.copilot/session-state/<session-id>/workspace.yaml` and use `summary`, `cwd`, `repository`, and `branch`. Skip sessions without `summary`. If `~/.copilot/session-state/` does not exist, continue with git and PRs.

For long review ranges, prefer PR history and explicit dates:

```bash
git log --author="$(git config user.name)" --since="2024-07-01" --until="2025-01-01" --oneline
```

## Review prep

| Step | Action |
| --- | --- |
| Gather | Collect entries from work log or Backfill. |
| Select | Pick the top 3-5 highest-impact items. |
| Rewrite | Include what I did, why it mattered, and proof. |
| Organize | Group by delivering results, customer/team impact, collaboration/mentoring/leadership, and growth/learning. |
| Ask for gaps | Prompt for missing metrics, beneficiaries, PRs, incident IDs, or docs. |

Use STAR for longer narratives: Situation → Task → Action → Result. For Microsoft Connect-style reviews, frame around Core Priorities: delivering results, customer obsession, teamwork, and growth mindset.

## Gotchas

- **No recent commits is not no impact**: check `gh pr list --author @me --state merged`, other repos, other branches, or fall back to guided interview.
- **Review periods may span 6-12 months**: set explicit `--since` and `--until` dates.
- **Pair programming needs attribution**: ask whether to credit as individual work, shared work, or skip.
- **Ambiguous "brag" may be launch copy**: confirm whether the user wants a work entry or a team announcement.
- **Weak periods should stay honest**: do not pad with trivial entries.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `copilot-brag-sheet` | extension | The user wants automatic background tracking of Copilot CLI sessions and the `save_to_brag_sheet`, `review_brag_sheet`, or `generate_work_log` tools. |

## Work-history terminology

Keep these terms available when mining or grouping sources: `auto-save`, `co-authored`, `cross-repo`, `file/feature`, `gh pr list --state merged`, `git/PRs/sessions`, `incidents/quarter`, and `self-review`.

## Output template

```markdown
## Brag sheet result

**Status:** captured | backfilled | review-pack | needs evidence | blocked
**Time range:** <explicit range>
**Sources scanned:** git | GitHub PRs | Copilot sessions | interview

### Week of <YYYY-MM-DD>

#### PRs & Features
- **<action>** → <result/impact> → <evidence>

#### Infrastructure
- **<action>** → <result/impact> → <evidence or `(evidence needed)`>

### Review themes
| Theme | Strongest entries | Evidence gaps |
| --- | --- | --- |
| `<theme>` | `<entries>` | `<missing proof>` |

### Validation
- Entries follow action → result → evidence: pass | fail
- Metrics source-verified or user-provided: pass | fail
- Draft shown before saving: yes | no
```

## Quality gate

- [ ] Time range and scope are explicit.
- [ ] Every entry has action → result → evidence or `(evidence needed)`.
- [ ] No metric, shipped status, or beneficiary is invented.
- [ ] Related commits, PRs, and sessions are grouped instead of duplicated.
- [ ] Draft entries are shown before saving.
- [ ] Missing tools or missing `~/.copilot/session-state/` are handled without error.
- [ ] Categories are assigned for pasteable review or weekly update output.

## References

- [copilot-brag-sheet](https://github.com/microsoft/copilot-brag-sheet)
