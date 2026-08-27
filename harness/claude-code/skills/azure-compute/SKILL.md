---
name: azure-compute
description: >-
  Route Azure virtual machine and scale set work, including size and image selection, pricing
  comparison, autoscale and orchestration modes, capacity reservation groups, and Essential
  Machine Management. Use when the user asks to create, provision, deploy, or spin up a VM,
  recommend a VM size or family, compare VM pricing, work with VMSS, scale sets, autoscale,
  burstable or GPU sizes, plan HPC, machine learning, or dev/test workloads, estimate compute
  cost, or reserve and guarantee capacity.
license: MIT
metadata:
  author: Microsoft
  version: 2.5.1
---

<!-- Generated from harness/github-copilot/skills/azure-compute/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Compute Skill

Routes Azure VM and Virtual Machine Scale Set (VMSS) requests to the right workflow.

## When to invoke

- User wants to **recommend, compare, or price** a VM or VMSS
- User wants to **create, provision, or deploy** a VM or VMSS
- User asks about **Capacity Reservation Groups** (CRG) — reserve, guarantee capacity, pre-provision
- User asks about **Essential Machine Management** (EMM) — machine enrollment, monitor

**Disambiguate with `azure-prepare`:** if the user wants to deploy an **application** (Docker service, web app, API, serverless workload), route to `azure-prepare`. `vm-creator` is for **bare VM/VMSS infrastructure** only.

## Routing

**Mandatory workflow-first routing:** never route directly to `references/*` files. First classify the user intent below, open the matched workflow file, then load only the reference files that workflow requests. Reference files are supporting material, not entry points. If the intent is unclear, ask a clarifying question to disambiguate between the workflows.

| Workflow | File | Use when |
|---|---|---|
| **VM Recommender** | [vm-recommender.md](workflows/vm-recommender/vm-recommender.md) | User asks which VM/VMSS to choose, whether to use VMSS/autoscaling, wants pricing, or wants to compare options |
| **VM Creator** | [vm-creator.md](workflows/vm-creator/vm-creator.md) | User wants to create, provision, or deploy a bare VM or VMSS (not an app deployment) |
| **Capacity Reservation** | [capacity-reservation.md](workflows/capacity-reservation/capacity-reservation.md) | User needs to reserve / guarantee VM capacity (CRG create / associate / disassociate) |
| **Essential Machine Management** | [essential-machine-management.md](workflows/essential-machine-management/essential-machine-management.md) | User asks about EMM / machine enrollment / monitor |

## Output template

```markdown
## Compute recommendation result

**Status:** recommended | provisioned | blocked
**Summary:** <one sentence covering scope and outcome>

### Details
VM or scale set size, image, orchestration mode, and cost basis.

### Validation
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] Size and image availability were confirmed for the target region.
- [ ] Quota was checked before recommending provisioning.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was performed and its evidence is shown.
- [ ] Irreversible Azure actions were confirmed with the user first.
