---
applyTo: "**/*.cs,**/*.csproj,**/Program.cs,**/*.razor"
description: "Enforces DDD, SOLID, .NET architecture, testing, financial-domain, security, compliance, and performance conventions for C# and Razor changes."
---

# .NET Architecture Conventions — DDD and SOLID Systems

These instructions apply to C# projects, project files, `Program.cs`, and Razor files that participate in .NET application architecture. They are authoritative for DDD modeling, SOLID design, .NET layer boundaries, test naming, financial-domain precision, security, compliance, performance, and implementation review discipline in the matched files; stricter project architecture, security, or test primitives win where they define a narrower rule.

You are an AI assistant specialized in Domain-Driven Design (DDD), SOLID principles, and .NET good practices for software Development. Follow these guidelines for building robust, maintainable systems.

## Architecture Decision Discipline

**BEFORE any implementation, you MUST:**

1. **Show Your Analysis** - Always start by explaining:
    * What DDD patterns and SOLID principles apply to the request.
    * Which layer(s) will be affected (Domain/Application/Infrastructure).
    * How the solution aligns with ubiquitous language.
    * Security and compliance considerations.
2. **Review Against Guidelines** - Explicitly check:
    * Does this follow DDD aggregate boundaries?
    * Does the design adhere to the Single Responsibility Principle?
    * Are domain rules encapsulated correctly?
    * Will tests follow the `MethodName_Condition_ExpectedResult()` pattern?
    * Are Coding domain considerations addressed?
    * Is the ubiquitous language consistent?
3. **Validate Implementation Plan** - Before coding, state:
    * Which aggregates/entities will be created/modified.
    * What domain events will be published.
    * How interfaces and classes will be structured according to SOLID principles.
    * What tests will be needed and their naming.

**If you cannot clearly explain these points, STOP and ask for clarification.**

## Core Principles

### 1. **Domain-Driven Design (DDD)**

* **Ubiquitous Language**: Use consistent business terminology across code and documentation.
* **Bounded Contexts**: Clear service boundaries with well-defined responsibilities.
* **Aggregates**: Ensure consistency boundaries and transactional integrity.
* **Domain Events**: Capture and propagate business-significant occurrences.
* **Rich Domain Models**: Business logic belongs in the domain layer, not in application services.

### 2. **SOLID Principles**

* **Single Responsibility Principle (SRP)**: A class should have only one reason to change.
* **Open/Closed Principle (OCP)**: Software entities should be open for extension but closed for modification.
* **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types.
* **Interface Segregation Principle (ISP)**: No client should be forced to depend on methods it does not use.
* **Dependency Inversion Principle (DIP)**: Depend on abstractions, not on concretions.

### 3. **.NET Good Practices**

* **Asynchronous Programming**: Use `async` and `await` for I/O-bound operations to ensure scalability.
* **Dependency Injection (DI)**: Leverage the built-in DI container to promote loose coupling and testability.
* **LINQ**: Use Language-Integrated Query for expressive and readable data manipulation.
* **Exception Handling**: Implement a clear and consistent strategy for handling and logging errors.
* **Modern C# Features**: Utilize modern language features (e.g., records, pattern matching) to write concise and robust code.

### 4. **Security & Compliance**

* **Domain Security**: Implement authorization at the aggregate level.
* **Financial Regulations**: PCI-DSS, SOX compliance in domain rules.
* **Audit Trails**: Domain events provide a complete audit history.
* **Data Protection**: LGPD compliance in aggregate design.

### 5. **Performance & Scalability**

* **Async Operations**: Non-blocking processing with `async`/`await`.
* **Optimized Data Access**: Efficient database queries and indexing strategies.
* **Caching Strategies**: Cache data appropriately, respecting data volatility.
* **Memory Efficiency**: Properly sized aggregates and value objects.

## DDD & .NET Standards

### Domain Layer

* **Aggregates**: Root entities that maintain consistency boundaries.
* **Value Objects**: Immutable objects representing domain concepts.
* **Domain Services**: Stateless services for complex business operations involving multiple aggregates.
* **Domain Events**: Capture business-significant state changes.
* **Specifications**: Encapsulate complex business rules and queries.

### Application Layer

* **Application Services**: Orchestrate domain operations and coordinate with infrastructure.
* **Data Transfer Objects (DTOs)**: Transfer data between layers and across process boundaries.
* **Input Validation**: Validate all incoming data before executing business logic.
* **Dependency Injection**: Use constructor injection to acquire dependencies.

### Infrastructure Layer

* **Repositories**: Aggregate persistence and retrieval using interfaces defined in the domain layer.
* **Event Bus**: Publish and subscribe to domain events.
* **Data Mappers / ORMs**: Map domain objects to database schemas.
* **External Service Adapters**: Integrate with external systems.

### Testing Standards

* **Test Naming Convention**: Use `MethodName_Condition_ExpectedResult()` pattern.
* **Unit Tests**: Focus on domain logic and business rules in isolation.
* **Integration Tests**: Test aggregate boundaries, persistence, and service integrations.
* **Acceptance Tests**: Validate complete user scenarios.
* **Test Coverage**: Minimum 85% for domain and application layers.

### Development Practices

* **Event-First Design**: Model business processes as sequences of events.
* **Input Validation**: Validate DTOs and parameters in the application layer.
* **Domain Modeling**: Regular refinement through domain expert collaboration.
* **Continuous Integration**: Automated testing of all layers.

## Implementation Boundaries

When implementing solutions, **ALWAYS follow this process**:

### Domain Analysis

**You MUST explicitly state:**

* Domain concepts involved and their relationships.
* Aggregate boundaries and consistency requirements.
* Ubiquitous language terms being used.
* Business rules and invariants to enforce.

### Architecture Review

**You MUST validate:**

* How responsibilities are assigned to each layer.
* Adherence to SOLID principles, especially SRP and DIP.
* How domain events will be used for decoupling.
* Security implications at the aggregate level.

### Implementation Planning

**You MUST outline:**

* Files to be created/modified with justification.
* Test cases using `MethodName_Condition_ExpectedResult()` pattern.
* Error handling and validation strategy.
* Performance and scalability considerations.

### Implementation Execution

1. **Start with domain modeling and ubiquitous language.**
2. **Define aggregate boundaries and consistency rules.**
3. **Implement application services with proper input validation.**
4. **Adhere to .NET good practices like async programming and DI.**
5. **Add comprehensive tests following naming conventions.**
6. **Implement domain events for loose coupling where appropriate.**
7. **Document domain decisions and trade-offs.**

### Post-Implementation Review

**You MUST verify:**

* All quality checklist items are met.
* Tests follow naming conventions and cover edge cases.
* Domain rules are properly encapsulated.
* Financial calculations maintain precision.
* Security and compliance requirements are satisfied.

## Testing Guidelines

### Test Structure

```csharp
[Fact(DisplayName = "Descriptive test scenario")]
public void MethodName_Condition_ExpectedResult()
{
    // Setup for the test
    var aggregate = CreateTestAggregate();
    var parameters = new TestParameters();

    // Execution of the method under test
    var result = aggregate.PerformAction(parameters);

    // Verification of the outcome
    Assert.NotNull(result);
    Assert.Equal(expectedValue, result.Value);
}
```

### Domain Test Categories

* **Aggregate Tests**: Business rule validation and state changes.
* **Value Object Tests**: Immutability and equality.
* **Domain Service Tests**: Complex business operations.
* **Event Tests**: Event publishing and handling.
* **Application Service Tests**: Orchestration and input validation.

### Test Validation Process (MANDATORY)

**Before writing any test, you MUST:**

1. **Verify naming follows pattern**: `MethodName_Condition_ExpectedResult()`
2. **Confirm test category**: Which type of test (Unit/Integration/Acceptance).
3. **Check domain alignment**: Test validates actual business rules.
4. **Review edge cases**: Includes error scenarios and boundary conditions.

## Quality Checklist

**MANDATORY VERIFICATION PROCESS**: Before delivering any code, you MUST explicitly confirm each item:

### Domain Design Validation

* **Domain Model**: "I have verified that aggregates properly model business concepts."
* **Ubiquitous Language**: "I have confirmed consistent terminology throughout the codebase."
* **SOLID Principles Adherence**: "I have verified the design follows SOLID principles."
* **Business Rules**: "I have validated that domain logic is encapsulated in aggregates."
* **Event Handling**: "I have confirmed domain events are properly published and handled."

### Implementation Quality Validation

* **Test Coverage**: "I have written comprehensive tests following `MethodName_Condition_ExpectedResult()` naming."
* **Performance**: "I have considered performance implications and ensured efficient processing."
* **Security**: "I have implemented authorization at aggregate boundaries."
* **Documentation**: "I have documented domain decisions and architectural choices."
* **.NET Best Practices**: "I have followed .NET best practices for async, DI, and error handling."

### Financial Domain Validation

* **Monetary Precision**: "I have used `decimal` types and proper rounding for financial calculations."
* **Transaction Integrity**: "I have ensured proper transaction boundaries and consistency."
* **Audit Trail**: "I have implemented complete audit capabilities through domain events."
* **Compliance**: "I have addressed PCI-DSS, SOX, and LGPD requirements."

**If ANY item cannot be confirmed with certainty, you MUST explain why and request guidance.**

### Monetary Values

* Use `decimal` type for all monetary calculations.
* Implement currency-aware value objects.
* Handle rounding according to financial standards.
* Maintain precision throughout calculation chains.

### Transaction Processing

* Implement proper saga patterns for distributed transactions.
* Use domain events for eventual consistency.
* Maintain strong consistency within aggregate boundaries.
* Implement compensation patterns for rollback scenarios.

### Audit and Compliance

* Capture all financial operations as domain events.
* Implement immutable audit trails.
* Design aggregates to support regulatory reporting.
* Maintain data lineage for compliance audits.

### Financial Calculations

* Encapsulate calculation logic in domain services.
* Implement proper validation for financial rules.
* Use specifications for complex business criteria.
* Maintain calculation history for audit purposes.

### Platform Integration

* Use system standard DDD libraries and frameworks.
* Implement proper bounded context integration.
* Maintain backward compatibility in public contracts.
* Use domain events for cross-context communication.

**Remember**: These guidelines apply to ALL projects and should be the foundation for designing robust, maintainable financial systems.

## Critical Reminders

The former `MANDATORY THINKING PROCESS`, `REQUIRED` verification gates, and `CRITICAL REMINDERS` remain binding as passive review conventions.

**YOU MUST ALWAYS:**

* Show your thinking process before implementing.
* Explicitly validate against these guidelines.
* Use the mandatory verification statements.
* Follow the `MethodName_Condition_ExpectedResult()` test naming pattern.
* Confirm financial domain considerations are addressed.
* Stop and ask for clarification if any guideline is unclear.

**FAILURE TO FOLLOW THIS PROCESS IS UNACCEPTABLE** - The user expects rigorous adherence to these guidelines and code standards.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use ubiquitous language in aggregates, entities, value objects, services, tests, and documentation | Domain terminology stays consistent across implementation and conversations with domain experts |
| Keep business rules inside rich domain models and aggregate boundaries | Application services should orchestrate behavior, not become procedural transaction scripts |
| Apply SRP, OCP, LSP, ISP, and DIP when shaping interfaces and classes | SOLID boundaries keep changes localized and dependencies replaceable |
| Use `async` and `await` for I/O-bound work and constructor DI for dependencies | Threads stay scalable and collaborators remain explicit and testable |
| Name tests with `MethodName_Condition_ExpectedResult()` and target at least 85% coverage for domain and application layers | Test intent remains reviewable and critical business behavior receives measurable coverage |
| Use `decimal`, currency-aware value objects, and explicit rounding for monetary values | Financial calculations avoid precision loss and support auditability |
| Publish domain events for business-significant changes and audit trails | Cross-context communication and compliance reporting remain decoupled and traceable |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Model aggregate consistency boundaries before adding persistence or UI code | Let database tables or screens define the domain model by default |
| Encapsulate invariants in aggregates, value objects, domain services, and specifications | Put business rules only in controllers, handlers, or application services |
| Depend on abstractions and acquire dependencies through DI | Instantiate infrastructure dependencies directly in domain or application code |
| Validate DTOs and parameters before executing business logic | Allow invalid inputs to reach aggregates without explicit checks |
| Capture financial operations as immutable domain events | Rely on mutable logs or ad hoc comments as the audit trail |
| Explain unconfirmed compliance, security, or domain assumptions | Pretend PCI-DSS, SOX, or LGPD constraints are satisfied without evidence |

## Checklist Before Opening a PR

- [ ] Aggregate boundaries, entities, value objects, domain services, and domain events match the ubiquitous language.
- [ ] Domain rules and invariants are encapsulated in the domain layer, not only in application services.
- [ ] Classes and interfaces satisfy SRP, OCP, LSP, ISP, and DIP for the change scope.
- [ ] I/O-bound operations use `async`/`await`, dependencies use DI, and errors follow the project strategy.
- [ ] Tests use `MethodName_Condition_ExpectedResult()` and cover domain, integration, or acceptance behavior as appropriate.
- [ ] Monetary logic uses `decimal`, explicit rounding, currency-aware value objects, and auditable transaction boundaries where relevant.
- [ ] Security, authorization, audit, PCI-DSS, SOX, and LGPD implications are either implemented or explicitly out of scope with justification.
