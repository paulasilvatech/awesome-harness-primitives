---
name: "react-audit-grep-patterns"
description: >-
  Provide verified grep command libraries for React 18.3.1 and React 19 migration audits, including deprecated APIs, removed APIs, unsafe lifecycle methods, batching risks, tests, dependencies, and peer conflicts. Use this skill when writing or running React migration audit scan commands.
---

# React audit grep patterns

Select the correct bundled scan catalog for a React migration audit, preserve the verified grep syntax, and report findings consistently instead of relying on memory for fragile multi-line and context-flag patterns.

## When to invoke

- "Run a React 18 migration audit."
- "Give me grep commands for React 19 removed APIs."
- "Scan this app for unsafe lifecycle methods and string refs."
- "Audit React tests for Enzyme and react-dom/test-utils."
- "Check React dependency and peer conflicts before upgrade."

## Scan library map

| Target | Read this bundled reference | Contains |
| --- | --- | --- |
| React 16/17 → 18.3.1 audit | `references/react18-scans.md` | Codebase profile, unsafe lifecycles, automatic batching vulnerabilities, legacy context, string refs, `findDOMNode`, root API, event delegation, Enzyme detection, and summary script. |
| React 18 → 19 audit | `references/react19-scans.md` | Removed APIs, deprecated APIs, test-file scans, StrictMode behavior, and summary script. |
| Tests for either target | `references/test-scans.md` | Setup file discovery, imports, Enzyme, `react-test-renderer`, old `act`, render helpers, assertions, async timers, `waitFor`, and `findBy`. |
| Dependencies for either target | `references/dep-scans.md` | React-related package versions, peer dependency conflicts, Enzyme detection, React Router version check, lockfile consistency, and duplicate React installs. |

## Base patterns used across all scans

Use these exact base fragments unless the repository uses a different source root or extension set:

```bash
# Standard flags used throughout:
# -r = recursive
# -n = show line numbers
# -l = show filenames only (for counting affected files)
# --include="*.js" --include="*.jsx" = JS/JSX files only
# | grep -v "\.test\.\|\.spec\.\|__tests__" = exclude test files
# | grep -v "node_modules" = safety (usually handled by not scanning node_modules)
# 2>/dev/null = suppress "no files found" errors

# Source files only (exclude tests):
SRC_FLAGS='--include="*.js" --include="*.jsx"'
EXCLUDE_TESTS='grep -v "\.test\.\|\.spec\.\|__tests__"'

# Test files only:
TEST_FLAGS='--include="*.test.js" --include="*.test.jsx" --include="*.spec.js" --include="*.spec.jsx"'
```

## Audit interpretation rules

| Finding type | Severity default | Interpretation |
| --- | --- | --- |
| React 19 removed API | Critical | `ReactDOM.render`, `ReactDOM.hydrate`, `unmountComponentAtNode`, `findDOMNode`, `createFactory`, legacy context, string refs, and removed `react-dom/test-utils` exports must be fixed before upgrade. |
| React 18 warning/deprecation | High | Unsafe lifecycle methods, string refs, legacy context, `findDOMNode`, and `ReactDOM.render` should be migrated before moving further. |
| Automatic batching risk | Medium | Async `setState`, `.then()`, `.catch()`, `setTimeout`, `addEventListener`, and post-`await` `this.state` reads require manual review; grep hits are candidates, not proof. |
| Test ecosystem issue | High | Enzyme, `react-test-renderer`, old `act`, `Simulate`, and brittle call-count assertions can block or destabilize upgrades. |
| Dependency conflict | High | Peer warnings, invalid packages, duplicate React installs, and React Router v5 require explicit assessment. |

## Progressive disclosure and bundled resources

- `references/react18-scans.md`: full React 18.3.1 scan phases and summary script.
- `references/react19-scans.md`: full React 19 removed/deprecated API and test scan phases.
- `references/test-scans.md`: test-specific commands shared by both auditors.
- `references/dep-scans.md`: dependency, peer conflict, Enzyme, router, lockfile, and duplicate React commands.

## Gotchas

- **Do not rewrite the multi-line patterns from memory**: batching scans rely on `-A` and `-B` context flags, then a second `grep` to locate nearby `setState` or `await` evidence.
- **Counts are triage, not proof**: inspect representative hits before claiming a file is safe or unsafe.
- **Exclude tests intentionally**: source scans and test scans answer different questions; do not mix them unless the reference says to.
- **React 19 `.propTypes` is not a deletion command**: runtime validation changes, but the standalone `prop-types` package can remain documentation/tooling.

## Output template

````markdown
## React audit grep result

**Status:** complete | partial | blocked
**Target:** React 18.3.1 | React 19 | tests | dependencies

| Scan area | Command source | Hits | Risk | Follow-up |
| --- | --- | --- | --- | --- |
| `<area>` | `references/<file>.md` | `<count or sample>` | Critical/High/Medium/Low | `<inspect/migrate/none>` |

### Commands run
```bash
<commands actually executed>
```

### Validation
- Reference files consulted: `<list>`
- Source root and extensions: `<src root and include flags>`
````

## Quality gate

- [ ] The correct bundled reference was used for React 18.3.1, React 19, tests, or dependencies.
- [ ] `SRC_FLAGS`, `EXCLUDE_TESTS`, and `TEST_FLAGS` semantics were preserved or repository-specific changes were stated.
- [ ] Scan commands excluded `node_modules` and separated source files from test files where required.
- [ ] Multi-line async and batching scans kept their `-A` or `-B` context flags.
- [ ] Findings distinguish raw grep hits from confirmed migration defects.
- [ ] The output includes commands run, hit counts or samples, and follow-up actions.
