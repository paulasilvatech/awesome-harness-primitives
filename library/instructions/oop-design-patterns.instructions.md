---
applyTo: "**/*.py,**/*.java,**/*.ts,**/*.js,**/*.cs"
description: "Enforces object-oriented design pattern and SOLID conventions for clean, maintainable, and scalable code. Use when generating or refactoring OOP code in Python, Java, TypeScript, JavaScript, or C#."
---

# OOP Design Pattern Conventions — GoF and SOLID

These instructions apply to object-oriented Python, Java, TypeScript, JavaScript, and C# source files. They are authoritative for applying Gang of Four (GoF) patterns, SOLID principles, composition, encapsulation, logging, error handling, documentation, and testability in matched files; language-specific style guides and project architecture win where they define stricter naming, framework, or layering rules.

## Core Architectural Philosophy

- Program to an Interface, not an Implementation: favor abstract classes or interfaces over concrete implementations and provide concrete instances through dependency injection.
- Favor Object Composition over Class Inheritance: combine behavior dynamically at runtime with composition and Delegation; avoid deep inheritance trees that break encapsulation.
- Encapsulate What Varies: identify varying behavior and separate it from stable code with Strategy, State, Bridge, or related patterns.
- Loose Coupling: minimize direct dependencies between classes with Mediator, Observer, abstract factories, or other abstractions when they solve a real dependency problem.
- Balance Simplicity and Flexibility: favor function definition over class definition when a simple function solves the problem; use classes and patterns only when they provide clear organizational benefits.

## Creational Patterns

| Pattern | Use when | Guardrail |
| --- | --- | --- |
| Abstract Factory | A system must be configured with one of multiple families of related products such as cross-platform UI widgets. | Clients interact only with the abstract factory and abstract product interfaces. |
| Factory Method | A class cannot anticipate the class of objects it must create. | Defer instantiation to subclasses without leaking concrete construction into clients. |
| Builder | Constructing a complex object requires a step-by-step process or multiple representations. | Keep the construction steps explicit and valid at the end. |
| Singleton | A single instance is absolutely necessary, such as a central configuration manager or hardware interface. | Prefer Dependency Injection over strict Singletons where possible. |
| Prototype | Creating from scratch is expensive or a factory hierarchy would be excessive. | Preserve invariants when cloning existing instances. |

## Structural Patterns

| Pattern | Use when | Guardrail |
| --- | --- | --- |
| Adapter | Incompatible interfaces must work together. | Prefer Object Adapters using composition over Class Adapters with multiple inheritance. |
| Bridge | An abstraction and its implementation must vary independently, such as `Window` and platform-specific `WindowImpl`. | Keep both sides independently replaceable. |
| Composite | Part-whole and `part-whole` hierarchies should be treated uniformly. | Expose a common `Component` interface for individual objects and compositions. |
| Decorator | Responsibilities must attach dynamically. | Prefer over subclassing to avoid class explosion; keep the Decorator interface identical to the decorated component. |
| Facade | A complex subsystem needs a simple entry point. | Do not hide important errors or lifecycle requirements. |
| Flyweight | Similar objects can share state to reduce memory or computational expense. | Separate intrinsic shared state from extrinsic caller-provided state. |
| Proxy | Access to another object needs lazy loading, access control, or remote communication. | Keep the surrogate behavior transparent where possible. |

## Behavioral Patterns

| Pattern | Use when | Guardrail |
| --- | --- | --- |
| Strategy | A family of algorithms should be interchangeable. | Replace complex `switch`/`if-else` behavior selection with a Strategy object. |
| Observer | A one-to-many dependency where one Subject change must notify many Observers. | Keep subjects and observers loosely coupled. |
| Command | A request must be an object for undo/redo, queues, or logging. | Keep command execution and command data clear. |
| State | An object's behavior changes based on internal state. | Represent each state as a separate class. |
| Template Method | A base class defines algorithm skeleton while subclasses fill steps. | Do not force subclasses to violate the base algorithm. |
| Chain of Responsibility | A request should pass through possible handlers until one handles it. | Avoid coupling senders to a concrete receiver. |
| Mediator | Complex communication between objects needs central coordination. | Keep colleagues from referring to each other explicitly. |
| Iterator | Aggregates need sequential access without exposing representation. | Hide storage details behind the iterator. |
| Visitor | Stable object structures need new operations such as Abstract Syntax Trees analysis. | Use only when element classes are stable enough to justify Visitor complexity. |
| Memento | Internal state must be captured and restored without violating encapsulation. | Use for complex Undo mechanisms without exposing internals. |

## SOLID, Generation, and Refactoring Rules

- Generate the interface or abstract base class before concrete implementations when the design calls for abstraction.
- Make fields `private` by default. Provide getters/setters only when necessary and favor immutable objects.
- Use pattern names in class names when they aid understanding, such as `TaxCalculationStrategy`, `ButtonDecorator`, or `WidgetFactory`; keep names natural to the domain otherwise.
- Break God Classes into smaller focused classes coordinated through a Mediator or composed of Strategy objects.
- Apply the Single Responsibility Principle: each class has one reason to change.
- Apply the Open/Closed Principle: classes are open for extension but closed for modification through abstract classes or interfaces.
- Apply the Liskov Substitution Principle: subclasses do not strengthen preconditions or weaken postconditions.
- Apply the Interface Segregation Principle: prefer many specific interfaces over one general-purpose interface.
- Apply the Dependency Inversion Principle: high-level modules and low-level modules depend on abstractions.
- Refactor iteratively with tests so behavior remains correct throughout the refactoring process.
- Use repositories and typing definitions for complex data structures or interactions when they improve separation of concerns and type clarity.

## Logging, Error Handling, and Documentation

Fail safe, loud, clear and early. Avoid silent failures. Log errors with enough context to debug and maintain code, using logging frameworks and appropriate info, debug, warning, error and critical levels. Use custom exceptions when they provide more meaningful messages or more granular handling, and reserve exception blocks for expected error conditions rather than normal control flow.

Document pattern intent in English when it is not obvious. Use docstrings for classes and methods, and use the numpy pattern for parameters and returns unless the existing codebase uses another style. Do not ask the developer which docstring style to use from inside a passive instruction; follow the repository's established style when present. Use Sphinx or JSDoc when the project already generates documentation from code. Keep user documentation and developer documentation current, concise, up-to-date, well-documented, and non-duplicative; extend a README when that is the established high-level architectural overview. Use UML diagrams only when they clarify class and pattern relationships.

## Good / Bad Examples

The examples below illustrate replacing conditional algorithm selection with Strategy.

**Good**

```csharp
public interface TaxCalculationStrategy
{
    decimal Calculate(Order order);
}

public sealed class RetailTaxCalculationStrategy : TaxCalculationStrategy
{
    public decimal Calculate(Order order) => order.Subtotal * 0.07m;
}
```

Why: the algorithm varies behind an interface, so adding a new tax calculation does not modify existing callers.

**Bad**

```csharp
public decimal CalculateTax(Order order, string type)
{
    if (type == "retail") return order.Subtotal * 0.07m;
    if (type == "wholesale") return order.Subtotal * 0.03m;
    return 0m;
}
```

Why: behavior selection is embedded in conditionals, encourages silent fallback, and violates Open/Closed Principle as new types appear.

## Conventions

| Rule | Rationale |
| --- | --- |
| Apply GoF patterns only when the problem maps to the pattern and the benefit is clear. | Pattern names do not justify over-engineering. |
| Prefer interfaces, abstract classes, composition, Delegation, and dependency injection over concrete coupling and deep inheritance. | Code stays replaceable, testable, and encapsulated. |
| Use Strategy, State, Bridge, Mediator, Observer, and factories to isolate real variation and coupling. | Variability moves behind stable abstractions. |
| Enforce SOLID principles during generation and refactoring. | Classes remain maintainable and substitutable as the system grows. |
| Integrate logging, custom exceptions, and fail-fast validation into pattern implementations. | Failures are diagnosable and do not disappear silently. |
| Keep documentation concise, English, and focused on intent, users, maintainers, and architecture. | Future maintainers understand why a pattern exists without reading redundant docs. |
| Validate design refactors with tests and profiling where performance is a concern. | Abstraction layers do not introduce unverified bugs or bottlenecks. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Name patterns in comments only when it clarifies intent. | Add comments that announce obvious boilerplate. |
| Start with a simple function when a class adds no value. | Force every behavior into a pattern or class hierarchy. |
| Use `TaxCalculationStrategy`, `ButtonDecorator`, or `WidgetFactory` when names help. | Use pattern names that obscure the domain. |
| Refactor God Classes into cohesive collaborators. | Let large managers accumulate unrelated responsibilities. |
| Use exceptions for exceptional or expected error conditions that need handling. | Use exception blocks to control normal program flow. |
| Extend existing documentation in the same style. | Create constantly new documentation files with duplicate content. |

## Checklist Before Opening a PR

- [ ] The chosen pattern solves a real maintainability, flexibility, testability, or readability problem.
- [ ] Interfaces or abstract bases exist where clients should not depend on concrete implementations.
- [ ] Composition is preferred over inheritance unless inheritance is the simpler correct model.
- [ ] SOLID violations introduced or touched by the change are addressed.
- [ ] Fields are private by default, mutation is minimized, and getters/setters are justified.
- [ ] Logging and error handling fail safe, loud, clear and early without silent failures.
- [ ] Documentation explains non-obvious pattern intent and avoids redundant new files.
- [ ] Tests verify behavior, and performance-sensitive abstractions are profiled or justified.
