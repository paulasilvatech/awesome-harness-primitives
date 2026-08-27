---
name: acreadiness-assess
description: >-
  Run the AgentRC AI-readiness assessment for the current repository, optionally apply a policy,
  and produce a self-contained HTML dashboard at reports/index.html. Use when asked to assess,
  audit, score, or report how AI-ready a repo is.
argument-hint: >-
  [--policy <path-or-pkg>] [--per-area] — e.g. /acreadiness-assess, /acreadiness-assess --policy
  ./policies/strict.json
---

<!-- Generated from harness/github-copilot/skills/acreadiness-assess/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AgentRC AI-readiness assessment

Run AgentRC readiness, transform the `CommandResult<T>` JSON into a tailored static HTML report, and summarize maturity, score, weak pillars, and remediation.

## When to invoke

- "Assess this repository's AI readiness."
- "Run an AgentRC readiness audit."
- "Score how AI-ready this repo is."
- "Generate the AI readiness dashboard with a policy."

## Inputs

Use `$ARGUMENTS` for optional scan flags. Accept `--policy <path-or-pkg>` to apply an org-specific policy and `--per-area` to request per-area output. If `$ARGUMENTS` is empty, run built-in AgentRC defaults unless `agentrc.config.json` declares a `policies` array.

## Prerequisites and context

- Node 20+ must be on `PATH`; check with `node --version` when uncertain.
- AgentRC is invoked with `npx -y github:microsoft/agentrc readiness`.
- The skill may create or overwrite only `reports/index.html`.
- The report must be self-contained and openable with `file://`.
- For a primer on policies, suggest the `acreadiness-policy` skill.

## Procedure

1. Confirm Node 20+ is available with `node --version` when the environment is unknown.
2. Choose policy input in precedence order: user-provided `--policy <source>`, `agentrc.config.json` `policies` array, then built-in defaults.
3. Run the readiness scan from the repository root with structured output:

```bash
npx -y github:microsoft/agentrc readiness --json [--policy <source>] [--per-area]
```

4. Treat the `CommandResult<T>` JSON envelope from `npx github:microsoft/agentrc readiness` as the source data for rendering.
5. Hand off interpretation and rendering to the `ai-readiness-reporter` custom agent, using the bundled `report-template.html` to produce `reports/index.html`.
6. Tell the user how to open `reports/index.html` and summarize maturity level, overall score, top three lowest pillars, and the highest-leverage next action.

## Dashboard content requirements

| Area | Required content |
| --- | --- |
| Summary | Maturity level, overall score, grade, and pass-rate versus threshold. |
| Pillars | All 9 pillars across Repo Health (8) and AI Setup (1). |
| Per-pillar explanation | What it measures, why it matters for AI, current state, and one specific recommendation. |
| Relevance | AI relevance badge: High, Medium, or Low. |
| Extras | Show separately; extras never affect the score. |
| Active Policy | Include disabled criteria, overridden criteria, disabled/overridden policy markers, and thresholds. |
| Remediation | Prioritised Remediation Plan grouped as Fix First, Fix Next, and Plan. |
| Raw data | Embed the raw AgentRC JSON for reuse. |

## Gotchas

- AgentRC has a built-in renderer with `--visual` / `--output report.html`, but this skill intentionally uses the custom dashboard for an opinionated report closer to a code review than a metrics dump.
- For CI gating, recommend `agentrc readiness --fail-level <n>` with a level from 1 to 5.
- The almost-always highest-leverage next action is to run the `acreadiness-generate-instructions` skill after reviewing the assessment.

## Progressive disclosure and bundled resources

- `report-template.html`: static dashboard template used by the `ai-readiness-reporter` custom agent. Inline all CSS so the report works under `file://`.

## Output template

```markdown
## AI-readiness assessment result

**Status:** report created | blocked
**Report:** `reports/index.html`
**Command:** `npx -y github:microsoft/agentrc readiness --json <policy/per-area flags>`

| Metric | Value |
| --- | --- |
| Maturity level | `<level>` |
| Overall score | `<score>` |
| Grade | `<grade>` |
| Pass-rate vs threshold | `<value>` |

### Lowest pillars
1. `<pillar>` - <reason>
2. `<pillar>` - <reason>
3. `<pillar>` - <reason>

### Highest-leverage next action
<next action, usually run the acreadiness-generate-instructions skill>
```

## Quality gate

- [ ] Node 20+ was verified or the environment already proved it.
- [ ] Policy precedence was applied: `$ARGUMENTS`, `agentrc.config.json`, then built-in defaults.
- [ ] Readiness ran with `--json` and preserved the `CommandResult<T>` envelope.
- [ ] `reports/index.html` was produced from `report-template.html` and is self-contained.
- [ ] The report includes all 9 pillars, extras, Active Policy details, remediation priorities, and raw JSON.
- [ ] No repository file other than `reports/index.html` was modified.
