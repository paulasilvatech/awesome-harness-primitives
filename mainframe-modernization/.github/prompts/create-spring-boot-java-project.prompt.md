---
name: "create-spring-boot-java-project"
description: "Scaffold the SIFAP 2.0 Spring Boot backend skeleton (Java 21 + PostgreSQL 16), deferring the mechanics to the create-spring-boot-java-project skill."
argument-hint: "projectName=<artifactId>"
agent: "implementer"
tools: ["read", "edit", "search", "execute"]
---
# /create-spring-boot-java-project

## Objective

Scaffold a fresh Spring Boot backend skeleton for SIFAP 2.0 and wire its baseline configuration, pinned to the kit's fixed stack (Java 21 + Spring Boot 3.3 + PostgreSQL 16). The step-by-step mechanics live in the [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) skill; this prompt applies them without restating them and overrides the skill's generic defaults.

> [!IMPORTANT]
> `backend/` does not exist yet — this command creates it from scratch in Stage 3. Do not assume an inherited prototype.

## When to Invoke

At the start of Stage 3, when the team creates the `backend/` module for the first time.

## Preconditions

- Java 21, Docker, and Docker Compose are installed
- The team agreed on the artifact name and base package
- No `backend/` module exists yet

## Inputs the Team Must Provide

- `projectName` — the Maven `artifactId` for the new module
- The base package (for example, `com.sifap.<context>`)
- Ask the user for anything that is missing.

## What I Will Do

- Follow the scaffolding steps in the [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) skill
- Override its defaults for this kit: Spring Boot 3.3.x, PostgreSQL 16, no Redis, no MongoDB
- Generate into `backend/` with starters `web, data-jpa, postgresql, validation, testcontainers` plus `springdoc-openapi-starter-webmvc-ui`
- Run `./mvnw clean test` to confirm the skeleton builds

## What I Will NOT Do

- Add `data-redis` or `data-mongodb`, or their configuration blocks
- Scaffold into the repository root, or use Spring Boot 3.4.x
- Create Docker Compose services other than PostgreSQL 16
- Commit secrets (credentials live in environment variables / Azure Key Vault)

## Output Format

```markdown
### Created
- `backend/` Spring Boot 3.3 skeleton (Java 21, PostgreSQL 16)
- Dependencies: web, data-jpa, postgresql, validation, testcontainers, springdoc
- `docker-compose.yaml` (PostgreSQL 16 only) — optional

### Build
`./mvnw clean test` → BUILD SUCCESS
```

## Definition of Done

- [ ] `backend/` contains a Spring Boot 3.3 skeleton on Java 21
- [ ] Dependencies are the kit set; no Redis or MongoDB is present
- [ ] Any Docker Compose contains only PostgreSQL 16
- [ ] `./mvnw clean test` passes and no secret is committed

## Prompt Body

The [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) skill owns the start.spring.io download and configuration steps — read it, then apply it with the kit overrides below.

**Step 1 — Confirm inputs.**
Fix the `artifactId` and base package with the team; verify Java 21 is available.

**Step 2 — Apply the skill.**
Generate the project per the skill, then narrow the dependency set to the kit stack and drop Redis/MongoDB.

**Step 3 — Respect the kit rules.**
Target Spring Boot 3.3.x and PostgreSQL 16, scaffold into `backend/`, and keep Docker Compose (if any) to PostgreSQL 16 only.

**Step 4 — Verify.**
Run `./mvnw clean test` and confirm a green build before handing off.

## Invocation Example

```
/create-spring-boot-java-project projectName=sifap-backend
```
