---
name: acreadiness-policy
description: >-
  Help the user pick, write, or apply an AgentRC policy. Policies customise readiness scoring by
  disabling irrelevant checks, overriding impact/level, setting pass-rate thresholds, or chaining
  org baselines with team overrides. Use when the user asks about strict mode, AI-only scoring,
  custom weights, CI gating, or wants org-wide standardisation.
argument-hint: >-
  [show | new <name> | apply <path-or-pkg>] — e.g. /acreadiness-policy show, /acreadiness-policy
  new strict-frontend
---

<!-- Generated from harness/github-copilot/skills/acreadiness-policy/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AgentRC readiness policies

Select, create, or apply AgentRC JSON policies that customize readiness scoring by disabling irrelevant criteria, overriding impact or level, setting pass-rate thresholds, and chaining organization baselines with team-specific overrides.

## When to invoke

- "Show which AgentRC policies are currently in effect."
- "Create a strict frontend readiness policy."
- "Apply this AgentRC policy and rerun readiness."
- "Set custom weights or pass-rate thresholds for CI gating."
- "Make an org-wide baseline with team overrides."

## Inputs

Use `$ARGUMENTS` as one of these subcommands: `show`, `new <name>`, or `apply <path-or-pkg>`. If `$ARGUMENTS` is empty, infer the intended action from the user request and ask only for the missing policy name or source path.

## Policy model

A policy is a JSON file with three optional top-level sections: `criteria`, `extras`, and `thresholds`. JSON policies can disable, override, and set thresholds, but cannot add new criteria. For new detection logic, direct users to AgentRC's TypeScript plugin system at `docs/dev/plugins.md`.

```jsonc
{
  "name": "my-policy",
  "criteria": {
    "disable": ["env-example", "observability", "dependabot"],
    "override": {
      "readme": { "impact": "high", "level": 2 },
      "lint-config": { "title": "Linter required" }
    }
  },
  "extras": {
    "disable": ["pre-commit"]
  },
  "thresholds": {
    "passRate": 0.9
  }
}
```

Built-in starting points in `examples/policies/`:

| Policy | What it does |
| --- | --- |
| `strict.json` | Requires 100% pass rate and raises impact on key criteria. |
| `ai-only.json` | Disables all repo-health checks and focuses on AI tooling. |
| `repo-health-only.json` | Disables AI checks and focuses on traditional quality. |

## Scoring and thresholds

| Impact | Weight |
| --- | --- |
| `critical` | 5 |
| `high` | 4 |
| `medium` | 3 |
| `low` | 2 |
| `info` | 0 |

Score formula: `Score = 1 − (deductions / max possible weight)`.

| Grade | Score |
| --- | --- |
| A | `≥ 0.9` |
| B | `≥ 0.8` |
| C | `≥ 0.7` |
| D | `≥ 0.6` |
| F | `< 0.6` |

Typical pass-rate thresholds: `0.7` lenient, `0.85` standard, and `1.0` strict.

## Procedure

1. For `show`, read `agentrc.config.json` and report the `policies` array, or state that no policies are configured.
2. For `new <name>`, scaffold `policies/<name>.json` with sensible defaults and walk the user through what to disable, what `must-haves` to raise, and the pass-rate threshold.
3. Reference a new policy from `agentrc.config.json` as `{ "policies": ["./policies/<name>.json"] }`.
4. For `apply <path-or-pkg>`, run `agentrc readiness --json --policy <source>` and `re-render` the report by handing off to `assess` or the `ai-readiness-reporter` workflow.
5. For layered policies, chain sources in order with `--policy ./org-baseline.json,./team-frontend.json`.
6. For CI gating, combine policy selection with `--fail-level`.

## Commands and CI examples

```bash
npx -y github:microsoft/agentrc readiness --json --policy ./org-baseline.json,./team-frontend.json
```

```yaml
- run: npx -y github:microsoft/agentrc readiness --policy ./policies/strict.json --fail-level 3
```

| Subcommand | Output |
| --- | --- |
| `show` | Current `agentrc.config.json` policy chain or none. |
| `new <name>` | `policies/<name>.json` plus config reference guidance. |
| `apply <path-or-pkg>` | Readiness JSON and rendered report using the requested policy source. |

## Operating rules

- **Never silently disable a pillar**: if the user wants to disable `observability`, confirm and explain the trade-off.
- **Prefer overriding `impact` over disabling**: disabling hides the gap entirely; overriding keeps it visible in the report.
- **Recommend extras stay enabled**: extras cost nothing because they do not affect the score.
- **Suggest layering**: most organizations want a baseline policy plus per-team overrides chained with `--policy a.json,b.json`.
- **Use built-in policies first**: start from `strict.json`, `ai-only.json`, or `repo-health-only.json` before writing a custom policy from scratch.


- Common override IDs include `readme` and `codeowners`; raise these `must-haves` instead of disabling them when they are organizational requirements.

## Output template

```markdown
## AgentRC policy result

**Status:** shown | created | applied | needs input | blocked
**Subcommand:** show | new | apply
**Policy source:** <path, package, or configured chain>

### Policy effect
- Disabled criteria/extras: <items or none>
- Overrides: <criteria and impact/level/title changes>
- Thresholds: <passRate and CI gate>

### Commands or files
- `<command or file path>`: <result>
```

## Quality gate

- [ ] `$ARGUMENTS` was resolved to `show`, `new <name>`, or `apply <path-or-pkg>`.
- [ ] Built-in policies in `examples/policies/` were considered before custom policy creation.
- [ ] Disabling a criterion or pillar is confirmed and its trade-off is explained.
- [ ] Impact weights, pass-rate threshold, and grade effects are stated when scoring changes.
- [ ] Layered policies preserve org baseline before team override order.
- [ ] CI gating uses `--fail-level` when enforcement is requested.
- [ ] The output follows `## Output template` exactly.
