---
paths:
  - "**/*.{py,js,jsx,ts,tsx,mjs,cjs,json,toml}"
---

<!-- Generated from harness/github-copilot/instructions/attester-verify-packages.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces PyPI and npm package and symbol verification with the attester.dev existence oracle before installing, importing, or calling uncertain third-party dependencies.

# Attester Package Verification Conventions — PyPI and npm Existence Checks

These instructions apply to Python and JavaScript dependency manifests, imports, package installation commands, and third-party symbol usage in matched files. They are authoritative for when and how to verify PyPI and npm package or symbol names with the attester.dev existence oracle; local project modules, standard library modules, and names already verified in the same session are outside this check unless their source is uncertain.

## Verification Triggers

Use the attester.dev existence oracle before adding any third-party dependency or using a library symbol that is not already confirmed from project code, lockfiles, installed package metadata, or official documentation. The oracle exists because models invent plausible package names; a USENIX Security 2025 study measured 5.2% to 21.7% of suggested package names as nonexistent depending on model and ecosystem.

| Trigger | Required check |
| --- | --- |
| Adding to `requirements.txt`, `pyproject.toml`, `package.json`, or another dependency file | Verify the package name first. |
| Running an install command for a package not chosen by the user | Verify the package name first. |
| Writing `import`, `require`, or `from ... import` for a third-party package | Verify the package unless already known in this session. |
| Calling a function, class, constant, or exported member that may not exist | Verify the symbol against the package. |
| Build failure reports a missing package or symbol | Check the name before renaming, replacing, or adding dependencies. |

Skip the oracle for standard library modules, local project modules, workspace packages, and names already verified in this session.

## Oracle Endpoints and Payloads

The free keyless endpoint requires no account or API key. Quota is 25 calls per day per client IP, reset at 00:00 UTC.

| Check | Endpoint | JSON body | Success condition |
| --- | --- | --- | --- |
| Package exists | POST `https://attester.dev/demo/v1/package/exists` | `{"ecosystem": "pypi" | "npm", "name": "<name>"}` | Proceed only when `exists` is `true`. |
| Symbol exists | POST `https://attester.dev/demo/v1/symbol/exists` | `{"ecosystem": "pypi" | "npm", "package": "<package>", "symbol": "<symbol>"}` | Proceed only when the symbol exists or a documented alternative is chosen. On a miss, prefer the `closest_match` suggestions over inventing variants. |

On HTTP 429 or network failure, state that the check was skipped and why, then continue conservatively: prefer well-known packages, pinned versions, existing project dependencies, and documented APIs over invented alternatives.

Preserve the symbol-miss behavior as `. On a miss, prefer the ` `closest_match` guidance: use the oracle's closest real suggestion before considering any manually invented variant.

## Interpreting Answers

| Oracle field | Convention |
| --- | --- |
| `exists: true` | Proceed; when pinning, prefer the version reported in `latest_version` unless the project already pins another compatible version. |
| `exists: false` | Do not install, import, or call the name; report the negative result and use `adjacent_to` or `closest_match` only when the user or documentation confirms the intended name. |
| `typosquat_adjacent: true` | Treat the name as a strong typo or hallucination signal; never install the flagged name. |
| `closest_match` | Prefer suggestions over inventing variants, but still verify the selected package or symbol. |

## Higher-Volume Use

The free tier covers normal editing sessions. For high-volume dependency audits, use the paid route documented by the service rather than trying to bypass the daily cap.

## Good / Bad Examples

The examples below illustrate checking a package before adding an import.

**Good:**

```bash
curl -sS https://attester.dev/demo/v1/package/exists   -H 'content-type: application/json'   -d '{"ecosystem":"npm","name":"vitest"}'
```

Why: The package name is checked against published npm artifacts before it reaches `package.json` or an `import` statement.

**Bad:**

```bash
npm install vitest-ai-runner
```

Why: The package name was not verified and may be a hallucinated or typosquat-adjacent dependency.

## Conventions

| Rule | Rationale |
|---|---|
| Verify uncertain PyPI and npm package names before installing, importing, or adding them to manifests | Hallucinated package names create supply-chain and build failures. |
| Verify uncertain third-party symbols before calling them | Published packages do not guarantee the model-invented API exists. |
| Proceed only when `exists` is `true` or a documented alternative is confirmed | Negative checks are safety signals, not naming suggestions to ignore. |
| Treat `typosquat_adjacent: true` as a stop condition | Typosquat-adjacent names can expose users to malicious packages. |
| On HTTP 429 or network failure, disclose the skipped check and choose the conservative option | The user needs to know the verification guarantee was not available. |

## Do / Do Not

| Do | Do not |
|---|---|
| Check `https://attester.dev/demo/v1/package/exists` before adding uncertain packages | Add plausible package names from memory. |
| Check `https://attester.dev/demo/v1/symbol/exists` before using uncertain exports | Invent function, class, or constant names because they sound idiomatic. |
| Use `latest_version`, `adjacent_to`, and `closest_match` as evidence fields | Treat suggestions as permission to install without verification. |
| Skip checks for standard library and local project modules | Spend quota on names already known from the current workspace. |
| Explain HTTP 429 or network failures clearly | Pretend verification happened when the oracle was unavailable. |

## Checklist Before Opening a PR

- [ ] New PyPI or npm dependency names were verified or came from an existing trusted project source.
- [ ] New third-party imports, `require` calls, and `from ... import` statements were verified when uncertain.
- [ ] New third-party symbols were checked when not confirmed by project code or documentation.
- [ ] No dependency with `exists: false` or `typosquat_adjacent: true` was installed or imported.
- [ ] Any skipped oracle check due to HTTP 429 or network failure was disclosed with a conservative fallback.
- [ ] Dependency versions use the project pin or the verified `latest_version` when pinning is needed.

## References

- attester.dev package existence endpoint: https://attester.dev/demo/v1/package/exists
- attester.dev symbol existence endpoint: https://attester.dev/demo/v1/symbol/exists
