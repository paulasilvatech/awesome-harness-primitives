# Component test contracts

Test these dimensions when they belong to the component:

| Dimension | Evidence |
| --- | --- |
| Rendering | User-visible content and semantics for supplied props/state |
| Interaction | Keyboard/pointer/user event changes observable behavior |
| State | Loading, empty, partial, success, error, disabled, access, recovery |
| Accessibility | Role/name/value/state, labels, errors, focus, announcements |
| Callback | Correct event and data at the public boundary |
| Integration boundary | API client/store/provider response produces the expected UI state |
| Cleanup | Timers, listeners, subscriptions, portals, and global state do not leak |

Do not assert internal methods, private state, framework scheduling, or incidental markup.
