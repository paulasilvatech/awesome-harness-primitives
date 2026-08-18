---
name: github-codespaces-efficiency
description: >-
  Audit and improve GitHub Codespaces efficiency. Use this skill when a user wants faster Codespaces startup, lower Codespaces spend, slim devcontainers, right-size machines, tune idle timeout, scope prebuilds, or create an efficient .devcontainer baseline.
---

# GitHub Codespaces efficiency

Inspect Codespaces configuration and usage evidence, identify the largest startup-time or spend waste, apply guardrails that protect developer experience, and return up to three ranked fixes with validation and impact.

## When to invoke

- "Make our Codespaces start faster."
- "Reduce GitHub Codespaces cost for this repo."
- "Audit this devcontainer for waste."
- "Right-size Codespaces machines and idle timeout."
- "Set up efficient Codespaces prebuilds."

## Prerequisites and context

- Use repository files under `.devcontainer/` when present.
- Use GitHub CLI only when authenticated and authorized; if `gh` auth fails or repo admin scope is unavailable, proceed with static analysis and mark machine-type and prebuild recommendations as unverified.
- If no `.devcontainer/` exists, read `references/codespaces.md` and define a baseline before proposing changes.

## Procedure

1. Measure the current configuration and available usage evidence:

```bash
find .devcontainer -maxdepth 2 -type f
gh codespace list
repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
gh api "/repos/$repo/codespaces/machines"
```

2. Inspect `.devcontainer/` files for image size, features, extensions, ports, post-create work, prebuild scope, machine type, and idle timeout.
3. Apply the guardrails in this skill before recommending any fix.
4. Rank supported fixes by estimated monthly cost savings in USD; select all that pass evidence and guardrails, up to three.
5. Verify by starting a test Codespace when possible; otherwise mark validation as `static-only` and name the remaining risk.

## Waste candidates and thresholds

| Candidate | Evidence to require | Decision rule |
| --- | --- | --- |
| Trim devcontainer | Image greater than 2 GB, more than 10 features, unused packages, or unused extensions. | Remove only tools not used for everyday development. |
| Right-size machine type | Machine larger than observed usage supports, or user reports over-provisioning. | Balance cost against throughput; do not assume smaller is always better. |
| Scope prebuilds | Prebuilds run on branches without sustained usage. | Keep default branch, `release/*` branches active in the last 14 days, and branches with more than 5 Codespaces per week. |
| Tune idle timeout | Sessions usually end before or after the default. | Use 30 min default, 15 min if most sessions end before 30 min, 60 min if most run longer. |
| Remove unused ports/extensions | Forwarded ports or extensions have no daily workflow owner. | Remove only with evidence or user confirmation. |
| Improve layer caching | Repeated package installation or volatile Dockerfile layers slow startup. | Put stable dependency layers before frequently changing source layers. |

Recommend adding `devcontainer-lock.json` when it is missing, because many repos predate lock-file support.

## Guardrails

- Do not remove tools the team uses every day.
- Do not turn the devcontainer into a production image or add production-only dependencies unless explicitly required.
- Prefer incremental changes; use a greenfield baseline only when no `.devcontainer/` exists.
- Split repo-editable changes from org-level or user-level Codespaces settings.
- Treat unexpected build or startup failures as real bugs even when the configuration appears correct.

## Progressive disclosure and bundled resources

- `references/codespaces.md`: devcontainer baseline, machine-sizing, machine sizing, prebuild, idle-timeout guidance, port-forwarding guidance, and reporting details.
- `references/review-rubric.md`: use when reviewing completed Codespaces efficiency work.

## Output template

```markdown
## GitHub Codespaces efficiency result

**Status:** proven live | static-only | blocked
**Scope:** `<repo or .devcontainer path>`

### Waste sources
| Rank | Source | Evidence | Impact |
| --- | --- | --- | --- |
| 1 | <cost/startup driver> | <file, command output, or assumption> | <startup/cost/utilization effect> |

### Proposed fixes
| Rank | Fix | Evidence | Estimated monthly savings (USD) | Risk |
| --- | --- | --- | --- | --- |
| 1 | <top fix> | <why supported> | <amount or unknown> | <remaining risk> |

### Validation
- Test Codespace: pass | fail | not run, <reason>
- Machine sizing: verified | unverified, <reason>
- Prebuild scope: verified | unverified, <reason>

### Impact
- Startup time: <expected or measured>
- Monthly spend: <expected or measured>
- Resource utilization: <expected or measured>
```

## Quality gate

- [ ] `.devcontainer/` was inspected or the absence of a devcontainer was handled with `references/codespaces.md`.
- [ ] `gh codespace list` and `/repos/$repo/codespaces/machines` were attempted when CLI access was available.
- [ ] Every proposed fix has audit evidence and passes all guardrails.
- [ ] No more than three fixes are recommended, ranked by estimated monthly cost savings in USD.
- [ ] Validation is labeled `proven live`, `static-only`, or `blocked` with remaining risk.
- [ ] Startup time, monthly spend, and resource utilization impact are separated.
