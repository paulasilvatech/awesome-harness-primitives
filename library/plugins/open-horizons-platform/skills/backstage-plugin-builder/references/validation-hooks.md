# Validation Hooks

Use this reference to add safety gates around Backstage plugin development.

## Standard Commands

Run what exists in the target package:

```bash
yarn lint
yarn tsc
yarn test
yarn build
```

For publication preparation:

```bash
npm pack --dry-run
```

## Hook Strategy

- Hooks are optional and local unless the repository already enforces them.
- Do not create hooks that require unavailable tools.
- Generate hooks only after checking `package.json` scripts.
- CI remains the source of truth for publication.

## Safe Pre-Commit Hook

The generated hook should:

1. Exit on failure.
2. Detect whether `yarn` exists.
3. Run only scripts present in `package.json`.
4. Avoid network or publishing commands.
5. Never read or print secrets.
