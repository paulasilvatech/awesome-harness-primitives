---
name: 'create-spring-boot-java-project'
description: 'Create a Spring Boot Java project skeleton with required tooling and project structure guidance.'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
argument-hint: 'artifactId=<name> packageName=<package> bootVersion=<version>'
---

# /create-spring-boot-java-project

## Objective

Create a Spring Boot Java project skeleton from Spring Initializr with Java 21, Maven, selected dependencies, additional OpenAPI and ArchUnit dependencies, local Redis/PostgreSQL/MongoDB configuration, Docker Compose services, `.gitignore` updates, and Maven validation.

## When to Invoke

Use this prompt when starting a new Spring Boot Java service that needs a ready local development stack with web, validation, persistence, cache, database, Testcontainers, OpenAPI, and architecture-test support.

## Preconditions

- Java 21 is installed and available through `java -version`.
- Docker and Docker Compose are installed if local Redis, PostgreSQL, and MongoDB services will be run.
- Network access to `https://start.spring.io/starter.zip` is available.
- The target directory is the intended project root and edits are allowed.
- The team has selected `artifactId`, `packageName`, and `bootVersion` values or accepts the defaults.

## Inputs the Team Must Provide

- `artifactId` — Maven artifact ID; default `demo`.
- `packageName` — Java base package; default `com.example`.
- `bootVersion` — Spring Boot version; default `3.4.5`.
- Whether to keep all requested dependencies: `lombok`, `configuration-processor`, `web`, `data-jpa`, `postgresql`, `data-redis`, `data-mongodb`, `validation`, `cache`, and `testcontainers`.
- Ask the user for anything that is missing when project naming or package naming would be wrong.

## What I Will Do

- Check Java with `java -version`.
- Download a Spring Boot Maven project from Spring Initializr using `curl https://start.spring.io/starter.zip`.
- Unzip `starter.zip`, remove it with `rm -f starter.zip`, and add `springdoc-openapi-starter-webmvc-ui` plus `archunit-junit5` to `pom.xml`.
- Add SpringDoc, Redis, JPA, and MongoDB settings to `application.properties`.
- Create `docker-compose.yaml` with `redis:6`, `postgresql:17`, and `mongo:8` services using the specified ports, passwords, and volumes.
- Add `redis_data`, `postgres_data`, and `mongo_data` to `.gitignore`.
- Run `./mvnw clean test` and report the result.

## What I Will NOT Do

- Assume Java, Docker, or Docker Compose is installed when checks fail.
- Hardcode a custom `artifactId`, `packageName`, or `bootVersion` without user input or accepted defaults.
- Start long-running services unless the user requests the optional run workflow.
- Hide local development passwords as production credentials; treat `rootroot`, `postgres`, and `root` as local-only defaults.
- Add dependencies unrelated to the requested Spring Boot skeleton.

## Output Format

Apply the project changes and report:

```markdown
## Spring Boot Project Result

### Generated Project
- Artifact ID: `demo`
- Package: `com.example`
- Spring Boot: `3.4.5`
- Java: `21`
- Packaging: `jar`
- Type: `maven-project`

### Dependencies
- `lombok`
- `configuration-processor`
- `web`
- `data-jpa`
- `postgresql`
- `data-redis`
- `data-mongodb`
- `validation`
- `cache`
- `testcontainers`
- `springdoc-openapi-starter-webmvc-ui` `2.8.6`
- `archunit-junit5` `1.2.1`

### Local Services
| Service | Image | Port | Volume |
| --- | --- | --- | --- |
| Redis | `redis:6` | `6379:6379` | `./redis_data:/data` (container path `/data`) |
| PostgreSQL | `postgresql:17` | `5432:5432` | `./postgres_data:/var/lib/postgresql/data` (container path `/var/lib/postgresql/data`) |
| MongoDB | `mongo:8` | `27017:27017` | `./mongo_data:/data/db` (container path `/data/db`) |

### Validation
- Command: `./mvnw clean test`
- Result: [passed/failed]
```

## Definition of Done

- [ ] Java 21 was checked with `java -version`.
- [ ] Spring Initializr project was downloaded with the selected `artifactId`, `bootVersion`, `javaVersion=21`, `packageName`, `packaging=jar`, and `type=maven-project`.
- [ ] `starter.zip` was unzipped and removed.
- [ ] `pom.xml` includes `springdoc-openapi-starter-webmvc-ui` version `2.8.6` and `archunit-junit5` version `1.2.1` with test scope.
- [ ] `application.properties` includes SpringDoc, Redis, JPA/PostgreSQL, and MongoDB configuration keys.
- [ ] `docker-compose.yaml` defines Redis, PostgreSQL, and MongoDB services with required ports, passwords, users, and volumes.
- [ ] `.gitignore` includes `redis_data`, `postgres_data`, and `mongo_data`.
- [ ] `./mvnw clean test` ran, or the failure reason is reported.

## Prompt Body

Follow these steps in order.

**Step 1 — Confirm prerequisites and project values.** Verify Java 21 with `java -version`. Confirm Docker and Docker Compose if services will be run. Use `artifactId=demo`, `packageName=com.example`, and `bootVersion=3.4.5` unless the user provides replacements.

**Step 2 — Download the Spring Boot project template.** Run this command, substituting confirmed values where needed:

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=demo \
  -d bootVersion=3.4.5 \
  -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,data-redis,data-mongodb,validation,cache,testcontainers \
  -d javaVersion=21 \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

**Step 3 — Unpack and clean up.** Run `unzip starter.zip -d .` and then `rm -f starter.zip`.

**Step 4 — Add additional dependencies.** Insert these dependencies into `pom.xml`:

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

**Step 5 — Configure SpringDoc, Redis, JPA, and MongoDB.** Add these properties to `application.properties`, preserving real secret handling if the project already has it:

```properties
# SpringDoc configurations
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha

# Redis configurations
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.password=rootroot

# JPA configurations
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=rootroot
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# MongoDB configurations
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=root
spring.data.mongodb.password=rootroot
spring.data.mongodb.database=test
```

**Step 6 — Add Docker Compose.** Create `docker-compose.yaml` at the project root. Define `redis:6` with password `rootroot`, port `6379:6379`, and volume `./redis_data:/data`; `postgresql:17` with password `rootroot`, port `5432:5432`, and volume `./postgres_data:/var/lib/postgresql/data`; and `mongo:8` with initdb root username `root`, initdb root password `rootroot`, port `27017:27017`, and volume `./mongo_data:/data/db`.

**Step 7 — Update `.gitignore`.** Add `redis_data`, `postgres_data`, and `mongo_data` directories.

**Step 8 — Validate with Maven.** Run `./mvnw clean test`. If the user requests the optional run workflow, use `docker-compose up -d`, then `./mvnw spring-boot:run`, and stop services with `docker-compose rm -sf` when finished.

## Invocation Example

```
/create-spring-boot-java-project artifactId=demo packageName=com.example bootVersion=3.4.5
```
