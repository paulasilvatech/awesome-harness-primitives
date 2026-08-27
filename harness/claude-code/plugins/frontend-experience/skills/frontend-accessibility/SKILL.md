---
name: frontend-accessibility
description: >-
  Define and verify WCAG 2.2 AA, semantic, keyboard, focus, zoom, contrast, motion, media, data
  visualization, form, SPA, and native accessibility behavior. Use this skill when frontend
  design, implementation, review, testing, or release evidence involves accessibility.
---

<!-- Generated from harness/github-copilot/plugins/frontend-experience/skills/frontend-accessibility/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend accessibility

Treat accessibility as product correctness across design, implementation, and runtime evidence. Target WCAG 2.2 Level AA unless a stricter approved policy applies.

## When to invoke

- "Add accessibility acceptance criteria to this frontend feature."
- "Review this component or flow against WCAG 2.2 AA."
- "Verify keyboard, focus, zoom, contrast, and screen-reader behavior."
- "Make this chart, form, dialog, or chat accessible."
- "Plan accessibility testing for a mobile or desktop experience."

## Criteria

Read [references/wcag-2.2-aa.md](references/wcag-2.2-aa.md) for the web inspection map and [references/native-accessibility.md](references/native-accessibility.md) for native profiles.

Cover when applicable:

- semantic structure, landmarks, headings, lists, tables, and document language;
- accessible names, roles, values, descriptions, and states;
- keyboard completion, logical order, visible focus, no traps, and focus restoration;
- native semantics or current WAI-ARIA patterns for composite widgets;
- text and non-text contrast, color-independent meaning, zoom, reflow, text spacing, forced colors, and dark mode;
- pointer cancellation, target size, drag alternatives, orientation, and motion alternatives;
- labels, instructions, errors, summaries, redundant-entry reduction, and accessible authentication;
- images, charts, diagrams, audio, video, captions, transcripts, and long descriptions;
- route announcements, async status, loading, errors, toasts, live regions, and streaming updates;
- dynamic type, VoiceOver, TalkBack, safe areas, and native accessibility APIs.

## Evidence strategy

Automated scans identify a subset of issues. Record engine, version, ruleset or tags, tested state, exclusions, and unresolved manual checks.

Manual smoke tests include keyboard-only use, a relevant screen-reader path when available, zoom or dynamic type, reduced motion, and high-contrast or forced-color behavior for applicable surfaces.

Use [assets/manual-a11y-checklist.md](assets/manual-a11y-checklist.md). A clean automated result is not certification.

## Design and implementation rules

- Prefer native elements and platform controls before ARIA or custom widgets.
- Keep visible labels and accessible names aligned.
- Manage focus for dialogs, menus, route changes, validation summaries, async outcomes, and destructive confirmations.
- Announce meaningful state without repeatedly interrupting users during streaming or frequent updates.
- Preserve input after recoverable errors and link field errors programmatically.
- Provide textual summaries or accessible tables for complex visualizations.
- Honor user settings and provide alternatives to drag, gestures, motion, images of text, and inaccessible authentication puzzles.

## Limits

- Do not claim legal compliance, procurement approval, certification, or assistive-technology support without the required authority and evidence.
- Do not map a finding to a success criterion when the relationship is uncertain.
- Do not weaken product behavior or security controls silently to satisfy a scan.
- Use `accessibility-runtime-tester` (agent) for focused browser behavior evidence when available.

## Output template

```markdown
## Frontend accessibility result
**Status:** pass | needs revision | blocked
**Target:** WCAG 2.2 AA or <approved stricter target>

### Criteria and evidence
| Area / criterion | Automated | Manual | Result | Evidence gap |
| --- | --- | --- | --- | --- |

### Findings
| Severity | Behavior | Expected | Evidence | Remediation | Retest |
| --- | --- | --- | --- | --- | --- |

### Unverified checks
- <tool, device, AT, state, and reason>
```

## Quality gate

- [ ] The target accessibility policy and applicable surface are explicit.
- [ ] Native semantics, keyboard, focus, names, states, zoom, contrast, motion, errors, media, and async behavior are covered when applicable.
- [ ] Automated and manual evidence are reported separately.
- [ ] Engine, version, tested state, exclusions, and unrun checks are recorded.
- [ ] Findings include behavior, severity, evidence, remediation direction, and retest.
- [ ] No scan is described as certification or complete proof.
