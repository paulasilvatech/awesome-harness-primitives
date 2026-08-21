---
name: "{{SKILL_NAME}}"
description: >-
  {{WHAT_THE_SKILL_DOES}}. Use this skill when {{POSITIVE_TRIGGER_CONDITIONS}}.
---

# {{SKILL_TITLE}}

> **Authoring note:** Replace every `{{UPPER_SNAKE_CASE}}` placeholder and
> delete all authoring guidance and optional sections that do not apply.
> Keep the final `SKILL.md` preferably under 200 lines and always under 500.

The `name` must be 1 to 64 characters, use kebab-case, and exactly match the
parent skill directory. The `description` must be 1 to 1024 characters and
state both **WHAT** the skill does and **WHEN** it should activate. Describe
only positive trigger conditions there; put exclusions in `## Limits`.

{{ONE_PARAGRAPH_SUMMARY_OF_INPUT_TRANSFORMATION_AND_OUTPUT}}

## Optional frontmatter

Keep the frontmatter minimal unless the skill needs an optional capability.
Add only the relevant lines inside the opening frontmatter block:

```yaml
user-invocable: true
argument-hint: "{{ARGUMENT_HINT}}"
allowed-tools: ["{{MINIMUM_REQUIRED_TOOL}}"]
```

- Add `user-invocable` only when direct invocation is useful.
- Add `argument-hint` only when user-supplied arguments change execution.
  When present, keep `## Inputs` and consume `$ARGUMENTS` there.
- Omit `allowed-tools` by default. If used, list only tools the skill actually
  requires. Do not add editing tools to consultative or review skills unless
  the skill is explicitly expected to change files.
- Other supported fields such as `disable-model-invocation`, `license`,
  `metadata`, and `tags` are optional. Add them only for a concrete need.

## When to invoke

- "{{POSITIVE_USER_REQUEST_ONE}}"
- "{{POSITIVE_USER_REQUEST_TWO}}"
- "{{POSITIVE_USER_REQUEST_THREE}}"

## Inputs

Delete this section unless `argument-hint` is enabled.

Use `$ARGUMENTS` as {{HOW_ARGUMENTS_CONTROL_THE_TASK}}. Validate it by
{{ARGUMENT_VALIDATION_RULE}}. If it is empty, {{ARGUMENT_FALLBACK_BEHAVIOR}}.

## Prerequisites and context

Delete this section when there are no prerequisites or required context.

- {{REQUIRED_TOOL_SERVICE_OR_CONFIGURATION}}
- {{REQUIRED_INPUT_OR_REPOSITORY_CONTEXT}}
- {{SOURCE_OF_TRUTH_AND_PRECEDENCE_RULE}}

## Procedure

Use this format when order matters. Delete `## Criteria` and add or remove as
many steps as the real procedure requires.

1. {{FIRST_REQUIRED_ACTION}}
2. {{NEXT_REQUIRED_ACTION_OR_DECISION}}
3. Continue with {{ADDITIONAL_ACTIONS_IN_EXECUTION_ORDER}}.
4. {{VALIDATE_AND_DELIVER_THE_RESULT}}

## Criteria

Use this format for reviews, debugging, or evaluation where judgment matters
more than sequence. Delete `## Procedure` unless both formats are necessary.

### {{CRITERION_GROUP_ONE}}

- [ ] {{VERIFIABLE_CRITERION}}
- [ ] {{VERIFIABLE_CRITERION_WITH_REQUIRED_EVIDENCE}}

### {{CRITERION_GROUP_TWO}}

- [ ] {{VERIFIABLE_CRITERION}}
- [ ] {{DECISION_RULE_FOR_AN_AMBIGUOUS_CASE}}

## Output template

Return exactly this structure:

```markdown
## {{RESULT_TITLE}}

**Status:** {{ALLOWED_STATUS_VALUE}}
**Summary:** {{ONE_SENTENCE_SUMMARY}}

### Details
{{ORDERED_FINDINGS_ACTIONS_OR_ARTIFACT}}

### Validation
- {{CHECK_PERFORMED}}: {{PASS_FAIL_RESULT_AND_EVIDENCE}}
```

## Examples

Delete this section when examples would not clarify a subtle distinction.

### Good

**Input:** `{{GOOD_INPUT}}`

**Expected behavior:** {{GOOD_BEHAVIOR_AND_WHY_IT_IS_CORRECT}}

### Bad

**Input:** `{{BAD_INPUT}}`

**Incorrect behavior:** {{BAD_BEHAVIOR_AND_HOW_TO_CORRECT_IT}}

## Limits

Delete this section only when the skill has no meaningful boundary.

- Do not use this skill for {{OUT_OF_SCOPE_REQUEST}}.
- Use `{{RELATED_PRIMITIVE_NAME}}` (`{{RELATED_PRIMITIVE_TYPE}}`) instead when
  {{HANDOFF_CONDITION}}.
- {{NON_GOAL_OR_SAFETY_BOUNDARY}}

## Gotchas

Delete this section when there are no non-obvious failure modes.

- **{{KEY_CONSTRAINT}}**: {{WHY_THE_CONSTRAINT_EXISTS}}
- {{COMMON_MISTAKE_AND_PREVENTIVE_ACTION}}

## Troubleshooting

Delete this section when there are no known reactive fixes.

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| {{SYMPTOM}} | {{LIKELY_CAUSE}} | {{ACTIONABLE_RESOLUTION}} |

## Progressive disclosure and bundled resources

At discovery time, only `name` and `description` are loaded. The full body
loads after activation, and bundled resources should be read or executed only
when needed. Move long explanations, large examples, catalogs, and complex
workflows out of `SKILL.md`.

- `references/{{REFERENCE_FILE}}`: detailed knowledge or decision rules.
- `scripts/{{SCRIPT_FILE}}`: deterministic, repeatable automation.
- `assets/{{ASSET_FILE}}`: static material consumed without modification.
- `templates/{{TEMPLATE_FILE}}`: starter content the agent modifies.

Delete unused entries. Every referenced resource must exist inside the skill
directory, and the core instructions must say when to use it.

## Related primitives

Refer to other primitives by name and type, without relative links.

| Name | Type | Use it when |
| --- | --- | --- |
| `{{PRIMITIVE_NAME}}` | `{{PRIMITIVE_TYPE}}` | {{PRIMITIVE_BOUNDARY_OR_HANDOFF}} |

## Quality gate

- [ ] `name` is valid kebab-case and matches the parent directory.
- [ ] `description` states WHAT and WHEN using positive trigger language.
- [ ] The chosen procedure or criteria match the task instead of forcing an
      arbitrary workflow.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was actually performed and includes evidence.
- [ ] If `argument-hint` is present, `$ARGUMENTS` is consumed and validated.
- [ ] `allowed-tools`, if present, contains only the minimum required tools.
- [ ] Every bundled resource referenced above exists and is used on demand.
- [ ] All unused optional sections, authoring guidance, and
      `{{UPPER_SNAKE_CASE}}` placeholders are removed.
- [ ] `wc -l SKILL.md` reports fewer than 500 lines, preferably fewer than 200.
