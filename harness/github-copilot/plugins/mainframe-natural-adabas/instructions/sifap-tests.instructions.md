---
description: "Requires SIFAP tests to prove requirement and legacy-behavior coverage with deterministic, privacy-safe fixtures. Use when editing backend, frontend, integration, or equivalence tests."
applyTo: "backend/src/test/**,frontend/**/*.test.*,frontend/**/*.spec.*,**/tests/**,**/*Test.java,**/*IT.java"
---

# SIFAP test conventions - Requirements and equivalence

These instructions apply to SIFAP automated tests. They are authoritative for requirement lineage,
behavior oracles, determinism, and privacy; the target repository's test framework and configured quality
gates define executable commands and numeric thresholds.

## Coverage and oracles

- Cite `REQ-NNN` in tests that verify an approved requirement.
- Prioritize requirement, risk, boundary, negative, error, and legacy-equivalence coverage.
- Use line or branch thresholds only when configured in the real build; do not invent 60, 80, or 100
  percent goals in a primitive.
- Capture legacy behavior before transformation and classify every modernized difference.
- Use Testcontainers for PostgreSQL semantics when persistence behavior matters.

## Determinism and privacy

- Control time, randomness, locale, ordering, concurrency, and external responses.
- Use synthetic fixtures and never copy production CPF, benefit amounts, credentials, or records.
- Compare financial values with exact decimal semantics.
- Write assertions that fail on a real behavior defect; reject tautologies and snapshot-only evidence.

## Conventions

| Rule | Rationale |
| --- | --- |
| Trace tests to `REQ-NNN` | Requirement coverage stays reviewable. |
| Pin legacy behavior before rewrite | Drift becomes executable evidence. |
| Use configured thresholds only | Primitives do not fabricate quality policy. |
| Keep fixtures deterministic and synthetic | Suites remain trustworthy and privacy-safe. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run a focused test before the broader suite | Claim green from compilation alone |
| Test observable behavior | Assert private implementation details |
| Record intentional differences | Update golden masters merely to pass |
| Report flaky tests as defects | Skip or weaken tests to force green |

## Checklist Before Opening a PR

- [ ] Changed behavior maps to approved requirements or explicit characterization evidence.
- [ ] Tests cover positive, boundary, negative, error, and drift paths as risk requires.
- [ ] Fixtures are deterministic, synthetic, and free of sensitive data.
- [ ] Assertions can fail on meaningful behavior changes.
- [ ] Focused and broader relevant suites pass, or exact blockers are reported.
- [ ] Coverage claims use repository configuration and actual reports.
