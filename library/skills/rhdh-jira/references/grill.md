# Grill Behavior

Shared challenging behavior for issue creation workflows. Each caller defines its own question list - this reference defines *how* to challenge the answers.

Load this alongside the command's type-specific questions. Apply every applicable behavior during the grill - don't skip challenges to be polite.

## Cadence

Ask one question at a time. Wait for the answer before asking the next. Adapt follow-ups based on what you learn. If the conversation already established context (e.g., chained from a parent issue), don't re-ask - carry it forward.

## Field Inference

Don't ask the user to fill in each Jira field manually. Instead, infer field values from the conversation and present a recommendation for confirmation. The grill is a conversation, not a form.

After the grill questions are complete, present all inferred fields at once:

> "Based on our discussion, here's what I'd set:"
>
> - **Priority**: Major - this is a functional gap, not a regression or blocker
> - **Team**: COPE - you mentioned this is in the dynamic plugins area
> - **Size**: M (3) - cross-team coordination + 4 AC items suggests ~3 sprints
> - **Component**: Plugins - primary area of change
> - **Assignee**: Allison Hill - top expertise in plugins per assign analysis
> - **Labels**: `rhdh-2.1-candidate`, `demo` - customer-facing feature targeting 2.1
>
> "Adjust any of these? [y to confirm / list changes]"

### Inference signals

| Field | Infer from |
|-------|------------|
| **Priority** | Severity of the problem, customer impact, blocker language, urgency words. Default to Major unless clear signals suggest otherwise. |
| **Team** | Components mentioned, domain area, who the user is, parent issue's team, which team owns the affected code. |
| **Size** | AC count, dependency count, complexity signals from the grill ("need to investigate", "multiple PRs", "cross-team"). Cross-reference against `references/sizing.md`. |
| **Component** | Technical domain discussed (RBAC, plugins, catalog, helm, operator, CI/CD, docs). Match against known components in `references/fields.md`. Also check codebase context - if the user has been editing files during the session, infer from file paths (see below). |
| **Assignee** | If the user is describing their own work, suggest them. Otherwise, run a lightweight expertise match from the conversation context (component + domain keywords against team roster). For deep analysis, suggest running `assign`. |
| **Labels** | Customer-facing → `demo`. Release target mentioned → `rhdh-X.Y-candidate`. Stretch goal language → `stretch`. Support origin → `rhdh-customer`. |

### Codebase-aware component inference

If the session involved editing or reading files, use the file paths to infer the component:

```bash
# Check recently modified files in the working tree
git diff --name-only HEAD~3 2>/dev/null | head -20
```

Path-to-component signals:

| Path pattern | Component |
|--------------|-----------|
| `plugins/catalog/`, `catalog-backend` | Catalog |
| `plugins/rbac/`, `rbac-backend` | RBAC |
| `plugins/tekton/` | Tekton |
| `plugins/topology/` | Topology |
| `plugins/lightspeed/` | Lightspeed |
| `plugins/bulk-import/` | Bulk Import |
| `packages/backend/`, `packages/app/` | Build |
| `docker/`, `Dockerfile`, `Containerfile` | Build |
| `charts/`, `helm/` | Helm |
| `docs/`, `*.md` in doc paths | Documentation |
| `e2e/`, `playwright/`, `cypress/` | Test Framework |
| `.github/`, `ci/`, `.tekton/` | CI/CD |

This is a hint, not definitive. Present as: "You've been working in `plugins/catalog/` - setting Component to Catalog." The user can override.

### When inference is weak

If a field can't be inferred with reasonable confidence, say so: "I'm not sure about the team - is this COPE or Install Method?" Don't guess silently. One targeted question is better than a wrong default.

## Challenge Behaviors

### Challenge sizing

After the user proposes a size (T-shirt or story points):

- Count the acceptance criteria items. If the AC count seems high for the proposed size, push back: "You have {N} acceptance criteria items - is {size} realistic?"
- Check for cross-team dependencies. Dependencies add coordination overhead that inflates effort.
- Check for unknowns. If the user said "we need to investigate" or "not sure about," that's a spike signal - suggest time-boxing or splitting the unknown into a separate spike.
- Cross-reference against the sizing guide. Load `references/sizing.md` for T-shirt size definitions (Features/Epics) and Fibonacci story point scale (Stories/Tasks).

### Challenge completeness

After the user describes scope and AC:

- **Testing**: "Does QE need to be involved? Is there a test plan or automation needed?" If the issue type is an Epic or Feature and no testing consideration was mentioned, ask.
- **Documentation**: "Does this change user-facing behavior? If so, docs need updating." If documentation wasn't mentioned for a user-facing change, flag it.
- **Upstream**: "Is there upstream Backstage work that needs to land first? Or is this purely downstream?" Don't assume - ask if not clear from context.
- **Security**: For features touching auth, RBAC, permissions, or API endpoints: "Any security considerations?"
- **Migration/Breaking changes**: "Does this change existing behavior? Will users need to update their configuration?"

Skip challenges that clearly don't apply. Don't ask about docs for a CI pipeline task. Don't ask about upstream for a purely downstream bug fix.

### Challenge scope

- **Split signals**: If a single AC item is complex enough to be its own issue, say so: "This AC item - '{item}' - sounds like it could be a separate {Story/Epic}. Should we split it?"
- **Overlap**: During the duplicate check (which runs after the grill), if related issues were found, revisit scope: "This overlaps with {KEY}. Should this issue be scoped to only the non-overlapping parts?"
- **Scope creep markers**: If the user keeps adding "also it should..." or "and maybe we could..." - pause and ask: "We're growing the scope. Should some of this be a follow-up issue?"

### Probe risks and unknowns

- "What could go wrong with this approach?"
- "Are there any unknowns that might change the sizing?"
- "Is there a dependency on another team or external service that could block this?"
- "Has this been attempted before? If so, what happened?"

Don't ask all four - pick the ones that are relevant based on context. For a simple Task with clear scope, skip risk probing. For a Feature with cross-team dependencies, probe harder.

### Cross-reference existing issues

During the grill (not just during duplicate check), search for related work:

- If the user mentions a component, search for open issues in that component: "There are {N} open issues in {component} - any of these related?"
- If the user mentions a dependency, verify it exists in Jira: "You mentioned depending on {thing} - is that tracked as a Jira issue?"
- If a related issue is found, ask whether to add an issue link (Blocks, Depends, Related).

Keep this lightweight. One search during the grill is enough - don't run a search after every answer.

### Validate before creating

Before proceeding to creation, verify the issue would pass the entry-status exit criteria from `references/workflows.md`:

- Are all required fields for New status determined? (Assignee, Priority, Team, Component - varies by type)
- Is the description substantive enough? A one-sentence description on a Feature is a red flag.
- Is the summary clear and specific? Summaries like "Update plugins" or "Fix bug" are too vague.

If validation fails, ask the user to fill the gap rather than creating a half-baked issue.

## Applicability by Issue Type

Not every behavior applies to every type. Use this as a guide:

| Behavior | Feature | Epic | Story | Task | Bug |
|----------|---------|------|-------|------|-----|
| Challenge sizing | ✅ | ✅ | ✅ | ✅ (if SP set) | ❌ |
| Completeness: testing | ✅ | ✅ | ✅ | ❌ | ❌ |
| Completeness: docs | ✅ | ✅ | ✅ (if user-facing) | ❌ | ❌ |
| Completeness: upstream | ✅ | ✅ | ✅ | ❌ | ❌ |
| Completeness: security | ✅ | ✅ | ✅ | ✅ | ❌ |
| Completeness: migration | ✅ | ✅ | ✅ | ❌ | ❌ |
| Challenge scope | ✅ | ✅ | ✅ | ❌ | ❌ |
| Probe risks | ✅ | ✅ | ❌ | ❌ | ❌ |
| Cross-reference | ✅ | ✅ | ✅ | ✅ | ✅ |
| Validate before creating | ✅ | ✅ | ✅ | ✅ | ✅ |

**Vulnerability** follows the Story column. Always requires Security component.

Bugs skip most challenges - the goal is to capture the defect accurately, not challenge whether it should exist. Cross-reference and validation still apply (check for duplicates, ensure fields are set).

Tasks skip scope/risk challenges unless they're complex (multi-day, cross-system). Use judgment.

## Comment Suggestions

After the issue is created, proactively suggest comments for context that emerged during the grill but doesn't belong in the description:

- **Decision trail**: "We discussed [alternative] but chose [approach] because [reason]."
- **Elaboration**: "Additional context about [topic] that supports the decision."
- **Abandoned paths**: "Initially considered [approach], abandoned because [reason]."
- **Customer context**: "This was raised by [customer type/use case] - relevant for prioritization."

Present each suggestion with a recommended comment text. The user approves, edits, or skips each one.
