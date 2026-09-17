# SonarQube Web API reference

Use this reference for direct, read-only SonarQube Server and SonarQube Cloud queries. Endpoint availability and deprecation can change by version and edition, so the target instance's `/api/webservices/list`, `/web_api`, or Web API v2 documentation remains authoritative.

## Verification snapshot

Verified on 2026-09-16 against:

- SonarQube Server Web API documentation: <https://docs.sonarsource.com/sonarqube-server/extension-guide/web-api>
- SonarQube Cloud Web API documentation: <https://docs.sonarsource.com/sonarqube-cloud/appendices/web-api>
- SonarQube Server public endpoint metadata: <https://next.sonarqube.com/sonarqube/api/webservices/list>
- SonarQube Cloud EU endpoint metadata: <https://sonarcloud.io/api/webservices/list>

The snapshot confirms that Web API v2 is gradually replacing v1. It does not prove that a v1 endpoint remains available on every instance. The bundled helper rediscovers endpoint metadata on each invocation.

## Base URLs

| Target | Web API v1 base URL |
| --- | --- |
| Self-hosted SonarQube Server | The instance root, including any context path, such as `https://sonarqube.example.com` or `https://example.com/sonarqube`. |
| SonarQube Cloud EU | `https://sonarcloud.io` |
| SonarQube Cloud US | `https://sonarqube.us` |

Cloud Web API v2 uses API-specific domains documented by SonarSource. Do not pass a v2 API domain to the bundled v1 helper, and do not derive v2 paths by rewriting v1 paths.

## Authentication and transport

- Prefer bearer authentication with a user token in the `Authorization` header.
- Keep the token in an approved environment variable or credential provider. The helper defaults to `SONARQUBE_TOKEN`.
- Never put a token in a URL, command argument, source file, report, or log.
- Anonymous GET requests can access only data the instance exposes publicly.
- The `X-Sonar-Passcode` scheme is for specific monitoring operations and is not supported by the bundled helper.
- A response may include `SonarQube-Authentication-Token-Expiration`; report it without exposing the token.
- Allow `http://` only when the selected local or internal instance actually uses it. Prefer HTTPS for remote instances.

## Supported endpoint map

The status below is the observation from the verification snapshot. Always rediscover before use.

| Information | Web API v1 endpoint | Important parameters | Snapshot notes |
| --- | --- | --- | --- |
| Endpoint capabilities | `/api/webservices/list` | None | Used before every helper query. |
| Projects | `/api/components/search` | `q`, `organization`, `qualifiers`, `p`, `ps` when exposed | Uses `qualifiers=TRK` when supported to return accessible projects without requiring project-provisioning administration. |
| Project detail | `/api/components/show` | `component`, `branch`, `pullRequest` | Branch and pull request are mutually exclusive. |
| Branches | `/api/project_branches/list` | `project` | Not paginated in the observed metadata. |
| Pull requests | `/api/project_pull_requests/list` | `project` | Returns analyzed pull requests, not source-control PR bodies. |
| Quality-gate status | `/api/qualitygates/project_status` | `projectKey`, `branch`, `pullRequest` | Observed as deprecated on Cloud, not on the public Server instance. |
| Assigned quality gate | `/api/qualitygates/get_by_project` | `project`, optional `organization` | Observed as deprecated on Cloud. |
| Quality gates | `/api/qualitygates/list` | Optional `organization` | Observed as deprecated on Cloud. |
| Measures | `/api/measures/component` | `component`, `metricKeys`, `branch`, `pullRequest` | Metric values may be strings. |
| Issues | `/api/issues/search` | Project, filters, `p`, `ps` | Project parameter was `components` on the public Server instance and `componentKeys` on Cloud. |
| Hotspots | `/api/hotspots/search` | Project, status, resolution, paging | Project parameter was `project` on Server and `projectKey` on Cloud. Search/show were observed as deprecated on both targets. |
| Hotspot detail | `/api/hotspots/show` | `hotspot` | Treat as a review target, not a confirmed vulnerability. |
| Analyses | `/api/project_analyses/search` | `project`, dates, optional branch, paging | Branch support differed by target metadata. |
| Quality profiles | `/api/qualityprofiles/search` | `project`, `language`, optional `organization` | Returns profiles visible to the caller. |
| Rule detail | `/api/rules/show` | `key`, optional `organization` | Preserve the returned rule key and taxonomy. |
| Metrics | `/api/metrics/search` | `p`, `ps` | Use this to validate metric keys before measure queries. |
| Server status | `/api/system/status` | None | Exposed by the public Server instance, not Cloud metadata. |
| Server version | `/api/server/version` | None | Plain text on Server; not exposed by Cloud metadata. |

## Common metric keys

Confirm keys with `/api/metrics/search` because editions and plugins can add or remove metrics.

| Goal | Common keys |
| --- | --- |
| Coverage | `coverage`, `new_coverage`, `line_coverage`, `branch_coverage` |
| Duplication | `duplicated_lines_density`, `new_duplicated_lines_density` |
| Size | `ncloc`, `lines`, `files`, `functions`, `classes` |
| Maintainability | `code_smells`, `sqale_rating`, `sqale_index` |
| Reliability | `bugs`, `reliability_rating`, `new_reliability_rating` |
| Security | `vulnerabilities`, `security_rating`, `security_hotspots`, `security_review_rating` |

Do not assume every key exists or that historical names retain the same semantics.

## Pagination

Many v1 list endpoints use:

- `p`: one-based page number.
- `ps`: page size.
- `paging.pageIndex`, `paging.pageSize`, and `paging.total` in the response.

Use the smallest page that answers the question. The helper defaults to 100 items and caps page size at 500. `--all-pages` is bounded by `--max-pages`; report `truncated: true` when the bound is reached before `paging.total`.

Some instances can return an item on adjacent pages. The helper removes duplicate objects by stable `key`, `id`, or `uuid`, reports the count removed, and stops with a truncated result if a page produces no new items.

## Scope and parameter differences

- Prefer an explicit project key. If absent, read only the exact `sonar.projectKey` property from a repository-root `sonar-project.properties`.
- Include `organization` only when the live endpoint exposes it.
- Select the issue project parameter from live metadata instead of hard-coding `components` or `componentKeys`.
- Select the hotspot project parameter from live metadata instead of hard-coding `project` or `projectKey`.
- Reject branch or pull-request input when the endpoint does not expose the corresponding parameter.
- Keep branch and pull request mutually exclusive.

## Response interpretation

| Response | Interpretation rule |
| --- | --- |
| Quality gate | Use the returned overall status and conditions. Do not replace it with a locally calculated verdict. |
| Issue | Preserve original status, severity or impact, type, rule, component, and line data. |
| Security hotspot | Report review status and probability context; do not call it a vulnerability unless SonarQube or a completed review does. |
| Measure | Parse numeric strings for presentation but retain the original metric key and value. |
| Empty collection | Verify permissions, organization, project, branch or pull request, filters, and pagination. |
| Deprecated endpoint | Report the exact `deprecatedSince` value and prefer a documented replacement when one is available. |

## Helper examples

Assume the credential is already present in the environment:

```bash
python3 scripts/sonarqube_query.py --base-url "$SONARQUBE_URL" capabilities
python3 scripts/sonarqube_query.py --base-url "$SONARQUBE_URL" projects --query payments
python3 scripts/sonarqube_query.py --base-url "$SONARQUBE_URL" \
  measures --project-key payments-api --metrics coverage,duplicated_lines_density
python3 scripts/sonarqube_query.py --base-url "$SONARQUBE_URL" \
  issues --project-key payments-api --resolved false --all-pages --max-pages 5
python3 scripts/sonarqube_query.py --base-url "$SONARQUBE_URL" \
  quality-gate --project-key payments-api --pull-request 42
```

The JSON envelope contains the endpoint, non-secret parameters, retrieval time, authentication mode, deprecation metadata, pagination state, token-expiration header when present, and result payload.
