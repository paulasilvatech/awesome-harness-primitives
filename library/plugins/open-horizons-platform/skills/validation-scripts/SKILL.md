---
name: validation-scripts
description: 'Use when running Open Horizons repository validation scripts for prerequisites, configuration, deployment health, naming, agent customization, documentation, or post-deploy checks. Produces command results, pass/fail summaries, and remediation guidance. DO NOT USE FOR: Terraform validation (use terraform-cli), Kubernetes checks (use kubectl-cli), Helm operations (use helm-cli). Triggers include "run validation scripts", "validate deployment", "validate config", "check agents", and "post-deploy validation".'
---

# Validation Scripts

Use this skill to run existing Open Horizons validation scripts without inventing new tooling. It produces command transcripts, pass/fail summaries, and remediation guidance for repository, deployment, and GitHub Copilot customization validation.

> [!NOTE]
> This skill depends on Bash, Python 3 for `scripts/validate-agents.py`, and any CLIs required by the specific validation script. Resolve bundled paths relative to this `SKILL.md`; do not assume the skill was copied to `.github/skills/`.

## When to invoke

- "Run validation scripts before deployment."
- "Validate the dev configuration."
- "Run post-deploy health checks."
- "Validate GitHub Copilot agents and skills."
- "Check Azure naming conventions."

## Prerequisites and context

- The repository root is the working directory.
- The script path exists before execution.
- Required CLIs for the selected script are installed.
- Target environment is known when the script requires `--environment`.

## Procedure

### Step 1: Select the existing script

| Task | Script |
| --- | --- |
| Prerequisites | `scripts/validate-prerequisites.sh` |
| Configuration | `scripts/validate-config.sh` |
| Deployment health | `scripts/validate-deployment.sh` |
| Documentation | `scripts/validate-docs.sh` |
| Agent and skill metadata | `scripts/validate-agents.py` |
| Azure naming | `scripts/validate-naming.sh` |

### Step 2: Verify script existence

```bash
test -f scripts/validate-prerequisites.sh
test -f scripts/validate-config.sh
test -f scripts/validate-deployment.sh
test -f scripts/validate-docs.sh
test -f scripts/validate-agents.py
test -f scripts/validate-naming.sh
```

### Step 3: Run the narrowest validation

```bash
./scripts/validate-prerequisites.sh
./scripts/validate-config.sh --environment dev
./scripts/validate-deployment.sh --environment dev
python3 scripts/validate-agents.py --strict
```

### Step 4: Classify validation findings

| Severity | Meaning |
| --- | --- |
| Critical | Validation exits non-zero for deployment readiness, strict metadata, or required tools. |
| High | Environment config drift or unhealthy required component. |
| Medium | Optional component missing or warning with documented workaround. |
| Low | Informational recommendation. |

### Step 5: Report and route remediation

Do not edit unrelated code from this skill. Route Terraform, Kubernetes, Helm, or pipeline failures to the matching skill.

```text
Validation action: <deployment-health|configuration|prerequisites|agents|naming>
Command: <command>
May contact live cluster or cloud: <yes|no>
Proceed with running validation? (y/n)
```

> [!IMPORTANT]
> Only run validation that contacts a live cluster, cloud account, or GitHub workflow after an explicit affirmative response when the user has not already requested that validation command. On a negative, ambiguous, or missing response, do not run the command; output the planned validation and stop.

## Limits

- Do not use this skill for: Terraform validation (use terraform-cli), Kubernetes checks (use kubectl-cli), Helm operations (use helm-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Script path is missing | Report the missing path and stop; do not invent a replacement. |
| Permission denied | Run with `bash <script>` if executable bit is missing, or report chmod need. |
| Required CLI missing | Use `prerequisites` to resolve tool availability. |
| Deployment validation fails | Summarize failing H1/H2/H3 check and route to the relevant operational skill. |
| Strict agent validation fails | Report exact file and frontmatter error from validator output. |

## Output template

Return exactly this structure:

```markdown
## Validation Report

**Script:** <path>
**Command:** `<command>`
**Exit code:** <code>
**Severity:** <Critical|High|Medium|Low>

### Summary
- Passed: <count-or-summary>
- Failed: <count-or-summary>
- Warnings: <count-or-summary>

### Findings
- <finding>

### Remediation
1. <step>
```

## Quality gate

- [ ] Used only existing validation scripts.
- [ ] Verified script paths exist before referencing them.
- [ ] Ran the narrowest script that covers the requested validation.
- [ ] Captured exit code and important output.
- [ ] Routed remediation to the correct domain skill.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
