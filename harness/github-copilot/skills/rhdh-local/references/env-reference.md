# Environment Variable Reference

Environment variables for configuring local RHDH instances via `rhdh-customizations/.env`.
See `scripts/NOTICE` for attribution.

<variables>

## Database (PostgreSQL)

Defaults work out of the box. Override only if using an external database.

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_DB` | `postgres` | Database name |
| `POSTGRES_HOST` | `db` | Database hostname (container name) |
| `POSTGRES_PORT` | `5432` | Database port |
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | `postgres` | Database password |

## GitHub Integration

Required for GitHub OAuth, org ingestion, and Scorecard plugin.

| Variable | Default | Description |
|----------|---------|-------------|
| `GITHUB_ORG` | | GitHub organization for catalog ingestion |
| `GITHUB_HOST_DOMAIN` | `https://github.com` | GitHub instance URL (change for GHE) |
| `AUTH_GITHUB_CLIENT_ID` | | OAuth app client ID |
| `AUTH_GITHUB_CLIENT_SECRET` | | OAuth app client secret |
| `GITHUB_TOKEN` | | Personal access token (for Scorecard plugin) |

## Jenkins

Required only if Jenkins is enabled via `compose.override.yaml`.

| Variable | Default | Description |
|----------|---------|-------------|
| `JENKINS_URL` | `http://jenkins:8080` | Jenkins base URL |
| `JENKINS_USERNAME` | | Jenkins admin user |
| `JENKINS_TOKEN` | | Jenkins API token |
| `JENKINS_CONFIG_PATH` | `.jenkins-data` | Path to Jenkins home dir to mount |

## Jira

Optional. Required for Jira Scorecard integration.

| Variable | Default | Description |
|----------|---------|-------------|
| `JIRA_BASE_URL` | | e.g., `https://your-instance.atlassian.net` |
| `JIRA_TOKEN` | | Base64-encoded API token |

## Email / SMTP

Optional. Required for feedback and notification plugins.

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_SENDER` | | Sender address for feedback emails |
| `EMAIL_USER` | | SMTP login username |
| `EMAIL_PASSWORD` | | SMTP password (use app-specific password) |
| `EMAIL_HOSTNAME` | `smtp.gmail.com` | SMTP server hostname |
| `EMAIL_PORT` | `587` | SMTP server port |

## Container Images

Override to pin specific RHDH versions.

| Variable | Default | Description |
|----------|---------|-------------|
| `RHDH_IMAGE` | `quay.io/rhdh-community/rhdh:<version>` | RHDH container image (check `rhdh-local/default.env` for current default) |
| `CATALOG_INDEX_IMAGE` | `quay.io/rhdh/plugin-catalog-index:<version>` | Extensions Catalog image (check `rhdh-local/default.env` for current default) |
| `CATALOG_ENTITIES_EXTRACT_DIR` | `/extensions` | Catalog entities extract path |

## Lightspeed / AI

Configure the LLM provider for the Lightspeed plugin.

### Ollama (default, local)

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://ollama:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.2:1b` | Model to use |
| `OLLAMA_MODELS_PATH` | | Host path to persist models across removals |

### External LLM Providers (set ONE to true)

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_VLLM` | | Enable vLLM provider |
| `ENABLE_OPENAI` | | Enable OpenAI provider |
| `ENABLE_VERTEX_AI` | | Enable Vertex AI provider |

### vLLM

| Variable | Default | Description |
|----------|---------|-------------|
| `VLLM_URL` | | vLLM endpoint (must end with `/v1`) |
| `VLLM_API_KEY` | | API key |
| `VLLM_MAX_TOKENS` | `4096` | Max tokens per request |
| `VLLM_TLS_VERIFY` | `true` | Verify TLS certificates |

### OpenAI

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | | OpenAI API key |

### Vertex AI

| Variable | Default | Description |
|----------|---------|-------------|
| `VERTEX_AI_CREDENTIALS_PATH` | | Path to service account JSON |
| `VERTEX_AI_PROJECT` | | GCP project ID |
| `VERTEX_AI_LOCATION` | `us-central1` | GCP region |

## Safety Guard (Llama Guard)

Optional content filtering for Lightspeed.

| Variable | Default | Description |
|----------|---------|-------------|
| `SAFETY_MODEL` | | Safety model name |
| `SAFETY_URL` | | Safety model API endpoint |
| `SAFETY_API_KEY` | | Safety model API key |

## Node / Telemetry / Logging

Fine-tuning RHDH runtime behavior.

| Variable | Default | Description |
|----------|---------|-------------|
| `NODE_ENV` | `development` | Node environment |
| `NODE_TLS_REJECT_UNAUTHORIZED` | `0` | Set to `1` in production |
| `LOG_LEVEL` | | RHDH log level (debug, info, warn, error) |
| `BASE_URL` | `http://localhost:7007` | RHDH base URL |
| `SEGMENT_WRITE_KEY` | | Telemetry key (empty = disabled) |
| `SEGMENT_TEST_MODE` | `true` | Test mode for telemetry |

</variables>

<usage>

## How to Use

1. Copy `.env.example` to `.env` in `rhdh-customizations/`:

   ```bash
   cp rhdh-customizations/.env.example rhdh-customizations/.env
   ```

2. Edit `.env` with your values - only set what you need, defaults handle the rest.

3. Apply and restart:

   ```bash
   rhdh local apply
   rhdh local down && rhdh local up --customized
   ```

**Security note:** `.env` files often contain secrets (tokens, passwords). They are gitignored by default. Use `rhdh local backup` to archive them safely - the backup command warns about credential files.

</usage>
