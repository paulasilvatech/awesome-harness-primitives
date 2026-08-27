---
name: sifap-requirements
description: >-
  Requires SIFAP EARS requirements to use REQ-NNN, valid source_legacy evidence, Given/When/Then
  acceptance criteria, and test lineage. Use when editing specifications or requirement artifacts.
paths:
  - specs/**/*.md
  - 02-modern-spec/**/*.md
  - 01-archaeology/**/*rules*.md
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/mainframe-natural-adabas-classic/instructions/sifap-requirements.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SIFAP requirements conventions - EARS and lineage

These instructions apply to SIFAP requirement and rule artifacts. They are authoritative for identifier
shape, source lineage, and acceptance form; `sifap-requirements-traceability` owns the ordered authoring
and deterministic validation workflow.

## Requirement identity and source

- Use exactly `REQ-NNN` with three digits until an approved repository-wide migration changes it.
- Express one behavior per requirement with an active `SHALL` response.
- Add one `source_legacy:` value within 20 lines of each approved declaration.
- Cite an existing approved corpus file or `[GREENFIELD]` plus a concrete justification.
- Keep candidates with unknown sources outside the approved requirement set.

## Acceptance and tests

- Write concrete Given/When/Then acceptance behavior tied to the same `REQ-NNN`.
- Cite the identifier in requirement-backed tests.
- Report completeness by requirement and risk; use line or branch thresholds only when build configuration
  defines them.
- Treat code/spec drift as a decision question, not proof that either side is automatically correct.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use one `REQ-NNN` namespace | Specifications, tests, and validators stay aligned. |
| Require real source evidence | Generated requirements cannot invent legacy behavior. |
| Keep one behavior per requirement | Acceptance tests remain discriminating and traceable. |
| Separate greenfield decisions | New obligations are not misrepresented as legacy parity. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run the traceability validator | Approve placeholder sources |
| Keep ambiguity as an owned question | Silently choose a business interpretation |
| Use Given/When/Then for behavior | Put implementation details in functional requirements |
| Cite inspected code | Trust comments or generated prose without corroboration |

## Checklist Before Opening a PR

- [ ] Every approved requirement has a unique `REQ-NNN`.
- [ ] Every statement is atomic, testable, and uses the applicable EARS form.
- [ ] Every source resolves to evidence or a justified `[GREENFIELD]` decision.
- [ ] Acceptance criteria are concrete and requirement-backed tests cite the ID.
- [ ] The traceability validator passes with no placeholders.
- [ ] Unknowns, contradictions, and unrun checks are reported explicitly.
