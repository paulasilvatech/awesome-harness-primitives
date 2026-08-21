# Service Principal and CI/CD Pipeline Templates

Reusable scripts for running the Fabric Git integration lifecycle headlessly (no
interactive login) from a CI/CD pipeline, driven by the Fabric CLI (`fab`).

These templates use the verified `fab` 1.6.1 output shape: `fab api <endpoint>`
prints `{"status_code": <code>, "text": <parsed body>}`, so response fields are
read with `jq -r '.text.<field>'`. Request bodies are passed with `-i` as either
a file path or an inline JSON string (`fab api` never reads a body from stdin).
Long-running operations return
`202`; capture `x-ms-operation-id` from `--show_headers` and poll
`operations/{id}` until `.text.status` is `Succeeded`.

Prerequisites for every template below:

- The service principal (or managed identity) is workspace **Admin** on the target
  workspace, and the workspace is assigned to a **capacity**.
- Install the Fabric CLI: `pip install -q ms-fabric-cli==1.6.1` (pin to keep `jq`
  output-shape parsing stable across CLI releases).
- Authenticate: `fab auth login -u "$CLIENT_ID" -p "$CLIENT_SECRET" --tenant
  "$TENANT_ID"` (or use `az login --service-principal` for the `az rest` fallback).
- For any provider driven by automation, `myGitCredentials` uses a
  `ConfiguredConnection` (a Fabric cloud connection holding the git credentials).
  See [SKILL.md § Create the Git provider connection (service principal)](../SKILL.md#create-the-git-provider-connection-service-principal).

## Reusable helper: poll a long-running operation

```bash
# Usage: wait_for_lro "<operation-id>"
wait_for_lro() {
  local op="$1" st i
  # Bounded poll (~10 min at 5s) so a stuck Running aborts instead of hanging
  # until the pipeline job timeout; Failed/Undefined are terminal too.
  for i in $(seq 1 120); do
    st=$(fab api "operations/${op}" | jq -r '.text.status')
    case "$st" in
      Succeeded)        echo "LRO ${op}: Succeeded"; return 0 ;;
      Failed|Undefined) echo "LRO ${op}: ${st}"; fab api "operations/${op}" | jq '.text.error'; return 1 ;;
      *)                sleep 5 ;;
    esac
  done
  echo "LRO ${op}: timed out after ~10m (last status: ${st:-unknown})"; return 1
}
```

## Bash: service principal status check, then update

End-to-end headless sync: authenticate, read status, and update the workspace from
Git only when the branch is ahead.

```bash
#!/usr/bin/env bash
set -euo pipefail
# Prerequisites: install CLI and authenticate — see Prerequisites section above.

WORKSPACE_ID="${WORKSPACE_ID:?Set WORKSPACE_ID}"

STATUS=$(fab api "workspaces/${WORKSPACE_ID}/git/status")
REMOTE=$(echo "$STATUS" | jq -r '.text.remoteCommitHash')
HEAD=$(echo "$STATUS" | jq -r '.text.workspaceHead')
echo "workspaceHead=$HEAD remoteCommitHash=$REMOTE"

if [ "$REMOTE" != "$HEAD" ]; then
  cat > update.json <<JSON
{
  "workspaceHead": "${HEAD}",
  "remoteCommitHash": "${REMOTE}",
  "conflictResolution": { "conflictResolutionType": "Workspace", "conflictResolutionPolicy": "PreferRemote" },
  "options": { "allowOverrideItems": true }
}
JSON
  RESP=$(fab api -X post "workspaces/${WORKSPACE_ID}/git/updateFromGit" -i update.json --show_headers)
  # updateFromGit may finish synchronously (200) or async (202); only poll when async.
  if [ "$(echo "$RESP" | jq -r '.status_code')" = "202" ]; then
    wait_for_lro "$(echo "$RESP" | jq -r '.headers["x-ms-operation-id"]')"
  fi
else
  echo "Workspace already in sync; nothing to update."
fi
```

## Bash: commit all workspace changes

```bash
#!/usr/bin/env bash
set -euo pipefail
# Assumes fab auth login already ran.
WORKSPACE_ID="${WORKSPACE_ID:?Set WORKSPACE_ID}"
COMMIT_MSG="${COMMIT_MSG:-Automated commit from CI/CD pipeline}"

STATUS=$(fab api "workspaces/${WORKSPACE_ID}/git/status")
HEAD=$(echo "$STATUS" | jq -r '.text.workspaceHead')
COUNT=$(echo "$STATUS" | jq '.text.changes | length')

if [ "$COUNT" -eq 0 ]; then
  echo "No workspace changes to commit."
  exit 0
fi

# jq builds a JSON-safe body so a comment with a quote, backslash, or newline
# can't corrupt the request (COMMIT_MSG often comes from a git title or PR message).
jq -n --arg head "$HEAD" --arg msg "$COMMIT_MSG" \
  '{mode:"All", workspaceHead:$head, comment:$msg}' > commit.json
RESP=$(fab api -X post "workspaces/${WORKSPACE_ID}/git/commitToGit" -i commit.json --show_headers)
# commitToGit may finish synchronously (200) or async (202); only poll when async.
if [ "$(echo "$RESP" | jq -r '.status_code')" = "202" ]; then
  wait_for_lro "$(echo "$RESP" | jq -r '.headers["x-ms-operation-id"]')"
fi
```

## Azure DevOps pipeline (YAML)

```yaml
trigger:
  branches:
    include: [ main ]

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: fabric-credentials   # TENANT_ID, CLIENT_ID, CLIENT_SECRET, WORKSPACE_ID

steps:
  - task: Bash@3
    displayName: 'Update Fabric workspace from Git'
    inputs:
      targetType: inline
      script: |
        set -euo pipefail
        # Prerequisites: install CLI and authenticate — see Prerequisites section above.

        STATUS=$(fab api "workspaces/$(WORKSPACE_ID)/git/status")
        REMOTE=$(echo "$STATUS" | jq -r '.text.remoteCommitHash')
        HEAD=$(echo "$STATUS" | jq -r '.text.workspaceHead')

        cat > update.json <<JSON
        { "workspaceHead": "$HEAD", "remoteCommitHash": "$REMOTE",
          "conflictResolution": { "conflictResolutionType": "Workspace", "conflictResolutionPolicy": "PreferRemote" },
          "options": { "allowOverrideItems": true } }
        JSON

        RESP=$(fab api -X post "workspaces/$(WORKSPACE_ID)/git/updateFromGit" -i update.json --show_headers)
        if [ "$(echo "$RESP" | jq -r '.status_code')" = "202" ]; then
          OP=$(echo "$RESP" | jq -r '.headers["x-ms-operation-id"]')
          for i in $(seq 1 120); do
            ST=$(fab api "operations/$OP" | jq -r '.text.status')
            [ "$ST" = "Succeeded" ] && break
            case "$ST" in Failed|Undefined) fab api "operations/$OP" | jq '.text.error'; exit 1 ;; esac
            [ "$i" = "120" ] && { echo "timed out waiting for $OP"; exit 1; }
            sleep 5
          done
        fi
```

## GitHub Actions workflow

```yaml
name: Sync Fabric Workspace
on:
  push:
    branches: [ main ]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Prerequisites: install CLI and authenticate — see Prerequisites section above.

      - name: Update workspace from Git
        env:
          WS: ${{ secrets.WORKSPACE_ID }}
        run: |
          set -euo pipefail
          STATUS=$(fab api "workspaces/$WS/git/status")
          REMOTE=$(echo "$STATUS" | jq -r '.text.remoteCommitHash')
          HEAD=$(echo "$STATUS" | jq -r '.text.workspaceHead')

          cat > update.json <<JSON
          { "workspaceHead": "$HEAD", "remoteCommitHash": "$REMOTE",
            "conflictResolution": { "conflictResolutionType": "Workspace", "conflictResolutionPolicy": "PreferRemote" },
            "options": { "allowOverrideItems": true } }
          JSON

          RESP=$(fab api -X post "workspaces/$WS/git/updateFromGit" -i update.json --show_headers)
          if [ "$(echo "$RESP" | jq -r '.status_code')" = "202" ]; then
            OP=$(echo "$RESP" | jq -r '.headers["x-ms-operation-id"]')
            for i in $(seq 1 120); do
              ST=$(fab api "operations/$OP" | jq -r '.text.status')
              [ "$ST" = "Succeeded" ] && break
              case "$ST" in Failed|Undefined) fab api "operations/$OP" | jq '.text.error'; exit 1 ;; esac
              [ "$i" = "120" ] && { echo "timed out waiting for $OP"; exit 1; }
              sleep 5
            done
          fi
```

## Notes

- On the `az rest` fallback, drop `fab auth login` for `az login --service-principal
  -u <client-id> -p <client-secret> --tenant <tenant-id>` and translate each call as
  in [SKILL.md § Example 2](../SKILL.md#example-2-az-rest-fallback-equivalents).
- Promoting item **definitions** from a cloned repo into a workspace (`fab deploy`)
  is a deployment concern and is out of scope for this Git integration skill.
