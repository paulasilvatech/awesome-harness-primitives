# React testing adapter

- Reuse the installed runner, React Testing Library or project utilities, providers, router setup, and user-event version.
- Render through public props and context rather than invoking component functions.
- Query by role, label, accessible name, text, or established test ID.
- Use `userEvent` and async find/wait assertions for user-visible updates.
- Test hooks through public consumers or the repository's established hook utility.
- Account for Strict Mode and effect cleanup without asserting implementation call counts unless contractually relevant.
- Use Storybook interaction tests only when Storybook is already present or explicitly approved.
