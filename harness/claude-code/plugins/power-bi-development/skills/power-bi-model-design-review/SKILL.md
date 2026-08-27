---
name: power-bi-model-design-review
description: >-
  Review Power BI data model architecture, relationships, storage modes, performance, security,
  governance, and maintainability. Use this skill when asked for a Power BI model design review,
  star schema assessment, relationship design evaluation, pre-production model review,
  modernization assessment, or optimization roadmap.
---

<!-- Generated from harness/github-copilot/plugins/power-bi-development/skills/power-bi-model-design-review/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power BI model design review

Evaluate a Power BI semantic model from business purpose, table structure, relationship network, storage strategy, DAX and governance evidence, then return prioritized findings and an implementation roadmap.

## When to invoke

- "Review this Power BI data model design."
- "Check whether our Power BI model follows star schema best practices."
- "Evaluate the relationships, storage modes, and performance risks in this model."
- "Run a pre-production Power BI semantic model review."
- "Create a modernization roadmap for this Power BI model."

## Source evidence

Use the model description, business purpose, architecture overview, table and relationship metadata, performance requirements, known issues, specific review focus areas, and available time/resource constraints. If the user omits metadata, review what is available and mark missing evidence explicitly.

## Review scope

| Area | Inspect | Good evidence |
| --- | --- | --- |
| Schema architecture | Fact tables, dimension tables, bridge tables, star vs. snowflake patterns, grain definition and consistency | Clear separation of fact and dimension tables; dimension tables contain descriptive attributes; bridge tables are justified for many-to-many |
| Table design quality | Names, data types, primary key and foreign key columns, descriptions | Meaningful table and column names; appropriate data types; consistent naming conventions; adequate documentation and descriptions |
| Relationships | Cardinality, filter directions, referential integrity settings, circular paths | Correct `1:*`, `*:*`, or `1:1`; single-direction filters by default; hidden foreign key columns from report view; minimal circular relationship paths; cross-filtering behavior documented |
| Storage mode strategy | Import, DirectQuery, Composite, Dual, Hybrid | Import for small-medium datasets; DirectQuery for large/real-time data; Dual for dimensions; Hybrid for fact tables when freshness and history differ |
| Performance architecture | Model size, compression efficiency, calculated columns vs. measures, DAX complexity, aggregations | Integer keys over text keys; low-cardinality relationship columns; unnecessary columns removed; aggregation and caching strategies documented |
| Maintainability | Measure organization, business rules, source documentation, version control | Logical grouping of related measures; modular design; clear separation of concerns; impact assessment and rollback procedures |
| Security and compliance | RLS, role-based access, sensitive data, audit and retention policies | Tested Row-Level Security; performance impact assessed; privacy and compliance requirements handled |

## Criteria

### Schema architecture

- [ ] Fact table grain is stated, consistent, and compatible with all measures.
- [ ] Dimension tables carry descriptive attributes and hierarchies instead of repeating dimension data in facts.
- [ ] Snowflaking is minimal and justified by maintenance, reuse, or size constraints.
- [ ] Many-to-many relationships use bridge tables or another explicit design instead of accidental ambiguity.
- [ ] Date table implementation supports the model's time intelligence needs.

### Relationship design

- [ ] Cardinality settings match data reality, including missing/orphaned records and referential integrity assumptions.
- [ ] Bidirectional relationships are present only when required and do not create ambiguous filter propagation paths.
- [ ] Relationship columns use efficient data types, preferably integer keys over high-cardinality text.
- [ ] Cross-filtering impact is understood for report interactions, RLS, and composite models.

### Data quality and integrity

- [ ] All required business entities and critical relationships are represented.
- [ ] Related columns use consistent data types, formatting, and encoding.
- [ ] NULL values, orphaned records, slowly changing dimensions, surrogate keys, natural keys, and reference data are handled deliberately.
- [ ] Business rules, transformations, and calculated fields are traceable and validated.

### Performance and scalability

- [ ] Data reduction opportunities are identified: unnecessary columns, redundant data, historical archiving, and pre-aggregation.
- [ ] High-cardinality columns, calculated columns in large tables, and measure complexity are flagged.
- [ ] Refresh requirements, query performance expectations, growth projections, and concurrent user capacity are considered.
- [ ] DirectQuery indexing requirements, aggregation tables, composite model optimization, and cache utilization are reviewed when applicable.

### Governance and readiness

- [ ] Table and column descriptions, relationship justification, data source documentation, and measure calculation explanations are present.
- [ ] Testing, validation, deployment, rollback, and user communication procedures are defined.
- [ ] RLS design, role-based access control, dynamic security patterns, audit trails, data retention, and sensitive data handling are validated.

## Review depth

| Review type | Timebox | Focus areas | Deliverables |
| --- | --- | --- | --- |
| Quick assessment | 30 minutes | Star schema principles, storage modes, relationships, hidden foreign keys, Date table, circular relationships, DAX variable use, calculated columns, naming, basic documentation | Top risks and quick wins |
| Comprehensive review | 4-8 hours | Architecture and design, data quality and integrity, performance and optimization, governance and security | Detailed review report with issue-level recommendations |
| Pre-production review | As needed before launch | Functionality completeness, performance validation, security implementation, user acceptance criteria, go-live readiness | Go/No-go recommendation, critical issue plan, benchmark validation, training needs, post-launch monitoring plan |
| Performance optimization review | As needed for slow models | Bottleneck identification, optimization opportunities, capacity planning, scalability, monitoring and alerting | Performance improvement roadmap, expected gains, priority matrix, success criteria |
| Modernization assessment | As needed for legacy models | Current state vs. best practices, technology upgrades, architecture improvement, process optimization, skills and training | Modernization strategy, cost-benefit analysis, risk mitigation, timeline, resource requirements, change management plan |

Treat defects that affect functionality/performance as high priority even when the remediation work is small.

## Recommendation format

For each issue, include:

| Field | Required content |
| --- | --- |
| Issue Description | Clear problem statement, impact on performance/maintenance/accuracy, risk level, urgency |
| Recommended Solution | Specific resolution steps, alternatives, expected benefits, implementation complexity, required resources, timeline |
| Implementation Guidance | Step-by-step instructions, code examples where appropriate, testing and validation, rollback considerations, success criteria |

## Gotchas

- **Do not reward complexity**: snowflake schemas, bidirectional filters, and many-to-many relationships require evidence because they increase ambiguity and performance cost.
- **Do not review storage mode in isolation**: Import, DirectQuery, Composite, Dual, and Hybrid choices affect relationships, aggregations, refresh, and user experience together.
- **Do not treat documentation as cosmetic**: missing descriptions, business rules, and relationship justifications are maintainability defects.

## Output template

```markdown
## Data model review summary — <model name>

**Verdict:** approve | approve with risks | fix required | not enough evidence
**Business domain and scope:** <domain>
**Primary use cases and user groups:** <summary>
**Current size and complexity metrics:** <tables, relationships, rows, storage modes, if known>

### Key findings
- **Critical issues requiring immediate attention:** <count and summary>
- **Performance optimization opportunities:** <count and summary>
- **Best practice compliance assessment:** <summary>
- **Security and governance status:** <summary>

### Priority recommendations
1. **High Priority:** <critical issues impacting functionality or performance>
2. **Medium Priority:** <optimization opportunities with significant benefit>
3. **Low Priority:** <best practice improvements and future considerations>

### Detailed findings
| Area | Finding | Impact | Risk | Recommendation | Validation |
| --- | --- | --- | --- | --- | --- |
| Schema Architecture | <fact/dimension/relationship issue> | <performance/maintenance/accuracy> | High | <specific fix> | <test or evidence> |
| Performance Architecture | <storage/DAX/size issue> | <impact> | Medium | <specific fix> | <benchmark or review> |
| Governance and Security | <RLS/documentation/compliance issue> | <impact> | Medium | <specific fix> | <evidence> |

### Implementation roadmap
- **Quick wins (1-2 weeks):** <actions>
- **Short-term improvements (1-3 months):** <actions>
- **Long-term strategic enhancements (3-12 months):** <actions>
```

## Quality gate

- [ ] The review states the model purpose, scope, known constraints, and evidence used.
- [ ] Fact table grain, dimension quality, relationship cardinality, filter direction, and storage modes were checked.
- [ ] Performance findings consider model size, DAX complexity, refresh, query performance, scalability, and concurrent usage.
- [ ] Security findings cover Row-Level Security, role-based access control, sensitive data, compliance, audit trail, and retention where applicable.
- [ ] Each issue includes impact, risk level, recommendation, implementation guidance, testing and validation, rollback consideration, and success criteria.
- [ ] The output follows `## Output template` exactly and separates high, medium, and low priorities.
