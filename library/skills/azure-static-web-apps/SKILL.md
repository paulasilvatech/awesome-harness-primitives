---
name: azure-static-web-apps
description: >-
  Create, configure, run, and deploy Azure Static Web Apps with the SWA CLI. Use when asked to deploy a static site to Azure, run SWA locally, configure staticwebapp.config.json, add Azure Functions APIs, set API runtimes, database connections, or GitHub Actions CI/CD for Static Web Apps.
---

# Azure Static Web Apps

Configure an Azure Static Web Apps project from an existing frontend and optional API, use the SWA CLI for local emulation and deployment, and produce the exact commands and files needed.

## When to invoke

- "Deploy this static site to Azure Static Web Apps."
- "Set up SWA local development with an API folder."
- "Configure staticwebapp.config.json routes and auth."
- "Add Azure Functions to my Static Web App."
- "Create a GitHub Actions workflow for Azure Static Web Apps."

## Prerequisites and context

- Install the SWA CLI with `npm install -D @azure/static-web-apps-cli` and verify with `npx swa --version`.
- `swa-cli.config.json` is CLI settings and is created by `swa init`; never create it manually.
- `staticwebapp.config.json` is runtime configuration for routes, auth, headers, navigation fallback, and API runtime; it can be created manually in the app source or output folder.
- Local SWA emulation defaults to `http://localhost:4280`; common dev server URLs include `http://localhost:3000`.

## Procedure

1. Install the CLI: `npm install -D @azure/static-web-apps-cli`.
2. Run `npx swa init` or `npx swa init --yes` before any `swa start` or `swa deploy`; this creates `swa-cli.config.json` with framework detection.
3. Build the application with the existing project command such as `npm run build` when needed.
4. Run `npx swa start` or a scoped `swa start` command to test locally.
5. Authenticate with `npx swa login`.
6. Deploy with `npx swa deploy --env production` or a preview deployment.
7. Validate routing, API calls, auth, and deployment output.

## Configuration files

| File | Created by | Purpose | Key fields |
| --- | --- | --- | --- |
| `swa-cli.config.json` | `swa init` only | CLI project settings. | `$schema`, `configurations`, `appLocation`, `apiLocation`, `outputLocation`, `appBuildCommand`, `apiBuildCommand`, `run`, `appDevserverUrl`. |
| `staticwebapp.config.json` | Manually or framework output | Runtime behavior. | `navigationFallback`, `rewrite`, `exclude`, `routes`, `allowedRoles`, `platform.apiRuntime`, headers, auth. |
| `.github/workflows/azure-static-web-apps.yml` | Azure portal, Azure CLI, or manual | CI/CD deployment. | `azure_static_web_apps_api_token`, `repo_token`, `action`, `app_location`, `api_location`, `output_location`, `skip_app_build`, `app_build_command`. |

```json
{
  "$schema": "https://aka.ms/azure/static-web-apps-cli/schema",
  "configurations": {
    "app": {
      "appLocation": ".",
      "apiLocation": "api",
      "outputLocation": "dist",
      "appBuildCommand": "npm run build",
      "run": "npm run dev",
      "appDevserverUrl": "http://localhost:3000"
    }
  }
}
```

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*", "/css/*"]
  },
  "routes": [
    { "route": "/api/*", "allowedRoles": ["authenticated"] }
  ],
  "platform": { "apiRuntime": "node:20" }
}
```

## Command reference

| Command | Use | Examples and flags |
| --- | --- | --- |
| `swa login` | Authenticate with Azure for deployment. | `swa login`, `swa login --subscription-id <id>`, `swa login --clear-credentials`; flags: `--subscription-id, -S`, `--resource-group, -R`, `--tenant-id, -T`, `--client-id, -C`, `--client-secret, -CS`, `--app-name, -n`. |
| `swa init` | Configure an existing frontend and optional API. | `swa init`, `swa init --yes`. |
| `swa build` | Build frontend and/or API. | `swa build`, `swa build --auto`, `swa build myApp`; flags: `--app-location, -a`, `--api-location, -i`, `--output-location, -O`, `--app-build-command, -A`, `--api-build-command, -I`. |
| `swa start` | Start local emulator. | `swa start`, `swa start ./dist`, `swa start http://localhost:3000`, `swa start ./dist --api-location ./api`, `swa start http://localhost:3000 --run "npm start"`; flags: `--port, -p`, `--api-location, -i`, `--api-port, -j`, `--run, -r`, `--open, -o`, `--ssl, -s`. |
| `swa deploy` | Deploy to Azure Static Web Apps. | `swa deploy`, `swa deploy ./dist`, `swa deploy --env production`, `swa deploy --deployment-token <TOKEN>`, `swa deploy --dry-run`, `swa deploy --print-token`; flags: `--env`, `--deployment-token, -d`, `--app-name, -n`. |
| `swa db` | Initialize database connections. | `swa db init --database-type mssql`, `swa db init --database-type postgresql`, `swa db init --database-type cosmosdb_nosql`. |

| Framework | Common port |
| --- | --- |
| React/Vue/Next.js | 3000 |
| Angular | 4200 |
| Vite | 5173 |


## Deployment vocabulary

Preserve these SWA distinctions when writing commands or workflows: `IMPORTANT`, `REQUIRED`, `auto-detects`, `auto-detection`, `auto-detected`, `auto-generated`, `preview`, `production`, `HTTPS`, `pre-built`, and `skip_app_build: true`. Use `preview` for non-production environments and `production` only when deploying the live environment.

## Azure Functions API

Create an API folder only when the app needs serverless endpoints.

```bash
mkdir api && cd api
func init --worker-runtime node --model V4
func new --name message --template "HTTP trigger"
```

`api/src/functions/message.js`:

```javascript
const { app } = require('@azure/functions');

app.http('message', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: async (request) => {
        const name = request.query.get('name') || 'World';
        return { jsonBody: { message: `Hello, ${name}!` } };
    }
});
```

Set API runtime in `staticwebapp.config.json` and keep the CLI config generated by `swa init` aligned:

```json
{ "platform": { "apiRuntime": "node:20" } }
```

Supported API runtimes are `node:18`, `node:20`, `node:22`, `dotnet:8.0`, `dotnet-isolated:8.0`, `python:3.10`, and `python:3.11`. Test with `npx swa start ./dist --api-location ./api` and access the API at `http://localhost:4280/api/message`.

## GitHub Actions deployment

Use Azure portal or Azure CLI to create the Static Web App and copy the deployment token to the repository secret `AZURE_STATIC_WEB_APPS_API_TOKEN`. The action also uses `GITHUB_TOKEN`.

```yaml
name: Azure Static Web Apps CI/CD
on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]
jobs:
  build_and_deploy:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: /
          api_location: api
          output_location: dist
  close_pr:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: close
```

Get deployment tokens from Azure Portal → Static Web App → Manage deployment token, `swa deploy --print-token`, or `SWA_CLI_DEPLOYMENT_TOKEN`.

## Troubleshooting

| Issue | Solution |
| --- | --- |
| 404 on client routes | Add `navigationFallback` with `rewrite: "/index.html"` to `staticwebapp.config.json`. |
| API returns 404 | Verify `api` folder structure, `platform.apiRuntime`, and function exports. |
| Build output not found | Verify `output_location` matches actual build output directory. |
| Auth not working locally | Use `/.auth/login/<provider>` to access auth emulator UI. |
| CORS errors | APIs under `/api/*` are same-origin; external APIs need CORS headers. |
| Deployment token expired | Regenerate in Azure Portal → Static Web App → Manage deployment token. |
| Config not applied | Ensure `staticwebapp.config.json` is in `app_location` or `output_location`. |
| Local API timeout | Default is 45 seconds; optimize the function or check for blocking calls. |

Debug with `swa start --verbose log`, `swa deploy --dry-run`, and `swa --print-config`.

## Output template

```markdown
## Azure Static Web Apps result

**Status:** configured | deployed | blocked
**App location:** `<app_location>`
**API location:** `<api_location or none>`
**Output location:** `<output_location>`

### Commands
- `npm install -D @azure/static-web-apps-cli`
- `npx swa init` or `npx swa init --yes`
- `<build command>`
- `<swa start command>`
- `<swa deploy command>`

### Files
| File | Status | Notes |
| --- | --- | --- |
| `swa-cli.config.json` | generated by `swa init` | <key settings> |
| `staticwebapp.config.json` | created / updated / unchanged | <routes, auth, runtime> |
| `.github/workflows/azure-static-web-apps.yml` | created / updated / unchanged | <token secret and paths> |

### Validation
- Local emulator `http://localhost:4280`: pass | fail | not run
- API `http://localhost:4280/api/message`: pass | fail | not applicable
- Deployment: pass | fail | not run
```

## Quality gate

- [ ] `swa init` is used to create `swa-cli.config.json`; the file is not manually invented.
- [ ] `staticwebapp.config.json` is placed in `app_location` or `output_location` when runtime config is needed.
- [ ] `output_location` matches the actual build output.
- [ ] API projects set a supported `platform.apiRuntime` and are tested through the SWA emulator.
- [ ] Deployment uses `AZURE_STATIC_WEB_APPS_API_TOKEN`, `SWA_CLI_DEPLOYMENT_TOKEN`, or an authenticated `swa login`; no token is committed.
- [ ] Client routing, auth, and `/api/*` behavior are validated locally or marked not run with a reason.

## References

- [SWA CLI schema](https://aka.ms/azure/static-web-apps-cli/schema)
