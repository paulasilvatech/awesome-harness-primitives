---
name: threat-model-analyst
description: >-
  Produce full or incremental STRIDE-A threat models for repositories and systems, including architecture overviews, DFD diagrams, findings, STRIDE heatmaps, and executive assessment. Use when the user asks to threat model a repo, refresh an existing threat-model-* report, compare commits or reports, identify trust boundary risks, or map findings to CVSS 4.0, CWE, and OWASP.
---

# Threat model analyst

Analyze a repository, system, commit range, or previous report; transform code and architecture evidence into a STRIDE-A security model; output a standalone threat-model folder with diagrams, inventory, findings, and verification artifacts.

## When to invoke

- "Run a threat model for this repository."
- "Refresh the threat model using the latest commit."
- "What changed security-wise since the last threat model?"
- "Compare these two threat-model reports."
- "Generate STRIDE-A findings with CVSS 4.0 and CWE mappings."

## Prerequisites and context

- Use this skill only when the user explicitly requests threat modeling, incremental threat model updates, report comparison, or `/threat-model-analyst` behavior.
- A full analysis can start from repository source alone; an incremental analysis needs a prior `threat-model-*` folder with `threat-inventory.json` or an explicitly supplied baseline report plus target commit or HEAD.
- Read the matching bundled orchestrator before doing substantive analysis; the orchestrators carry the mandatory workflow, sub-agent governance, verification rules, and output skeleton requirements.

## Mode selection

| User request or evidence | Mode | Required resource | Result |
| --- | --- | --- | --- |
| "update", "refresh", "re-run", "incremental", "what changed", "since last analysis" plus a `threat-model-*` baseline | Incremental mode | `references/incremental-orchestrator.md` | Reuse the old report skeleton, verify every old item against current code, discover new items, and emit status annotations for new, resolved, and still-present threats. |
| Explicit baseline folder plus target commit or HEAD | Incremental mode | `references/incremental-orchestrator.md` | Compare baseline evidence with the target revision and produce an updated report with embedded HTML comparison. |
| Compare two commits or two reports | Incremental mode | `references/incremental-orchestrator.md` | Treat the older report or commit as baseline and the newer state as target. |
| Analyze a repo, generate a DFD, perform STRIDE-A, validate controls, identify trust boundaries | Single analysis mode | `references/orchestrator.md` | Execute the complete 10-step workflow and create architecture, DFD, STRIDE-A, prioritized findings, and executive assessment outputs. |

## STRIDE-A analysis map

| Area | Inspect | Evidence standard |
| --- | --- | --- |
| Spoofing | Authentication entry points, session creation, identity propagation, service-to-service credentials | Show the live owner path and the exact boundary where identity is asserted or trusted. |
| Tampering | Request validation, persistence writes, queues, deserialization, infrastructure mutation | Prove whether integrity controls exist before flagging a write path. |
| Repudiation | Audit logs, actor attribution, request IDs, immutable event trails | Distinguish absent evidence from weak evidence; do not infer auditability from generic logging. |
| Information disclosure | Secrets, tokens, PII, debug output, storage policies, cross-tenant data flows | Verify the data class, exposure route, and trust boundary. |
| Denial of service | Rate limits, pagination, expensive queries, fan-out, retries, queue backpressure | Tie the risk to an externally triggerable path or operational limit. |
| Elevation of privilege | Authorization checks, admin paths, object-level access, role transitions | Require code or configuration evidence for both the caller role and protected action. |
| Abuse | Business-logic misuse, workflow bypass, fraud paths, unsafe automation | Model the malicious but protocol-valid user, not only broken inputs. |

## Report artifacts

| Artifact | Use | Required content |
| --- | --- | --- |
| `0.1-architecture.md` | Architecture overview | Components, trust boundaries, entry points, data stores, assumptions, and Mermaid architecture diagrams. |
| `1-threatmodel.md` | Threat inventory | DFD elements, data flows, STRIDE-A threats, mitigations, and open questions. |
| `2-stride-analysis.md` | STRIDE heatmap | Component-by-component and flow-by-flow STRIDE-A coverage with severity rationale. |
| `3-findings.md` | Prioritized findings | Exploit path, affected assets, evidence, likelihood, impact, CVSS 4.0, CWE, OWASP, and remediation. |
| `0-assessment.md` | Executive assessment | Security posture, critical decisions, residual risk, and recommended next steps. |
| `threat-inventory.json` | Incremental baseline | Stable identifiers, current status, evidence anchors, and comparison-ready metadata. |

## Progressive disclosure and bundled resources

Read only the resource needed for the current phase, then follow it exactly.

| Resource | Read when | Contains |
| --- | --- | --- |
| `references/orchestrator.md` | Starting any single analysis | Complete 10-step workflow, 34 mandatory rules, tool usage, sub-agent governance, and verification process. |
| `references/incremental-orchestrator.md` | Updating, refreshing, re-running, or comparing reports or commits | Baseline loading, old skeleton inheritance, change detection, status annotations, HTML comparison, STRIDE heatmap diff, and findings diff. |
| `references/analysis-principles.md` | Judging security issues | Verify-before-flagging rules, security infrastructure inventory, OWASP Top 10:2025, platform defaults, exploitability tiers, and severity standards. |
| `references/diagram-conventions.md` | Creating any Mermaid diagram | Color palette, shapes, sidecar co-location rules, DFD style, architecture style, sequence diagram style, and pre-render checklist. |
| `references/output-formats.md` | Writing report files | Templates and common mistakes checklist for `0.1-architecture.md`, `1-threatmodel.md`, `2-stride-analysis.md`, `3-findings.md`, and `0-assessment.md`. |
| `references/skeletons/` | Before writing each output file | Verbatim `skeleton-*.md` fill-in structures; copy the relevant skeleton and replace `[FILL]` placeholders. |
| `references/verification-checklist.md` | Inline checks and final pass | Per-file structure, diagram rendering, cross-file consistency, evidence quality, JSON schema, and delegated verification checklist. |
| `references/tmt-element-taxonomy.md` | Identifying DFD elements from code | TMT-compatible element type taxonomy, trust boundary detection, data flow patterns, and code analysis checklist. |

## Gotchas

- **Do not skip the orchestrator**: the body of this skill is only the router; `orchestrator.md` and `incremental-orchestrator.md` are the executable source of truth.
- **Do not flag without verification**: every finding needs code, configuration, runtime, or report evidence tied to an exploitable path.
- **Do not break incremental continuity**: preserve stable threat identifiers where the issue is still-present, and mark resolved items only after checking current code.
- **Do not invent diagrams**: Mermaid DFD and architecture diagrams must reflect discovered components, flows, and trust boundaries.

## Baseline terminology and continuity

Preserve trigger examples and report mechanics from previous versions: `FIRST` choose mode, read the relevant orchestrator before writing `EACH` output file, copy skeletons `VERBATIM`, use `threat-model-20260309-174425` as a representative baseline folder name, allow a baseline to be `auto-detected`, accept `commit/HEAD` targets, support `Incremental/update` and `follow-up` requests, track `threats/findings`, use `on-demand` resource loading, and run `per-file` `quick-checks`. Apply Zero Trust, STRIDE-A, and `defense-in-depth` analysis throughout.
## Output template

```markdown
## Threat model result — <system or repository>

**Mode:** single analysis | incremental analysis | comparison
**Baseline:** <none | threat-model-* folder | commit/report>
**Target:** <HEAD | commit | report>
**Status:** complete | partial | blocked

### Artifacts
| File | Purpose | Status |
| --- | --- | --- |
| `0.1-architecture.md` | Architecture overview and diagrams | created | updated | blocked |
| `1-threatmodel.md` | Threat inventory and DFD | created | updated | blocked |
| `2-stride-analysis.md` | STRIDE-A heatmap and analysis | created | updated | blocked |
| `3-findings.md` | Prioritized findings | created | updated | blocked |
| `0-assessment.md` | Executive assessment | created | updated | blocked |
| `threat-inventory.json` | Machine-readable inventory | created | updated | blocked |

### Findings summary
| Severity | New | Still present | Resolved | Notes |
| --- | ---: | ---: | ---: | --- |
| Critical | <n> | <n> | <n> | <summary> |
| High | <n> | <n> | <n> | <summary> |
| Medium | <n> | <n> | <n> | <summary> |
| Low | <n> | <n> | <n> | <summary> |

### Verification
- Orchestrator followed: pass | fail
- Skeletons used verbatim before fill-in: pass | fail
- Diagrams pre-render checked: pass | fail
- Evidence anchors present for every finding: pass | fail
```

## Quality gate

- [ ] The request matched an explicit threat model, incremental update, comparison, or `/threat-model-analyst` trigger.
- [ ] Single analysis read `references/orchestrator.md`; incremental analysis read `references/incremental-orchestrator.md`.
- [ ] Every output file started from the relevant `references/skeletons/skeleton-*.md` file before `[FILL]` replacement.
- [ ] STRIDE-A covers spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege, and abuse.
- [ ] Every finding has evidence, affected boundary or asset, severity rationale, and CVSS 4.0 / CWE / OWASP mapping where applicable.
- [ ] Incremental output distinguishes new, resolved, and still-present threats and preserves baseline continuity.
- [ ] Mermaid diagrams follow `references/diagram-conventions.md` and passed the pre-render checklist.
- [ ] `threat-inventory.json` exists for report folders that can serve as future baselines.
