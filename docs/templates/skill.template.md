---
name: "{{SKILL_NAME}}"
description: >-
  {{WHAT_THE_SKILL_DOES}}. Use this skill when {{POSITIVE_TRIGGER_CONDITIONS}}.
---

# {{SKILL_TITLE}}

> **Authoring note:** Replace every `{{UPPER_SNAKE_CASE}}` placeholder and
> delete all authoring guidance and every CONDITIONAL section whose trigger is
> not met. Keep the final `SKILL.md` preferably under 200 lines and always
> under 500.

## Section map

Skills use the loosest structure of all primitive types. Only four elements are
mandatory; everything else is earned by real content. Adding a CONDITIONAL
section with placeholder filler is worse than omitting it.

| Section | Status | Include when |
| --- | --- | --- |
| `## When to invoke` | MANDATORY | Always. First section after the summary. |
| Domain sections | MANDATORY | Always. One or more, freely titled after the actual subject matter. This is where the skill's real knowledge lives and where most of its length belongs. |
| `## Output template` | MANDATORY | Always. Second-to-last section. |
| `## Quality gate` | MANDATORY | Always. Last section, unless `## References` follows it. |
| `## Optional frontmatter` | AUTHORING ONLY | Never ships. Delete before delivery. |
| `## Inputs` | CONDITIONAL | `argument-hint` is set in the frontmatter. |
| `## Prerequisites and context` | CONDITIONAL | The skill needs a tool, service, credential, or file that may be absent. |
| `## Procedure` | CONDITIONAL | Execution order is load-bearing and a wrong order produces a wrong result. |
| `## Criteria` | CONDITIONAL | The skill reviews or evaluates, and judgment matters more than sequence. |
| `## Examples` | CONDITIONAL | A subtle good/bad distinction is not obvious from the rules alone. |
| `## Limits` | CONDITIONAL | The skill has an out-of-scope boundary or hands off to another primitive. |
| `## Gotchas` | CONDITIONAL | There are non-obvious failure modes a competent agent would still hit. |
| `## Troubleshooting` | CONDITIONAL | There are known symptoms with known reactive fixes. |
| `## Progressive disclosure and bundled resources` | CONDITIONAL | The skill directory contains `references/`, `scripts/`, `assets/`, or `templates/`. |
| `## Related primitives` | CONDITIONAL | Another primitive owns an adjacent responsibility worth naming. |
| `## References` | CONDITIONAL | The skill cites absolute external URLs such as specs, RFCs, books, or vendor docs. Place it after `## Quality gate`. |

`## Procedure` and `## Criteria` are alternatives. Use both only when the skill
genuinely runs an ordered workflow and then applies judgment to the result.

Section titles for MANDATORY sections use sentence case exactly as written
above. Domain section titles are free.

The `name` must be 1 to 64 characters, use kebab-case, and exactly match the
parent skill directory. The `description` must be 1 to 1024 characters and
state both **WHAT** the skill does and **WHEN** it should activate. Describe
only positive trigger conditions there; put exclusions in `## Limits`.

{{ONE_PARAGRAPH_SUMMARY_OF_INPUT_TRANSFORMATION_AND_OUTPUT}}

## Optional frontmatter

AUTHORING ONLY. Delete this whole section from the delivered skill.

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

MANDATORY. Quote the phrases a real user would type, not paraphrases.

- "{{POSITIVE_USER_REQUEST_ONE}}"
- "{{POSITIVE_USER_REQUEST_TWO}}"
- "{{POSITIVE_USER_REQUEST_THREE}}"

## {{DOMAIN_SECTION_TITLE}}

MANDATORY, repeatable. Add one section per real subject area, titled after the
domain rather than after this template. This is where the skill's substance
lives: rules, tables, commands, patterns, anti-patterns, thresholds, and
worked detail. A skill whose only content is the mandatory scaffolding has no
reason to exist.

{{DOMAIN_KNOWLEDGE_AS_PROSE_TABLES_OR_CODE}}

## Inputs

CONDITIONAL. Include only when `argument-hint` is set. Otherwise delete.

Use `$ARGUMENTS` as {{HOW_ARGUMENTS_CONTROL_THE_TASK}}. Validate it by
{{ARGUMENT_VALIDATION_RULE}}. If it is empty, {{ARGUMENT_FALLBACK_BEHAVIOR}}.

## Prerequisites and context

CONDITIONAL. Include only when the skill depends on a tool, service,
credential, or file that may be absent. Otherwise delete.

- {{REQUIRED_TOOL_SERVICE_OR_CONFIGURATION}}
- {{REQUIRED_INPUT_OR_REPOSITORY_CONTEXT}}
- {{SOURCE_OF_TRUTH_AND_PRECEDENCE_RULE}}

## Procedure

CONDITIONAL. Include only when execution order is load-bearing and a wrong
order produces a wrong result. Delete `## Criteria` when you use this.

1. {{FIRST_REQUIRED_ACTION}}
2. {{NEXT_REQUIRED_ACTION_OR_DECISION}}
3. Continue with {{ADDITIONAL_ACTIONS_IN_EXECUTION_ORDER}}.
4. {{VALIDATE_AND_DELIVER_THE_RESULT}}

## Criteria

CONDITIONAL. Include only for reviews, debugging, or evaluation where judgment
matters more than sequence. Delete `## Procedure` unless the skill genuinely
runs an ordered workflow and then applies judgment to its result.

### {{CRITERION_GROUP_ONE}}

- [ ] {{VERIFIABLE_CRITERION}}
- [ ] {{VERIFIABLE_CRITERION_WITH_REQUIRED_EVIDENCE}}

### {{CRITERION_GROUP_TWO}}

- [ ] {{VERIFIABLE_CRITERION}}
- [ ] {{DECISION_RULE_FOR_AN_AMBIGUOUS_CASE}}

## Output template

MANDATORY. Return exactly this structure:

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

CONDITIONAL. Include only when a subtle good/bad distinction is not obvious
from the rules alone. Otherwise delete.

### Good

**Input:** `{{GOOD_INPUT}}`

**Expected behavior:** {{GOOD_BEHAVIOR_AND_WHY_IT_IS_CORRECT}}

### Bad

**Input:** `{{BAD_INPUT}}`

**Incorrect behavior:** {{BAD_BEHAVIOR_AND_HOW_TO_CORRECT_IT}}

## Limits

CONDITIONAL. Include only when the skill has an out-of-scope boundary or hands
off to another primitive. Otherwise delete.

- Do not use this skill for {{OUT_OF_SCOPE_REQUEST}}.
- Use `{{RELATED_PRIMITIVE_NAME}}` (`{{RELATED_PRIMITIVE_TYPE}}`) instead when
  {{HANDOFF_CONDITION}}.
- {{NON_GOAL_OR_SAFETY_BOUNDARY}}

## Gotchas

CONDITIONAL. Include only when there are non-obvious failure modes a competent
agent would still hit. Otherwise delete.

- **{{KEY_CONSTRAINT}}**: {{WHY_THE_CONSTRAINT_EXISTS}}
- {{COMMON_MISTAKE_AND_PREVENTIVE_ACTION}}

## Troubleshooting

CONDITIONAL. Include only when there are known symptoms with known reactive
fixes. Otherwise delete.

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| {{SYMPTOM}} | {{LIKELY_CAUSE}} | {{ACTIONABLE_RESOLUTION}} |

## Progressive disclosure and bundled resources

CONDITIONAL. Include only when the skill directory contains `references/`,
`scripts/`, `assets/`, or `templates/`. Otherwise delete.

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

CONDITIONAL. Include only when another primitive owns an adjacent
responsibility worth naming. Otherwise delete.

Refer to other primitives by name and type, without relative links.

| Name | Type | Use it when |
| --- | --- | --- |
| `{{PRIMITIVE_NAME}}` | `{{PRIMITIVE_TYPE}}` | {{PRIMITIVE_BOUNDARY_OR_HANDOFF}} |

## Quality gate

MANDATORY. Last section, unless `## References` follows it.

- [ ] `name` is valid kebab-case and matches the parent directory.
- [ ] `description` states WHAT and WHEN using positive trigger language.
- [ ] The chosen procedure or criteria match the task instead of forcing an
      arbitrary workflow.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was actually performed and includes evidence.
- [ ] If `argument-hint` is present, `$ARGUMENTS` is consumed and validated.
- [ ] `allowed-tools`, if present, contains only the minimum required tools.
- [ ] Every bundled resource referenced above exists and is used on demand.
- [ ] Every MANDATORY section is present, in order, with sentence-case titles.
- [ ] At least one domain section carries real subject-matter knowledge.
- [ ] Every CONDITIONAL section present has a met trigger; none is filler.
- [ ] All unused CONDITIONAL sections, authoring guidance, and
      `{{UPPER_SNAKE_CASE}}` placeholders are removed.
- [ ] `wc -l SKILL.md` reports fewer than 500 lines, preferably fewer than 200.

## References

CONDITIONAL. Include only when the skill cites absolute external URLs such as
specs, RFCs, books, or vendor docs. Relative links between primitives are never
allowed; absolute external URLs are legitimate technical content.

- [{{EXTERNAL_SOURCE_TITLE}}]({{ABSOLUTE_URL}})
