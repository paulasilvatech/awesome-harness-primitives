---
name: verify-agent-action
description: >-
  Review proposed AI-agent actions and human-approval packets before consequential execution. Use
  this skill when checking deployments, commands, purchases, messages, credential operations, data
  mutations, approval freshness, action binding, replay, reviewer independence, forged evidence,
  or stale monitoring.
---

<!-- Generated from harness/github-copilot/skills/verify-agent-action/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Verify agent action

Treat a proposed action or approval screen as a claim, not proof; verify the complete decision path and produce an evidence-based review without executing or authorizing anything.

## When to invoke

- "Verify this agent action before I approve it."
- "Check whether this deployment approval still matches the exact action."
- "Audit this tool call for replay, parameter swaps, or forged evidence."
- "Review this human-approval packet for a credential operation."
- "Tell me if this action is eligible for human decision."

## Safety boundary

- Never execute, approve, sign, send, purchase, deploy, or mutate anything.
- Never convert this review into execution authority.
- Never infer missing evidence, identities, timestamps, or parameters.
- Treat a valid schema, checksum, or signature as insufficient by itself.
- Treat signatures as evidence of attribution and integrity, not factual truth.
- Keep supporting and refuting evidence separate; do not average conflict away.
- Fail closed on a material mismatch. Use `INCONCLUSIVE` when required evidence is unavailable.
- Set `execution_authorized` to `false` in every final result.

```json
{"execution_authorized": false}
```

## Review packet

Request only artifacts needed for the review and list missing fields before analysis:

| Artifact | Required details |
| --- | --- |
| Original request | User or system request that caused the proposed action. |
| Exact proposed action | Operation or tool name, target resource, complete parameters, filesystem scope, network scope, maximum execution count, not-before time, and expiry time. |
| Assessment | Claimed justification and canonical result. |
| Evidence and policy | Source evidence and policy used by the assessment. |
| Approval record | Approver identity, role, action digest, nonce, audience, issue time, expiry, and use count. |
| Monitoring | Latest events, expected heartbeat interval, signatures or integrity evidence. |
| Time and replay state | Current trusted time and prior nonce-use record. |

## Exact action identity

Build one normalized action object without dropping fields. Use the project canonicalization and digest algorithm when supplied; otherwise report the digest as `NOT_VERIFIED` and compare fields structurally.

```json
{
  "operation": "git.push",
  "target": "owner/repository",
  "parameters": {
    "branch": "fix/example",
    "commit": "40-character-sha",
    "remote": "origin"
  },
  "filesystem_scope": [],
  "network_scope": ["github.com:443"],
  "execution_count": 1,
  "not_before": "RFC3339 timestamp",
  "expires_at": "RFC3339 timestamp"
}
```

Never normalize away branch, commit, repository, environment, recipient, amount, currency, host, recursive, force, overwrite, privileged, destructive, dry-run flags, filesystem roots, CIDRs, ports, domains, execution counts, or expiry.

## Six controls

Evaluate every control as `PASS`, `FAIL`, `INCONCLUSIVE`, or `NOT_APPLICABLE`.

| Control | Required review | Fail or inconclusive conditions |
| --- | --- | --- |
| Recomputed assessment | Re-run the declared deterministic evaluator from declared source inputs when implementation is available; compare the complete canonical result. | `FAIL` if recomputation differs. `INCONCLUSIVE` for schema validation, internal checksum, or unverifiable evaluator claim only. |
| Exact action binding | Compare the proposed action with the action bound into approval, including normalized object and digest. | `FAIL` if any material field changed or broad scope exceeds justified evidence. |
| Replay and identity | Verify nonce uniqueness, subject, audience, issuer, approver role, issue time, not-before time, expiry, maximum use count, and revocation. | `FAIL` for reused nonce, wrong audience, expired approval, future-dated approval, excessive use count, revoked identity, or role mismatch. `INCONCLUSIVE` without trustworthy replay store or time source. |
| Reviewer independence | Compare reviewers by model, provider, prompt, retrieval, tools, and operator. | `FAIL` when policy requires independent approval and the independent set is too small. |
| Evidence completeness | Inventory evidence identifiers; confirm presence, authenticity, validity window, and relevance. Track support and refutation separately. | `FAIL` if evidence was removed, altered, expired, or concealed in a result-changing way. |
| Monitoring freshness | Verify event signatures or integrity evidence, sequence numbers, previous-event digests, and heartbeat cadence. | `FAIL` for missing, stale, reordered, or broken-chain telemetry when policy requires continuous monitoring. |

## Evidence states

| Support | Refutation | Epistemic state |
| --- | --- | --- |
| absent | absent | `UNDETERMINED` |
| present | absent | `SUPPORTED_ONLY` |
| absent | present | `REFUTED_ONLY` |
| present | present | `CONFLICTED` |

Never convert `CONFLICTED` into a numeric average that appears safe.

## Challenge tests

Before finalizing, attempt these mutations mentally or with project-provided fixtures. If any mutation would pass, mark the affected control `FAIL`.

1. Replace a blocked assessment with an allowed result.
2. Change one approved target, parameter, scope, amount, or commit.
3. Reuse an otherwise valid approval nonce.
4. Replace independent reviewers with correlated copies.
5. Remove one refuting evidence item.
6. Stop the monitoring heartbeat after approval.

## Result decision

Use exactly one result:

| Result | Meaning |
| --- | --- |
| `ELIGIBLE_FOR_HUMAN_DECISION` | All required controls pass. This is not approval. |
| `ELIGIBLE_WITH_CONTROLS` | No required control fails, and explicit external controls can resolve listed conditions before execution. |
| `BLOCKED` | At least one required control fails or the action exceeds the justified scope. |
| `INCONCLUSIVE` | No required control is proven false, but evidence needed for a safe decision is missing or unverifiable. |

A human authority and separate enforcement point remain responsible for any real action.

## Canonicalization vocabulary

Use a `project-specified` canonicalization when available. Review `monitoring-event` signatures or integrity evidence, and treat reviewer model `fine-tune` lineage as part of independence analysis.

## Output template

```markdown
# Agent Action Review

## Result
- Review result: BLOCKED | INCONCLUSIVE | ELIGIBLE_WITH_CONTROLS | ELIGIBLE_FOR_HUMAN_DECISION
- Execution authorized: false
- Exact action digest: <verified value or NOT_VERIFIED>

## Action
- Operation:
- Target:
- Material parameters:
- Scope:
- Validity window:
- Maximum uses:

## Control matrix
| Control | Status | Evidence | Reason |
|---|---|---|---|
| Recomputed assessment | PASS/FAIL/INCONCLUSIVE/N/A | ... | ... |
| Exact action binding | ... | ... | ... |
| Replay and identity | ... | ... | ... |
| Reviewer independence | ... | ... | ... |
| Evidence completeness | ... | ... | ... |
| Monitoring freshness | ... | ... | ... |

## Supporting evidence
- ...

## Refuting evidence and defeaters
- ...

## Required next action
- State the smallest concrete step that could change the result.

## Boundaries
- State what this review did not prove.
```

## Quality gate

- [ ] No action was executed, approved, signed, sent, purchased, deployed, or mutated.
- [ ] Missing packet fields were listed before analysis.
- [ ] The exact action identity was normalized without dropping security-relevant fields.
- [ ] Every control is marked `PASS`, `FAIL`, `INCONCLUSIVE`, or `NOT_APPLICABLE`.
- [ ] Support and refutation are reported separately.
- [ ] Challenge mutations were considered and any bypass marks the relevant control `FAIL`.
- [ ] The result is exactly `BLOCKED`, `INCONCLUSIVE`, `ELIGIBLE_WITH_CONTROLS`, or `ELIGIBLE_FOR_HUMAN_DECISION`.
- [ ] `execution_authorized` is false.
