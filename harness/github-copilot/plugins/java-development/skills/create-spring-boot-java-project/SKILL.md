---
name: create-spring-boot-java-project
description: >-
  Create a Spring Boot Java project skeleton from Spring Initializr with Maven, Java 21, common data dependencies, SpringDoc, ArchUnit, local Docker Compose services for Redis, PostgreSQL, and MongoDB, application.properties settings, .gitignore entries, and Maven validation. Use when asked to create or scaffold a Spring Boot Java project.
---

# Spring Boot Java project creation

Create a Java 21 Spring Boot Maven project from Spring Initializr, add project dependencies and local service configuration, and verify the generated skeleton with Maven tests.

## When to invoke

- "Create a Spring Boot Java project."
- "Scaffold a Java 21 Spring Boot Maven app."
- "Generate a Spring Boot skeleton with JPA, Redis, MongoDB, and PostgreSQL."
- "Set up docker-compose for a new Spring Boot app."

## Prerequisites and context

- Java 21 must be installed; verify with `java -version`.
- Docker and Docker Compose must be installed before running local Redis, PostgreSQL, or MongoDB.
- Use the requested project name; otherwise use `demo-java` for `artifactId` and `com.example` for `packageName`.
- Use Spring Boot `3.4.5` unless the user requests another `bootVersion`; this replaces the old `download-spring-boot-project-template` anchor workflow.

## Procedure

1. Verify Java:

```shell
java -version
```

2. Download the Spring Initializr template. Change `artifactId`, `packageName`, or `bootVersion` only when the user asks.

```shell
curl https://start.spring.io/starter.zip   -d artifactId=${input:projectName:demo-java}   -d bootVersion=3.4.5   -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,data-redis,data-mongodb,validation,cache,testcontainers   -d javaVersion=21   -d packageName=com.example   -d packaging=jar   -d type=maven-project   -o starter.zip
```

3. Unzip and remove the archive:

```shell
unzip starter.zip -d ./${input:projectName:demo-java}
rm -f starter.zip
cd ${input:projectName:demo-java}
```

4. Add dependencies to `pom.xml`:

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.8.6</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.2.1</version>
  <scope>test</scope>
</dependency>
```

5. Add `application.properties` settings for SpringDoc, Redis, JPA, and MongoDB:

```properties
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.******
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
spring.datasource.username=postgres
spring.datasource.******
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=root
spring.data.mongodb.******
spring.data.mongodb.database=test
```

6. Create `docker-compose.yaml` at the project root with `redis:6`, `postgresql:17`, and `mongo:8` services.

| Service | Required settings |
| --- | --- |
| Redis | Password `rootroot`; port `6379:6379`; volume `./redis_data:/data`; directory `./redis_data`; mount target `/data`. |
| PostgreSQL | Password `rootroot`; port `5432:5432`; volume `./postgres_data:/var/lib/postgresql/data`; directory `./postgres_data`; mount target `/var/lib/postgresql/data`. |
| MongoDB | Init root username `root`; init root password `rootroot`; port `27017:27017`; volume `./mongo_data:/data/db`; directory `./mongo_data`; mount target `/data/db`. |

7. Add `redis_data`, `postgres_data`, and `mongo_data` to `.gitignore`.
8. Validate the project:

```shell
./mvnw clean test
```

9. Optionally run locally:

```shell
docker-compose up -d
./mvnw spring-boot:run
docker-compose rm -sf
```

The optional run commands are `docker-compose up -d`, `./mvnw spring-boot:run`, and `docker-compose rm -sf`.

## Project configuration rules

| Area | Rule |
| --- | --- |
| Dependencies | Keep Spring Initializr dependencies plus `springdoc-openapi-starter-webmvc-ui` and `archunit-junit5`. |
| Database defaults | Use local development defaults only; do not commit real credentials. |
| Docker volumes | Keep database data directories out of Git with `.gitignore`. |
| Tests | Run Maven tests before declaring the skeleton usable. |

## Gotchas

- **Do not leave `starter.zip` behind**; remove it after unzipping.
- **Do not start services before Docker is available**; project generation can complete without running containers.
- **Do not use real passwords in `application.properties`**; the shown `******` placeholders mark values that must be supplied safely.
- **Do not skip `.gitignore` data directories**; local databases create large mutable files.

## Output template

```markdown
## Spring Boot project result

**Status:** created | blocked
**Project:** `<projectName>`
**Package:** `<packageName>`
**Spring Boot:** `<bootVersion>`

### Files configured
| File | Change |
| --- | --- |
| `pom.xml` | <dependencies added> |
| `src/main/resources/application.properties` | <settings added> |
| `docker-compose.yaml` | <services added> |
| `.gitignore` | <data directories ignored> |

### Validation
- `java -version`: <result>
- `./mvnw clean test`: <pass|fail and evidence>
```

## Quality gate

- [ ] Java 21, Docker, and Docker Compose prerequisites were checked or reported as blockers.
- [ ] Spring Initializr command used the intended `artifactId`, `bootVersion`, `dependencies`, `javaVersion`, `packageName`, `packaging`, and `type`.
- [ ] `springdoc-openapi-starter-webmvc-ui` and `archunit-junit5` were added to `pom.xml`.
- [ ] SpringDoc, Redis, JPA, and MongoDB properties were added without committing real secrets.
- [ ] `docker-compose.yaml` defines Redis, PostgreSQL, and MongoDB with required ports, passwords, and volumes.
- [ ] `.gitignore` excludes `redis_data`, `postgres_data`, and `mongo_data`.
- [ ] `./mvnw clean test` was run or the blocker is documented.
