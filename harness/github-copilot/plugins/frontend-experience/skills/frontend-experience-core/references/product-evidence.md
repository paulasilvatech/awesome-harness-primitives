# Product evidence inventory

Collect only evidence needed for the active frontend decision.

| Area | Inspect | Record |
| --- | --- | --- |
| User and job | Approved requirements, research, support cases, product docs | Actor, outcome, environment, frequency, urgency, error cost |
| Product language | Routes, labels, enums, statuses, permissions, domain models | Real nouns and constraints; placeholder content is not evidence |
| Existing experience | Runtime, screenshots, components, navigation, content | Current behavior, strengths, defects, state transitions |
| Visual system | Tokens, themes, typography, icons, imagery, spacing, motion | Reusable roles and explicit gaps |
| Data and contracts | API schemas, clients, fixtures, errors, auth, events | Shapes, units, freshness, partial states, failure semantics |
| Surfaces | Browser support, native targets, windows, viewports, inputs | Required profiles and unsupported profiles |
| Inclusion | Locale, RTL, long content, zoom, dynamic type, AT, motion | Applicable adaptations and manual evidence |
| Quality | Tests, CI, budgets, incident history, release policy | Existing commands, environments, risk and evidence gaps |

## Confidence

- **Verified:** directly observed in approved code, runtime, contract, or product evidence.
- **Inferred:** supported by multiple clues but not explicitly approved.
- **Unknown:** missing or conflicting; requires a decision.

Do not treat examples, generated fixtures, design trends, or another product's behavior as facts about the consuming product.
