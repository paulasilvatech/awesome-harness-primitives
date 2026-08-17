<!-- AUTHORING — delete this block after copying.
Target path: instructions/<name>.instructions.md   Filename must match ^[A-Za-z0-9._-]+\.instructions\.md$
Spec: docs/COPILOT-HARNESS-SPEC.md §2

Frontmatter — ONLY these four keys are recognized; anything else is ignored:
  applyTo       Comma-separated globs in a SINGLE string. "**" matches every file.
                Omitting it means the file is never auto-applied (validator: IN004 WARNING).
                Correct:   applyTo: "**/*.ts,**/*.tsx,src/**"
                Wrong:     applyTo: ["**/*.ts"]        (array)
  description   Optional but recommended; shown on hover.
  name          Optional display name; defaults to the filename.
  excludeAgent  Optional: "code-review" | "cloud-agent".

Body: non-empty, focused, roughly two pages. Instructions must be GENERAL conventions, not a task
procedure — a procedure belongs in a skill. Keep code blocks short and illustrative; move long
walkthroughs into a skill and reference it by name.
-->
---
description: "<What conventions this file carries.> Use when <creating or reviewing the matching files>."
applyTo: "<glob>,<glob>"
---

# <Topic> Conventions

<One paragraph: which files activate this file, which toolchain and versions it assumes, and what the
reader is expected to already have in place. State the default choice when several options exist.>

## Conventions

| Rule | Rationale |
| --- | --- |
| <The rule, stated as an imperative.> | <Why it exists — the failure it prevents.> |
| <The rule.> | <Rationale.> |

## <Specific Area>

<Repeat this section per area. Keep each explanation to a few sentences plus a minimal example.>

```<language>
<The smallest snippet that makes the convention unambiguous.>
```

## Do / Do Not

| Do | Do not |
| --- | --- |
| <Correct practice.> | <The exact mistake it replaces.> |
| <Correct practice.> | <The exact mistake it replaces.> |

## Checklist Before Opening a PR

- [ ] <Condition a reviewer can check by reading the diff.>
- [ ] <Command that must pass locally, matching the CI gate.>
- [ ] <Security or hygiene condition, such as no secret outside the vault.>

## Related Primitives

| Name | Type | Use it for |
| --- | --- | --- |
| `<skill-name>` | skill | <the deeper review or generation task these conventions defer to> |
| `<agent-name>` | agent | <the agent that owns changes in this area> |
