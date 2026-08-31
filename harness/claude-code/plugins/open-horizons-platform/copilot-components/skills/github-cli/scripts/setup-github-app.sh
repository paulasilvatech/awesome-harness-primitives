#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - GITHUB APP SETUP
# =============================================================================
#
# Creates and configures GitHub Apps and OAuth Apps for platform integrations.
# With AUTH_PROVIDER=entra and GitHub Enterprise Managed Users, this remains
# the technical GitHub integration path for catalog, scaffolder, Actions, PRs,
# Codespaces, and packages; Entra handles user sign-in.
# Supports Backstage, ArgoCD, and custom integrations
#
# Usage: ./scripts/setup-github-app.sh [options]
#
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Defaults
DRY_RUN=false
APP_TYPE="github-app"
TARGET="backstage"

# Logging
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "${PURPLE}[STEP]${NC} $1"; }

# Usage
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Create and configure GitHub Apps/OAuth Apps for platform integrations.
In Entra ID + GitHub Enterprise Managed Users deployments, create a GitHub App
for Backstage integration even though user login happens through Entra ID.

OPTIONS:
    --github-org        GitHub organization name (required)
    --app-name          Application name (required)
    --homepage-url      Homepage URL (required)
    --callback-url      OAuth callback URL (required)
    --webhook-url       Webhook URL (optional)
    --type              App type: github-app, oauth-app (default: github-app)
    --target            Target integration: backstage, argocd, custom (default: backstage)
    --keyvault          Azure Key Vault name to store secrets
    --dry-run           Show what would be done
    --help              Show this help message

EXAMPLES:
    # Create GitHub App for Backstage
    $(basename "$0") --github-org myorg --app-name myorg-backstage \\
        --homepage-url https://backstage.example.com \\
        --callback-url https://backstage.example.com/api/auth/github/handler/frame \\
        --target backstage

    # Create GitHub App for Backstage in Entra/EMU mode
    $(basename "$0") --github-org myorg --app-name myorg-backstage \
        --homepage-url https://backstage.example.com \
        --callback-url https://backstage.example.com/api/auth/github/handler/frame \
        --target backstage

    # Create OAuth App for ArgoCD
    $(basename "$0") --github-org myorg --app-name myorg-argocd \\
        --homepage-url https://argocd.example.com \\
        --callback-url https://argocd.example.com/api/dex/callback \\
        --type oauth-app --target argocd

EOF
    exit 0
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --github-org)
                GITHUB_ORG="$2"
                shift 2
                ;;
            --app-name)
                APP_NAME="$2"
                shift 2
                ;;
            --homepage-url)
                HOMEPAGE_URL="$2"
                shift 2
                ;;
            --callback-url)
                CALLBACK_URL="$2"
                shift 2
                ;;
            --webhook-url)
                WEBHOOK_URL="$2"
                shift 2
                ;;
            --type)
                APP_TYPE="$2"
                shift 2
                ;;
            --target)
                TARGET="$2"
                shift 2
                ;;
            --keyvault)
                KEYVAULT_NAME="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --help)
                usage
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                ;;
        esac
    done
    
    # Validate required args
    [[ -z "${GITHUB_ORG:-}" ]] && { log_error "Missing: --github-org"; exit 1; }
    [[ -z "${APP_NAME:-}" ]] && { log_error "Missing: --app-name"; exit 1; }
    [[ -z "${HOMEPAGE_URL:-}" ]] && { log_error "Missing: --homepage-url"; exit 1; }
    [[ -z "${CALLBACK_URL:-}" ]] && { log_error "Missing: --callback-url"; exit 1; }
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    local missing=()
    command -v gh &>/dev/null || missing+=("gh (GitHub CLI)")
    command -v jq &>/dev/null || missing+=("jq")
    
    if [[ -n "${KEYVAULT_NAME:-}" ]]; then
        command -v az &>/dev/null || missing+=("az (Azure CLI)")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing prerequisites: ${missing[*]}"
        exit 1
    fi
    
    # Check GitHub login
    if ! gh auth status &>/dev/null; then
        log_error "Not logged in to GitHub. Run: gh auth login"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Generate webhook secret
generate_webhook_secret() {
    openssl rand -hex 32
}

# Create GitHub App manifest
create_github_app_manifest() {
    log_step "Creating GitHub App manifest..."
    
    local webhook_config=""
    if [[ -n "${WEBHOOK_URL:-}" ]]; then
        webhook_config="\"hook_attributes\": {
            \"url\": \"${WEBHOOK_URL}\",
            \"active\": true
        },"
    fi
    
    # Permissions based on target
    local permissions
    case $TARGET in
        backstage)
            permissions='{
                "contents": "read",
                "metadata": "read",
                "pull_requests": "write",
                "issues": "write",
                "workflows": "write",
                "actions": "read",
                "members": "read"
            }'
            ;;
        argocd)
            permissions='{
                "contents": "read",
                "metadata": "read"
            }'
            ;;
        *)
            permissions='{
                "contents": "read",
                "metadata": "read"
            }'
            ;;
    esac
    
    local manifest_dir manifest_file
    manifest_dir="$(mktemp -d "${TMPDIR:-/tmp}/github-app.XXXXXX")"
    manifest_file="${manifest_dir}/github-app-manifest.json"
    cat > "$manifest_file" << EOF
{
    "name": "${APP_NAME}",
    "url": "${HOMEPAGE_URL}",
    ${webhook_config}
    "redirect_url": "${CALLBACK_URL}",
    "callback_urls": ["${CALLBACK_URL}"],
    "public": false,
    "default_permissions": ${permissions},
    "default_events": [
        "push",
        "pull_request",
        "repository"
    ]
}
EOF
    
    log_success "Manifest created: ${manifest_file}"
    cat "$manifest_file"
}

# Create GitHub App (manual steps)
create_github_app() {
    log_step "Creating GitHub App..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create GitHub App: $APP_NAME"
        create_github_app_manifest
        return
    fi
    
    # GitHub Apps cannot be created fully via CLI - provide instructions
    create_github_app_manifest
    
    echo ""
    log_warning "GitHub Apps must be created via web UI:"
    echo ""
    echo "1. Go to: https://github.com/organizations/${GITHUB_ORG}/settings/apps/new"
    echo ""
    echo "2. Fill in the following:"
    echo "   - GitHub App name: ${APP_NAME}"
    echo "   - Homepage URL: ${HOMEPAGE_URL}"
    echo "   - Callback URL: ${CALLBACK_URL}"
    if [[ -n "${WEBHOOK_URL:-}" ]]; then
        echo "   - Webhook URL: ${WEBHOOK_URL}"
        echo "   - Webhook secret: $(generate_webhook_secret)"
    fi
    echo ""
    echo "3. Set permissions based on target ($TARGET):"
    echo "   - Repository: Contents (Read)"
    echo "   - Repository: Metadata (Read)"
    if [[ "$TARGET" == "backstage" ]]; then
        echo "   - Repository: Pull requests (Write)"
        echo "   - Repository: Issues (Write)"
        echo "   - Repository: Workflows (Write)"
        echo "   - Repository: Actions (Read)"
        echo "   - Organization: Members (Read)"
    fi
    echo ""
    echo "4. After creation:"
    echo "   - Note the App ID"
    echo "   - Generate a Private Key"
    echo "   - Install the app on your organization"
    echo ""
    echo "5. Run this script again with --store-credentials to save to Key Vault"
}

# Create OAuth App
create_oauth_app() {
    log_step "Creating OAuth App..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create OAuth App: $APP_NAME"
        return
    fi
    
    # OAuth Apps also need web UI
    echo ""
    log_warning "OAuth Apps must be created via web UI:"
    echo ""
    echo "1. Go to: https://github.com/organizations/${GITHUB_ORG}/settings/applications/new"
    echo ""
    echo "2. Fill in:"
    echo "   - Application name: ${APP_NAME}"
    echo "   - Homepage URL: ${HOMEPAGE_URL}"
    echo "   - Authorization callback URL: ${CALLBACK_URL}"
    echo ""
    echo "3. After creation, note the Client ID and generate a Client Secret"
}

# Create org webhook
create_webhook() {
    if [[ -z "${WEBHOOK_URL:-}" ]]; then
        return
    fi
    
    log_step "Creating organization webhook..."
    
    WEBHOOK_SECRET=$(generate_webhook_secret)
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create webhook for: $WEBHOOK_URL"
        return
    fi
    
    # Create webhook via API
    gh api \
        --method POST \
        -H "Accept: application/vnd.github+json" \
        "/orgs/${GITHUB_ORG}/hooks" \
        -f name='web' \
        -f "config[url]=${WEBHOOK_URL}" \
        -f config[content_type]='json' \
        -f "config[secret]=${WEBHOOK_SECRET}" \
        -F active=true \
        -f events[]='push' \
        -f events[]='pull_request' \
        -f events[]='repository' || {
            log_warning "Could not create webhook (may need admin access)"
            return
        }
    
    log_success "Webhook created"
    echo "Webhook secret: ${WEBHOOK_SECRET}"
    echo ""
    log_warning "Save this webhook secret - it won't be shown again!"
}

# Store credentials in Key Vault
store_keyvault_credentials() {
    if [[ -z "${KEYVAULT_NAME:-}" ]]; then
        return
    fi
    
    log_step "Storing credentials in Key Vault: $KEYVAULT_NAME"
    
    echo ""
    echo "To store credentials, run:"
    echo ""
    echo "# GitHub App credentials"
    echo "az keyvault secret set --vault-name ${KEYVAULT_NAME} --name github-app-id --value '<APP_ID>'"
    echo "az keyvault secret set --vault-name ${KEYVAULT_NAME} --name github-app-private-key --file '<PRIVATE_KEY_FILE>'"
    echo "az keyvault secret set --vault-name ${KEYVAULT_NAME} --name github-app-webhook-secret --value '<WEBHOOK_SECRET>'"
    echo ""
    echo "# OAuth App credentials"
    echo "az keyvault secret set --vault-name ${KEYVAULT_NAME} --name github-oauth-client-id --value '<CLIENT_ID>'"
    echo "az keyvault secret set --vault-name ${KEYVAULT_NAME} --name github-oauth-client-secret --value '<CLIENT_SECRET>'"
}

# Generate Kubernetes secret manifest
generate_k8s_secret() {
    log_step "Generating Kubernetes secret manifest..."
    
    local namespace
    case $TARGET in
        backstage) namespace="backstage" ;;
        argocd) namespace="argocd" ;;
        *) namespace="default" ;;
    esac
    
    cat << EOF

# Apply after filling in values:
---
apiVersion: v1
kind: Secret
metadata:
  name: github-app-credentials
  namespace: ${namespace}
type: Opaque
stringData:
  GITHUB_APP_ID: "<APP_ID>"
  GITHUB_APP_CLIENT_ID: "<CLIENT_ID>"
  GITHUB_APP_CLIENT_SECRET: "<CLIENT_SECRET>"
  GITHUB_APP_WEBHOOK_SECRET: "<WEBHOOK_SECRET>"
  GITHUB_APP_PRIVATE_KEY: |
    -----BEGIN RSA PRIVATE KEY-----
    <PRIVATE_KEY_CONTENT>
    -----END RSA PRIVATE KEY-----
EOF
}

# Print summary
print_summary() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  GITHUB APP SETUP SUMMARY${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Configuration:"
    echo "  Organization: ${GITHUB_ORG}"
    echo "  App Name:     ${APP_NAME}"
    echo "  App Type:     ${APP_TYPE}"
    echo "  Target:       ${TARGET}"
    echo "  Homepage:     ${HOMEPAGE_URL}"
    echo "  Callback:     ${CALLBACK_URL}"
    [[ -n "${WEBHOOK_URL:-}" ]] && echo "  Webhook:      ${WEBHOOK_URL}"
    echo ""
    
    if [[ "$TARGET" == "backstage" ]]; then
        echo "Backstage app-config.yaml configuration:"
        cat << EOF
integrations:
  github:
    - host: github.com
      apps:
        - appId: \${GITHUB_APP_ID}
          clientId: \${GITHUB_APP_CLIENT_ID}
          clientSecret: \${GITHUB_APP_CLIENT_SECRET}
          webhookSecret: \${GITHUB_APP_WEBHOOK_SECRET}
          privateKey: \${GITHUB_APP_PRIVATE_KEY}
EOF
    elif [[ "$TARGET" == "argocd" ]]; then
        echo "ArgoCD Dex configuration:"
        cat << EOF
dex.config: |
  connectors:
    - type: github
      id: github
      name: GitHub
      config:
        clientID: \${GITHUB_OAUTH_CLIENT_ID}
        clientSecret: \${GITHUB_OAUTH_CLIENT_SECRET}
        orgs:
          - name: ${GITHUB_ORG}
EOF
    fi
}

# Main
main() {
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  OPEN HORIZONS - GITHUB APP SETUP                         ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    parse_args "$@"
    
    [[ "$DRY_RUN" == "true" ]] && log_warning "DRY-RUN MODE"
    
    check_prerequisites
    
    if [[ "$APP_TYPE" == "github-app" ]]; then
        create_github_app
    else
        create_oauth_app
    fi
    
    create_webhook
    store_keyvault_credentials
    generate_k8s_secret
    print_summary
    
    log_success "GitHub App setup instructions complete!"
}

main "$@"
