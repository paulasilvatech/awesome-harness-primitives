---
description: "{{DESCRIPTION_OF_CONVENTIONS}} Use when {{WHEN_THESE_INSTRUCTIONS_APPLY}}."
applyTo: "{{COMMA_SEPARATED_GLOBS}}"
---

# {{TOPIC}} Conventions — {{SHORT_QUALIFIER}}

MANDATORY authority paragraph. Follow the reference style: state what the file
covers, declare what it is authoritative for, and name what wins when another
primitive defines a stricter or broader rule. Keep it to one dense paragraph
placed directly under the H1, before the first `##` section.

These instructions apply to `{{SCOPE_DESCRIPTION}}` matched by the `applyTo` globs. They assume `{{STACK_TOOLS_AND_VERSION_CONTEXT}}` and use `{{DEFAULT_APPROACH}}` when several valid options exist. They are authoritative for `{{OWNED_CONCERNS}}` in the matched files; `{{HIGHER_AUTHORITY_SOURCE}}` wins where anything here appears to differ. They define passive conventions and boundaries, not a step-by-step workflow; detailed setup, migration, generation, or review procedures belong in a skill.

> **Authoring note — remove before saving:** Replace every `{{UPPER_SNAKE_CASE}}` placeholder, set `applyTo` to one quoted comma-separated glob string (for example, `"**/*.ext,src/**"`), and remove every CONDITIONAL section or row whose trigger is not met. Use direct imperatives; reserve MUST and NEVER for constraints whose violation risks correctness, security, data loss, or compatibility.

## Section map

Remove this section before saving.

Instructions have a free middle and a fixed ending. The domain sections carry
the weight; the closing trio is invariant across all reference files.

| Section | Status | Include when |
| --- | --- | --- |
| Authority paragraph under the H1 | MANDATORY | Always. One dense paragraph declaring scope, what the file is authoritative for, and what wins on conflict. All three reference files open this way, with no `## Scope` section. |
| Domain sections | MANDATORY | Always. One or more, freely titled after the real subject areas, for example `## State`, `## Error Handling Pattern`, `## Accessibility (WCAG 2.1 AA)`. This is the bulk of the file. |
| `## Conventions` | MANDATORY | Always. Use a `\| Rule \| Rationale \|` table. |
| `## Do / Do Not` | MANDATORY | Always. Use a `\| Do \| Do not \|` table. |
| `## Checklist Before Opening a PR` | MANDATORY | Always. Last section unless `## References` follows. Checkboxes only. |
| `## Authoritative Sources and Precedence` | CONDITIONAL | Precedence is complex enough that one paragraph cannot carry it, for example three or more competing sources. |
| `## Responsibility Split` | CONDITIONAL | Another primitive owns an overlapping slice of the same files. |
| `## Good / Bad Examples` | CONDITIONAL | A convention is hard to follow from the rule text alone. |
| `## Related Primitives` | CONDITIONAL | Another primitive owns an adjacent responsibility worth naming. |
| `## References` | CONDITIONAL | The file cites absolute external URLs such as specs, RFCs, books, or vendor docs. Place it after the checklist. |

Do not omit the `\| Rule \| Rationale \|` and `\| Do \| Do not \|` tables. A rule
without a rationale gets overridden by the first person who disagrees with it.

## Authoritative Sources and Precedence

CONDITIONAL. Include only when precedence is complex enough that the authority paragraph cannot carry it, for example three or more competing sources. Otherwise delete and keep the precedence statement in the authority paragraph.

Follow these sources in order:

1. `{{PRIMARY_AUTHORITY_NAME}}` for `{{PRIMARY_AUTHORITY_SCOPE}}`.
2. `{{SECONDARY_AUTHORITY_NAME}}` for `{{SECONDARY_AUTHORITY_SCOPE}}`.
3. `{{FALLBACK_SOURCE_NAME}}` only when it is consistent with the higher-priority sources.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another source.

## Responsibility Split

CONDITIONAL. Include only when another primitive owns an overlapping slice of the same files. Otherwise delete.

This file owns `{{OWNED_RESPONSIBILITIES}}`. `{{OTHER_PRIMITIVE_NAME}}` ({{OTHER_PRIMITIVE_TYPE}}) owns `{{DEFERRED_RESPONSIBILITIES}}`; follow that primitive for those concerns instead of restating its rules here.

## {{CONVENTION_AREA}}

MANDATORY, repeatable. Title each section after the real subject area, not after this template. Add as many as the domain requires; these sections are the bulk of the file.

{{SHORT_CONTEXT_FOR_THIS_AREA}}

- {{AREA_RULE_1}} — {{AREA_RULE_1_RATIONALE}}
- {{AREA_RULE_2}} — {{AREA_RULE_2_RATIONALE}}
- {{AREA_RULE_3}} — {{AREA_RULE_3_RATIONALE}}

## Good / Bad Examples

CONDITIONAL. Include only when a convention is hard to follow from the rule text alone. Otherwise delete.

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

## Conventions

MANDATORY. Cross-cutting rules that do not belong to a single domain section. Every rule carries a rationale.

| Rule | Rationale |
| --- | --- |
| {{RULE_1_AS_DIRECT_IMPERATIVE}} | {{RULE_1_FAILURE_OR_COST_PREVENTED}} |
| {{RULE_2_AS_DIRECT_IMPERATIVE}} | {{RULE_2_FAILURE_OR_COST_PREVENTED}} |
| {{RULE_3_AS_DIRECT_IMPERATIVE}} | {{RULE_3_FAILURE_OR_COST_PREVENTED}} |

## Do / Do Not

MANDATORY.

| Do | Do not |
| --- | --- |
| {{PREFERRED_PRACTICE_1}} | {{MISTAKE_1}} |
| {{PREFERRED_PRACTICE_2}} | {{MISTAKE_2}} |
| {{PREFERRED_PRACTICE_3}} | {{MISTAKE_3}} |

## Checklist Before Opening a PR

MANDATORY. Checkboxes only. Last section unless `## References` follows.

- [ ] The change stays within `{{SCOPE_DESCRIPTION}}` and respects the responsibility split.
- [ ] The implementation follows the authoritative sources and the conventions above.
- [ ] `{{CHANGE_SPECIFIC_CONDITION}}` is satisfied.
- [ ] Relevant formatting, linting, testing, or validation commands pass: `{{VALIDATION_COMMANDS}}`.
- [ ] `{{SECURITY_RELIABILITY_OR_HYGIENE_CONDITION}}` is verified.
- [ ] The change contains no unrelated edits or leftover placeholders.

## Related Primitives

CONDITIONAL. Include only when another primitive owns an adjacent responsibility worth naming. Otherwise delete. Refer to each primitive by name and type in text, never by a relative path.

- `{{RELATED_PRIMITIVE_NAME}}` ({{RELATED_PRIMITIVE_TYPE}}): use it for {{RELATED_PRIMITIVE_PURPOSE}}.

## References

CONDITIONAL. Include only when the file cites absolute external URLs such as specs, RFCs, books, or vendor docs. Relative links between primitives are never allowed; absolute external URLs are legitimate technical content.

- [{{EXTERNAL_SOURCE_TITLE}}]({{ABSOLUTE_URL}})
