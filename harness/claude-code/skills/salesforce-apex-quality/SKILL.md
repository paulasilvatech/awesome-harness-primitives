---
name: salesforce-apex-quality
description: >-
  Review or generate Salesforce Apex classes, triggers, handlers, batch jobs, and test classes
  with quality guardrails for bulk safety, explicit sharing, CRUD/FLS enforcement, SOQL injection
  prevention, PNB tests, trigger architecture, and modern Apex idioms. Use when asked to catch
  governor limit risks, security gaps, and Apex deployment quality issues.
---

<!-- Generated from harness/github-copilot/skills/salesforce-apex-quality/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Salesforce Apex quality

Apply Apex guardrails to code generation and review so Salesforce code remains bulk-safe, secure, testable, and deployable under governor limits.

## When to invoke

- "Review this Apex trigger for governor limit issues."
- "Generate a bulk-safe Apex service and tests."
- "Check this Salesforce class for CRUD and FLS enforcement."
- "Make this Apex test cover positive, negative, and bulk paths."
- "Refactor SOQL in loops and unsafe dynamic queries."

## Governor limit safety

Scan every Apex class, trigger, and test before declaring it acceptable. SOQL/DML bulk-safety is an automatic fail area.

| Pattern | Required action |
| --- | --- |
| `[SELECT` or `[SELECT ...]` inside a `for` loop | Refactor: collect IDs, query once outside the loop, then use maps or grouped lists. |
| `Database.query` inside a loop | Refactor to a single parameterized or whitelisted query outside the loop. |
| `insert`, `update`, `delete`, `upsert`, or `merge` inside a loop | Collect records and perform one DML statement outside the loop. |
| Per-record trigger logic or query/update loops | Move business logic to a handler that accepts collections. |

```apex
// NEVER — causes LimitException at scale
for (Account a : accounts) {
    List<Contact> contacts = [SELECT Id FROM Contact WHERE AccountId = :a.Id];
    update a;
}

// ALWAYS — collect, query once, update once
Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();
Map<Id, List<Contact>> contactsByAccount = new Map<Id, List<Contact>>();
for (Contact c : [SELECT Id, AccountId FROM Contact WHERE AccountId IN :accountIds]) {
    if (!contactsByAccount.containsKey(c.AccountId)) {
        contactsByAccount.put(c.AccountId, new List<Contact>());
    }
    contactsByAccount.get(c.AccountId).add(c);
}
update accounts;
```

## Sharing and security

Every class must declare sharing intent explicitly. Undeclared sharing inherits from the caller and creates unpredictable behaviour.

| Declaration | Use when |
| --- | --- |
| `public with sharing class Foo` | Default for service, handler, selector, and controller classes. |
| `public without sharing class Foo` | Only for required elevated behavior such as system-level logging or trigger bypass; require a code comment explaining why. |
| `public inherited sharing class Foo` | Framework entry points that should respect the caller's sharing context. |

Apex code that reads or writes records on behalf of a user must enforce object and field access. Treat missing CRUD/FLS. as a deployment blocker. UI-facing, REST-facing, and `@InvocableMethod` code must use CRUD/FLS checks; trusted internal services may rely on `with sharing` only when the call path is controlled.

```apex
if (!Schema.sObjectType.Contact.fields.Email.isAccessible()) {
    throw new System.NoAccessException();
}

List<Contact> contacts = [SELECT Id, Email FROM Contact WHERE AccountId = :accId WITH USER_MODE];
List<Contact> contacts2 = Database.query('SELECT Id, Email FROM Contact', AccessLevel.USER_MODE);
```

## SOQL injection prevention

| Query shape | Rule |
| --- | --- |
| Static SOQL | Use bind variables such as `:userInput`. |
| Dynamic SOQL values | Bind values where possible; never concatenate raw user input. |
| Dynamic field or sort names | Validate user-controlled values against a whitelist before adding to the query string. |

```apex
// NEVER — concatenates user input into SOQL
String soql = 'SELECT Id FROM Account WHERE Name = \'' + userInput + '\'';

// ALWAYS — bind variable
List<Account> rows = [SELECT Id FROM Account WHERE Name = :userInput];

Set<String> allowedFields = new Set<String>{'Name', 'Industry', 'AnnualRevenue'};
if (!allowedFields.contains(userInput)) {
    throw new IllegalArgumentException('Field not permitted: ' + userInput);
}
```

## Tests and trigger architecture

PNB coverage is mandatory: Positive, Negative, and Bulk.

| Path | Required evidence |
| --- | --- |
| Positive | Expected input produces exact expected field values, counts, or return values. |
| Negative | Nulls, invalid inputs, empty collections, and errors throw the right type/message and do not mutate records. |
| Bulk | Insert, update, or delete **200–251 records** in one test transaction and assert all records process without governor failures. |

```apex
@isTest(SeeAllData=false)
private class AccountServiceTest {
    @TestSetup
    static void makeData() {
        // Create all test data here; use a factory if one exists.
    }

    @isTest
    static void givenValidInput_whenProcessAccounts_thenFieldsUpdated() {
        List<Account> accounts = [SELECT Id FROM Account LIMIT 10];
        Test.startTest();
        AccountService.processAccounts(accounts);
        Test.stopTest();
        List<Account> updated = [SELECT Status__c FROM Account WHERE Id IN :accounts];
        Assert.areEqual('Processed', updated[0].Status__c, 'Status should be Processed');
    }
}
```

Trigger checklist:

- [ ] One trigger per object; consolidate any second trigger into the handler.
- [ ] Trigger body contains only context checks, handler invocation, and routing logic.
- [ ] No business logic, SOQL, or DML lives directly in the trigger body.
- [ ] Existing trigger frameworks such as Trigger Actions Framework, ff-apex-common, or a custom base class are extended instead of bypassed.
- [ ] Handler class is `with sharing` unless elevated access is documented.

## Modern Apex idioms

| Old pattern | Modern replacement |
| --- | --- |
| `if (obj != null) { x = obj.Field__c; }` | `x = obj?.Field__c;` |
| `x = (y != null) ? y : defaultVal;` | `x = y ?? defaultVal;` |
| `System.assertEquals(expected, actual)` | `Assert.areEqual(expected, actual)` |
| `System.assert(condition)` | `Assert.isTrue(condition)`; migrate `System.assert` and `System.assertEquals` to `Assert.isTrue` and `Assert.areEqual`. |
| `[SELECT ... WHERE ...]` with no sharing context | `[SELECT ... WHERE ... WITH USER_MODE]` |

## Hardcoded anti-patterns

| Pattern | Action |
| --- | --- |
| `escape="false"` on user data in Visualforce | Remove it; auto-escaping enforces XSS prevention. |
| Empty `catch` block | Add logging and appropriate re-throw or error handling. |
| Test with no assertion | Add meaningful `Assert.*` calls. |
| Hardcoded record ID such as `'001...'` | Replace with queried or inserted test data. |

Inline API names to preserve: `Test.startTest()` and `Test.stopTest()` isolate governor counters for async and bulk assertions.

## Output template

```markdown
## Apex quality result

**Status:** pass | fix required | blocked
**Scope:** `<files/classes/triggers reviewed>`

| Area | Severity | Evidence | Required fix |
| --- | --- | --- | --- |
| Bulk safety | `<High|Medium|Low>` | `<line or snippet>` | `<fix>` |

### Tests
- Positive path: <covered|missing>
- Negative path: <covered|missing>
- Bulk path: <covered|missing, record count>

### Validation
- Sharing declaration: <pass|fail>
- CRUD/FLS: <pass|fail|not applicable>
- SOQL injection: <pass|fail>
```

## Quality gate

- [ ] No SOQL, `Database.query`, Insert/update/delete operations, or DML appears inside a loop.
- [ ] Every class declares `with sharing`, `without sharing`, or `inherited sharing` with justification where needed.
- [ ] User-facing record access enforces CRUD/FLS with schema checks, `WITH USER_MODE`, or `AccessLevel.USER_MODE`.
- [ ] Dynamic SOQL uses bind variables or whitelisted identifiers.
- [ ] Tests cover Positive, Negative, and Bulk paths with meaningful `Assert.*` calls.
- [ ] Triggers contain routing only and delegate to handlers.
