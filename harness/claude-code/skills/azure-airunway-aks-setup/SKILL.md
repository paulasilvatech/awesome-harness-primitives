---
name: azure-airunway-aks-setup
description: >-
  Set up AI Runway on AKS from a bare cluster to a running model, covering cluster verification,
  controller install, GPU assessment, provider setup, and the first deployment. Use when the user
  asks to set up or install AI Runway, onboard an AKS cluster, run AI Runway setup, deploy a model
  to AKS, enable GPU inference on AKS, configure KAITO on AKS, run an LLM or vLLM on AKS, set up
  model serving on AKS, or work with the AI Runway controller.
argument-hint: "[skip-to-step N]"
license: MIT
metadata:
  author: Microsoft
  version: 1.1.1
---

<!-- Generated from harness/github-copilot/skills/azure-airunway-aks-setup/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure AI Runway AKS Setup

This skill walks users from a bare Kubernetes cluster to a running AI model deployment. Follow each step in sequence unless the user provides `skip-to-step N` to resume from a specific phase.

> **Cost awareness:** GPU node pools incur significant compute charges (A100-80GB can cost $3–5+/hr). Confirm the user understands cost implications before provisioning GPU resources.

## Prerequisites

This skill assumes an AKS cluster already exists. If the user does not have a cluster, hand off to the `azure-kubernetes` skill first to provision one (with a GPU node pool unless CPU-only inference is acceptable), then return here.

## Quick Reference

| Property | Value |
|----------|-------|
| Best for | End-to-end AI Runway onboarding on AKS |
| CLI tools | `kubectl`, `make`, `curl` |
| MCP tools | None |
| Related skills | `azure-kubernetes` (cluster setup), `azure-diagnostics` (troubleshooting) |

## When to invoke

Use this skill when the user wants to:
- Set up AI Runway on an existing AKS cluster from scratch
- Install the AI Runway controller and CRDs
- Assess GPU hardware compatibility for model deployment
- Choose and install an inference provider (KAITO, Dynamo, KubeRay)
- Deploy their first AI model to AKS via AI Runway
- Resume a partially-complete AI Runway setup from a specific step

## MCP Tools

This skill uses no MCP tools. All cluster operations are performed directly via `kubectl` and `make`.

## Rules

1. Execute steps in sequence — load the reference for each step as you reach it
2. Report cluster state at each step: ✓ healthy, ✗ missing/failed
3. Ask for user confirmation before any install or deployment action
4. If a step is already complete, report status and skip to the next step
5. If the user provides `skip-to-step N`, start at step N; assume prior steps are complete

## Steps

| # | Step | Reference |
|---|------|-----------|
| 1 | **Cluster Verification** — context check, node inventory, GPU detection | [step-1-verify.md](references/steps/step-1-verify.md) |
| 2 | **Controller Installation** — CRD + controller deployment | [step-2-controller.md](references/steps/step-2-controller.md) |
| 3 | **GPU Assessment** — detect GPU models, flag dtype/attention constraints | [step-3-gpu.md](references/steps/step-3-gpu.md) |
| 4 | **Provider Setup** — recommend and install inference provider | [step-4-provider.md](references/steps/step-4-provider.md) |
| 5 | **First Deployment** — pick a model, deploy, verify Ready | [step-5-deploy.md](references/steps/step-5-deploy.md) |
| 6 | **Summary** — recap, smoke test, next steps | [step-6-summary.md](references/steps/step-6-summary.md) |

## Error Handling

| Error / Symptom | Likely Cause | Remediation |
|-----------------|--------------|-------------|
| No kubeconfig context | Not connected to a cluster | Run `az aks get-credentials` or equivalent |
| Controller in CrashLoopBackOff | Config or RBAC issue | `kubectl logs -n airunway-system -l control-plane=controller-manager --previous` |
| Provider not ready | Image pull or RBAC issue | `kubectl logs <pod-name> -n <namespace>` for the provider pod |
| ModelDeployment stuck in Pending | GPU scheduling failure or provider not ready | `kubectl describe modeldeployment <name> -n <namespace>` events |
| `bfloat16` errors at inference | T4 or V100 lacks bfloat16 support | Add `--dtype float16` to serving args |

For full error handling and rollback procedures, see [troubleshooting.md](references/troubleshooting.md).

## Output template

```markdown
## AI Runway setup result

**Status:** ready | partial | blocked
**Summary:** <one sentence covering scope and outcome>

### Details
Cluster checks, controller install, GPU capacity, provider config, and first model deployment.

### Validation
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] GPU capacity and quota were confirmed before deployment.
- [ ] The first model responded to a test request.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was performed and its evidence is shown.
- [ ] Irreversible Azure actions were confirmed with the user first.
