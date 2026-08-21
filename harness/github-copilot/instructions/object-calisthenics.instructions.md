---
applyTo: '**/*.{cs,ts,java}'
description: 'Enforces the original 9 Object Calisthenics rules for business domain code, with pragmatic exemptions for DTOs, API contracts, configuration, infrastructure, and tests.'
name: 'Object Calisthenics Conventions'
---

# Object Calisthenics Conventions — Domain Object Discipline

This file applies to C#, TypeScript, and Java business domain code, especially aggregates, entities, value objects, domain services, application services, and use case handlers. It is authoritative for the original 9 Object Calisthenics rules in this scope; when DTO, API contract, configuration, infrastructure, or test conventions conflict, apply the explicit exemptions in this file without adding, replacing, or removing any of the 9 rules.

## Scope and Exemptions

Apply the rules strictly to business domain code:

- Aggregates
- Entities
- Value objects
- Domain services
- Application services
- Use case handlers

Relax the rules where the original instruction explicitly allows pragmatism:

| Code type | Exemption |
| --- | --- |
| DTOs and data transfer objects | Rules 3, 8, and 9 may be relaxed; public getters and setters are acceptable |
| API models and contracts | Data-shape concerns may outweigh domain encapsulation |
| Configuration classes | Framework binding may require simple public properties |
| Simple data containers without business logic | Do not force domain-object ceremony where no behavior exists |
| Infrastructure code | Flexibility may be needed for framework, persistence, or integration seams |
| Tests | Rules may be relaxed for readability and maintainability; test behavior rather than object state |

Do not add a tenth rule, replace any rule, or remove any rule. Examples and organization may change, but the original 9 rules remain the complete rule set.

## Rule 1: One Level of Indentation per Method

Keep each method at one level of indentation. Extract nested logic into intention-revealing methods or filter the input before iteration.

**Bad:**

```csharp
public void SendNewsletter()
{
    foreach (var user in users)
    {
        if (user.IsActive)
        {
            mailer.Send(user.Email);
        }
    }
}
```

**Good:**

```csharp
public void SendNewsletter()
{
    foreach (var user in users)
    {
        SendEmail(user);
    }
}

private void SendEmail(User user)
{
    if (user.IsActive)
    {
        mailer.Send(user.Email);
    }
}
```

**Good:**

```csharp
public void SendNewsletter()
{
    var activeUsers = users.Where(user => user.IsActive);

    foreach (var user in activeUsers)
    {
        mailer.Send(user.Email);
    }
}
```

## Rule 2: Do Not Use the `else` Keyword

Avoid `else` to reduce branching complexity and improve readability. Prefer early returns, fail-fast checks, and guard clauses at the beginning of methods.

**Bad:**

```csharp
public void ProcessOrder(Order order)
{
    if (order.IsValid)
    {
        Process(order);
    }
    else
    {
        Reject(order);
    }
}
```

**Good:**

```csharp
public void ProcessOrder(Order order)
{
    if (!order.IsValid) return;

    Process(order);
}
```

**Good:**

```csharp
public void ProcessOrder(Order order)
{
    if (order is null) throw new ArgumentNullException(nameof(order));
    if (!order.IsValid) throw new InvalidOperationException("Invalid order");

    Process(order);
}
```

## Rule 3: Wrap All Primitives and Strings

Do not model domain concepts with raw primitives or strings when the value has meaning or behavior. Wrap values in small types that validate invariants and expose intention.

**Bad:**

```csharp
public class User
{
    public string Name { get; set; }
    public int Age { get; set; }
}
```

**Good:**

```csharp
public class User
{
    private readonly UserName name;
    private readonly Age age;

    public User(UserName name, Age age)
    {
        this.name = name;
        this.age = age;
    }
}

public class Age
{
    private readonly int value;

    public Age(int value)
    {
        if (value < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(value), "Age cannot be negative");
        }

        this.value = value;
    }
}
```

## Rule 4: Use First Class Collections

Encapsulate collections in dedicated classes instead of exposing raw data structures. A class that contains an array or collection as an attribute should not contain any other attributes; the collection wrapper owns collection behavior.

**Bad:**

```csharp
public class Group
{
    public int Id { get; private set; }
    public string Name { get; private set; }
    public List<User> Users { get; private set; }

    public int GetNumberOfUsersIsActive()
    {
        return Users
            .Where(user => user.IsActive)
            .Count();
    }
}
```

**Good:**

```csharp
public class Group
{
    public int Id { get; private set; }
    public string Name { get; private set; }
    public GroupUserCollection UserCollection { get; private set; }

    public int GetNumberOfUsersIsActive()
    {
        return UserCollection
            .GetActiveUsers()
            .Count();
    }
}
```

## Rule 5: One Dot per Line

Avoid Law of Demeter violations by keeping only one member-access dot per line. Ask objects for the domain result you need instead of navigating through their internals.

**Bad:**

```csharp
public void ProcessOrder(Order order)
{
    var userEmail = order.User.GetEmail().ToUpper().Trim();
    SendConfirmation(userEmail);
}
```

**Good:**

```csharp
public class User
{
    public NormalizedEmail GetEmail()
    {
        return NormalizedEmail.Create(/*...*/);
    }
}

public class Order
{
    public NormalizedEmail ConfirmationEmail()
    {
        return User.GetEmail();
    }
}

public void ProcessOrder(Order order)
{
    var confirmationEmail = order.ConfirmationEmail();
    SendConfirmation(confirmationEmail);
}
```

## Rule 6: Do Not Abbreviate

Use meaningful names for classes, methods, variables, packages, and namespaces. Avoid abbreviations that make intent ambiguous.

**Bad:**

```csharp
public class U
{
    public string N { get; set; }
}
```

**Good:**

```csharp
public class User
{
    public string Name { get; set; }
}
```

## Rule 7: Keep Entities Small

Keep classes, methods, packages, and namespaces small enough to remain readable and single-purpose.

| Entity | Constraint |
| --- | --- |
| Class | Maximum 50 lines |
| Class methods | Maximum 10 methods per class |
| Package or namespace | Maximum 10 classes |

Each class should have one responsibility and be as small as possible.

**Bad:**

```csharp
public class UserManager
{
    public void CreateUser(string name) { /*...*/ }
    public void DeleteUser(int id) { /*...*/ }
    public void SendEmail(string email) { /*...*/ }
}
```

**Good:**

```csharp
public class UserCreator
{
    public void CreateUser(string name) { /*...*/ }
}

public class UserDeleter
{
    public void DeleteUser(int id) { /*...*/ }
}

public class UserUpdater
{
    public void UpdateUser(int id, string name) { /*...*/ }
}
```

## Rule 8: No Classes with More Than Two Instance Variables

Limit each class to two instance variables to keep responsibilities narrow. Do not count `ILogger` or any other logger as an instance variable for this rule.

**Bad:**

```csharp
public class UserCreateCommandHandler
{
    private readonly IUserRepository userRepository;
    private readonly IEmailService emailService;
    private readonly ILogger logger;
    private readonly ISmsService smsService;

    public UserCreateCommandHandler(
        IUserRepository userRepository,
        IEmailService emailService,
        ILogger logger,
        ISmsService smsService)
    {
        this.userRepository = userRepository;
        this.emailService = emailService;
        this.logger = logger;
        this.smsService = smsService;
    }
}
```

**Good:**

```csharp
public class UserCreateCommandHandler
{
    private readonly IUserRepository userRepository;
    private readonly INotificationService notificationService;
    private readonly ILogger logger;

    public UserCreateCommandHandler(
        IUserRepository userRepository,
        INotificationService notificationService,
        ILogger logger)
    {
        this.userRepository = userRepository;
        this.notificationService = notificationService;
        this.logger = logger;
    }
}
```

## Rule 9: No Getters or Setters in Domain Classes

Do not expose setters on domain classes. Create domain objects through private constructors and static factory methods, and expose behavior instead of mutable state. This rule applies primarily to domain classes; DTOs and data transfer objects are exempt where public getters and setters are needed.

**Bad:**

```csharp
public class User
{
    public string Name { get; set; }
}
```

**Good:**

```csharp
public class User
{
    private readonly string name;

    private User(string name)
    {
        this.name = name;
    }

    public static User Create(string name) => new User(name);
}
```

**Acceptable for DTOs:**

```csharp
public class UserDto
{
    public string Name { get; set; }
}
```

## Layer Application

| Layer | Application |
| --- | --- |
| Domain classes | Use private constructors and static factory methods; avoid setters; apply all 9 rules strictly |
| Application layer | Apply the rules to use case handlers and application services, focusing on single responsibility and clean abstractions |
| DTOs and data objects | Relax rules 3, 8, and 9 when data transfer shape requires primitives, several properties, or public getters and setters |
| Tests | Validate object behavior rather than state; relax rules only when readability and maintainability require it |
| Code reviews | Enforce the rules for domain and application code; stay pragmatic for infrastructure and DTO code |

## Good / Bad Examples

The examples below illustrate applying several rules together: guard clauses instead of `else`, wrapped primitives, small domain behavior, and no public setters in a domain object.

**Good:**

```csharp
public class Order
{
    private readonly OrderLines lines;
    private readonly CustomerEmail customerEmail;

    private Order(OrderLines lines, CustomerEmail customerEmail)
    {
        this.lines = lines;
        this.customerEmail = customerEmail;
    }

    public static Order Create(OrderLines lines, CustomerEmail customerEmail)
    {
        if (lines is null) throw new ArgumentNullException(nameof(lines));
        if (customerEmail is null) throw new ArgumentNullException(nameof(customerEmail));

        return new Order(lines, customerEmail);
    }

    public Invoice DraftInvoice()
    {
        return lines.ToInvoiceFor(customerEmail);
    }
}
```

Why: The domain class has two instance variables, wraps meaningful values, uses guard clauses, avoids setters, and asks its collection object for behavior.

**Bad:**

```csharp
public class Order
{
    public List<OrderLine> Lines { get; set; }
    public string Email { get; set; }
    public decimal Total { get; set; }

    public Invoice DraftInvoice()
    {
        if (Lines.Count > 0)
        {
            return new Invoice(Email.Trim().ToUpper(), Total);
        }
        else
        {
            return Invoice.Empty();
        }
    }
}
```

Why: The domain class exposes setters, uses primitives for domain concepts, has more than two instance variables, uses `else`, navigates through raw collection state, and chains multiple dots on one line.

## Conventions

| Rule | Rationale |
|---|---|
| Keep each method to one level of indentation | Nested control flow hides intent and makes extraction harder |
| Avoid `else`; use early returns, fail-fast checks, and guard clauses | Branching stays linear and invalid states exit early |
| Wrap primitives and strings that represent domain concepts | Value objects carry validation, behavior, and meaning |
| Encapsulate collections as first class collections | Collection behavior stays near the data and raw structures do not leak |
| Keep one dot per line | Objects collaborate through behavior instead of exposing internals |
| Use complete, meaningful names without abbreviations | Names communicate intent without local tribal knowledge |
| Keep classes under 50 lines, classes under 10 methods, and packages or namespaces under 10 classes | Small units preserve single responsibility and reviewability |
| Limit classes to two instance variables, excluding loggers | Object responsibilities stay narrow and composable |
| Avoid getters and setters in domain classes; use private constructors and static factories | Domain objects protect invariants and expose behavior, not mutable state |
| Apply all 9 rules strictly to business domain code and pragmatically to exempt code | The discipline improves domain design without fighting DTOs, infrastructure, or tests |

## Do / Do Not

| Do | Do not |
|---|---|
| Extract nested logic into named methods or filtered inputs | Add multiple indentation levels inside a method |
| Use guard clauses and fail-fast validation | Add `else` branches for normal control flow |
| Model meaningful values as value objects | Pass raw strings and primitives through domain behavior |
| Put collection behavior in a first class collection | Expose raw lists and arrays from domain objects |
| Ask an object for the result you need | Chain through another object's internals with multiple dots |
| Write full names for classes, methods, variables, packages, and namespaces | Abbreviate names into unclear codes such as `U` or `N` |
| Split responsibilities into small classes and packages | Let managers, helpers, or namespaces grow without clear ownership |
| Keep at most two non-logger instance variables per class | Inject or store several collaborators in one class |
| Create domain objects with private constructors and static factories | Expose public setters on domain classes |
| Relax rules 3, 8, and 9 for DTOs when needed | Force DTOs, API contracts, configuration, or tests into domain-object shapes |

## Checklist Before Opening a PR

- [ ] Domain and application code applies exactly the original 9 Object Calisthenics rules.
- [ ] No method exceeds one indentation level unless the file is explicitly exempt.
- [ ] No domain or application method introduces an `else` where a guard clause, early return, or fail-fast check would work.
- [ ] Domain primitives and strings with business meaning are wrapped in value objects.
- [ ] Raw domain collections are hidden behind first class collection objects.
- [ ] Domain code avoids multi-dot navigation and asks collaborators for behavior.
- [ ] New names are meaningful and do not rely on abbreviations.
- [ ] Classes stay within 50 lines and 10 methods; packages or namespaces stay within 10 classes.
- [ ] Classes have no more than two non-logger instance variables.
- [ ] Domain classes avoid public setters and use private constructors plus static factory methods where object creation needs control.
- [ ] DTOs, API contracts, configuration, infrastructure, and tests use only the documented exemptions.
- [ ] Tests focus on object behavior rather than exposing or asserting internal state.

## References

- Object Calisthenics - Original 9 Rules by Jeff Bay: https://www.cs.helsinki.fi/u/luontola/tdd-2009/ext/ObjectCalisthenics.pdf
- ThoughtWorks - Object Calisthenics: https://www.thoughtworks.com/insights/blog/object-calisthenics
- Clean Code: A Handbook of Agile Software Craftsmanship, Robert C. Martin: https://www.oreilly.com/harness/github-copilot/view/clean-code-a/9780136083238/
