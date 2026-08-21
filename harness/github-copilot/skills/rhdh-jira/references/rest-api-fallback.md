# Jira REST API Fallback

Use the Jira REST API when `acli` cannot update a custom field. This is a fallback only - always try `acli` first. For complex read queries, see `references/graphql-queries.md`.

Authentication setup: see `references/auth.md`. All examples below assume `AUTH` is set per that file.

## JQL Search via REST

The REST API v3 search endpoint (`/rest/api/3/search`) returns **HTTP 410 Gone** on the Red Hat Jira instance (both POST and GET). This is an Atlassian-side deprecation - do not attempt REST search as a fallback.

**Search priority order:**

1. `acli jira workitem search` (with `--limit 200` or `--paginate`)
2. GraphQL `issueSearchStable` (beta, requires experimental header)
3. REST search is **not available** on this instance

REST remains valid for single-issue reads (`GET /rest/api/3/issue/{key}`) and field updates (`PUT /rest/api/3/issue/{key}`).

## Schema Discovery

The REST API v3 has a published OpenAPI spec. Use it to discover endpoints, field formats, and payload shapes.

### Download the OpenAPI spec

```bash
curl -s -o jira-openapi.json \
  'https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json'
```

The spec is ~4MB JSON. Do not load it into context. Query it programmatically:

### Look up an endpoint

```bash
# Find the PUT issue endpoint schema
python -c "
import json, sys
spec = json.load(open('jira-openapi.json'))
put = spec['paths'].get('/rest/api/3/issue/{issueIdOrKey}', {}).get('put', {})
print(json.dumps({'summary': put.get('summary'), 'parameters': [p['name'] for p in put.get('parameters', [])], 'requestBody': list(put.get('requestBody', {}).get('content', {}).keys())}, indent=2))
"
```

### List all issue field endpoints

```bash
python -c "
import json
spec = json.load(open('jira-openapi.json'))
for path, methods in spec['paths'].items():
    if '/issue/' in path:
        for method in methods:
            if method in ('get','put','post','delete'):
                print(f'{method.upper():6} {path}')
" | head -30
```

### Discover field metadata from your instance

```bash
# List all fields (standard + custom) with IDs and types
curl -s -u "$AUTH" \
  'https://redhat.atlassian.net/rest/api/3/field' | \
  python -c "
import json, sys
fields = json.load(sys.stdin)
for f in sorted(fields, key=lambda x: x['id']):
    print(f\"{f['id']:30} {f.get('schema',{}).get('type','?'):15} {f['name']}\")
"
```

This returns the live field registry from the Jira instance - including custom field IDs, types, and display names. Use it when you encounter an unknown field or need to verify a custom field ID.

### Check which fields are editable on a specific issue

```bash
curl -s -u "$AUTH" \
  'https://redhat.atlassian.net/rest/api/3/issue/RHIDP-123/editmeta' | \
  python -c "
import json, sys
meta = json.load(sys.stdin)
for fid, info in meta.get('fields', {}).items():
    ops = [o['id'] for o in info.get('operations', [])]
    print(f\"{fid:30} {info['name']:25} ops={ops}\")
"
```

Use this when a field update returns 400 - it shows which fields are editable and their allowed operations/values.

### Schema discovery comparison

| | REST API | GraphQL |
|--|---------|---------|
| **Spec format** | OpenAPI 3.0 JSON (~4MB downloadable file) | No spec file - self-describing via introspection queries |
| **Download** | `curl -o jira-openapi.json 'https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json'` | `__schema` or `__type` introspection queries against the live endpoint |
| **Live field registry** | `GET /rest/api/3/field` returns all field IDs, types, names | `__type(name: "JiraIssue")` returns typed fields on the issue object |
| **Editability check** | `GET /rest/api/3/issue/{key}/editmeta` | Not available - use REST |

## Updating Custom Fields

### Story Points (customfield_10028) - number

```bash
curl -s -X PUT \
  -u "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10028": 5}}' \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-123"
```

### Size (customfield_10795) - dropdown

```bash
curl -s -X PUT \
  -u "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10795": {"value": "M"}}}' \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-123"
```

Valid values: XS, S, M, L, XL.

### Team (customfield_10001) - atlassian-team

```bash
curl -s -X PUT \
  -u "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10001": {"id": "TEAM_ID"}}}' \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-123"
```

To find the team ID, fetch the issue first and inspect `customfield_10001.id` from an issue already assigned to that team.

### Release Note Type (customfield_10785) - dropdown

```bash
curl -s -X PUT \
  -u "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10785": {"value": "Enhancement"}}}' \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-123"
```

Valid values: Feature, Enhancement, Developer Preview, Deprecated Functionality, Removed Functionality, Release Note Not Required.

## Response Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 204 | Success (no content) | Field updated. |
| 400 | Bad request | Check field ID, value format, or allowed values. Use `editmeta` endpoint to check editability. |
| 401 | Unauthorized | See `references/auth.md` → Common Auth Errors. |
| 403 | Forbidden | User lacks edit permission on this issue. |
| 404 | Not found | Issue key is wrong. |
| 429 | Rate limited | Wait 5 seconds, retry once. |

## Verifying the Update

After a REST API update, verify the field was set:

```bash
curl -s -u "$AUTH" \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-123?fields=customfield_10028,customfield_10795,customfield_10001"
```

## Common Mistakes

- **Wrong value format for dropdowns.** Use `{"value": "M"}` not `"M"`. Number fields are bare numbers, not strings.
- **PUT is a partial update.** Jira's `PUT /rest/api/3/issue/{key}` only updates the fields you include in the payload - you do not need to send the full issue body. There is no separate PATCH endpoint.
- **Forgetting the `fields` wrapper.** The payload must be `{"fields": {"customfield_X": ...}}`, not `{"customfield_X": ...}`.
- **Guessing field IDs.** Use the `/rest/api/3/field` endpoint or the OpenAPI spec to discover the correct field ID and type. Do not assume `customfield_XXXXX` mappings - verify them.
- **Reading `.jira-token` into context.** See `references/auth.md` - never read credentials into the conversation.
