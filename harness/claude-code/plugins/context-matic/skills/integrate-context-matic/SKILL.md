---
name: integrate-context-matic
description: >-
  Discover and integrate third-party APIs with the context-matic MCP server using fetch_api, ask,
  model_search, endpoint_search, add_guidelines, add_skills, and update_activity. Use this skill
  when the user asks to integrate a third-party API, add an API client or SDK, implement features
  with an external API, or work with PayPal, Twilio, or another third-party API.
---

<!-- Generated from harness/github-copilot/plugins/context-matic/skills/integrate-context-matic/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# API integration with context-matic

Integrate external APIs by detecting the project language, ensuring context-matic guidelines and skills exist, discovering the supported API catalog, asking focused implementation questions, looking up SDK models and endpoints, and recording only real integration milestones.

## When to invoke

- "Integrate this third-party API."
- "Add an SDK client for PayPal."
- "Implement a feature with Twilio."
- "Use an external API in this project."
- "Look up endpoint details for this API SDK."

## Prerequisites and context

- Use the context-matic MCP server. Do not rely only on model memory for API availability or SDK details.
- If the requested API is not returned by `fetch_api`, stop and report that the API is not currently available in context-matic instead of guessing SDK usage.
- Check context-matic-generated guidelines and skills independently; one present file does not prove the rest exist.

## Language detection

Inspect the workspace and choose the primary language before any context-matic call that requires `language`.

| File or pattern | Language |
| --- | --- |
| `*.csproj`, `*.sln` | `csharp` |
| `package.json` with `"typescript"` dependency or `.ts` files | `typescript` |
| `requirements.txt`, `pyproject.toml`, `*.py` | `python` |
| `go.mod`, `*.go` | `go` |
| `pom.xml`, `build.gradle`, `*.java` | `java` |
| `Gemfile`, `*.rb` | `ruby` |
| `composer.json`, `*.php` | `php` |

## Context-matic workflow

1. Detect the language from repository files.
2. Check for existing generated materials:
   - `{language}-conventions` skill from `add_skills`.
   - `{language}-security-guidelines.md` and `{language}-test-guidelines.md` from `add_guidelines`.
   - `update-activity-workflow.md` from `add_guidelines`.
3. If required guideline files are missing, call `add_guidelines`.
4. If `{language}-conventions` is missing, call `add_skills`.
5. Call `fetch_api` with `language` and the API `key` from the user's request, such as `"paypal"` or `"twilio"`.
6. If there is no exact match and a catalog is returned, identify the correct API by name and description, then extract its `key`.
7. Ask focused implementation questions with `ask`, providing `language`, `key`, and `query`.
8. Look up SDK definitions with `model_search` and endpoint details with `endpoint_search` as needed.
9. Implement code following the returned guidance and project conventions.
10. Call `update_activity` only after a milestone is concretely reached in code or infrastructure.
11. Compile or test the project after each code modification.

## Tool usage rules

| Tool | Required parameters | Use it when | Do not use it for |
| --- | --- | --- | --- |
| `add_guidelines` | Project context from repository | Missing `{language}-security-guidelines.md`, `{language}-test-guidelines.md`, or `update-activity-workflow.md`. | Refreshing files that already exist unless the user asks. |
| `add_skills` | Detected `language` | Missing `{language}-conventions`. | Recreating an existing conventions skill. |
| `fetch_api` | `language`, `key` | First API discovery call for every integration. | Recording progress; it is discovery, not integration. |
| `ask` | `language`, `key`, `query` | Authentication, create payment, rate limits, error handling, webhook setup, or focused code guidance. | Broad multi-part questions that should be split. |
| `model_search` | `language`, `key`, case-sensitive `query` such as `availableBalance` or `TransactionId` | Model or object definitions. | Calling the external API. |
| `endpoint_search` | `language`, `key`, case-sensitive `query` such as `createUser` or `get_account_balance` | Endpoint method details. | Calling the external API. |
| `update_activity` | Appropriate `milestone` | Concrete progress reached in code or infrastructure. | Questions, searches, planning, or `fetch_api` results. |

## Milestones

| Milestone | Pass it only when |
| --- | --- |
| `sdk_setup` | SDK package is installed and the package command succeeded, such as `npm install`, `pip install`, or `go get`. |
| `auth_configured` | API credentials are explicitly present in runtime configuration such as `.env`, a secrets manager, or config file, and actual code references them. |
| `first_call_made` | First API call code was written and executed. |
| `error_encountered` | The developer reports a bug, error response, or failing call. |
| `error_resolved` | A fix was applied and the API call is confirmed working. |

## Gotchas

- **`fetch_api` is not progress**: do not call `update_activity` just because an API was discovered.
- **Keys are exact after discovery**: use the returned context-matic `key` for all later calls, not a display name you inferred.
- **Model and endpoint searches are definitions only**: they do not perform network calls against the third-party API.
- **Absent APIs are hard stops**: if the API is missing, ask the user how to proceed rather than inventing integration code.

Use the API name/key distinction carefully: the display name may differ from the returned `key`. Guidelines are language-specific, model_search returns a model/object definition, and update_activity is valid only after concrete code/infrastructure progress.

## Output template

```markdown
## Context-matic API integration result

**Status:** integrated | guidance only | blocked
**Language:** `<language>`
**API key:** `<context-matic key or not found>`

| Step | Tool or check | Result |
| --- | --- | --- |
| Language detection | repository files | `<evidence>` |
| Guidelines/skills | `add_guidelines` / `add_skills` / skipped | `<result>` |
| API discovery | `fetch_api` | `<result>` |
| Guidance | `ask` | `<queries asked>` |
| SDK details | `model_search` / `endpoint_search` | `<models/endpoints>` |
| Milestone | `update_activity` | `<milestone or none>` |
| Validation | `<compile/test command>` | `<pass/fail/not run>` |

**Next action:** <specific implementation step or user decision needed>
```

## Quality gate

- [ ] The primary language was detected from repository files before context-matic calls.
- [ ] Missing guideline files and `{language}-conventions` were checked independently.
- [ ] `fetch_api` was called first with the detected `language` and requested API `key`.
- [ ] The returned API `key` was used for `ask`, `model_search`, and `endpoint_search`.
- [ ] Missing APIs were reported as unavailable in context-matic without guessing SDK usage.
- [ ] `update_activity` was called only for concrete milestones: `sdk_setup`, `auth_configured`, `first_call_made`, `error_encountered`, or `error_resolved`.
- [ ] The project compiled or tested after code changes, or the blocker is stated.
