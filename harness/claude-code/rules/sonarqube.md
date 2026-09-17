<!-- Generated from harness/github-copilot/instructions/sonarqube.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Requires evidence-backed, read-only SonarQube Server and SonarQube Cloud lookups when work depends on projects, quality gates, issues, hotspots, measures, analyses, metrics, rules, branches, or pull requests.

# SonarQube Conventions - Read-Only Remote Evidence

These instructions apply when a task depends on SonarQube Server or SonarQube Cloud state rather than only on workspace files. They are authoritative for query scope, source precedence, credentials, read-only boundaries, result interpretation, and evidence reporting; repository-specific security policy and the target instance's live API schema win where they are stricter. They define passive conventions, while `sonarqube-api-query` (skill) owns the ordered lookup workflow and bundled fallback.

## Source precedence

Use SonarQube evidence in this order:

1. The user's explicit instance, organization, project, branch, or pull-request selection.
2. An available authenticated SonarQube-native tool or official `sonar` CLI response.
3. The target instance's live `/api/webservices/list`, `/web_api`, or Web API v2 documentation.
4. Exact workspace configuration such as `sonar.projectKey` in a repository-root `sonar-project.properties`.
5. First-party SonarSource documentation for general behavior.

Do not infer current remote quality-gate status, issue counts, hotspot review state, measures, or analysis history from source code, cached reports, badges, or CI configuration when live read access is available.

## Scope resolution

- Resolve the base URL before querying. Do not assume SonarQube Cloud EU, SonarQube Cloud US, or a self-hosted context path.
- Resolve organization only when the instance and endpoint require it.
- Resolve project key from explicit input, authenticated integration context, or the exact `sonar.projectKey` property before broad project search.
- Keep branch and pull request mutually exclusive.
- Ask for a selection when multiple plausible scopes would materially change the answer.
- State the final instance label, organization, project, and branch or pull-request scope in the result.

## Read-only boundary

Use GET operations or a tool operation explicitly documented as read-only. Querying is not authorization to:

- Create or revoke tokens.
- Change quality gates, quality profiles, permissions, settings, or project bindings.
- Assign, transition, suppress, accept, or resolve issues and hotspots.
- Trigger scans, analyses, imports, or background tasks.
- Reconfigure the SonarQube integration or install tooling.

If the user requests a mutation, separate it from the information lookup and obtain the authorization required by the applicable workflow.

## Credentials and sensitive data

- Prefer existing credential providers or authenticated SonarQube integrations.
- For direct API access, read the bearer token from an approved environment variable such as `SONARQUBE_TOKEN`.
- Never request a token in chat, pass it as a CLI argument, embed it in a URL, or display an authorization header.
- Reject base URLs containing credentials, query strings, or fragments.
- Treat internal hostnames, project keys, branch names, source paths, issue details, and raw payloads as potentially sensitive.
- Return only requested fields and bounded supporting evidence.

## Endpoint selection and freshness

- Discover the live endpoint and parameter schema before direct Web API use.
- Do not hard-code Server and Cloud parameter names when live metadata differs, including issue and hotspot project parameters.
- Treat `deprecatedSince` as a warning to prefer a documented replacement, not as permission to invent a Web API v2 path.
- Use the target instance documentation for edition- and version-specific behavior.
- Report the exact endpoint or tool operation, retrieval time, deprecation warning, pagination state, and token-expiration header when present.

## Result interpretation

- Use the returned quality-gate verdict and conditions; do not compute a competing verdict.
- Keep issues and security hotspots distinct. A hotspot is a review target, not automatically a confirmed vulnerability.
- Preserve the response's original status, severity or impact, type, resolution, rule key, component key, and metric key.
- Parse numeric measure strings for presentation without changing their meaning.
- Treat empty results as scoped evidence. Verify permissions, organization, project, branch or pull request, filters, and pagination before claiming absence.
- When recommending a fix, cite the project or component and rule that produced the finding.

## Failure handling

- Surface `401`, `403`, `404`, and `429` distinctly instead of replacing them with an empty result.
- Honor `Retry-After` when rate-limited and avoid automatic rapid retries.
- Report an unavailable endpoint as a version, edition, or route limitation; do not silently switch to a mutation or unrelated local analysis.
- If native tools and the official CLI are unavailable, use the bounded helper from `sonarqube-api-query` (skill).
- Do not claim a lookup succeeded unless a live response was received and parsed.

## Conventions

| Rule | Rationale |
| --- | --- |
| Query live SonarQube state before drawing remote conclusions | Workspace files and cached reports cannot prove current server state |
| Resolve instance, organization, project, and branch or pull request explicitly | SonarQube results are scope-dependent and easy to misattribute |
| Use only documented read operations for information retrieval | Read intent must not cause configuration or workflow mutations |
| Discover endpoint parameters at runtime | Server, Cloud, edition, and API generation can expose different schemas |
| Keep credentials in approved providers or environment variables | Tokens must not leak through chat, URLs, process arguments, or logs |
| Report pagination, deprecation, permissions, and retrieval time | Consumers need to distinguish complete current evidence from partial results |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Prefer a SonarQube-native tool, then the official CLI, then the bundled helper | Invent a tool name, CLI subcommand, or Web API v2 replacement |
| Narrow project, branch or pull request, filters, fields, and page size | Dump every accessible project or a large raw response by default |
| Preserve original SonarQube taxonomy and identifiers | Relabel hotspots as vulnerabilities or translate status fields silently |
| Explain authentication, permission, endpoint, and rate-limit failures | Return a success-shaped empty result after an API error |
| Use `sonarqube-api-query` (skill) for the ordered lookup procedure | Duplicate its step-by-step workflow inside passive instructions |

## Checklist Before Opening a PR

- [ ] SonarQube-dependent claims are backed by a live read response or explicitly labeled unavailable.
- [ ] Instance, organization, project, and branch or pull-request scope are stated.
- [ ] The operation is documented as read-only and no mutation was performed.
- [ ] No token, passcode, authorization header, internal raw dump, or unrelated project data is exposed.
- [ ] Endpoint metadata, deprecation, pagination, permissions, rate limiting, and retrieval time are reported when relevant.
- [ ] Issues, hotspots, quality gates, measures, rules, and analyses retain their source semantics.
- [ ] Empty and partial results are described with their scope and limitations.
- [ ] The change contains no unrelated edits or leftover placeholders.

## Related Primitives

- `sonarqube-api-query` (skill): use it to route and execute SonarQube information lookups, including the bounded Python Web API fallback.

## References

- [SonarQube Server Web API](https://docs.sonarsource.com/sonarqube-server/extension-guide/web-api)
- [SonarQube Cloud Web API](https://docs.sonarsource.com/sonarqube-cloud/appendices/web-api)
