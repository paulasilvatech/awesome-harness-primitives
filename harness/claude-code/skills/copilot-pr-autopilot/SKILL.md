---
name: copilot-pr-autopilot
description: >-
  Run a GitHub Copilot Code Review loop on a pull request: request review with GraphQL, wait, list
  open Copilot/human/advanced-security threads, triage fix/decline/escalate, dispatch bounded
  fixes, build/test/lint, commit per iteration, reply and resolve, then re-trigger until HEAD is
  reviewed and no threads await the agent. Use for address copilot comments, run a copilot review
  loop, fix this PR, or iterate on copilot feedback.
---

<!-- Generated from harness/github-copilot/skills/copilot-pr-autopilot/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Copilot PR autopilot

Drive a pull request through repeated GitHub Copilot review rounds until every loop-owned thread has a fix acknowledgement, decline rationale, or explicit hand-off, with one focused commit per round and proof that HEAD was reviewed.

## When to invoke

- "Address Copilot comments on this PR."
- "Run a Copilot review loop."
- "Fix this PR based on Copilot feedback."
- "Request Copilot review and iterate until clean."
- "Triage all open review threads."

## Prerequisites and context

- `gh` CLI must be installed and authenticated. Every script dot-sources `scripts/_lib.ps1`, which runs `Assert-GhReady` and halts before work if `gh` is missing or `gh auth status` fails.
- PowerShell must be on PATH: Windows PowerShell 5.1+ (`powershell.exe`) or PowerShell 7+ (`pwsh`).
- Full multi-round autopilot requires Triage or Write permission on the target repo because GitHub's public API for adding the Copilot bot reviewer through GraphQL `requestReviewsByLogin` is permission-gated.
- If `scripts/01-request-review.ps1` fails because GitHub Copilot Code Review is unavailable, run a single iteration over existing human, advanced-security, or other bot threads by skipping trigger and wait.

| Actor | What works |
| --- | --- |
| Repo collaborator with Triage / Write | Full loop: `01` triggers Copilot, `02` waits, `04`–`08` triage, fix, reply, then loop. |
| External PR author without write permission | `01` errors. Use `-SingleIteration`, address current findings once, then ask the maintainer to trigger review in the UI or push a substantive commit to fire `synchronize`. |

In single-iteration mode, `Converged: true` means `OpenThreadsAwaitingReply == 0`; maintainer-side re-trigger drives later rounds.

## Procedure

1. **Request review** with `scripts/01-request-review.ps1`, following `references/01-request-review.md`.
2. **Wait for review** with the 20-minute cap in `references/02-wait.md`.
3. **List and categorize open threads** with `references/03-list-threads.md` and `scripts/03-list-open-threads.ps1`.
4. **Triage** each batch with `references/04-triage.md`: fix, decline, or escalate-to-user.
5. **Fix** with parallel bounded sub-agents as allowed by `references/05-fix.md`.
6. **Build, test, and lint** using repository conventions from `CONTRIBUTING`, `AGENTS`, `README`, `package.json`, or `Makefile`, following `references/06-build-test.md`.
7. **Commit and push** one focused commit per round using `references/07-commit-push.md`.
8. **Reply and resolve** with `references/08-reply-resolve.md` and `scripts/08-reply-and-resolve.ps1`; use `-NoResolve` for escalate-to-user hand-offs.
9. **Verify convergence** with `references/09-convergence.md` and `scripts/02-check-review-status.ps1`.
10. If `Converged: false`, loop back to step 1. If `Converged: true`, run cleanup once with `references/10-cleanup.md` and `scripts/10-cleanup-outdated.ps1`.

At every 10th round, run the round-cap recap gate in `references/09-convergence.md#round-cap--recap-gate-circuit-breaker`. Recap all prior rounds against the PR's original scope and choose `CONTINUE`, `REVERT-AND-SHIP`, or `HAND-OFF`.

## Loop ownership rules

| Thread type | Default disposition |
| --- | --- |
| GitHub Copilot thread | Loop-owned: fix or decline, then reply and resolve when disposition is complete. |
| Human reviewer thread | Default to `escalate-to-user`; reply with analysis and leave open unless the user explicitly owns resolution. |
| `github-advanced-security` thread | Default to `escalate-to-user` unless a safe fix is clearly in scope. |
| Design tradeoff | Decline with rationale or hand off; do not over-engineer to satisfy speculative feedback. |
| Outdated unresolved thread | Still reply and resolve if loop-owned; unresolved state is source of truth. |

Convergence requires HEAD-match, zero-awaiting, and at-HEAD review. Print proof fields such as `HeadOid`, `LatestCopilotReview.commitOid`, and `submittedAt` in the completion message. Do not call `task_complete` before `Converged: true`.

## Gotchas

- **Reply to every open thread**: resolve only `fix` and `decline` dispositions; leave `escalate-to-user` open with `08-reply-and-resolve.ps1 -NoResolve`.
- **One focused commit per round**: bundling rounds destroys the audit trail and hurts `git bisect`.
- **Use the repo's own build/test/lint commands**: do not invent tooling.
- **Trust bundled scripts for invariants**: `copilot_work_started` event id, `Converged`, HEAD match, zero-awaiting, at-HEAD review, single-iteration fallback, and PR-state guard are enforced there.
- **Read `references/api-quirks.md` before modifying scripts**: it documents `gh api graphql -F` type coercion, `git stash push -m` positional parsing, and the three GraphQL reviewer mutation traps.

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| `prerequisite missing — gh CLI is not on PATH` | Install `gh` from `https://cli.github.com` or with `winget install GitHub.cli` on Windows and `brew install gh` on macOS; then run `gh auth login`. Surface the script message and stop. |
| `prerequisite missing — gh CLI is not authenticated` | Run `gh auth login`; stop until complete. |
| Trigger fails or no `copilot_work_started` event lands | Push a substantive non-whitespace commit; persistent failure may mean Copilot Code Review is disabled in repo settings or account-level Copilot Pro/Pro+. |
| No new review after about 10 minutes | Quiet period or trivial-diff suppression. Push a substantive commit and retry; do not blindly rerun `01-request-review.ps1` while it reports `InFlight`. |
| Outdated unresolved threads appear | Expected; unresolved state is source of truth. Reply and resolve loop-owned items, then let `10-cleanup-outdated.ps1` run only as final safety net. |
| Unsure fix vs decline | Use `references/04-triage.md`. |
| Need reply phrasing | Use `templates/reply-fix.md`, `templates/reply-decline.md`, `templates/reply-drift.md`, or `templates/reply-partial.md`. |

## Progressive disclosure and bundled resources

- `references/orchestration.md`: time-boxing, extension protocol, sub-agent map, single-iteration fallback, and loop-wide notes.
- `references/01-request-review.md` through `references/10-cleanup.md`: per-step contracts for request, wait, list, triage, fix, build-test, commit-push, reply-resolve, convergence, and cleanup.
- `references/api-quirks.md`: GitHub API behavior and GraphQL traps.
- `templates/reply-fix.md`, `templates/reply-decline.md`, `templates/reply-drift.md`, `templates/reply-partial.md`: reply templates.
- `scripts/_lib.ps1`: `Invoke-Gh`, `Invoke-GhGraphQL`, `Resolve-RepoCoords`, and `Assert-GhReady`.
- `scripts/01-request-review.ps1`: trigger Copilot review and verify pickup.
- `scripts/02-check-review-status.ps1`: snapshot review state; emits `Converged: true` only when all conditions hold.
- `scripts/03-list-open-threads.ps1`: unresolved PR review threads from all reviewers.
- `scripts/08-reply-and-resolve.ps1`: post a reply and resolve in one call.
- `scripts/10-cleanup-outdated.ps1`: final outdated Copilot thread safety net.

<!-- Baseline technical terms preserved for loss check: `MORE`, `NN-*.md`, `OPEN`, `REST`, `STOP`, `Triage/Write`, `accepted-fix`, `anti-patterns`, `auto-assign`, `auto-detect`, `auto-triggers`, `bot-review`, `but-unresolved`, `cross-cutting`, `dead-ends`, `decline-with-rationale`, `declined-with-rationale`, `dot-sourced`, `fix-acknowledgement`, `fix-vs-decline`, `follow-up`, `in-scope`, `one-time`, `other-bot`, `post-convergence`, `re-check`, `re-derive`, `re-request`, `re-run`, `re-triggers`, `reply-guidance`, `round-over-round`, `single-shot`, `substantive-commit`, `test-plan`, `type-coercion` -->

## Output template

```markdown
### Copilot PR autopilot result

**Status:** converged | single-iteration complete | hand-off | blocked
**PR:** <owner/repo#number>
**Rounds:** <count>
**HeadOid:** `<sha>`
**LatestCopilotReview.commitOid:** `<sha or none>`
**submittedAt:** `<timestamp or none>`

| Round | Threads triaged | Fixed | Declined | Escalated | Commit | Validation |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| <n> | <count> | <count> | <count> | <count> | `<sha>` | <build/test/lint result> |

**OpenThreadsAwaitingReply:** <count>
**Converged:** true | false
**Remaining open hand-offs:** <human/design/security threads or none>
```

## Quality gate

- [ ] `gh` and authentication prerequisites were checked by `Assert-GhReady`.
- [ ] Full loop used only when the actor had Triage or Write permission; otherwise single-iteration mode was used.
- [ ] Every open thread was categorized as fix, decline, or escalate-to-user.
- [ ] Every loop-owned thread received a reply and was resolved only when appropriate.
- [ ] Build/test/lint followed repository conventions.
- [ ] Each round produced one focused commit or documented why no commit was needed.
- [ ] The 10th-round recap gate ran on rounds 10, 20, 30, and so on.
- [ ] Completion included `HeadOid`, `LatestCopilotReview.commitOid`, `submittedAt`, and `Converged: true` proof.

## References

- [GitHub CLI](https://cli.github.com)
