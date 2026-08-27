---
name: mvvm-toolkit-messenger
description: >-
  Configure CommunityToolkit.Mvvm Messenger pub/sub for decoupled ViewModel communication. Use
  this skill when users ask to send messages between ViewModels, choose WeakReferenceMessenger vs
  StrongReferenceMessenger, use IRecipient<TMessage>, RequestMessage<T>, AsyncRequestMessage<T>,
  CollectionRequestMessage<T>, ValueChangedMessage<T>, channel tokens, or ObservableRecipient
  activation in WPF, WinUI 3, .NET MAUI, Uno, or Avalonia.
---

<!-- Generated from harness/github-copilot/skills/mvvm-toolkit-messenger/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# CommunityToolkit.Mvvm Messenger

Configure CommunityToolkit.Mvvm messenger communication by choosing weak, strong, or scoped `IMessenger` instances, defining message types, and returning registration, send, token, request/reply, and lifecycle patterns for ViewModels.

Pub/sub messaging for ViewModels (or any objects) without forcing a shared
reference graph. Part of `CommunityToolkit.Mvvm` 8.x.

> **TL;DR.** Default to `WeakReferenceMessenger.Default`. Register handlers
> with the `(recipient, message)` lambda and the `static` modifier so you
> never capture `this`. Inherit from `ObservableRecipient` and toggle
> `IsActive` at activation/deactivation to get automatic register/unregister.

---

## When to invoke

- "Send a message between ViewModels with CommunityToolkit.Mvvm."
- "Choose WeakReferenceMessenger or StrongReferenceMessenger."
- "Use RequestMessage<T> or AsyncRequestMessage<T> for request/reply."
- "Scope MVVM Toolkit messages with channel tokens."
- "Debug why my messenger handler never fires."

For source generators, base classes, and commands see the **`mvvm-toolkit`**
skill. For DI wiring (registering an `IMessenger` instance), see
**`mvvm-toolkit-di`**.

---

## Choose an implementation

| Type | When |
|------|------|
| `WeakReferenceMessenger.Default` | **Default.** Recipients held weakly — eligible for GC even while registered. Internal trimming runs during full GCs; no manual `Cleanup()` needed. |
| `StrongReferenceMessenger.Default` | Profiler shows the messenger is hot and allocation matters. Recipients are pinned until you `Unregister`. Forgetting unregistration leaks them. |
| Custom `IMessenger` instance | Per-window/per-scope (e.g., one messenger per app window). Construct directly, inject via DI. |

`ObservableRecipient`'s parameterless constructor uses
`WeakReferenceMessenger.Default`. Pass a different `IMessenger` to its
constructor to override.

---

## Define a message

The toolkit ships base classes; any class works.

```csharp
using CommunityToolkit.Mvvm.Messaging.Messages;

// Single-payload broadcast
public sealed class LoggedInUserChangedMessage(User user)
    : ValueChangedMessage<User>(user);

// Custom shape (records are great for this)
public sealed record ThemeChangedMessage(AppTheme NewTheme);

// Empty signal
public sealed record RefreshRequestedMessage;
```

---

## Register a recipient

### Lambda style (recommended)

```csharp
WeakReferenceMessenger.Default.Register<MyViewModel, ThemeChangedMessage>(
    this,
    static (recipient, message) => recipient.OnThemeChanged(message.NewTheme));
```

The `static` modifier prevents accidental closure allocation and keeps
`this` out of the lambda — use the `recipient` parameter instead.

### `IRecipient<TMessage>` interface style

```csharp
public sealed class MyViewModel : ObservableRecipient,
    IRecipient<ThemeChangedMessage>,
    IRecipient<RefreshRequestedMessage>
{
    public void Receive(ThemeChangedMessage message) { /* ... */ }
    public void Receive(RefreshRequestedMessage message) { /* ... */ }
}
```

`ObservableRecipient.OnActivated()` calls `Messenger.RegisterAll(this)`,
which subscribes every `IRecipient<T>` interface implemented by the type.
If you're not using `ObservableRecipient`, register manually:

```csharp
WeakReferenceMessenger.Default.RegisterAll(this);
```

---

## Send a message

```csharp
WeakReferenceMessenger.Default.Send(new ThemeChangedMessage(AppTheme.Dark));

// Empty payloads use the parameterless overload:
WeakReferenceMessenger.Default.Send<RefreshRequestedMessage>();
```

---

## Channels (tokens)

Scope messages to a sub-system or window with a token (any equatable
value — `int`, `string`, `Guid`):

```csharp
const int LeftPaneChannel = 1;

WeakReferenceMessenger.Default.Register<MyViewModel, RefreshRequestedMessage, int>(
    this, LeftPaneChannel,
    static (r, _) => r.RefreshLeft());

WeakReferenceMessenger.Default.Send(new RefreshRequestedMessage(), LeftPaneChannel);
```

Messages sent without a token use the default shared channel — they are
**not** delivered to channel-scoped recipients.

---

## Request / reply

For ask-style scenarios where a recipient provides a value back to the
sender, use the `RequestMessage<T>` family.

### Sync request

```csharp
public sealed class CurrentUserRequest : RequestMessage<User> { }

WeakReferenceMessenger.Default.Register<UserService, CurrentUserRequest>(
    this,
    static (r, m) => m.Reply(r.CurrentUser));

User user = WeakReferenceMessenger.Default.Send<CurrentUserRequest>();
```

The implicit conversion from `CurrentUserRequest` to `User` throws if no
recipient called `Reply`. Capture the message to check first:

```csharp
var request = WeakReferenceMessenger.Default.Send<CurrentUserRequest>();
if (request.HasReceivedResponse)
    User user = request.Response;
```

### Async request

```csharp
public sealed class CurrentUserRequest : AsyncRequestMessage<User> { }

WeakReferenceMessenger.Default.Register<UserService, CurrentUserRequest>(
    this,
    static (r, m) => m.Reply(r.GetCurrentUserAsync()));

User user = await WeakReferenceMessenger.Default.Send<CurrentUserRequest>();
```

### Collection requests (fan-in)

`CollectionRequestMessage<T>` and `AsyncCollectionRequestMessage<T>` collect
a `Reply` from every responding recipient:

```csharp
public sealed class OpenDocumentsRequest : CollectionRequestMessage<Document> { }

var docs = WeakReferenceMessenger.Default.Send<OpenDocumentsRequest>();
foreach (Document doc in docs) { /* ... */ }
```

---

## Lifecycle

Even with `WeakReferenceMessenger`, unregister explicitly when a recipient
is being torn down — it trims dead entries and improves performance:

```csharp
WeakReferenceMessenger.Default.Unregister<ThemeChangedMessage>(this);
WeakReferenceMessenger.Default.Unregister<ThemeChangedMessage, int>(this, LeftPaneChannel);
WeakReferenceMessenger.Default.UnregisterAll(this);
```

`ObservableRecipient.OnDeactivated()` does this automatically when
`IsActive` flips to `false`. Set it from your activation hook:

```csharp
protected override void OnNavigatedTo(NavigationEventArgs e)
{
    base.OnNavigatedTo(e);
    ViewModel.IsActive = true;
}

protected override void OnNavigatedFrom(NavigationEventArgs e)
{
    ViewModel.IsActive = false;
    base.OnNavigatedFrom(e);
}
```

---

## Gotchas

- **Weak-reference lifetime is still observable**: even with weak-reference registration, unregister during teardown to trim stale entries and improve dispatch performance.

1. **Capturing `this` in the lambda.** `(r, m) => OnX(m)` implicitly
   captures `this`; allocates a closure and confuses lifetime. Always use
   `(r, m) => r.OnX(m)` with `static`.
2. **Strong-ref recipients without `Unregister`.** With
   `StrongReferenceMessenger`, recipients (and their entire object graph)
   stay pinned forever. Either inherit from `ObservableRecipient`
   (auto-unregisters in `OnDeactivated`) or call `UnregisterAll(this)`.
3. **Inherited message types.** A handler registered for `BaseMessage` is
   **not** invoked for `DerivedMessage : BaseMessage`. Register each
   concrete type.
4. **Wrong messenger instance.** Sending via `WeakReferenceMessenger.Default`
   and registering via an injected per-window messenger means the message
   never arrives. Use the same `IMessenger` everywhere (typically inject
   it via `ObservableRecipient(messenger)`).
5. **`OnActivated` never runs.** `ObservableRecipient` only registers
   `IRecipient<T>` handlers when `IsActive` flips from `false` to `true`.
6. **Cross-thread updates.** The messenger is thread-agnostic. If a
   handler updates UI, marshal manually
   (`DispatcherQueue.TryEnqueue` / `Dispatcher.BeginInvoke`).

---

## Multiple messengers (per-window scoping)

```csharp
services.AddSingleton<IMessenger>(WeakReferenceMessenger.Default); // app-wide
services.AddScoped<WindowScopedMessenger>();                       // per-window
```

Inject the appropriate `IMessenger` into the ViewModel constructor:

```csharp
public sealed partial class WindowViewModel(IMessenger messenger)
    : ObservableRecipient(messenger) { }
```

This isolates broadcasts to a single window — useful for multi-window
desktop apps (WinUI 3, WPF, MAUI desktop, Avalonia).

---

## Progressive disclosure and bundled resources

| Topic | File |
|-------|------|
| Full deep dive (more channel/lifecycle examples, diagnostics) | [`references/messenger-patterns.md`](references/messenger-patterns.md) |

## Output template

```markdown
## MVVM Toolkit messenger result

**Status:** implemented | guidance only | blocked
**Messenger:** `WeakReferenceMessenger.Default` | `StrongReferenceMessenger.Default` | custom `IMessenger`
**Message types:** `<messages defined or reviewed>`

### Pattern
- Registration: `<Register<TRecipient,TMessage> or RegisterAll>`
- Sending: `<Send(...)>`
- Scope: default channel | token `<token>`
- Lifecycle: `ObservableRecipient.IsActive` | manual `UnregisterAll(this)`

### Validation
- Static handler lambda: pass | fail
- Same messenger instance used for send and receive: pass | fail
- UI dispatch handled for UI updates: pass | fail
```

## Quality gate

- [ ] `WeakReferenceMessenger.Default` is used by default unless profiling or scoping justifies another `IMessenger`.
- [ ] Registration lambdas use `static (recipient, message)` and avoid capturing `this`.
- [ ] `StrongReferenceMessenger` recipients unregister through `ObservableRecipient.OnDeactivated()` or `UnregisterAll(this)`.
- [ ] Token-scoped sends and registrations use the same token type and value.
- [ ] Request messages check `HasReceivedResponse` before reading `Response` when no response is possible.
- [ ] UI updates from handlers marshal through `DispatcherQueue.TryEnqueue` or `Dispatcher.BeginInvoke`.

## References

External:

- Messenger docs: <https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/messenger>
- `WeakReferenceMessenger` API: <https://learn.microsoft.com/en-us/dotnet/api/communitytoolkit.mvvm.messaging.weakreferencemessenger>
- Source: <https://github.com/CommunityToolkit/dotnet>
