---
name: copilot-usage-metrics
description: >-
  Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the
  GitHub CLI, REST API, and bundled scripts. Use when the user asks about Copilot usage, adoption,
  active users, acceptance rates, suggestions, chat interactions, per-user breakdowns,
  organization metrics, enterprise metrics, or usage on a specific date.
---

<!-- Generated from harness/github-copilot/skills/copilot-usage-metrics/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Copilot usage metrics

Collect GitHub Copilot usage metrics at organization or enterprise scope, choose aggregate or per-user scripts, pass an optional `YYYY-MM-DD` day, and summarize adoption, suggestions, acceptance, and chat activity.

## When to invoke

- "Show Copilot usage metrics for my organization."
- "How many people are using Copilot in this enterprise?"
- "Get per-user Copilot adoption for 2026-02-01."
- "Show Copilot acceptance rates and suggestions."
- "Retrieve Copilot chat usage statistics."

## Prerequisites and context

- Use GitHub CLI (`gh`) authentication for API access.
- The endpoints require GitHub Enterprise Cloud.
- The caller must have appropriate permissions: enterprise owner, billing manager, or token scopes such as `manage_billing:copilot` / `read:enterprise`.
- The "Copilot usage metrics" policy must be enabled in enterprise settings.
- Metrics data is available starting from October 10, 2025, and historical data is accessible for up to 1 year.

## Request classification

| User asks for | Scope | Detail | Script |
| --- | --- | --- | --- |
| Organization aggregate metrics | Organization name | Optional day | `get-org-metrics.sh <org> [day]` |
| Organization per-user metrics | Organization name | Optional day | `get-org-user-metrics.sh <org> [day]` |
| Enterprise aggregate metrics | Enterprise slug | Optional day | `get-enterprise-metrics.sh <enterprise> [day]` |
| Enterprise per-user metrics | Enterprise slug | Optional day | `get-enterprise-user-metrics.sh <enterprise> [day]` |

Ask for the org name or enterprise slug only when it is not provided and cannot be inferred. Ask whether the user wants aggregate or per-user metrics only when their request is ambiguous.

## Metrics to summarize

| Metric family | Present as |
| --- | --- |
| Active users | Total active users and, for per-user reports, user rows. |
| Code suggestions | Total suggestions, accepted suggestions, and acceptance rate when fields are available. |
| Chat usage | Total chat interactions or available chat activity fields. |
| Date filtering | Specific day in `YYYY-MM-DD` format, or general/recent metrics when no day is supplied. |
| Trends | Highlight changes only when multiple days are returned or the script output supports comparison. |

## Procedure

1. Determine organization versus enterprise scope.
2. Resolve the org name or enterprise slug.
3. Determine aggregate versus per-user output.
4. Parse an optional day in `YYYY-MM-DD` format; otherwise request recent/general metrics.
5. Run the matching bundled script from the skill directory.
6. Format aggregate results as key metrics and per-user results as a table.
7. If the API returns 403, advise the user to check token permissions and enterprise policy settings.

## Available scripts

- `get-org-metrics.sh`: aggregated organization metrics.
- `get-org-user-metrics.sh`: per-user organization metrics.
- `get-enterprise-metrics.sh`: aggregated enterprise metrics.
- `get-enterprise-user-metrics.sh`: per-user enterprise metrics.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `403` from API | Missing role, token scope, or enterprise policy. | Check enterprise owner/billing manager access, `manage_billing:copilot` / `read:enterprise`, and the Copilot usage metrics policy. |
| No historical data | Requested date before October 10, 2025 or older than 1 year. | Choose a supported date range. |
| Script cannot authenticate | `gh` is not logged in or token is wrong account. | Run `gh auth status` and reauthenticate. |

## Output template

```markdown
### Copilot usage metrics

**Status:** complete | needs input | blocked
**Scope:** organization | enterprise
**Name:** `<org or enterprise slug>`
**Detail:** aggregate | per-user
**Day:** `<YYYY-MM-DD or recent>`

| Metric | Value |
| --- | --- |
| Active users | `<count>` |
| Acceptance rate | `<percent or unavailable>` |
| Total suggestions | `<count or unavailable>` |
| Chat interactions | `<count or unavailable>` |

### Per-user breakdown
| User | Active | Suggestions | Accepted | Chat interactions |
| --- | --- | --- | --- | --- |
| `<login>` | `<yes/no>` | `<count>` | `<count>` | `<count>` |

**Validation**
- Script: `<script name>`
- API access: pass | fail
```

## Quality gate

- [ ] Scope is identified as organization or enterprise.
- [ ] Org name or enterprise slug is present before running a script.
- [ ] Aggregate versus per-user detail is selected.
- [ ] Optional day uses `YYYY-MM-DD` format when provided.
- [ ] The chosen script matches scope and detail.
- [ ] Output summarizes active users, acceptance rate, suggestions, and chat interactions when available.
- [ ] A `403` response is explained with permission, scope, and policy checks.
- [ ] Date availability limits are reported when relevant.
