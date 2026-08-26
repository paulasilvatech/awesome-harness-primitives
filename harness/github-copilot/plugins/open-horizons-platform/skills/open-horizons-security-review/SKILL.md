---
name: open-horizons-security-review
description: >-
  Performs an independent, read-only security review of one Open Horizons change or surface with severity-ranked, evidence-backed findings and verification criteria. Use when reviewing code, Terraform, Kubernetes, identity, workflows, Backstage, MAF agents, MCP tools, secrets, or policy review.
---

# Open Horizons security review

Review one bounded scope without implementing remediation or approving risk.

## When to invoke

- Review a proposed or completed Open Horizons change independently.
- Validate Terraform, Kubernetes, workflow, identity, auth, API, MCP, or agent-tool controls.
- Triage scanner findings or verify a claimed remediation.
- Assess trust boundaries, external input, sensitive data, secrets, or privileged operations.

## Prerequisites and context

Require exact scope, expected security properties, applicable policies, severity threshold, and
available evidence. Use read-only live access only when repository evidence cannot answer the
bounded question and authorization is explicit.

## Criteria

Review applicable dimensions:

| Dimension | Evidence to seek |
| --- | --- |
| Identity and authorization | Principal, scope, least privilege, separation of duties, default deny |
| Inputs and tools | Validation, prompt/tool argument filtering, injection resistance, rate limits |
| Secrets and data | References instead of values, classification, tenant isolation, retention |
| Terraform and cloud | Private access, encryption, state safety, policy, identities, drift |
| Kubernetes | Non-root, resources, probes, network policy, secret references, pinned images |
| GitHub and CI/CD | Minimal permissions, pinned actions, OIDC, protected environments, supply chain |
| Agent governance | Tool allowlist, approval gates, bounded loops, fail closed, metadata-only audit |

Assign severity from demonstrated impact and exploitability. Mark insufficient evidence as a
hypothesis, not a confirmed finding.

## Procedure

1. Freeze the review boundary and expected controls.
2. Inspect the diff and owning artifacts before broad scanning.
3. Trace trust boundaries, identities, sensitive data, external input, and privileged operations.
4. Run only read-only checks relevant to the scope and redact sensitive output.
5. Challenge each candidate finding with counter-evidence and avoid duplicate root causes.
6. Report findings with location, evidence, impact, remediation requirement, owner, and verification.
7. On re-review, test the original finding; do not implement the fix or approve exceptions.

## Output template

```markdown
## Security review result

**Status:** PASS | FINDINGS | BLOCKED
**Scope:** <bounded scope>

### Findings
| Severity | Finding | Location | Evidence | Impact | Owner | Verification |
| --- | --- | --- | --- | --- | --- | --- |

### Assumptions and gaps
- <hypothesis, missing evidence, or none>
```

## Limits

- Do not edit remediation, mutate access or policy, suppress alerts, expose secret values, accept
  risk, or deploy.
- Do not claim compliance from configuration intent alone.
- Do not combine unrelated findings into one broad recommendation.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-security-reviewer` | `agent` | An independent reviewer should execute this method. |
| `agent-safety` | `instructions` | The scope contains agents, tools, policies, or orchestration. |
| `test-coverage` | `skill` | Security remediation requires regression coverage evidence. |
| `open-horizons-deployment-operator` | `agent` | Verified remediation is ready for approved execution. |

## Quality gate

- [ ] Scope and expected controls are explicit.
- [ ] Findings have reproducible evidence and severity rationale.
- [ ] Hypotheses are separated from confirmed findings.
- [ ] No source, policy, or live state was modified.
- [ ] Every finding has an owner and independent verification criterion.