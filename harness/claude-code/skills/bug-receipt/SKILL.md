---
name: bug-receipt
description: >-
  Close bugs and incidents with an auditable BUG RECEIPT that states VERIFIED, PARTIAL, or BLOCKED
  based on baseline, root cause, change, proof, gaps, and evidence source. Use when the user asks
  for defect repair, regression proof, production incident closeout, issue closure,
  machine-readable receipt JSON, or CI integration of bug evidence.
---

<!-- Generated from harness/github-copilot/skills/bug-receipt/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Bug receipt

Turn a bug fix, incident investigation, or closure decision into a strict receipt; preserve the observed defect, prove the responsible mechanism and change, then output only the receipt or its validated JSON artifact.

## When to invoke

- "Close this bug with proof."
- "Produce a bug receipt for this incident."
- "Did the fix actually verify the user-visible behavior?"
- "Generate the machine-readable bug receipt JSON."
- "Mark this defect VERIFIED, PARTIAL, or BLOCKED."

## Prerequisites and context

- Use current execution evidence when available; otherwise label evidence as `supplied` or `mixed` and do not imply it was executed now.
- For JSON artifacts, read `references/receipt-contract.md`, start from `assets/receipt.template.json`, and validate with `node scripts/validate-receipt.mjs <receipt.json>` from this skill directory.
- Do not commit a generated receipt unless the user explicitly requests it.

## Evidence boundary

Before editing or closing, record the defect, intended behavior, strongest direct check, and source boundary.

| Field | Required standard | Forbidden shortcut |
| --- | --- | --- |
| Problem | Observed defect plus intended behavior. | A vague issue title with no observable contract. |
| Baseline | Failing interaction or command and decisive result, or explicit `not run`. | Treating an old log as a reproduction executed now. |
| Root cause | Proven mechanism at a concrete location or runtime transition, or explicit `unproven hypothesis`. | Naming a plausible component because the patch touched it. |
| Change | Responsible repair, or `none`. | Listing unrelated cleanup as proof of repair. |
| Proof | Executed or supplied check with every decisive layer. | Passing build, stale log, or source read alone for user-visible behavior. |
| Gaps | `none`, or the exact missing proof and one minimal next experiment/package. | Hiding gaps to make the receipt look verified. |
| Source | `executed now`, `supplied`, or `mixed`. | Blending supplied and executed evidence without labeling it. |

## Trace and repair rules

1. Follow the live owner path from input to symptom.
2. Separate observed facts, bounded inferences, and gaps.
3. Require a concrete code location, configuration setting, request transition, database transition, or runtime handoff before naming root cause.
4. Make the smallest responsible change.
5. Avoid unrelated cleanup, retries, silent fallbacks, and fixture-specific exceptions.
6. Do not convert a plausible patch, stale log, source read, or passing build into proof of user-visible behavior.

## Direct proof boundaries

| Surface | Required direct proof |
| --- | --- |
| Logic or failing test | Original failing input or focused regression test now passes. |
| UI behavior | Real interaction plus relevant console and network observation. |
| API or integration | Request, response, and responsible service behavior. |
| Persistence | Write/read or reload round trip through the real owner path. |
| Race or lifecycle | Repeated concurrent trigger; zero-or-one success; affected-row and transaction evidence; final invariant. |
| Cross-system blocker | One sanitized failing request/response with timestamp or request ID, edge and application logs, and identity-provider logs when the trace reaches that owner. |

## Cross-system evidence package

When the trace reaches an identity provider, include sanitized identity-provider or `identity-pro` evidence with the request ID, edge log, application log, and timestamp. The receipt may stay `PARTIAL` or `BLOCKED` until that correlated package is available.
## Status assignment

| Status | Use only when | Required gap language |
| --- | --- | --- |
| `VERIFIED` | Baseline observed, concrete cause proven, responsible change made, all declared checks passed, and no material gap remains. | `Gaps       none` |
| `PARTIAL` | Useful evidence exists, but a required proof layer is missing or inconclusive. | Name the single minimal experiment or correlated evidence package that closes the gap. |
| `BLOCKED` | A specific external condition prevents reproduction, repair, or proof. | Name the external blocker and the smallest evidence package needed to unblock. |

## Progressive disclosure and bundled resources

| Resource | Use when | Contract |
| --- | --- | --- |
| `references/receipt-contract.md` | Machine-readable receipt, CI integration, or status invariants are requested | Follow the JSON fields and status invariants exactly. |
| `references/receipt.schema.json` | Validating or explaining JSON structure | Treat as the schema source of truth. |
| `assets/receipt.template.json` | Creating a JSON artifact | Copy to a task-owned path, fill the fields, then validate. |
| `scripts/validate-receipt.mjs` | Checking a JSON receipt | Run `node scripts/validate-receipt.mjs <receipt.json>` from the skill directory. |

## Gotchas

- **Return the complete receipt as the entire user-facing result**: concision shortens field values; it never removes or renames rows.
- **Use explicit placeholders**: write `not run`, `unproven`, or `none`; do not omit a row.
- **Do not overclaim**: supplied evidence stays supplied, and source reads are not behavioral proof.
- **One gap only**: for `PARTIAL` or `BLOCKED`, name the decisive next experiment or evidence package, not a generic task list.

## Output template

```markdown
BUG RECEIPT · VERIFIED | PARTIAL | BLOCKED

Problem    <observed defect and intended behavior>
Baseline   <failing interaction or command and decisive result; or not run>
Root cause <proven mechanism; or unproven hypothesis>
Change     <responsible change; or none>
Proof      <supplied or executed check: result; include every decisive layer>
Gaps       <none; or exact missing proof and single next experiment/package>
Source     executed now | supplied | mixed
```

## Quality gate

- [ ] The final user-facing result is the complete BUG RECEIPT and no prose replaces it.
- [ ] Status is exactly `VERIFIED`, `PARTIAL`, or `BLOCKED` and matches the evidence standard.
- [ ] `Problem`, `Baseline`, `Root cause`, `Change`, `Proof`, `Gaps`, and `Source` rows are present and not renamed.
- [ ] The proof includes every decisive layer for the affected surface or names the missing layer as the gap.
- [ ] Supplied evidence, executed evidence, and mixed evidence are labeled honestly.
- [ ] JSON artifacts, when requested, were created from `assets/receipt.template.json` and validated with `node scripts/validate-receipt.mjs <receipt.json>`.

## References

- [Original bug-receipt repository](https://github.com/lMysticl/bug-receipt)
