---
name: story-planning
description: 'Use when decomposing epics into INVEST user stories, mapping personas, writing acceptance criteria, grooming backlog items, or creating GitHub Issues for sprint-ready work. Produces story maps, issue bodies, labels, duplicate checks, and optional GitHub Issues. DO NOT USE FOR: test analysis (use test-coverage), pipeline diagnostics (use pipeline-diagnostics), Azure infrastructure design (use azure-infrastructure). Triggers include "decompose this epic", "write user stories", "create GitHub issues for these stories", and "prepare sprint backlog".'
---

# Story Planning

Use this skill to decompose epics into INVEST-compliant user stories and, after approval, create GitHub Issues with consistent labels and acceptance criteria. It produces a story map, duplicate-check summary, issue-ready Markdown bodies, and optional `gh issue create` commands.

> [!NOTE]
> This skill depends on the `gh` CLI and authenticated GitHub access when creating or inspecting GitHub Issues. It does not use an MCP server by default.

## When to invoke

- "Break this epic into user stories."
- "Create GitHub Issues for these stories."
- "Check whether these stories meet INVEST."
- "Prepare sprint-ready backlog items."
- "Find duplicate issues before we create new stories."

## Prerequisites and context

- Epic description, target personas, and expected business outcome are available.
- Repository owner/name is known for GitHub Issue operations.
- `gh auth status` succeeds if querying or creating issues.
- Labels are known or can be proposed, such as `user-story`, `epic:<name>`, and `priority:<level>`.

## Procedure

### Step 1: Understand the epic

Capture problem, target users, desired outcome, constraints, and out-of-scope items.

### Step 2: Identify personas

Common Open Horizons personas include Developer, SRE, Platform Engineer, Tech Lead, Product Owner, Security Engineer, and Backstage Portal Admin.

### Step 3: Decompose into INVEST stories

| INVEST criterion | Check |
| --- | --- |
| Independent | Story can deliver value without hidden dependency. |
| Negotiable | Implementation details are not over-specified. |
| Valuable | Benefit is clear to a persona or business goal. |
| Estimable | Scope is clear enough for team estimation. |
| Small | Fits within one sprint. |
| Testable | Acceptance criteria are observable. |

### Step 4: Check for duplicate issues

```bash
gh issue list --search "<keywords>" --state open
gh issue list --label "epic:<name>" --state open
```

### Step 5: Classify story readiness

| Severity | Meaning |
| --- | --- |
| Critical | Story lacks persona, value, or acceptance criteria. |
| High | Duplicate likely exists or story is too large for a sprint. |
| Medium | Labels, priority, or dependency needs refinement. |
| Low | Wording or formatting issue. |

### Step 6: User confirmation gate for GitHub Issue creation

```text
Repository: <owner>/<repo>
Epic: <epic>
Stories to create: <count>
Labels: user-story, epic:<name>, priority:<level>
Proceed with creating GitHub Issues? (y/n)
```

> [!IMPORTANT]
> Only create GitHub Issues after an explicit affirmative response. On a negative, ambiguous, or missing response, do not create issues; output the issue-ready story bodies and stop.

### Step 7: Create approved issues

```bash
gh issue create --title "Story: <title>" --body "<markdown body>" --label "user-story,epic:<name>,priority:<level>"
```

## Limits

- Do not use this skill for: test analysis (use test-coverage), pipeline diagnostics (use pipeline-diagnostics), Azure infrastructure design (use azure-infrastructure).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Epic lacks persona or value | Ask a focused question before creating stories. |
| More than eight stories are needed | Recommend splitting the epic. |
| Duplicate issue exists | Link the duplicate and do not create a new issue unless approved. |
| GitHub auth fails | Ask the operator to run `gh auth login`. |
| Label does not exist | Create issue without the missing label only if the user approves; otherwise stop. |

## Output template

Return exactly this structure:

```markdown
## Epic Decomposition Report

**Epic:** <name>
**Personas:** <personas>
**Stories:** <count>
**GitHub Issues Created:** <yes|no>

### Stories
| # | Title | Persona | INVEST status | Labels |
| --- | --- | --- | --- | --- |
| 1 | <title> | <persona> | <pass|needs work> | `user-story` |

### Duplicate Check
- <result>

### Next Steps
1. <step>
```

## Quality gate

- [ ] Every story has persona, capability, and benefit.
- [ ] Every story has 3-5 acceptance criteria.
- [ ] INVEST criteria were checked.
- [ ] Duplicate issues were searched before creation.
- [ ] No story point estimates were invented.
- [ ] Explicit approval was received before creating GitHub Issues.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
