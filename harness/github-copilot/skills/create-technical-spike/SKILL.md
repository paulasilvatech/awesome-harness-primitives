---
name: create-technical-spike
argument-hint: "spike title, category, owner, timebox, priority, and optional output folder"
description: >-
  Create time-boxed technical spike documents that answer critical implementation questions before development proceeds. Use this skill when the user asks to create a technical spike, research an API or architecture decision, document a proof of concept, evaluate performance or security options, or unblock development with an evidence-based recommendation.
---

# Create technical spike

Create a focused technical spike markdown file that frames one unresolved decision, defines time-boxed research, captures evidence, and ends with an actionable recommendation.

## When to invoke

- "Create a technical spike document."
- "Write a spike for this API integration decision."
- "Plan research before we implement this architecture."
- "Document a proof of concept for this risky feature."
- "Create a time-boxed investigation for performance or security options."

## Inputs

Use `$ARGUMENTS` for spike title, category, owner, timebox, priority, output folder, and any known context. If the folder is not supplied, default to `docs/spikes`. If values are missing, use placeholders in the document and call them out in the result.

## File and frontmatter rules

Create one file per spike in `docs/spikes` or the user-supplied folder. Name it with kebab-case: `[category]-[short-description]-spike.md`, for example `api-copilot-integration-spike.md`, `performance-realtime-audio-spike.md`, or `architecture-state-management-spike.md`.

Use this frontmatter shape, preserving user-provided values when available:

```yaml
---
title: "<SpikeTitle>"
category: "<Category|Technical>"
status: "Not Started"
priority: "<Priority|High>"
timebox: "<Timebox|1 week>"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: "<Owner>"
tags: ["technical-spike", "<category|technical>", "research"]
---
```

## Spike categories

| Category | Use for |
| --- | --- |
| API Integration | Third-party API capabilities, limitations, authentication, rate limits, and integration patterns. |
| Architecture & Design | System architecture decisions, design pattern applicability, and component interaction models. |
| Performance & Scalability | Latency, throughput, bottlenecks, resource utilization, and scalability options. |
| Platform & Infrastructure | Platform capabilities, infrastructure requirements, deployment, and hosting constraints. |
| Security & Compliance | Authentication, authorization, compliance constraints, security requirements, and implementations. |
| User Experience | Interaction patterns, accessibility requirements, and interface design decisions. |

## Research strategy

1. Gather information from existing documentation, external resources, APIs, libraries, examples, and the codebase's existing patterns and constraints.
2. Validate assumptions with focused prototypes, proof of concept work, or targeted experiments when evidence is needed.
3. Synthesize findings into a recommendation, rationale, implementation notes, and follow-up tasks.

## Spike quality rules

| Rule | Requirement |
| --- | --- |
| One Question Per Spike | Each document focuses on a single technical decision or research question. |
| Time-Boxed Research | Define specific time limits, deliverables, and decision deadline. |
| Evidence-Based Decisions | Require concrete evidence from tests, prototypes, documentation, or analysis. |
| Clear Recommendations | Document a specific recommendation and rationale. |
| Dependency Tracking | Identify related components, dependencies, other spikes, and blocked decisions. |
| Outcome-Focused | End with an actionable decision or recommendation. |

## File naming examples

| Category | Examples |
| --- | --- |
| API/Integration | `api-copilot-chat-integration-spike.md`, `api-azure-speech-realtime-spike.md`, `api-vscode-extension-capabilities-spike.md` |
| Performance | `performance-audio-processing-latency-spike.md`, `performance-extension-host-limitations-spike.md`, `performance-webrtc-reliability-spike.md` |
| Architecture | `architecture-voice-pipeline-design-spike.md`, `architecture-state-management-spike.md`, `architecture-error-handling-strategy-spike.md` |

## Legacy input and tool vocabulary

If migrating an older template, map `${input:FolderPath|docs/spikes}` and `FolderPath` to `$ARGUMENTS` plus the `docs/spikes` default. Do not expose legacy VS Code tool labels as active CLI tools: `search/searchResults`, `search/fetch`, and `fetch/githubRepo` describe research intent only. Use `development/architecture` when describing why the spike matters to implementation decisions.

## Output template

```markdown
---
title: "<SpikeTitle>"
category: "<Category|Technical>"
status: "Not Started"
priority: "<Priority|High>"
timebox: "<Timebox|1 week>"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: "<Owner>"
tags: ["technical-spike", "<category|technical>", "research"]
---

# <SpikeTitle>

## Summary

**Spike Objective:** <clear, specific question or decision that needs resolution>

**Why This Matters:** <impact on development or architecture decisions>

**Timebox:** <allocated time>

**Decision Deadline:** <deadline to avoid blocking development>

## Research Question(s)

**Primary Question:** <main technical question>

**Secondary Questions:**

- <related question 1>
- <related question 2>
- <related question 3>

## Investigation Plan

### Research Tasks

- [ ] <specific research task 1>
- [ ] <specific research task 2>
- [ ] <specific research task 3>
- [ ] Create proof of concept/prototype
- [ ] Document findings and recommendations

### Success Criteria

**This spike is complete when:**

- [ ] <specific criteria 1>
- [ ] <specific criteria 2>
- [ ] Clear recommendation documented
- [ ] Proof of concept completed (if applicable)

## Technical Context

**Related Components:** <components affected>

**Dependencies:** <other spikes or decisions that depend on this>

**Constraints:** <known limitations or requirements>

## Research Findings

### Investigation Results

<research findings, test results, and evidence gathered>

### Prototype/Testing Notes

<prototype, spike, or technical experiment results>

### External Resources

- <relevant documentation>
- <API references>
- <community discussions>
- <examples/tutorials>

## Decision

### Recommendation

<clear recommendation based on findings>

### Rationale

<why this approach was chosen over alternatives>

### Implementation Notes

<key implementation considerations>

### Follow-up Actions

- [ ] <action item 1>
- [ ] <action item 2>
- [ ] Update architecture documents
- [ ] Create implementation tasks

## Status History

| Date | Status | Notes |
| --- | --- | --- |
| <Date> | Not Started | Spike created and scoped |
| <Date> | In Progress | Research commenced |
| <Date> | Complete | <Resolution summary> |

---

_Last updated: <Date> by <Name>_
```

## Quality gate

- [ ] `$ARGUMENTS` was consumed for title, category, owner, timebox, priority, and folder when provided.
- [ ] The file path uses `docs/spikes` or the requested folder and the name matches `[category]-[short-description]-spike.md`.
- [ ] The spike has exactly one primary question.
- [ ] The frontmatter includes title, category, status, priority, timebox, created, updated, owner, and tags.
- [ ] Investigation tasks include research, prototype or validation when applicable, findings, and recommendation.
- [ ] Success criteria make the time-boxed outcome objectively checkable.
- [ ] The document includes Technical Context, Research Findings, Decision, Follow-up Actions, and Status History.
