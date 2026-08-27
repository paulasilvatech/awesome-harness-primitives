---
name: create-spring-boot-kotlin-project
description: >-
  Create a Spring Boot Kotlin project skeleton from Spring Initializr with Gradle Kotlin DSL, Java
  21, WebFlux, reactive data dependencies, SpringDoc, ArchUnit, and local Redis/PostgreSQL/MongoDB
  Docker services. Use when asked to create or scaffold a Spring Boot Kotlin project.
---

<!-- Generated from harness/github-copilot/plugins/java-kotlin-development/skills/create-spring-boot-kotlin-project/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create Spring Boot Kotlin project

Scaffolds a Kotlin Spring Boot application from Spring Initializr, customizes dependencies and local service configuration, and validates the generated project with Gradle tests.

## When to invoke

- "Create a Spring Boot Kotlin project."
- "Scaffold a reactive Kotlin Spring Boot service."
- "Generate a Spring Boot Kotlin starter with Redis, PostgreSQL, and MongoDB."
- "Set up a Gradle Kotlin Spring Boot skeleton."

## Prerequisites and context

- Java 21 is installed; verify with `java -version`.
- Docker and Docker Compose are installed if local services are required.
- Customize `${input:projectName:demo-kotlin}` before running commands when the user supplies a project name.
- Customize `artifactId`, `packageName`, and `bootVersion` in the Spring Initializr request when the project name, package, or Spring Boot version should differ.

## Procedure

1. Check Java with `java -version`.
2. Download the Spring Initializr archive from https://start.spring.io/starter.zip .
3. Unzip `starter.zip` into `./${input:projectName:demo-kotlin}`.
4. Remove `starter.zip` after extraction with `rm -f starter.zip`.
5. Add the extra dependencies and application properties below.
6. Create `docker-compose.yaml` with Redis, PostgreSQL, and MongoDB services when local backing services are needed.
7. Add generated data directories to `.gitignore`.
8. Run `./gradlew clean test` from the generated project root.

## Spring Initializr request

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-kotlin} \
  -d bootVersion=3.4.5 \
  -d dependencies=configuration-processor,webflux,data-r2dbc,postgresql,data-redis-reactive,data-mongodb-reactive,validation,cache,testcontainers \
  -d javaVersion=21 \
  -d language=kotlin \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=gradle-project-kotlin \
  -o starter.zip
unzip starter.zip -d ./${input:projectName:demo-kotlin}
rm -f starter.zip
```

## Dependency additions

Insert these into `build.gradle.kts` without duplicating existing entries:

```gradle.kts
dependencies {
  implementation("org.springdoc:springdoc-openapi-starter-webflux-ui:2.8.6")
  testImplementation("com.tngtech.archunit:archunit-junit5:1.2.1")
}
```

Use `springdoc-openapi-starter-webflux-ui`, not `springdoc-openapi-starter-webmvc-ui`, because the generated project includes `webflux`.

## Application configuration

Add the following `application.properties` sections and fill secret values through the project's normal secret mechanism rather than committing real passwords:

```properties
# SpringDoc configurations
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha

# Redis configurations
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.password=rootroot

# R2DBC configurations
spring.r2dbc.url=r2dbc:postgresql://localhost:5432/postgres
spring.r2dbc.username=postgres
spring.r2dbc.password=rootroot
spring.sql.init.mode=always
spring.sql.init.platform=postgres
spring.sql.init.continue-on-error=true

# MongoDB configurations
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=root
spring.data.mongodb.password=rootroot
spring.data.mongodb.database=test
```

## Local service profile

Create `docker-compose.yaml` at the project root when local dependencies are needed.

| Service | Image | Port | Volume | Required credentials |
| --- | --- | --- | --- | --- |
| Redis | `redis:6` | `6379:6379` | `./redis_data:/data` | password `rootroot` |
| PostgreSQL | `postgres:17` or `postgresql:17` only if that image exists in the target environment | `5432:5432` | `./postgres_data:/var/lib/postgresql/data` | password `rootroot` |
| MongoDB | `mongo:8` | `27017:27017` | `./mongo_data:/data/db` | initdb root username `root`, password `rootroot` |

Add `redis_data`, `postgres_data`, and `mongo_data` directories to `.gitignore`.

## Validation commands

```shell
./gradlew clean test
docker-compose up -d
./gradlew spring-boot:run
docker-compose rm -sf
```

Run the optional Docker and application commands only when the user wants services started locally.

## Gotchas

- **Do not unzip twice**: the original instructions repeated the unzip step; extract `starter.zip` once, then delete it.
- **Do not commit real secrets**: use local defaults only for disposable development and replace them for shared environments.
- **Do not mix MVC and WebFlux starters**: match SpringDoc to WebFlux because `webflux` is in the generated dependency list.

## Spring Initializr anchors

The original `download-spring-boot-project-template` anchor maps to the Spring Initializr request in this skill. Preserve local service paths exactly: `./redis_data` maps to `/data`, `./postgres_data` maps to `/var/lib/postgresql/data`, and `./mongo_data` maps to `/data/db`. Optional commands are `docker-compose up -d`, `./gradlew spring-boot:run`, and `docker-compose rm -sf`.

## Output template

```markdown
### Spring Boot Kotlin project result

**Status:** created | instructions only | blocked
**Project:** `${input:projectName:demo-kotlin}`
**Package:** `com.example`

**Generated with**
- Java: `21`
- Spring Boot: `3.4.5`
- Build: `gradle-project-kotlin`
- Dependencies: `configuration-processor,webflux,data-r2dbc,postgresql,data-redis-reactive,data-mongodb-reactive,validation,cache,testcontainers`

**Files changed**
- `build.gradle.kts`: <dependency summary>
- `application.properties`: <configuration summary>
- `docker-compose.yaml`: <services added>
- `.gitignore`: <data directories added>

**Validation**
- `java -version`: pass | fail
- `./gradlew clean test`: pass | fail
```

## Quality gate

- [ ] `artifactId`, `packageName`, and `bootVersion` match the user's request or documented defaults.
- [ ] `starter.zip` is removed after extraction.
- [ ] `build.gradle.kts` contains SpringDoc WebFlux UI and ArchUnit dependencies without duplicates.
- [ ] Redis, R2DBC, MongoDB, and SpringDoc properties are present.
- [ ] `docker-compose.yaml` defines Redis, PostgreSQL, and MongoDB only when local services are needed.
- [ ] `redis_data`, `postgres_data`, and `mongo_data` are ignored by Git.
- [ ] `./gradlew clean test` was run or the blocker is reported.
