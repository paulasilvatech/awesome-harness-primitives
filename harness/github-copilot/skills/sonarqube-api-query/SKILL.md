---
name: sonarqube-api-query
description: >-
  Query read-only SonarQube Server or SonarQube Cloud data through available SonarQube tools, the official sonar CLI, or a bundled Web API helper. Use when the user asks to list projects, inspect quality gates, issues, security hotspots, measures, analyses, metrics, rules, branches, pull requests, or server status in SonarQube or SonarCloud.
compatibility: "Requires network access to a SonarQube Server or SonarQube Cloud instance. The bundled fallback requires Python 3 and reads credentials only from environment variables."
---

# SonarQube API query

Turn a SonarQube information request into a narrowly scoped, evidence-backed, read-only query, then summarize the result without exposing credentials or dumping unrelated project data.

## When to invoke

- "List the SonarQube projects I can access."
- "Why is this project's quality gate failing?"
- "Show open critical SonarQube issues for this branch."
- "Get coverage and duplication measures for this pull request."
- "List security hotspots, recent analyses, branches, or pull requests."
- "Look up this SonarQube rule or metric."
- "Check the SonarQube server status."

## Prerequisites and context

- Use the SonarQube instance selected by the user. For the bundled helper, resolve it from `--base-url` or `SONARQUBE_URL`.
- Use an existing authenticated SonarQube tool or CLI session when available. The bundled helper reads a bearer token from `SONARQUBE_TOKEN` by default and also permits anonymous access to public data.
- For SonarQube Cloud, resolve the correct EU or US instance and the organization key instead of assuming either.
- Never ask the user to paste a token into chat, place a token in a command argument, or print an authorization header.
- Treat project names, keys, branch names, issue details, and internal server URLs as potentially sensitive. Return only fields needed for the request.

## Query route

Choose the first route that exactly covers the request:

| Priority | Route | Use when |
| --- | --- | --- |
| 1 | Available SonarQube-native tool | Its exposed schema directly supports the requested lookup. |
| 2 | Official `sonar` CLI | It is installed and authenticated, and a read-only command such as project, issue, quality-gate, or `sonar api get` lookup covers the request. |
| 3 | Bundled `scripts/sonarqube_query.py` | Native tools are unavailable or do not expose the required read-only data. |

Do not invent a tool name or CLI subcommand. Inspect the available schema or run `sonar --help` before using an unfamiliar command. Do not install or reconfigure integrations unless the user asks.

## Context resolution

Resolve query context in this order:

1. Explicit user input.
2. Existing authenticated integration context.
3. `sonar.projectKey` from a repository-root `sonar-project.properties`.
4. A project search narrowed by name or key.

Keep branch and pull-request scopes mutually exclusive. If more than one organization, project, branch, or pull request is plausible and the choice changes the result, ask the user to select one.

## Procedure

1. Classify the request as capabilities, project discovery, project detail, quality gate, measures, issues, hotspots, analyses, branches, pull requests, quality profiles, rules, metrics, or server health.
2. Resolve the instance, authentication state, organization when applicable, project key, and optional branch or pull-request scope.
3. Select the highest-priority query route that supports the exact request.
4. For direct Web API use, discover the live endpoint metadata before querying. Treat reported deprecation as evidence to prefer a documented v2 or native-tool replacement, not as proof that a guessed replacement exists.
5. Apply the narrowest filters and page size that answer the question. Fetch additional pages only when needed, and report truncation.
6. Parse the response before presenting it. Do not relay a raw payload unless the user explicitly requests raw JSON.
7. Report the query scope, retrieval time, endpoint or tool used, result count, deprecation warning, pagination state, and token-expiration header when present.

## Bundled helper

Run the helper from this skill directory. Connection options precede the subcommand:

```bash
python3 scripts/sonarqube_query.py \
  --base-url "$SONARQUBE_URL" \
  --organization "$SONARQUBE_ORGANIZATION" \
  issues --project-key my-project --resolved false --severities CRITICAL,BLOCKER
```

The helper supports:

| Command | Information returned |
| --- | --- |
| `capabilities` | Availability, parameters, and deprecation metadata for supported endpoints. |
| `projects`, `project` | Accessible projects or one project component. |
| `branches`, `pull-requests` | Project branch and pull-request analysis metadata. |
| `quality-gate`, `quality-gate-definition`, `quality-gates` | Project gate status, assigned gate, or available gates. |
| `measures` | Requested metric values for a project, branch, or pull request. |
| `issues` | Filtered project issues with bounded pagination. |
| `hotspots`, `hotspot` | Security hotspot summaries or one hotspot. |
| `analyses` | Project analysis history with optional dates. |
| `quality-profiles` | Profiles associated with a project or language. |
| `rule`, `metrics` | Rule detail or metric catalog entries. |
| `server-status`, `server-version` | Server health or version when the instance exposes it. |

Use `--all-pages --max-pages <n>` only on paginated commands. The helper is GET-only, refuses endpoints reported as POST, does not support arbitrary paths, and never accepts a token argument.

Read [Web API reference](references/web-api.md) when choosing endpoints, interpreting API differences, or handling deprecations.

## Interpretation rules

- Treat the quality-gate status and condition values returned by SonarQube as authoritative; do not recompute a different verdict.
- Distinguish an issue from a security hotspot. A hotspot requires review and is not automatically a confirmed vulnerability.
- Preserve the server's status, severity, software-quality impact, resolution, and rule identifiers. Do not translate between old and new taxonomies without showing the original value.
- Parse numeric measures deliberately because Web API values may be encoded as strings.
- Treat an empty result as scoped evidence only. Check permissions, organization, project, branch or pull request, filters, and pagination before concluding that no data exists.
- Cite the rule key and project/component key when recommending remediation.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `401` | Missing, expired, or invalid token. | Verify the approved credential source and retry without displaying the token. |
| `403` | The authenticated principal lacks Browse or administrative permission. | Report the missing access boundary; do not request broader access automatically. |
| `404` | Wrong base URL, project key, endpoint, or unsupported server version. | Re-run `capabilities`, verify the context path, and resolve the project key. |
| `429` | SonarQube Cloud rate limit. | Honor `Retry-After` when present and retry later; do not loop aggressively. |
| Endpoint is deprecated | The instance is migrating from Web API v1 to v2. | Prefer an available native tool or documented v2 endpoint; otherwise report the deprecated read path used. |
| Empty result | Scope, permissions, or filters do not match. | State the exact scope and relax one filter at a time. |

## Limits

- This skill is read-only. Do not create tokens, change quality gates or profiles, assign issues, transition hotspots, suppress findings, trigger analyses, or edit server configuration.
- Do not use local SonarQube for IDE findings as a substitute for remote project state unless the user explicitly asks for local IDE analysis.
- Do not guess Web API v2 paths from deprecated v1 paths. Use the instance documentation or a SonarQube-native tool.
- Use purpose-built official SonarQube plugin skills when they are installed and exactly match the request; use this skill for unified routing, unsupported lookups, or the Python fallback.

## Output template

```markdown
## SonarQube query result

**Status:** complete | empty | needs input | blocked
**Instance:** `<server label or redacted origin>`
**Organization:** `<key or not applicable>`
**Project:** `<key or not applicable>`
**Scope:** `<main | branch | pull request | server>`
**Retrieved:** `<UTC timestamp>`
**Route:** `<native tool | sonar CLI | bundled helper>`

### Result
<focused table, gate conditions, measures, or findings>

### Evidence
- Endpoint or operation: `<read-only operation>`
- Items returned: `<count or not applicable>`
- Pagination: `<complete | truncated | not applicable>`
- Deprecation: `<none reported | exact warning>`
- Token expiration: `<date | not reported | anonymous>`

### Next step
<one useful drill-down or none>
```

## Quality gate

- [ ] The instance, organization, project, and branch or pull-request scope are explicit.
- [ ] The selected route is available and uses only read operations.
- [ ] No token, authorization header, passcode, or unrelated raw payload is exposed.
- [ ] Live endpoint metadata was checked before direct Web API use.
- [ ] Deprecation, pagination, rate limits, permissions, and token expiration are reported when present.
- [ ] Issue, hotspot, quality-gate, and measure semantics remain faithful to the response.
- [ ] Empty or partial results are not presented as global absence.
- [ ] The output follows the template and names the evidence-producing operation.

## References

- [SonarQube Server Web API](https://docs.sonarsource.com/sonarqube-server/extension-guide/web-api)
- [SonarQube Cloud Web API](https://docs.sonarsource.com/sonarqube-cloud/appendices/web-api)
- [Official SonarQube agent plugins](https://github.com/SonarSource/sonarqube-agent-plugins)
