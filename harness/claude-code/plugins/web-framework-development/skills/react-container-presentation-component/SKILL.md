---
name: react-container-presentation-component
description: >-
  Create a React Container/Presentation component under src/components with TypeScript, Storybook,
  SCSS module, ui/features classification, optional Mantine replacement, and validation. Use when
  explicitly asked for a Container/Presentation component or when running
  /react-container-presentation-component.
argument-hint: componentName type(ui|features)
user-invocable: true
---

<!-- Generated from harness/github-copilot/plugins/web-framework-development/skills/react-container-presentation-component/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# React container/presentation component

Create a React component under `src/components` that follows this repository's Container/Presentation pattern, TypeScript conventions, SCSS module rules, and Storybook minimums.

## When to invoke

- "/react-container-presentation-component UserCard ui"
- "`/react-container-presentation-component`"
- "Create a Container/Presentation component."
- "Create a Container/Presentation-based component."
- "Scaffold a React component under src/components/features."
- "Help decide whether this component belongs in ui or features."
- "Replace direct Mantine usage with a reusable ui component."

## Inputs

Use `$ARGUMENTS` as `componentName type(ui|features)`. Validate that the component name is PascalCase and the type is exactly `ui` or `features`. If arguments are incomplete, ask for missing information before creating files; if the environment has an `ask_user` interaction primitive, use it.

Required questions when missing:

| Missing input | Question requirement |
| --- | --- |
| Component name | Require PascalCase. |
| Type | Offer only `ui` and `features`. |
| Replacement intent for `ui` | Ask whether equivalent direct Mantine or other UI-library usage in existing `features` should be replaced. |

## Classification rules

| Type | Directory | Use when | Required files |
| --- | --- | --- | --- |
| `ui` | `src/components/ui/<ComponentName>` | Pure reusable rendering with no business logic, async processing, context/store update, or feature-specific state management. | `index.tsx`, `index.module.scss`, `index.stories.tsx` |
| `features` | `src/components/features/<ComponentName>` | Component coordinates state management, side effects, async processing, context/store updates, or business logic. | `index.tsx`, `use<ComponentName>.tsx`, `presentation.tsx`, `types.ts`, `presentation.module.scss`, `presentation.stories.tsx` |

Even when the user specifies `ui`, apply `Reclassification Rule` in `references/component-architecture.md` before creating files. If the implementation is closer to `features`, pause and confirm one of these choices: `Create as features` or `Keep ui and move state/logic to parent or features`.

## Procedure

1. Read `references/component-architecture.md` and `references/typescript-and-scss-rules.md`.
2. Parse `$ARGUMENTS` and ask for any missing component name, type, or `ui` replacement decision.
3. Check whether `src/components/ui/<ComponentName>` or `src/components/features/<ComponentName>` already exists.
4. If a target exists, do not overwrite it; confirm whether to stop, extend, or choose a different name.
5. Decide the target directory from the classification table.
6. Create the required files for `ui` or `features`.
7. If creating `ui` and the user approved replacements, replace equivalent direct implementations using Mantine or other UI libraries in existing `features`.
8. Run the repository's build and lint commands and fix issues introduced by the new or updated files.
9. Follow `Storybook Minimum` from `references/component-architecture.md`. Ask whether to run a Storybook check, with run/skip choices such as `Run` or `Skip for now`.
10. Run `npm run storybook` only if the user selects `Run`; otherwise report that Storybook execution was skipped.

## Responsibility placement

| Concern | `ui` location | `features` location |
| --- | --- | --- |
| Rendering markup | `index.tsx` | `presentation.tsx` |
| Styles | `index.module.scss` | `presentation.module.scss` |
| Public props | `index.tsx` types when small | `types.ts` |
| State and effects | Parent or feature component, not `ui` | `use<ComponentName>.tsx` hook |
| Storybook examples | `index.stories.tsx` | `presentation.stories.tsx` |
| Business logic | Not allowed | Container/hook, not presentation |

## Progressive disclosure and bundled resources

| Resource | Use it when |
| --- | --- |
| `references/component-architecture.md` | Classification, Reclassification Rule, Storybook Minimum, dependency direction, and Container/Presentation responsibilities. |
| `references/typescript-and-scss-rules.md` | TypeScript exports, props, SCSS module naming, and style conventions. |

## Gotchas

- **Do not overwrite existing components**: existing directories require explicit confirmation.
- **Do not force `ui`**: state management, side effects, async processing, context/store updates, or business logic mean `features` unless logic is moved upward.
- **Do not run Storybook without consent**: ask first and report `Run` or `Skip for now`.
- **Do not violate dependency direction**: `ui` must not depend on `features`.

## Output template

```markdown
## React component scaffold result

**Status:** created | needs input | blocked
**Component:** `<ComponentName>`
**Classification:** `ui` | `features`
**Target directory:** `src/components/<ui|features>/<ComponentName>`

### Files created
- `<path>`

### Replacements
- `<changed file>`: <replacement details or none>

### Usage example
```tsx
<<ComponentName> />
```

### Responsibilities
- State and side effects: <where they live>
- Rendering: <where it lives>
- Styling: <where it lives>
- Dependency direction violations: none | <details>

### Validation
- Build: pass | fail | not run
- Lint: pass | fail | not run
- Storybook: run with `npm run storybook` | skipped by user
- Unresolved items: <none or list>
```

## Quality gate

- [ ] `$ARGUMENTS` was parsed as `componentName type(ui|features)` and missing values were requested.
- [ ] Component name is PascalCase and type is `ui` or `features`.
- [ ] Existing `src/components/ui/<ComponentName>` and `src/components/features/<ComponentName>` were checked before writing.
- [ ] `ui` classification was re-checked against state, side effects, async processing, context/store updates, and business logic.
- [ ] Required files were created for the selected classification.
- [ ] Approved replacements in existing `features` were reported, or none were performed.
- [ ] Build and lint commands were run or a concrete blocker was reported.
- [ ] Storybook execution was run only after user approval or explicitly reported as skipped.
