---
name: secret-scanning
description: >-
  Configure and manage GitHub secret scanning, push protection, custom patterns, exclusions, alert triage, remediation, bypass workflows, and pre-commit secret scans through the Advanced Security plugin. Use this skill when enabling secret scanning, resolving blocked pushes, writing secret_scanning.yml, creating regex patterns, triaging alerts, or scanning code before committing.
---

# Secret scanning

Configure GitHub secret scanning and push protection, define custom patterns, remediate alerts, and guide AI coding agents toward pre-commit scans before secrets reach the repository.

## When to invoke

- "Enable secret scanning and push protection for this repo."
- "Resolve this GitHub blocked push for a secret."
- "Create a custom secret scanning regex pattern."
- "Triage these secret scanning alerts."
- "Scan my local changes for secrets before committing."

## Prerequisites and context

- Public repositories receive secret scanning automatically for supported patterns.
- Private and internal organization-owned repositories require GitHub Secret Protection on Team or Enterprise Cloud.
- User-owned repositories require Enterprise Cloud with Enterprise Managed Users.
- Pre-commit scanning inside GitHub Copilot CLI uses the Advanced Security plugin: `advanced-security@copilot-plugins`.

## How secret scanning works

Secret scanning detects exposed credentials across full Git history on all branches, issues, pull requests, discussions, wikis, and secret gists. Alerts may be user alerts, partner alerts, or push protection alerts.

| Feature | Scope |
| --- | --- |
| Secret scanning | Finds supported provider patterns, custom patterns, non-provider patterns, and AI-detected generic secrets. |
| Push protection | Blocks supported secrets in command line pushes, GitHub UI commits, file uploads, REST API requests, and REST API content creation endpoints. |
| Validity checks | Shows `active`, `inactive`, or `unknown` by testing credentials against provider APIs. |
| Extended metadata checks | Adds ownership context after validity checks are enabled. |
| Exclusions | `.github/secret_scanning.yml` can auto-close alerts and skip push protection for ignored paths. |

## Procedure

1. Enable Secret Protection in repository Settings → Advanced Security, or use organization Settings → Advanced Security → Global settings → Security configurations for scale.
2. Enable Push protection under Secret Protection.
3. Add `.github/secret_scanning.yml` only when exclusions are necessary.
4. Optionally enable non-provider patterns, AI-powered generic secret detection, validity checks, and extended metadata checks.
5. For custom secrets, create a pattern, save and dry run, review up to 1,000 results, publish, then optionally enable push protection.
6. For alerts, rotate the credential first, then review context, validity, author, and history removal needs.
7. For local AI-agent pre-commit scans, install the Advanced Security plugin and use its secret scanning skill/tool.

## Exclusions

```yaml
paths-ignore:
  - "docs/**"
  - "test/fixtures/**"
  - "**/*.example"
```

| Limit or rule | Requirement |
| --- | --- |
| Entry count | Maximum 1,000 entries in `paths-ignore`. |
| File size | `.github/secret_scanning.yml` must be under 1 MB. |
| Push protection | Excluded paths also skip push protection checks. |
| Hygiene | Be specific, explain exclusions, review periodically, and inform the security team. |

## Blocked push resolution

| Option | Use when | Actions |
| --- | --- | --- |
| Remove latest-commit secret | The secret is only in the latest commit. | Remove it, run `git commit --amend --all`, then `git push`. |
| Remove earlier-commit secret | The secret is in an older commit. | Find it with `git log`, run `git rebase -i <COMMIT-ID>~1`, edit the offending commit, `git add .`, `git commit --amend`, `git rebase --continue`, `git push`. |
| Bypass | The detected value is safe to push. | Visit the push error URL, choose `It's used in tests`, `It's a false positive`, or `I'll fix it later`, then re-push within 3 hours. |
| Delegated bypass request | Delegated bypass is enabled and the user lacks bypass privileges. | Visit the URL, add a justification, submit request, wait for approval/denial, then push only if approved. |

Read `references/push-protection.md` for detailed bypass, delegated bypass, command line, REST API, and user push protection behavior.

## Custom patterns

| Scope | Applies to |
| --- | --- |
| Repository level | One repository. |
| Organization level | All repositories with secret scanning enabled. |
| Enterprise level | All organizations in the enterprise. |

Create patterns under Settings → Advanced Security → Custom patterns → New pattern. Provide a name, regex, sample test string, `Save and dry run`, review false positives, `Publish pattern`, and enable push protection when the pattern is reliable. Copilot-assisted generation can draft regexes from a description and examples. Read `references/custom-patterns.md` for regex syntax, dry runs, scopes, and Copilot generation.

## Alert management

| Type | Description | Visibility |
| --- | --- | --- |
| User alerts | Secrets found in repository content. | Security tab. |
| Push protection alerts | Secrets pushed through bypass. | Security tab with filter `bypassed: true`. |
| Partner alerts | Secrets reported to providers. | Provider-only, not shown in repository. |
| Generic alerts | Non-provider and AI-detected secrets. | Limited to 5,000 per repository. |

Remediate in this order: rotate the credential immediately, review location/commit/author, prioritize `active` over `unknown` over `inactive`, and remove from Git history only when needed after rotation. Dismiss only as `False positive`, `Revoked`, or `Used in tests` with documented rationale. Read `references/alerts-and-remediation.md` for alert types, validity, metadata, generic alerts, remediation, git history, and REST API details.

## Pre-commit scanning via AI coding agents

Install the Advanced Security plugin when an AI coding agent must scan code before committing:

```bash
/plugin install advanced-security@copilot-plugins
```

In Visual Studio Code, open Chat: Plugins or use `@agentPlugins`, install `advanced-security`, then run `/secret-scanning` in Copilot Chat. The plugin provides `run_secret_scanning` and a dedicated scanning skill.

## Progressive disclosure and bundled resources

- `references/push-protection.md`: push protection mechanics, bypass workflow, delegated bypass, command line, REST API, user push protection.
- `references/custom-patterns.md`: custom pattern creation, regex syntax, dry runs, publish flow, scopes, Copilot-assisted pattern generation.
- `references/alerts-and-remediation.md`: alert types, validity checks, extended metadata, generic alerts, remediation, git history, REST API.

## Secret scanning terminology

Preserve exact alert, bypass, and scope vocabulary: `Copilot`, `Private/internal`, `REST API`, `Team/Enterprise`, `auto-closed`, `bypass`, `bypass request`, `command line`, `custom pattern`, `delegated`, `dry run`, `enterprise`, `generic`, `git history`, `metadata`, `org-owned`, `organization`, `organization-specific`, `partner alert`, `provider-only`, `publish`, `regex`, `remediation`, `secret_scanning.yml`, `time-intensive`, `user alert`, `user push protection`, and `validity`.

## Output template

```markdown
## Secret scanning result

**Status:** configured | remediated | needs action | blocked
**Scope:** repository | organization | enterprise | local pre-commit

### Actions
| Area | Action | Evidence |
| --- | --- | --- |
| Secret scanning | `<enabled/configured/skipped>` | `<settings, command, or file>` |
| Push protection | `<enabled/configured/skipped>` | `<settings or reason>` |
| Custom patterns | `<pattern name or none>` | `<dry-run result>` |
| Alerts | `<rotated/dismissed/open>` | `<alert IDs or links>` |

### Remediation
- Credential rotation: complete | required | not applicable
- Git history rewrite: required | not required | deferred
- Bypass: not used | used with reason `<reason>` | requested

### Validation
- `.github/secret_scanning.yml`: valid | not present | needs fix
- Pre-commit scan: pass | fail | not run
```

## Quality gate

- [ ] Secret rotation is prioritized before alert dismissal or history cleanup.
- [ ] Push protection bypasses include a documented allowed reason and 3-hour re-push window when relevant.
- [ ] `.github/secret_scanning.yml` respects the 1,000-entry and 1 MB limits.
- [ ] Custom patterns were dry-run before publishing.
- [ ] Alert status distinguishes `active`, `inactive`, and `unknown`.
- [ ] Pre-commit AI-agent scanning uses `advanced-security@copilot-plugins` and `run_secret_scanning` when available.

## References

- [Secret scanning in AI coding agents via the GitHub MCP Server](https://github.blog/changelog/2026-03-17-secret-scanning-in-ai-coding-agents-via-the-github-mcp-server/)
