---
name: "deploy-platform"
description: "Execute one approval-gated Open Horizons operation from an immutable artifact and exact commands."
argument-hint: "ref=<git-ref> artifact=<path> digest=<sha256> command=<exact-command>"
agent: "open-horizons-deployment-operator"
tools: ["read", "search", "execute"]
---

# Deploy platform

## Objective

Execute exactly one supplied deployment, dry run, rollout, rollback, or verification without
editing source.

## When to Invoke

Use only after the reviewed operation package and required approvals exist.

## Preconditions

Every required input below is exact, current, and applies to the same immutable package. If any
input is missing, inconsistent, stale, or unverifiable, return `BLOCKED` without execution.

## Inputs the Team Must Provide

- Repository and exact ref: `${input:repository_ref}`.
- Environment and operation: `${input:environment_operation}`.
- Artifact path and digest: `${input:artifact}` and `${input:digest}`.
- Expected actions: `${input:expected_actions}`.
- Exact execution command: `${input:command}`.
- Exact validation command: `${input:validation}`.
- Exact rollback command and trigger: `${input:rollback}`.
- Approval evidence and change window: `${input:approval}`.

## What I Will Do

- Invoke the `open-horizons-deployment-operation` skill.
- Verify the supplied package and live context without substituting artifacts or commands.
- For a mutating operation, present the exact command, impact, and rollback and obtain immediate
  explicit approval before executing it once.
- Run the exact validation command and report sanitized evidence.

## What I Will NOT Do

- Edit source, generate or repair an artifact, choose a replacement command, or infer approval.
- Continue after drift, failed preflight, unexpected actions, or missing rollback.
- Print credentials or unsanitized sensitive output.

## Output Format

Chat response only:

```markdown
## Deployment operation result
**Status:** PASS | BLOCKED | ROLLBACK-REQUIRED
**Package:** <ref, artifact, digest, environment, operation>
- Approval: <verified evidence or missing>
- Execution: <exact command and sanitized result, or not run>
- Validation: <exact command and result>
- Rollback: <ready, executed, or blocked>
- Follow-up owner: <owner or none>
```

## Definition of Done

- [ ] Ref, artifact digest, expected actions, and live context match.
- [ ] Any mutation received immediate explicit approval for the exact command.
- [ ] Only the supplied command ran, followed by the supplied validation.
- [ ] No source file changed and rollback status is explicit.

## Prompt Body

Have `open-horizons-deployment-operator` invoke `open-horizons-deployment-operation` with exactly
the supplied inputs. Stop on any mismatch. For mutation, request immediate approval for
`${input:command}` before execution. Never edit source or improvise a repair.

## Invocation Example

Run **Chat: Run Prompt**, select `deploy-platform`, and provide the exact repository ref,
environment/operation, artifact path and digest, expected actions, execution command, validation
command, rollback command/trigger, approval evidence, and change window.
