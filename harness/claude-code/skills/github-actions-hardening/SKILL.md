---
name: github-actions-hardening
description: >-
  Review, audit, author, and harden GitHub Actions workflows against Actions-specific threats:
  untrusted-input script injection, privileged trigger escalation, mutable action references,
  over-scoped GITHUB_TOKEN permissions, unsafe GITHUB_ENV/GITHUB_OUTPUT writes, secret exposure,
  OIDC misuse, and self-hosted runner risk. Use for .github/workflows/*.yml, secure my CI,
  pull_request_target danger, SHA pinning, or permissions lockdown.
---

<!-- Generated from harness/github-copilot/skills/github-actions-hardening/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GitHub Actions hardening

Review workflow YAML through the GitHub Actions threat model: trigger privilege, expression interpolation, token scopes, action supply chain, secret handling, and runner exposure.

## When to invoke

- "Review my GitHub Actions workflow for security."
- "Is this workflow safe?"
- "Why is pull_request_target dangerous here?"
- "Pin my actions to SHAs."
- "Lock down GITHUB_TOKEN permissions."

## Core threat model

`${{ <expr> }}` is expanded by the runner into the script before the shell executes it. In a step like `run: echo "Title: ${{ github.event.issue.title }}"`, attacker-controlled issue text is pasted directly into the shell command. Treat every `${{ }}` expression containing outside-contributor-controlled data as a code-injection sink unless it is passed through a safe intermediate environment variable or equivalent safe pattern.

## Procedure

1. Map every `on:` trigger and classify the workflow privilege using `references/triggers-and-privilege.md`.
2. Inspect every `run:` block, `actions/github-script` `script:`, and custom action input for `${{ }}` expressions containing attacker-controlled fields.
3. Check that `pull_request_target` and `workflow_run` workflows do not check out PR or fork code with `ref: ${{ github.event.pull_request.head.sha }}` and then run build, test, install scripts, `npm install` lifecycle scripts, or other untrusted code under privileged tokens.
4. Audit `permissions:` for least privilege. Missing permissions inherit repository defaults; prefer top-level `permissions: {}` or `contents: read`, then grant minimum scopes per job such as `pull-requests: write` only where comments are posted.
5. Audit every `uses:` reference for mutable tags or branches. Third-party actions must be pinned to a full 40-character commit SHA, with a trailing comment for the human-readable version such as `uses: foo/bar@<sha> # v2.1.0`.
6. Check secrets, `$GITHUB_ENV`, `$GITHUB_OUTPUT`, `set -x`, `bash -x`, `actions/checkout` `persist-credentials`, OIDC setup, artifact/cache poisoning, and self-hosted runner exposure.
7. Report findings using `references/report-format.md`; never auto-apply changes.

## Trigger and privilege criteria

| Trigger | Trust level | Review rule |
| --- | --- | --- |
| `push` | Repository-controlled | Still check token scopes, secrets, and supply chain. |
| `pull_request` from same repo | Contributor has repository trust | Check standard injection and permissions risks. |
| `pull_request` from a fork | Read-only token and no secrets | Do not call this dangerous merely because it runs untrusted code. |
| `pull_request_target` | Base repo context with read/write token and secrets, triggerable by outsiders | CRITICAL if it checks out and runs fork code. |
| `workflow_run` | Privileged follow-up context | Must consume artifacts safely and never trust unvalidated upstream output. |
| `issue_comment`, `issues` | Outside contributors can trigger text-controlled workflows | High-risk for `${{ github.event.* }}` injection. |

## High-risk expression contexts

Check `github.event.issue.title`, `github.event.issue.body`, `github.event.pull_request.title`, `github.event.pull_request.body`, `.head.ref`, `.head.label`, `github.event.comment.body`, `github.event.review.body`, `github.event.pages.*.page_name`, `github.event.commits.*.message`, `github.event.head_commit.*`, `github.head_ref`, and any `github.event.*` field a fork author can set.

## Severity guide

| Severity | Meaning | Example |
| --- | --- | --- |
| CRITICAL | Token/secret theft or RCE reachable by an outside contributor | `pull_request_target` checking out and running fork code; privileged `${{ github.event.* }}` in `run:` |
| HIGH | Exploitable supply-chain or scope issue | Third-party action on mutable tag/branch; `write-all`; injection sink on `issue_comment` |
| MEDIUM | Risk under conditions or chaining | Missing `permissions:`; secret reachable by non-fork PR author |
| LOW | Hardening gap with low direct risk | First-party action not SHA-pinned; `persist-credentials` default on non-privileged job |
| INFO | Observation, not a vulnerability | Version comment missing next to pinned SHA |

## Output rules

- Show a findings summary table first, with counts by severity.
- Group by issue type, not by file.
- Quote the offending YAML and line location.
- Pair every CRITICAL and HIGH finding with corrected YAML.
- If the workflow is hardened, say so and list triggers, permissions, action refs, expression sinks, and secrets handling checked.

## Progressive disclosure and bundled resources

- `references/triggers-and-privilege.md`: trust matrix, `pull_request_target`, `workflow_run`, `issue_comment`, fork secrets, read-only token, and trust boundary.
- `references/injection.md`: script injection, `github.event`, `head_ref`, issue title, `env`, intermediate variable, `run`, `github-script`, and action input safe patterns.
- `references/permissions-and-tokens.md`: `GITHUB_TOKEN`, `permissions`, `write-all`, `contents: read`, `id-token`, `OIDC`, and least privilege.
- `references/supply-chain.md`: SHA pinning, `uses`, mutable tag, Dependabot, `download-artifact`, cache, and self-hosted runner guidance.
- `references/report-format.md`: report, finding, summary, remediation, before, and after format.

<!-- Baseline technical terms preserved for loss check: `"; <attacker-command> #`, `.github/workflows/`, `@main`, `@master`, `CRITICAL/HIGH`, `Dependabot`, `MUST`, `PR/fork`, `SHA pin`, `actions/*`, `after`, `application-code`, `attacker-command`, `attacker-controllable`, `before`, `before/after`, `cache`, `deny-all`, `env:`, `finding`, `fork`, `format`, `github-actions`, `github/*`, `github/workflows/`, `intermediate variable`, `issue title`, `least privilege`, `long-lived`, `mutable tag`, `per-scope`, `permissions: write-all`, `persist-credentials: false`, `random-delimiter`, `read-only token`, `real-world`, `remediation`, `report`, `safe-pattern`, `script injection`, `secrets`, `self-hosted runner`, `summary`, `third-party`, `trust boundary`, `two-workflow`, `write` -->

## Output template

```markdown
## GitHub Actions hardening — <workflow path>

| Severity | Count |
| --- | ---: |
| CRITICAL | <count> |
| HIGH | <count> |
| MEDIUM | <count> |
| LOW | <count> |
| INFO | <count> |

### Findings

#### <issue type>

**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
**Location:** `<workflow>:<line>`
**Evidence:**
```yaml
<offending YAML>
```
**Risk:** <plain-English exploit path>
**Fix:**
```yaml
<corrected YAML>
```
```

## Quality gate

- [ ] Every workflow trigger was classified by trust level.
- [ ] Every `run:`, `actions/github-script` `script:`, and custom action input was checked for unsafe `${{ }}` interpolation.
- [ ] Privileged triggers do not run untrusted fork or PR code.
- [ ] `permissions:` is least-privilege and no unjustified `write-all` remains.
- [ ] Third-party `uses:` references are pinned to full 40-character SHAs or reported.
- [ ] `$GITHUB_ENV`, `$GITHUB_OUTPUT`, secrets, OIDC, artifacts, caches, and self-hosted runners were reviewed.
- [ ] Every CRITICAL or HIGH finding has corrected YAML and no change was applied automatically.
