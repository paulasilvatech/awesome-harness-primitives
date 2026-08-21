---
name: java-helidon
description: >-
  Apply Helidon 4 SE and MP best practices for Java 21 applications, including routing, DB Client, Jakarta and MicroProfile APIs, configuration, security, observability, and tests. Use when working with Helidon SE, Helidon MP, HttpService, HttpRules, MicroProfile Config, Helidon DB Client, Helidon Security, or Helidon testing.
---

# Java Helidon

Guide Helidon 4 code generation and review so SE and MP applications compile, keep business logic out of transport layers, use Java 21 idioms, bind data safely, and avoid common Helidon 3 API mistakes.

## When to invoke

- "Write a Helidon 4 SE service."
- "Review this Helidon MP resource."
- "Fix Helidon DB Client code that does not compile."
- "Add Helidon tests without hardcoding a port."
- "Migrate Helidon 3 APIs to Helidon 4."

## Helidon 3 to 4 API changes

Check generated code against this table before returning it. The left column commonly appears in older examples and does not compile or is wrong for Helidon 4.

| Do not use | Use in Helidon 4 |
| --- | --- |
| `io.helidon.common.http.Http.Status` | `io.helidon.http.Status` |
| `io.helidon.webserver.Service` | `io.helidon.webserver.http.HttpService` |
| `Routing.Rules`, `update(Routing.Rules)` | `HttpRules`, `routing(HttpRules)` |
| `request.path().param("id")` | `request.path().pathParameters().get("id")` |
| `String s = column.as(String.class)` | `column.getString()` or `column.get(String.class)` |
| `dbClient.execute(exec -> ...)` returning `Single`/`Multi` | `dbClient.execute()` returning `Optional<DbRow>` or `Stream<DbRow>` |
| `javax.*` | `jakarta.*` |
| `helidon-microprofile-tests-junit5` | `helidon-microprofile-testing-junit5` |

`Value.as(Class)` returns `OptionalValue<T>`, not `T`; `DbColumn.as(String.class)` returns `OptionalValue<String>`, not `String`. This is the most common generated-code compile error in high-quality Helidon 4 work.

Migration tokens to verify explicitly: `DbColumn.as(String.class)`, `OptionalValue<String>`, `String`.

## Project setup and programming model

| Concern | Rule |
| --- | --- |
| Programming model | Determine whether the repository uses Helidon SE or Helidon MP before generating code; do not mix them unless explicitly required. |
| Java version | Use Java 21 or later for Helidon 4. |
| Build | Use the existing `pom.xml` or `build.gradle`; align Helidon versions with the Helidon BOM or platform. |
| Packages | Organize by feature or domain, such as `com.example.app.order` and `com.example.app.customer`, not only technical layers. |
| Configuration files | Store non-secret configuration in `application.yaml` or `application.properties`; use environment-dependent and deployment-specific overrides for runtime values. |
| Secrets | Never hardcode credentials, API keys, tokens, private certificates, `DB_USERNAME`, or `DB_PASSWORD`. |

Use the project's secret-management system for production credentials.

## Helidon SE patterns

| Layer | Rule |
| --- | --- |
| Bootstrap | Compose dependencies explicitly in the application startup layer. |
| Services | Use constructor injection with `private final` fields. |
| Routing | Group related routes in focused `HttpService` classes and register them with `routing.register(...)`. |
| Request handling | Keep handlers small; validate parameters and delegate business logic. |
| Concurrency | Prefer straightforward blocking code on Helidon 4 virtual-thread-based request handling. Do not generate `Single`, `Multi`, or `CompletionStage` chains without a project-specific reason. |

SE route shape:

```java
import io.helidon.http.Status;
import io.helidon.webserver.http.HttpRules;
import io.helidon.webserver.http.HttpService;
import io.helidon.webserver.http.ServerRequest;
import io.helidon.webserver.http.ServerResponse;

public final class CustomerHttpService implements HttpService {
    private final CustomerService customerService;

    public CustomerHttpService(CustomerService customerService) {
        this.customerService = customerService;
    }

    @Override
    public void routing(HttpRules rules) {
        rules.get("/{id}", this::findById);
    }

    private void findById(ServerRequest request, ServerResponse response) {
        var id = request.path().pathParameters().get("id");
        customerService.findById(id)
                .ifPresentOrElse(response::send, () -> response.status(Status.NOT_FOUND_404).send());
    }
}
```

Register with `WebServer.builder().routing(routing -> routing.register("/customers", customerHttpService)).build().start();`.

## Helidon MP patterns

| Layer | Rule |
| --- | --- |
| Standards | Prefer Jakarta EE and Eclipse MicroProfile APIs when available. |
| Injection | Use CDI constructor injection for required dependencies. |
| Scopes | Choose `@ApplicationScoped` and `@RequestScoped` intentionally. |
| Normal-scoped beans | Add a `non-private` `no-argument` constructor to normal-scoped beans that also use constructor injection so CDI proxies can be created. |
| REST resources | Keep REST resources thin and delegate business operations to service classes. |
| Portability | Use portable Jakarta and MicroProfile APIs when portability matters. |

MP resource shape:

```java
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/customers")
@RequestScoped
@Produces(MediaType.APPLICATION_JSON)
public class CustomerResource {
    private final CustomerService customerService;

    protected CustomerResource() { this.customerService = null; }

    @Inject
    public CustomerResource(CustomerService customerService) { this.customerService = customerService; }

    @GET
    @Path("/{id}")
    public Response findById(@PathParam("id") String id) {
        return customerService.findById(id)
                .map(customer -> Response.ok(customer).build())
                .orElseGet(() -> Response.status(Response.Status.NOT_FOUND).build());
    }
}
```

## Web and service layer rules

| Area | Rule |
| --- | --- |
| DTOs | Use request and response models; never expose persistence entities directly through APIs. |
| Validation | Validate path parameters, query parameters, headers, and bodies before business logic. |
| Status codes | Return appropriate HTTP status codes; on `PUT` and `DELETE`, return 404 when the target does not exist. |
| Errors | Use centralized error handling in SE and Jakarta REST `ExceptionMapper` in MP. Do not expose stack traces, database details, filesystem paths, or internal exception messages. |
| Transactions | Put transaction boundaries around complete business operations. |
| Mapping | Map persistence entities to API models at the service boundary; avoid `Optional<CustomerEntity>` leaking where callers expect `Optional<Customer>`. |
| State | Avoid mutable shared state in application-scoped components unless access is coordinated. |

A service can throw `IllegalArgumentException` for blank IDs or invalid `CreateCustomerRequest` data, map `CustomerEntity` to `Customer.fromEntity`, and use `@Transactional` on methods that change persistent state.

## Data layer rules

| Concern | Rule |
| --- | --- |
| Access technology | Use Helidon DB Client, Jakarta Persistence, or the persistence mechanism already established by the project. |
| SQL safety | Always bind parameters or use prepared statements; never concatenate untrusted input into SQL. |
| Column reads | Use `column("name").getString()`, `column("name").get(String.class)`, `getInt()`, `getLong()`, or other typed accessors. |
| Nullability | Use `asOptional()` or optional-aware accessors for nullable columns; direct `getString()` throws for null. |
| Whole-row mapping | `DbRow.as(Customer.class)` returns the mapped instance directly but requires a `DbMapper` registered through a `DbMapperProvider` service-loader entry; use this whole-row path only when repeated row shapes justify it. |
| Migrations | Use a migration tool for schema changes; do not rely on destructive automatic schema updates. |
| Entity separation | Keep `CustomerEntity` and public API records separate. |

Helidon DB Client repository shape:

```java
import io.helidon.dbclient.DbClient;

public final class DbCustomerRepository implements CustomerRepository {
    private static final String FIND_BY_ID = "SELECT id, name FROM customers WHERE id = :id";
    private static final String INSERT = "INSERT INTO customers (id, name) VALUES (:id, :name)";
    private final DbClient dbClient;

    public Optional<Customer> findById(String id) {
        return dbClient.execute()
                .createGet(FIND_BY_ID)
                .addParam("id", id)
                .execute()
                .map(row -> new Customer(row.column("id").getString(), row.column("name").getString()));
    }
}
```

For Helidon MP persistence, keep `JpaCustomerRepository` CDI-managed, inject `EntityManager` with `@PersistenceContext`, and return entities only inside the data layer.

Named statements may live in config:

```yaml
db:
  source: "jdbc"
  connection:
    url: "jdbc:postgresql://localhost:5432/customers"
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  statements:
    find-customer-by-id: >
      SELECT id, name
      FROM customers
      WHERE id = :id
```

Reference named SQL with `createNamedGet("find-customer-by-id")` and bound parameters.

## Observability, logging, testing, and security

| Area | Rule |
| --- | --- |
| Health | Use Helidon Health in SE or MicroProfile Health in MP for liveness and readiness. |
| Metrics | Use Helidon Metrics or MicroProfile Metrics; avoid user IDs, request IDs, email addresses, and raw URLs as metric tags. |
| Tracing | Propagate tracing context across inbound and outbound service calls. |
| Logging | Use the project's logging API; never log passwords, access tokens, authorization headers, cookies, sensitive bodies, secrets, or personal data. |
| Unit tests | Use JUnit 5 for services. |
| SE tests | Use `helidon-webserver-testing-junit5` with `@ServerTest` for full server tests or `@RoutingTest` for routing-only tests; inject `Http1Client` and never hardcode a port. |
| MP tests | Use `helidon-microprofile-testing-junit5` with `@HelidonTest`; confirm coordinates because the artifact was renamed across 4.x releases. |
| Integration tests | Consider Testcontainers for real databases, brokers, or infrastructure. |
| Failure paths | Test validation failures, missing resources, external-service failures, and authorization failures. |
| Authentication | Use Helidon Security or supported Jakarta and MicroProfile security APIs. |
| Authorization | Deny protected operations by default and enforce permissions at a clear boundary. |
| JWT/OIDC | Validate token signatures, issuers, audiences, and expirations. |
| TLS | Use TLS in production and verify outbound certificates. |
| CORS | Configure allowed origins explicitly; do not combine wildcard origins with credentials. |
| Outbound requests | Validate destinations to reduce server-side request forgery risk. |

## Gotchas

- **`Value.as(Class)` is not a direct value**: unwrap `OptionalValue<T>` or use typed accessors.
- **Helidon 4 is not the old reactive API**: avoid `Single`, `Multi`, and `CompletionStage` patterns copied from Helidon 3.
- **CDI proxy construction matters**: normal-scoped MP beans with constructor injection need a non-private no-argument constructor.
- **Testing ports must be dynamic**: `@ServerTest`, `@RoutingTest`, and `@HelidonTest` manage server lifecycle; do not hardcode ports.

## Output template

```markdown
## Helidon result

**Status:** complete | needs changes | blocked
**Programming model:** SE | MP
**Files reviewed or generated:** <paths>

### Findings or changes
| Area | Evidence | Action |
| --- | --- | --- |
| API migration | `<old API>` | `<Helidon 4 replacement>` |
| Web layer | `<route/resource evidence>` | `<fix>` |
| Data layer | `<query or mapper evidence>` | `<fix>` |
| Tests | `<test evidence>` | `<fix>` |

### Validation
- Compile check: pass | fail | not run
- Tests: pass | fail | not run
```

## Quality gate

- [ ] The output identifies Helidon SE or Helidon MP and does not mix models accidentally.
- [ ] No Helidon 3 APIs from the migration table remain in generated code.
- [ ] Java 21, aligned Helidon dependencies, and existing `pom.xml` or `build.gradle` conventions are respected.
- [ ] Route/resource classes validate inputs, return correct HTTP statuses, and delegate business logic.
- [ ] SQL uses bound parameters and safe typed accessors; nullable columns use optional-aware reads.
- [ ] Entities are separated from API DTOs or records.
- [ ] Configuration and secrets are externalized through `application.yaml`, `application.properties`, environment, or secret management.
- [ ] Tests use the correct Helidon testing artifact and dynamic server ports.
- [ ] Security, logging, metrics, CORS, OIDC, and TLS guidance is applied where relevant.
