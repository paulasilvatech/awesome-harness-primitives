---
name: open-horizons-deployment-operation
description: >-
  Executes one approval-gated Open Horizons deployment, rollout, rollback, or verification from an immutable change package. Use when the exact environment, artifact, command, expected actions, approval, validation, and rollback are already known.
---

# Open Horizons deployment operation

Execute one supplied live operation without acquiring planning, implementation, review, or repair authority.

## When to invoke

- Execute an approved Terraform saved plan.
- Run an approved Open Horizons rollout or rollback.
- Run an approved deployment dry run or immediate verification.
- Resume a previously approved operation after revalidating its immutable package.

## Prerequisites and context

The package must identify repository and ref, target environment, artifact path and digest, expected
actions, exact command, approval evidence, validation command, rollback command, and change window.
Authentication must already be configured for the approved operator identity.

## Procedure

1. Confirm the package is complete and approval applies to the exact artifact and command.
2. Verify repository ref, clean or approved working-tree state, environment, subscription, tenant,
   cluster, namespace, artifact digest, and expected action summary.
3. Run repository prerequisite and configuration checks plus the approved dry run or plan inspection.
4. Stop on drift, unexpected actions, stale approval, missing rollback, or failed validation.
5. Present the exact mutating command, expected impact, and rollback immediately before execution.
6. Obtain explicit confirmation for that command and execute it once without substitution or repair.
7. Run the approved immediate verification and record sanitized identifiers, timestamps, and status.
8. Report `PASS`, `ROLLBACK-REQUIRED`, or `BLOCKED`; return defects to their owning agent.

## Criteria

| Decision | Required result |
| --- | --- |
| Execute | Package, context, digest, expected actions, approval, and rollback all match |
| Stop | Any ambiguity, drift, policy denial, validation failure, or unexpected action |
| Roll back | Approved rollback trigger is met and the exact rollback command is authorized |
| Escalate | Implementation, security, readiness, or reliability defect requires another owner |

## Output template

```markdown
## Deployment operation result

**Status:** PASS | BLOCKED | ROLLBACK-REQUIRED
**Environment:** <environment>
**Operation:** <dry-run | apply | rollout | rollback | verify>
**Artifact:** <path/ref and digest>

### Evidence
| Check | Result | Sanitized evidence |
| --- | --- | --- |

### Execution
- Approved command: `<exact command or not run>`
- Approval: <evidence or missing>
- Immediate verification: <result>
- Rollback status: <not required | ready | executed | blocked>

### Follow-up
- <owner and blocker or none>
```

## Limits

- Do not author, edit, generate, or replace source, plans, manifests, configuration, or approvals.
- Do not infer approval from tests, labels, plans, dry runs, or previous conversations.
- Do not execute destroy, delete, public exposure, quota, paid-service, or identity changes unless
  the exact operation and rollback are explicitly approved.
- Do not troubleshoot by changing the deployment package during execution.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-deployment-operator` | `agent` | One approved live operation should execute this procedure. |
| `prerequisites` | `skill` | Local tool and authentication prerequisites need validation. |
| `validation-scripts` | `skill` | Repository-owned validation commands apply to the package. |
| `open-horizons-sre-investigator` | `agent` | Independent post-operation diagnosis is required. |

## Quality gate

- [ ] Artifact identity and expected actions are immutable and verified.
- [ ] Live context matches the approved environment.
- [ ] A mutating command has immediate explicit approval.
- [ ] No source or package content changed during execution.
- [ ] Verification, rollback status, and sanitized evidence are recorded.