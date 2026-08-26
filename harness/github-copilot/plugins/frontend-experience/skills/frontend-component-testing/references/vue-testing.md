# Vue testing adapter

- Reuse the installed runner, Vue Testing Library or Vue Test Utils, global plugins, router, Pinia/store setup, and mount helpers.
- Test public props, slots, emitted events, visible content, and user interaction.
- Prefer role and label queries when Testing Library is present; avoid brittle component-tree selectors.
- Await Vue updates and user-visible outcomes through established utilities rather than arbitrary delays.
- Test composables through a realistic host or the repository's established helper.
- Keep shallow mounting only where the project uses it and child behavior is not part of the contract.
