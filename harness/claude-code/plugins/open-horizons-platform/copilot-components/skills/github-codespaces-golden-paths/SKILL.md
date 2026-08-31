---
name: github-codespaces-golden-paths
description: >-
  Configures GitHub Codespaces devcontainer environments for Backstage Golden Path templates. Use this skill when creating or validating devcontainer.json, Codespaces setup, Python FastAPI templates, Node app templates, Terraform templates, Java templates, AI/ML pipelines, data pipelines, container features, SDK pre-installation, or template mapping.
---

# GitHub Codespaces Golden Paths Skill

Configure GitHub Codespaces dev environments for each Golden Path template type so developers receive a fully ready workspace when they scaffold from the Backstage portal.

## When to invoke

- "Add a devcontainer to a Golden Path template."
- "Configure Codespaces for Python FastAPI, Node, Terraform, Java, AI/ML, or data pipeline templates."
- "Map Backstage Golden Path templates to ready-to-code Codespaces environments."
- "Validate SDK and tool preinstallation for a scaffolded repository."

## Prerequisites and context

### Scope

| Aspect | Detail |
|--------|--------|
| **Purpose** | Auto-create Codespaces with SDKs, tools, and configs per template |
| **Trigger** | Developer scaffolds a Golden Path → repo created → Codespace ready |
| **Used by** | `@backstage-expert`, `@open-horizons-deployment-operator` |

## Procedure

### How it works

1. Developer selects a Golden Path template in the portal Backstage
2. Scaffolder creates a new repo with skeleton files
3. Skeleton includes `.devcontainer/devcontainer.json` configured for that template type
4. Developer clicks "Open in Codespaces" → fully configured environment

### Detailed devcontainer templates

For Python, Node.js, Terraform, Java, AI/ML, and data pipeline devcontainer templates plus Golden Path mapping, read `references/devcontainer-templates.md`.

## Output template

Return exactly this structure:

```markdown
# Codespaces Golden Path result

**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the devcontainer configuration outcome.

### Details
- Template type: <Python FastAPI | Node | Terraform | Java | AI/ML | data pipeline>
- Devcontainer path: `.devcontainer/devcontainer.json`
- Features and SDKs: <configured items>
- Golden Path mapping: <template or repository mapping>

### Validation evidence
- <command or file check performed>: <result and relevant output>
```

## Limits

- Do not use this skill for Backstage portal deployment.
- Use `backstage-deployment` (`skill`) instead when deploying or operating Backstage.
- Use `backstage-plugin-builder` (`skill`) instead when creating custom Backstage plugins.
- Use `deploy-orchestration` (`skill`) instead when designing or running CI/CD deployment pipelines.

## Progressive disclosure and bundled resources

- `references/devcontainer-templates.md`: Python, Node.js, Terraform, Java, AI/ML, and data pipeline devcontainer templates plus Golden Path mapping.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `backstage-deployment` | `skill` | Registering Golden Paths in a deployed Backstage portal. |
| `backstage-plugin-builder` | `skill` | Building Backstage plugins that consume or extend Golden Paths. |
| `deploy-orchestration` | `skill` | Wiring template outputs into platform deployment workflows. |
| `validation-scripts` | `skill` | Running repository validation after template changes. |
| `backstage-expert` | `agent` | Owning Backstage portal and Golden Path integration work. |
| `open-horizons-engineer` | `agent` | Improving developer platform experience and scaffolder flows. |

## Quality gate

- [ ] The selected Golden Path template type is identified.
- [ ] `.devcontainer/devcontainer.json` requirements are mapped from the reference.
- [ ] Required SDKs, tools, and container features are preserved or validated.
- [ ] The scaffolded repository path and Codespaces entry point are reported.
- [ ] No unsupported template type or tool is invented.
