---
name: breakdown-test
description: >-
  Create comprehensive test planning, QA strategy, GitHub issue breakdowns, and quality validation plans from feature artifacts. Use when asked to produce a test strategy, break down test work, plan QA for an epic or feature, apply ISTQB techniques, map ISO 25010 quality characteristics, or create test issues for GitHub project management.
---

# Test planning and quality assurance

Turn feature artifacts into a test strategy, test-issue checklist, and QA plan aligned with ISTQB test design, ISO 25010 quality attributes, risk-based testing, GitHub issue standards, and measurable quality gates.

## When to invoke

- "Create a test strategy for this feature."
- "Break down QA tasks for this epic."
- "Generate GitHub test issues from the implementation plan."
- "Apply ISTQB and ISO 25010 to this project plan."
- "Define quality gates and coverage targets."

## Prerequisites and context

Use the available feature artifacts as source material. Expected project paths are:

| Artifact | Path |
| --- | --- |
| Feature PRD | `/docs/ways-of-work/plan/{epic-name}/{feature-name}.md` |
| Technical breakdown | `/docs/ways-of-work/plan/{epic-name}/{feature-name}/technical-breakdown.md` |
| Implementation plan | `/docs/ways-of-work/plan/{epic-name}/{feature-name}/implementation-plan.md` |
| GitHub project plan | `/docs/ways-of-work/plan/{epic-name}/{feature-name}/project-plan.md` |

Create or update these outputs:

| Output | Path |
| --- | --- |
| Test strategy | `/docs/ways-of-work/plan/{epic-name}/{feature-name}/test-strategy.md` |
| Test issues checklist | `/docs/ways-of-work/plan/{epic-name}/{feature-name}/test-issues-checklist.md` |
| Quality assurance plan | `/docs/ways-of-work/plan/{epic-name}/{feature-name}/qa-plan.md` |

## Procedure

1. Read the PRD, technical breakdown, implementation plan, and project plan.
2. Extract scope, acceptance criteria, architecture, data flows, risks, dependencies, and release constraints.
3. Select ISTQB techniques and test types based on the feature risk profile.
4. Map ISO 25010 characteristics to measurable checks and priorities.
5. Create test issues by level, type, dependency, estimate, label, and acceptance criteria.
6. Define QA entry criteria, exit criteria, metrics, escalation, and quality gates.
7. Write the three output files and verify they cross-reference the same feature, risks, dependencies, and targets.

## ISTQB and ISO 25010 framework

| Area | Apply |
| --- | --- |
| Test process activities | Planning, monitoring, analysis, design, implementation, execution, completion. |
| Test design techniques | Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, State Transition Testing, and Experience-Based Testing. |
| Test types | Functional, Non-Functional, Structural, and Change-Related testing. |
| Risk-Based Testing | Rank scenarios by probability, impact, detectability, and mitigation. |
| ISO 25010 | Functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability. |

## Test strategy content

| Section | Required content |
| --- | --- |
| Test Strategy Overview | Testing Scope, Quality Objectives, Risk Assessment, Test Approach. |
| ISTQB Framework Implementation | Technique selection, test-type coverage matrix, and rationale. |
| ISO 25010 Quality Characteristics Assessment | Priority matrix with measurement approach for each characteristic. |
| Test Environment and Data Strategy | Hardware, software, network, privacy, maintenance, tools, automation platform, and CI/CD Integration. |

For each ISO 25010 characteristic, name the validation focus: Functional Suitability covers completeness, correctness, appropriateness; Performance Efficiency covers time behavior, resource utilization, capacity; Compatibility covers co-existence and interoperability; Usability covers UI, accessibility, and UX; Reliability covers fault tolerance, recoverability, availability; Security covers confidentiality, integrity, authentication, authorization; Maintainability covers modularity, reusability, testability; Portability covers adaptability, installability, replaceability.

## Test issue breakdown rules

| Issue type | Include |
| --- | --- |
| Test Strategy Issue | Overall testing approach and quality validation plan. |
| Unit Test Issues | Component-level testing for each implementation task, estimated `0.5-1` story point per component. |
| Integration Test Issues | Interface and interaction tests, estimated `1-2` story points per interface. |
| End-to-End Test Issues | Complete user workflows using Playwright, estimated `2-3` story points per workflow. |
| Performance Test Issues | Non-functional requirement validation, estimated `3-5` story points per performance requirement. |
| Security Test Issues | Security requirement and vulnerability testing, estimated `2-4` story points per security requirement. |
| Accessibility Test Issues | WCAG compliance and inclusive design validation. |
| Regression Test Issues | Risk-based regression and confirmation testing. |

Document Implementation Dependencies, Environment Dependencies, Tool Dependencies, Cross-Team Dependencies, Sequential Dependencies, Parallel Development, Critical Path Identification, Resource Allocation, Skill-Based Assignment, Capacity Planning, Knowledge Transfer, and Cross-Training Opportunities.

## Quality targets and labels

| Metric | Target |
| --- | --- |
| Code Coverage | `>80%` line coverage and `>90%` branch coverage for critical paths. |
| Functional Coverage | `100%` acceptance criteria validation. |
| Risk Coverage | `100%` high-risk scenario validation. |
| Quality Characteristics Coverage | Validation approach for every applicable ISO 25010 characteristic. |
| Defect Detection Rate | `>95%` of defects found before production. |
| Test Execution Efficiency | `>90%` test automation coverage. |
| Quality Gate Compliance | `100%` gates passed before release. |
| Test Planning Time | `<2 hours` for comprehensive strategy. |
| Test Implementation Speed | `<1 day` per story point. |
| Quality Feedback Time | `<2 hours` from test completion. |
| Documentation Completeness | `100%` of test issues have complete template information. |

Use labels consistently: `unit-test`, `integration-test`, `e2e-test`, `performance-test`, `security-test`, `quality-gate`, `iso25010`, `istqb-technique`, `risk-based`, `test-critical`, `test-high`, `test-medium`, `test-low`, `frontend-test`, `backend-test`, `api-test`, `database-test`, `test-strategy`, `istqb`, `quality-gates`, `playwright`, `quality-validation`, `quality-assurance`.

## GitHub issue templates

### Test strategy issue

```markdown
# Test Strategy: {Feature Name}

## Test Strategy Overview
{Summary of testing approach based on ISTQB and ISO 25010}

## ISTQB Framework Application
**Test Design Techniques Used:**
- [ ] Equivalence Partitioning
- [ ] Boundary Value Analysis
- [ ] Decision Table Testing
- [ ] State Transition Testing
- [ ] Experience-Based Testing

**Test Types Coverage:**
- [ ] Functional Testing
- [ ] Non-Functional Testing
- [ ] Structural Testing
- [ ] Change-Related Testing (Regression)

## ISO 25010 Quality Characteristics
- [ ] Functional Suitability: {Critical/High/Medium/Low}
- [ ] Performance Efficiency: {Critical/High/Medium/Low}
- [ ] Compatibility: {Critical/High/Medium/Low}
- [ ] Usability: {Critical/High/Medium/Low}
- [ ] Reliability: {Critical/High/Medium/Low}
- [ ] Security: {Critical/High/Medium/Low}
- [ ] Maintainability: {Critical/High/Medium/Low}
- [ ] Portability: {Critical/High/Medium/Low}

## Quality Gates
- [ ] Entry criteria defined
- [ ] Exit criteria established
- [ ] Quality thresholds documented

## Labels
`test-strategy`, `istqb`, `iso25010`, `quality-gates`

## Estimate
{Strategic planning effort: 2-3 story points}
```

### Playwright test implementation issue

```markdown
# Playwright Tests: {Story/Component Name}

## Test Implementation Scope
{Specific user story or component being tested}

## ISTQB Test Case Design
**Test Design Technique**: {Selected ISTQB technique}
**Test Type**: {Functional/Non-Functional/Structural/Change-Related}

## Test Cases to Implement
- [ ] Happy path scenarios
- [ ] Error handling validation
- [ ] Boundary value testing
- [ ] Input validation testing
- [ ] Performance testing (response time < {threshold})
- [ ] Accessibility testing (WCAG compliance)
- [ ] Cross-browser compatibility
- [ ] Mobile responsiveness

## Playwright Implementation Tasks
- [ ] Page Object Model development
- [ ] Test fixture setup
- [ ] Test data management
- [ ] Test case implementation
- [ ] Visual regression tests
- [ ] CI/CD integration

## Acceptance Criteria
- [ ] All test cases pass
- [ ] Code coverage targets met (>80%)
- [ ] Performance thresholds validated
- [ ] Accessibility standards verified

## Labels
`playwright`, `e2e-test`, `quality-validation`

## Estimate
{Test implementation effort: 2-5 story points}
```

### Quality assurance issue

```markdown
# Quality Assurance: {Feature Name}

## Quality Validation Scope
{Overall quality validation for feature/epic}

## ISO 25010 Quality Assessment
- [ ] Functional Suitability: Completeness, correctness, appropriateness
- [ ] Performance Efficiency: Time behavior, resource utilization, capacity
- [ ] Usability: Interface aesthetics, accessibility, learnability, operability
- [ ] Security: Confidentiality, integrity, authentication, authorization
- [ ] Reliability: Fault tolerance, recovery, availability
- [ ] Compatibility: Browser, device, integration compatibility
- [ ] Maintainability: Code quality, modularity, testability
- [ ] Portability: Environment adaptability, installation procedures

## Quality Gates Validation
**Entry Criteria:**
- [ ] All implementation tasks completed
- [ ] Unit tests passing
- [ ] Code review approved

**Exit Criteria:**
- [ ] All test types completed with >95% pass rate
- [ ] No critical/high severity defects
- [ ] Performance benchmarks met
- [ ] Security validation passed

## Quality Metrics
- [ ] Test coverage: {target}%
- [ ] Defect density: <{threshold} defects/KLOC
- [ ] Performance: Response time <{threshold}ms
- [ ] Accessibility: WCAG {level} compliance
- [ ] Security: Zero critical vulnerabilities

## Labels
`quality-assurance`, `iso25010`, `quality-gates`

## Estimate
{Quality validation effort: 3-5 story points}
```


## Test technique terminology

Use `white-box`, `experience-based`, `non-functional`, and `change-related` language when naming test techniques and test types because those terms map directly to ISTQB terminology. Add a `high-uncertainty` buffer to estimates when risk, unclear requirements, external dependencies, or unfamiliar tooling make the test work hard to size.

## Output template

```markdown
## Test planning result — {epic-name}/{feature-name}

**Status:** complete | needs input | blocked
**Artifacts reviewed:** PRD, technical breakdown, implementation plan, project plan

### Files created or updated
- `/docs/ways-of-work/plan/{epic-name}/{feature-name}/test-strategy.md`
- `/docs/ways-of-work/plan/{epic-name}/{feature-name}/test-issues-checklist.md`
- `/docs/ways-of-work/plan/{epic-name}/{feature-name}/qa-plan.md`

### Coverage plan
| Level | Techniques | Quality characteristics | Target | Issues |
| --- | --- | --- | --- | --- |
| Unit | <techniques> | <ISO 25010 areas> | <target> | <issue titles> |

### Quality gates
- Entry criteria: <summary>
- Exit criteria: <summary>
- Escalation: <summary>

### Validation
- Source artifacts aligned: pass | fail
- Dependencies checked for circular blockers: pass | fail
- Labels and estimates assigned: pass | fail
```

## Quality gate

- [ ] All four expected input artifacts were used or missing artifacts were reported.
- [ ] The three output files were created or updated at the required paths.
- [ ] ISTQB techniques and test types are mapped to feature risks and acceptance criteria.
- [ ] Every applicable ISO 25010 characteristic has a validation approach.
- [ ] Coverage targets include code, functional, risk, and quality-characteristic coverage.
- [ ] GitHub test issues include dependencies, labels, estimates, and acceptance criteria.
- [ ] QA gates include entry criteria, exit criteria, metrics, and escalation procedures.
- [ ] Circular dependencies and critical path risks were checked.
