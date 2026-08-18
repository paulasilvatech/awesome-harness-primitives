---
name: refactor-plan
description: >-
  Create a concrete, evidence-backed plan before a multi-file refactor. Use this skill when the user asks to plan, sequence, scope, or safely execute a refactor across multiple files, when hidden coupling is likely, or when implementation should wait for confirmation after a plan.
---

# Refactor plan

Investigate the repository without editing, define a safe phased refactor plan, include verification and rollback steps, then stop for confirmation before code changes unless the user explicitly authorized continuing after the plan.

## When to invoke

- "Plan this refactor before changing code."
- "Sequence a multi-file refactor safely."
- "What files are affected by this refactor?"
- "Create a refactor plan and wait for approval."
- "How should we roll back this risky refactor?"

## Procedure

1. Do not edit files while preparing the plan.
2. Search the codebase to understand current implementation, tests, configuration, and documentation.
3. Identify affected files, ownership boundaries, dependencies, and likely hidden coupling.
4. Define current state and target state in repository-specific terms.
5. Sequence changes safely: contracts and types first, implementations second, callers third, tests fourth, cleanup last.
6. Add verification steps between phases and a final validation command.
7. Add rollback or recovery steps for the riskiest phases.
8. Output the complete plan using the template below.
9. Stop after the plan and ask: "Shall I proceed with Phase 1?"

If the request is too ambiguous to plan safely, ask concise clarifying questions instead of editing files.

## Refactor planning criteria

| Area | What to capture | Why it matters |
| --- | --- | --- |
| Current state | How the code works now, including entry points and data flow. | Prevents plans based on assumptions. |
| Target state | The intended architecture or behavior after the refactor. | Keeps phases aligned to the user's goal. |
| Affected files | Modify/create/delete classification and dependencies. | Shows scope and review size. |
| Boundaries | API contracts, ownership, generated code, external integrations. | Avoids breaking callers or editing regenerated files. |
| Hidden coupling | Tests, config, docs, fixtures, serialization, DI, reflection, migrations. | Refactors often fail outside the obvious source files. |
| Verification | Checks after each phase plus final command. | Provides early failure points and confidence. |
| Rollback | How to undo risky phases. | Makes the plan executable under uncertainty. |

## Phase sequencing rules

| Phase | Prefer | Avoid |
| --- | --- | --- |
| Types and interfaces | Add or adjust contracts before implementations. | Editing callers first without a stable contract. |
| Implementation | Change internals behind the prepared contracts. | Mixing broad cleanup with behavior changes. |
| Callers | Migrate call sites in small groups with verification. | Big-bang updates with no intermediate checks. |
| Tests | Update or add tests that prove preserved behavior and new structure. | Weakening assertions to make the refactor pass. |
| Cleanup | Remove deprecated code and update documentation after validation. | Removing compatibility shims before all callers move. |

## Limits

- Do not use this skill for single-file edits where no sequencing or hidden coupling exists.
- Do not implement during the planning response unless the user explicitly said to continue without review after the plan.
- If the user's instructions conflict with stopping for approval, follow the explicit latest user instruction and state the assumption in the plan.

## Output template

```markdown
## Refactor Plan: [title]

### Current State
[Brief description of how things work now]

### Target State
[Brief description of how things will work after]

### Affected Files
| File | Change Type | Dependencies |
|------|-------------|--------------|
| path | modify/create/delete | blocks X, blocked by Y |

### Execution Plan

#### Phase 1: Types and Interfaces
- [ ] Step 1.1: [action] in `file.ts`
- [ ] Verify: [how to check it worked]

#### Phase 2: Implementation
- [ ] Step 2.1: [action] in `file.ts`
- [ ] Verify: [how to check]

#### Phase 3: Tests
- [ ] Step 3.1: Update tests in `file.test.ts`
- [ ] Verify: Run `npm test`

#### Phase 4: Cleanup
- [ ] Remove deprecated code
- [ ] Update documentation

### Rollback Plan
If something fails:
1. [Step to undo]
2. [Step to undo]

### Risks
- [Potential issue and mitigation]

Shall I proceed with Phase 1?
```

## Quality gate

- [ ] No files were edited while preparing the plan.
- [ ] The plan cites repository-specific evidence from implementation, tests, configuration, or docs.
- [ ] Current state, target state, affected files, phases, verification, rollback, and risks are all present.
- [ ] Phases are sequenced from contracts/types to implementation, callers, tests, and cleanup unless a different order is justified.
- [ ] Ambiguity is resolved with concise questions rather than speculative edits.
- [ ] The response stops after the plan and asks "Shall I proceed with Phase 1?" unless explicitly authorized to continue.
