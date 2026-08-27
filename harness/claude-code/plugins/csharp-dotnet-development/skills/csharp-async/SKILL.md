---
name: csharp-async
description: >-
  Review, design, and fix C# async code using Task, Task<T>, ValueTask<T>, cancellation,
  ConfigureAwait, async streams, and TAP conventions. Use when the user asks for C# async best
  practices, deadlock fixes, async method naming, parallel awaits, or replacing .Wait(), .Result,
  and async void.
---

<!-- Generated from harness/github-copilot/plugins/csharp-dotnet-development/skills/csharp-async/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# C# async programming best practices

Apply Task-based asynchronous pattern rules to C# code so async APIs are correctly named, awaitable, cancellable, exception-safe, and free of sync-over-async deadlocks in async/await code.

## When to invoke

- "Review this C# async code for best practices."
- "Fix .Wait() or .Result deadlocks in this method."
- "Should this return Task, Task<T>, ValueTask<T>, or async void?"
- "Add cancellation and Task.WhenAll to this async workflow."

## API shape rules

| Concern | Rule | Example |
| --- | --- | --- |
| Naming | Add `Async` suffix to async methods and match synchronous counterparts when applicable. | `GetData()` → `GetDataAsync()` |
| Returns a value | Return `Task<T>` by default. | `Task<Customer>` |
| No value | Return `Task`. | `Task SaveAsync(...)` |
| High-performance cached or frequently synchronous result | Consider `ValueTask<T>` only when allocation reduction is measured and callers can obey its constraints; this is a high-performance exception, not the default. | `ValueTask<int>` |
| Event handler | `async void` is allowed only for event handlers; plain `void` async APIs are otherwise forbidden. | `async void Button_Click(...)` |
| Public API style | Follow the task-based asynchronous pattern (TAP). | Accept `CancellationToken` for cancellable work. |

## Exception, cancellation, and context rules

- Use `try`/`catch` around awaited operations when you can add context, translate known exceptions, or perform cleanup; keep this as the explicit try/catch rule.
- Do not swallow exceptions; rethrow with `throw;` or return a meaningful failed `Task`.
- Use `Task.FromException()` when constructing an already-faulted `Task` result without running an async state machine.
- Use `CancellationToken` for long-running operations and pass it through to I/O APIs.
- Use `ConfigureAwait(false)` in library code that does not need a captured synchronization context; avoid applying it blindly in app/UI code where context may be required.

## Concurrency patterns

| Pattern | Use when | Avoid when |
| --- | --- | --- |
| `await` sequentially | Later work depends on earlier results. | Independent I/O could run in parallel. |
| `Task.WhenAll()` | Multiple independent operations should run concurrently and all must complete. | Operations must be throttled or ordered. |
| `Task.WhenAny()` | Implement timeout, fallback, or first-success behavior. | You would abandon tasks without cancellation/observation. |
| Pass through task | The method only returns another task with no cleanup, `try`/`catch`, or transformation. | You need `using`, `finally`, exception context, or post-processing. |
| `IAsyncEnumerable<T>` | Stream asynchronous sequences without buffering all results. | Consumers require a materialized list and data size is small. |

## Common pitfalls

| Pitfall | Why it is wrong | Fix |
| --- | --- | --- |
| `.Wait()`, `.Result`, `.GetAwaiter().GetResult()` | Blocks threads and can deadlock under synchronization contexts. | Make the call chain async and `await`. |
| Mixing blocking and async code | Wastes thread-pool threads and hides deadlocks. | Use async I/O end to end. |
| Unnecessary `async` / `await` | Adds a state machine without benefit. | Return the existing `Task` directly when safe. |
| Fire-and-forget `Task` | Exceptions can be lost and lifetime is unclear. | Await, return, or route to a supervised background service. |
| Missing await | Work may run after the caller thinks it completed. | Always await or intentionally capture and observe the `Task`. |

## Output template

````markdown
## C# async review - <file or API>

**Status:** pass | fixes recommended | fixed | blocked

| Finding | Evidence | Recommendation |
| --- | --- | --- |
| `<deadlock/naming/return/cancellation/concurrency issue>` | `<code reference>` | `<specific async pattern>` |

### Suggested shape
```csharp
<corrected signature or representative snippet>
```

### Validation
- Build/tests: `<command and result or not run>`
````

## Quality gate

- [ ] Async methods use the `Async` suffix unless they are event handlers or framework-mandated names.
- [ ] Return types are `Task<T>`, `Task`, justified `ValueTask<T>`, or event-handler-only `async void`.
- [ ] No `.Wait()`, `.Result`, or `.GetAwaiter().GetResult()` remains in async call paths without a documented boundary reason.
- [ ] Long-running or I/O-bound APIs accept and propagate `CancellationToken` where appropriate.
- [ ] Independent operations use `Task.WhenAll()` or `Task.WhenAny()` only when lifetime and exception handling are correct.
- [ ] Library code uses `ConfigureAwait(false)` where context capture is unnecessary.
