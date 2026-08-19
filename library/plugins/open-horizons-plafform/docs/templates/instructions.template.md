---
description: "{{DESCRIPTION_OF_CONVENTIONS}} Use when {{WHEN_THESE_INSTRUCTIONS_APPLY}}."
applyTo: "{{COMMA_SEPARATED_GLOBS}}"
---

# {{TOPIC}} Conventions

## Scope and Stack Context

These instructions apply to `{{SCOPE_DESCRIPTION}}` matched by the `applyTo` globs. They assume `{{STACK_TOOLS_AND_VERSION_CONTEXT}}` and use `{{DEFAULT_APPROACH}}` when several valid options exist.

They define passive conventions and boundaries for changes in this scope. They do not define a step-by-step workflow; detailed setup, migration, generation, or review procedures belong in a skill.

> **Authoring note — remove before saving:** Replace every `{{UPPER_SNAKE_CASE}}` placeholder, set `applyTo` to one quoted comma-separated glob string (for example, `"**/*.ext,src/**"`), and remove all optional sections or rows that do not apply. Use direct imperatives; reserve MUST and NEVER for constraints whose violation risks correctness, security, data loss, or compatibility.

## Authoritative Sources and Precedence

Follow these sources in order:

1. `{{PRIMARY_AUTHORITY_NAME}}` for `{{PRIMARY_AUTHORITY_SCOPE}}`.
2. `{{SECONDARY_AUTHORITY_NAME}}` for `{{SECONDARY_AUTHORITY_SCOPE}}`.
3. `{{FALLBACK_SOURCE_NAME}}` only when it is consistent with the higher-priority sources.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another source.

## Responsibility Split (Optional)

This file owns `{{OWNED_RESPONSIBILITIES}}`. `{{OTHER_PRIMITIVE_NAME}}` ({{OTHER_PRIMITIVE_TYPE}}) owns `{{DEFERRED_RESPONSIBILITIES}}`; follow that primitive for those concerns instead of restating its rules here.

## Core Conventions

| Rule | Rationale |
| --- | --- |
| {{RULE_1_AS_DIRECT_IMPERATIVE}} | {{RULE_1_FAILURE_OR_COST_PREVENTED}} |
| {{RULE_2_AS_DIRECT_IMPERATIVE}} | {{RULE_2_FAILURE_OR_COST_PREVENTED}} |
| {{RULE_3_AS_DIRECT_IMPERATIVE}} | {{RULE_3_FAILURE_OR_COST_PREVENTED}} |

## {{CONVENTION_AREA}}

{{SHORT_CONTEXT_FOR_THIS_AREA}}

- {{AREA_RULE_1}} — {{AREA_RULE_1_RATIONALE}}
- {{AREA_RULE_2}} — {{AREA_RULE_2_RATIONALE}}
- {{AREA_RULE_3}} — {{AREA_RULE_3_RATIONALE}}

## Good / Bad Examples

The examples below illustrate `{{RULE_DEMONSTRATED_BY_EXAMPLES}}`.

**Good**

```{{LANGUAGE}}
{{SMALL_GOOD_EXAMPLE}}
```

Why: {{WHY_THE_GOOD_EXAMPLE_FOLLOWS_THE_CONVENTION}}

**Bad**

```{{LANGUAGE}}
{{SMALL_BAD_EXAMPLE}}
```

Why: {{WHY_THE_BAD_EXAMPLE_BREAKS_THE_CONVENTION}}

## Do / Do Not

| Do | Do not |
| --- | --- |
| {{PREFERRED_PRACTICE_1}} | {{MISTAKE_1}} |
| {{PREFERRED_PRACTICE_2}} | {{MISTAKE_2}} |
| {{PREFERRED_PRACTICE_3}} | {{MISTAKE_3}} |

## Verification Checklist

- [ ] The change stays within `{{SCOPE_DESCRIPTION}}` and respects the responsibility split.
- [ ] The implementation follows the authoritative sources and the conventions above.
- [ ] `{{CHANGE_SPECIFIC_CONDITION}}` is satisfied.
- [ ] Relevant formatting, linting, testing, or validation commands pass: `{{VALIDATION_COMMANDS}}`.
- [ ] `{{SECURITY_RELIABILITY_OR_HYGIENE_CONDITION}}` is verified.
- [ ] The change contains no unrelated edits or leftover placeholders.

## Related Primitives (Optional)

Remove this section when no related primitive is needed. Refer to each primitive by name and type in text, never by a relative path.

- `{{RELATED_PRIMITIVE_NAME}}` ({{RELATED_PRIMITIVE_TYPE}}): use it for {{RELATED_PRIMITIVE_PURPOSE}}.
