# Authentication and Token Setup

Shared authentication for REST API and GraphQL calls. Both use the same `.jira-token` file with basic auth.

**Never read the `.jira-token` file into context.** Pass it to `curl -u` via shell substitution.

## Token File

The `.jira-token` file lives next to the `acli` executable (same directory). Format is a single line:

```
email@example.com:your-api-token
```

Use the same API token you used to authenticate `acli`.

## Token Discovery (Shell)

```bash
ACLI_DIR="$(dirname "$(readlink -f "$(which acli)" 2>/dev/null || which acli)")"
TOKEN_FILE="$ACLI_DIR/.jira-token"
if [ ! -f "$TOKEN_FILE" ]; then
  echo "ERROR: .jira-token not found next to acli at $ACLI_DIR"
  echo "Create it with: echo 'your-email@example.com:your-api-token' > $TOKEN_FILE"
  echo "Then: chmod 600 $TOKEN_FILE"
  exit 1
fi
AUTH=$(cat "$TOKEN_FILE")
```

The `AUTH` value is `email:api-token`, passed directly as basic auth credentials via `curl -u "$AUTH"`.

## Security

The `.jira-token` file contains plaintext credentials. Restrict permissions:

- Unix/macOS: `chmod 600 .jira-token`
- Windows: restrict access via file properties → Security tab

The `setup.py` script warns when the file is group/world-readable.

## Instance Config

```bash
CLOUD_ID="2b9e35e3-6bd3-4cec-b838-f4249ee02432"
JIRA_BASE="https://redhat.atlassian.net"
GRAPHQL_URL="$JIRA_BASE/gateway/api/graphql"
ORG_ID="4k7c08c0-9kb0-1aca-k606-d1417cc24104"
```

- `CLOUD_ID` - required for all Jira GraphQL queries (`issueSearchStable`, `issueByKey`).
- `GRAPHQL_URL` - the GraphQL endpoint. Derived from `JIRA_BASE`.
- `ORG_ID` - the Atlassian organization ID. Required for the Teams GraphQL API (`team.teamSearchV2` for searching teams by name). Not needed for `team.teamV2` (direct lookup by team ID, which uses `CLOUD_ID` as `siteId`).

### Discovering your cloudId

The `cloudId` above is for `redhat.atlassian.net`. To discover it for any Jira Cloud instance:

```bash
curl -s -u "$AUTH" "$JIRA_BASE/_edge/tenant_info" | python -c "import json,sys; print(json.load(sys.stdin)['cloudId'])"
```

### Discovering your orgId

The `ORG_ID` is visible in the Atlassian admin URL: `https://admin.atlassian.com/o/{ORG_ID}/...`. It can also be found via the Teams API - any team entity returned by `team.teamSearchV2` includes `organizationId` in its response. The value `4k7c08c0-9kb0-1aca-k606-d1417cc24104` is the Red Hat organization.

## Common Auth Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 on REST/GraphQL calls | `.jira-token` is bare token without email prefix | Format must be `email:token` |
| 401 after token was working | API token expired or revoked | User must regenerate at Atlassian account settings |
| `acli auth status` says unauthorized | False negative - `auth status` checks OAuth, not API tokens | Ignore. Use `acli jira project list --recent 1` as smoke test |
| `.jira-token` not found | File is next to symlink, not the real binary | `setup.py` uses `resolve()` to follow symlinks - place file next to real binary |
