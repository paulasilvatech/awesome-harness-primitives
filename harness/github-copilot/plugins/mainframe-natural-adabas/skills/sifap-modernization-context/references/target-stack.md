# SIFAP target stack

The workshop baseline is:

| Area | Baseline |
| --- | --- |
| Backend | Java 21, Spring Boot 3.3, JPA/Hibernate |
| Database | PostgreSQL 16 with Flyway |
| Frontend | Next.js 15 App Router, React 19, TypeScript strict, Tailwind CSS, shadcn/ui |
| Testing | JUnit 5, Testcontainers, Vitest, Testing Library, Playwright where applicable |
| Infrastructure | Terraform with an AzureRM 3.x compatibility baseline |
| Delivery | GitHub Actions, Docker, and Docker Compose when needed |

These are deliberate workshop compatibility constraints, not claims that the versions are current or
latest. Change a baseline only through an approved ADR that records compatibility evidence, migration
impact, and validation results.

Default architecture is a modular monolith. Module boundaries follow business evidence; they do not
default to one deployable per legacy file or one microservice per bounded context.

For Adabas MU and PE structures, prefer explicit relational modeling when fields have stable structure
or query semantics. Use JSONB only when evidence supports semi-structured storage and the decision is
recorded in an ADR.
