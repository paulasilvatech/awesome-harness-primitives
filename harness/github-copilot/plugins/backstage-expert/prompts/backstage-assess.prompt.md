---
name: "backstage-assess"
description: "Assess a Backstage repository, identify its mode and version, map capabilities and risks, and return a validated remediation plan without changing files."
argument-hint: "scope=app|ai|catalog|templates|plugins|techdocs|auth|kubernetes|notifications|permissions|search|integrations|operations"
agent: "backstage-expert"
tools: ["read", "search", "web"]
---

# /backstage-assess

## Objective

Assess `${input:scope:app, ai, catalog, templates, plugins, techdocs, auth, kubernetes, notifications, permissions, search, integrations, or operations}` and return evidence-based findings in Chat without changing repository files.

## When to Invoke

Use before a Backstage migration, setup, integration, security change, upgrade, incident
remediation, or implementation plan when repository mode and current behavior must be established.

## Preconditions

- A Backstage repository or package is open and readable.
- The requested scope identifies a Backstage subsystem.
- The assessment remains read-only.

If a precondition is not met, report it and stop before proposing edits.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Scope | `${input:scope}` | Yes | Limit discovery and findings to this Backstage subsystem. |
| Repository context | Active workspace | Yes | Inspect repository identity, mode, version, config, and existing checks. |
| Selected context | `${selection}` | No | Use when present; do not infer missing selected content. |

## What I Will Do

- Detect adopter, core or fork, legacy or dual, Open Horizons, RHDH, or unknown mode.
- Inspect version evidence, relevant configuration, packages, scripts, and target files.
- Check first-party Backstage sources for version-sensitive behavior.
- Return prioritized findings, risks, remediation steps, and unrun validation.

## What I Will NOT Do

- Modify files, dependencies, provider systems, runtime resources, or data.
- Treat static inspection as runtime proof.
- Apply product-specific assumptions without positive evidence.
- Invent missing repository facts or validation outcomes.

## Output Format

```markdown
## Backstage assessment

**Mode:** adopter | core | legacy | dual | open-horizons | rhdh | unknown
**Version:** <version and evidence>
**Scope:** <subsystem>

### Findings
| Priority | Finding | Evidence | Remediation |
| --- | --- | --- | --- |

### Validation
| Check | Result or reason not run |
| --- | --- |

### Next step
- <focused action or blocker>
```

## Definition of Done

- [ ] Repository mode and Backstage version are evidenced.
- [ ] Findings remain within the requested subsystem.
- [ ] Version-sensitive claims cite first-party sources and a verification date.
- [ ] Risks and remediation are prioritized and traceable.
- [ ] Runtime checks not performed are labeled explicitly.
- [ ] No workspace or external-system changes occurred.

## Prompt Body

Follow these steps in order:

1. **Detect mode and version.** Inspect repository identity, `backstage.json`, package metadata,
   config layers, and contributor guidance.
2. **Bound the scope.** Limit inspection to `${input:scope}` and directly related dependencies.
3. **Gather evidence.** Read relevant files and first-party documentation; distinguish facts,
   inferences, and unknowns.
4. **Assess behavior and risk.** Inventory setup, configuration, security, compatibility,
   operations, and validation gaps.
5. **Return the report.** Use the required output format, remain read-only, and state every check
   not run.

## Invocation Example

1. Run **Chat: Run Prompt** and select `/backstage-assess`.
2. Enter `ai` for scope to assess AI Catalog, Actions Registry, and MCP Actions.
3. Verify the result appears in Chat and no workspace file changes.

## Related Primitives

- `backstage-expert` (agent): owns Backstage-specific judgment.
- `backstage-change` (prompt): applies an approved focused change.
