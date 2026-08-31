#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - IDENTITY FEDERATION SETUP
# =============================================================================
#
# Configures Azure ↔ GitHub identity federation using OIDC
# No secrets required - uses federated credentials
#
# Usage: ./scripts/setup-identity-federation.sh [options]
#
# Options:
#   --github-org        GitHub organization name
#   --github-repo       GitHub repository name (or * for all)
#   --resource-group    Azure resource group for RBAC
#   --app-name          App registration name
#   --environments      Comma-separated environments (dev,staging,prod)
#   --dry-run           Show what would be done without executing
#   --help              Show this help message
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
ENVIRONMENTS="main,dev,staging,prod"
ENABLE_PR_FEDERATION=true

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

Configure Azure ↔ GitHub identity federation using OIDC.

OPTIONS:
    --github-org        GitHub organization name (required)
    --github-repo       GitHub repository name, or * for all repos (required)
    --resource-group    Azure resource group for RBAC assignment (required)
    --app-name          App registration display name (default: {project}-github-actions)
    --environments      Comma-separated environments (default: main,dev,staging,prod)
    --no-pr-federation  Skip federated credential for pull requests
    --dry-run           Show what would be done without executing
    --help              Show this help message

EXAMPLES:
    $(basename "$0") --github-org myorg --github-repo platform-gitops --resource-group rg-prod
    $(basename "$0") --github-org myorg --github-repo "*" --resource-group rg-prod --environments dev,prod

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
            --github-repo)
                GITHUB_REPO="$2"
                shift 2
                ;;
            --resource-group)
                RESOURCE_GROUP="$2"
                shift 2
                ;;
            --app-name)
                APP_NAME="$2"
                shift 2
                ;;
            --environments)
                ENVIRONMENTS="$2"
                shift 2
                ;;
            --no-pr-federation)
                ENABLE_PR_FEDERATION=false
                shift
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
    if [[ -z "${GITHUB_ORG:-}" ]]; then
        log_error "Missing required argument: --github-org"
        exit 1
    fi
    if [[ -z "${GITHUB_REPO:-}" ]]; then
        log_error "Missing required argument: --github-repo"
        exit 1
    fi
    if [[ -z "${RESOURCE_GROUP:-}" ]]; then
        log_error "Missing required argument: --resource-group"
        exit 1
    fi
    
    # Set defaults
    APP_NAME="${APP_NAME:-${GITHUB_ORG}-github-actions}"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    local missing=()
    
    command -v az &>/dev/null || missing+=("az (Azure CLI)")
    command -v gh &>/dev/null || missing+=("gh (GitHub CLI)")
    command -v jq &>/dev/null || missing+=("jq")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing prerequisites: ${missing[*]}"
        exit 1
    fi
    
    # Check Azure login
    if ! az account show &>/dev/null; then
        log_error "Not logged in to Azure. Run: az login"
        exit 1
    fi
    
    # Check GitHub login
    if ! gh auth status &>/dev/null; then
        log_error "Not logged in to GitHub. Run: gh auth login"
        exit 1
    fi
    
    log_success "All prerequisites met"
}

# Create App Registration
create_app_registration() {
    log_step "Creating App Registration: $APP_NAME"
    
    # Check if app already exists
    EXISTING_APP=$(az ad app list --display-name "$APP_NAME" --query "[0].appId" -o tsv 2>/dev/null || echo "")
    
    if [[ -n "$EXISTING_APP" ]]; then
        log_warning "App Registration already exists: $EXISTING_APP"
        APP_ID="$EXISTING_APP"
    else
        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY-RUN] Would create App Registration: $APP_NAME"
            APP_ID="dry-run-app-id"
        else
            APP_ID=$(az ad app create \
                --display-name "$APP_NAME" \
                --sign-in-audience "AzureADMyOrg" \
                --query appId -o tsv)
            log_success "Created App Registration: $APP_ID"
        fi
    fi
    
    # Create Service Principal if not exists
    if [[ "$DRY_RUN" != "true" ]]; then
        if ! az ad sp show --id "$APP_ID" &>/dev/null; then
            az ad sp create --id "$APP_ID" >/dev/null
            log_success "Created Service Principal"
        fi
    fi
}

# Create a federated identity credential.
#   $1 name · $2 subject/pattern · $3 description · $4 use_wildcard(true|false)
# When use_wildcard=true the subject contains a "*" and a standard subject match
# is impossible, so a *flexible* FIC is emitted using claimsMatchingExpression
# (claims['sub'] matches '<pattern>'), per the Azure workload-identity docs.
# The parameter file is created with mktemp and always removed via a RETURN trap.
create_fic() {
    local name="$1" subject="$2" description="$3" use_wildcard="$4"
    local tmp
    tmp="$(mktemp "${TMPDIR:-/tmp}/fedcred.XXXXXX")"
    # shellcheck disable=SC2064
    trap "rm -f '$tmp'" RETURN

    if [[ "$use_wildcard" == "true" ]]; then
        cat > "$tmp" << EOF
{
  "name": "${name}",
  "issuer": "https://token.actions.githubusercontent.com",
  "audiences": ["api://AzureADTokenExchange"],
  "description": "${description}",
  "claimsMatchingExpression": {
    "value": "claims['sub'] matches '${subject}'",
    "languageVersion": 1
  }
}
EOF
    else
        cat > "$tmp" << EOF
{
  "name": "${name}",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "${subject}",
  "description": "${description}",
  "audiences": ["api://AzureADTokenExchange"]
}
EOF
    fi

    az ad app federated-credential create \
        --id "$APP_ID" \
        --parameters "@$tmp" >/dev/null
}

# Create Federated Credentials
create_federated_credentials() {
    log_step "Creating Federated Credentials..."

    local use_wildcard="false"
    local repo_pattern
    if [[ "$GITHUB_REPO" == "*" ]]; then
        use_wildcard="true"
        repo_pattern="repo:${GITHUB_ORG}/*"
        log_info "Org-wide scope requested: using flexible FIC (claimsMatchingExpression)"
    else
        repo_pattern="repo:${GITHUB_ORG}/${GITHUB_REPO}"
    fi

    # Create credential for each environment
    IFS=',' read -ra ENV_ARRAY <<< "$ENVIRONMENTS"
    for env in "${ENV_ARRAY[@]}"; do
        local cred_name="github-${env}"
        local subject

        if [[ "$env" == "main" ]]; then
            subject="${repo_pattern}:ref:refs/heads/main"
        else
            subject="${repo_pattern}:environment:${env}"
        fi

        log_info "Creating federated credential: $cred_name"

        if [[ "$DRY_RUN" == "true" ]]; then
            if [[ "$use_wildcard" == "true" ]]; then
                log_info "[DRY-RUN] claimsMatchingExpression: claims['sub'] matches '${subject}'"
            else
                log_info "[DRY-RUN] Subject: $subject"
            fi
            continue
        fi

        # Check if credential exists
        if az ad app federated-credential show --id "$APP_ID" --federated-credential-id "$cred_name" &>/dev/null; then
            log_warning "Credential already exists: $cred_name"
        else
            create_fic "$cred_name" "$subject" "GitHub Actions - ${env}" "$use_wildcard"
            log_success "Created credential: $cred_name"
        fi
    done

    # Create PR credential if enabled
    if [[ "$ENABLE_PR_FEDERATION" == "true" ]]; then
        local pr_subject="${repo_pattern}:pull_request"
        log_info "Creating federated credential for Pull Requests"

        if [[ "$DRY_RUN" == "true" ]]; then
            if [[ "$use_wildcard" == "true" ]]; then
                log_info "[DRY-RUN] claimsMatchingExpression: claims['sub'] matches '${pr_subject}'"
            else
                log_info "[DRY-RUN] Subject: $pr_subject"
            fi
        elif az ad app federated-credential show --id "$APP_ID" --federated-credential-id "github-pr" &>/dev/null; then
            log_warning "Credential already exists: github-pr"
        else
            create_fic "github-pr" "$pr_subject" "GitHub Actions - Pull Requests" "$use_wildcard"
            log_success "Created credential: github-pr"
        fi
    fi
}

# Assign RBAC roles
assign_rbac_roles() {
    log_step "Assigning RBAC roles..."
    
    SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}"
    
    local roles=(
        "Contributor"
        "Azure Kubernetes Service Cluster Admin Role"
    )
    
    for role in "${roles[@]}"; do
        log_info "Assigning role: $role"
        
        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY-RUN] Would assign $role to $APP_ID on $SCOPE"
        else
            # Check if assignment exists
            EXISTING=$(az role assignment list \
                --assignee "$APP_ID" \
                --role "$role" \
                --scope "$SCOPE" \
                --query "[0].id" -o tsv 2>/dev/null || echo "")
            
            if [[ -n "$EXISTING" ]]; then
                log_warning "Role already assigned: $role"
            else
                az role assignment create \
                    --assignee "$APP_ID" \
                    --role "$role" \
                    --scope "$SCOPE" >/dev/null
                log_success "Assigned role: $role"
            fi
        fi
    done
}

# Store credentials in GitHub
store_github_secrets() {
    log_step "Storing credentials in GitHub..."
    
    SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    TENANT_ID=$(az account show --query tenantId -o tsv)
    
    if [[ "$GITHUB_REPO" == "*" ]]; then
        log_warning "Cannot store org-wide secrets via CLI. Store manually:"
        echo ""
        echo "  AZURE_CLIENT_ID=$APP_ID"
        echo "  AZURE_TENANT_ID=$TENANT_ID"
        echo "  AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID"
        return
    fi
    
    local secrets=(
        "AZURE_CLIENT_ID:$APP_ID"
        "AZURE_TENANT_ID:$TENANT_ID"
        "AZURE_SUBSCRIPTION_ID:$SUBSCRIPTION_ID"
    )
    
    for secret in "${secrets[@]}"; do
        local name="${secret%%:*}"
        local value="${secret##*:}"
        
        log_info "Setting secret: $name"
        
        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY-RUN] Would set $name in $GITHUB_ORG/$GITHUB_REPO"
        else
            gh secret set "$name" \
                --body "$value" \
                --repo "${GITHUB_ORG}/${GITHUB_REPO}" 2>/dev/null || \
                log_warning "Could not set secret (may need admin access)"
        fi
    done
}

# Print summary
print_summary() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  IDENTITY FEDERATION SETUP COMPLETE${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "App Registration:"
    echo "  Name:      $APP_NAME"
    echo "  Client ID: $APP_ID"
    echo ""
    echo "Federated Credentials:"
    IFS=',' read -ra ENV_ARRAY <<< "$ENVIRONMENTS"
    for env in "${ENV_ARRAY[@]}"; do
        echo "  - github-${env}"
    done
    [[ "$ENABLE_PR_FEDERATION" == "true" ]] && echo "  - github-pr"
    echo ""
    echo "RBAC Assignments:"
    echo "  - Contributor on $RESOURCE_GROUP"
    echo "  - AKS Cluster Admin on $RESOURCE_GROUP"
    echo ""
    echo "GitHub Secrets to configure:"
    echo "  AZURE_CLIENT_ID=$APP_ID"
    echo "  AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)"
    echo "  AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)"
    echo ""
    echo "GitHub Actions workflow example:"
    cat << 'EOF'
    - name: Azure Login
      uses: azure/login@v2
      with:
        client-id: ${{ secrets.AZURE_CLIENT_ID }}
        tenant-id: ${{ secrets.AZURE_TENANT_ID }}
        subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
EOF
}

# Main
main() {
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  OPEN HORIZONS - IDENTITY FEDERATION SETUP                ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    parse_args "$@"
    
    [[ "$DRY_RUN" == "true" ]] && log_warning "DRY-RUN MODE - No changes will be made"
    
    check_prerequisites
    create_app_registration
    create_federated_credentials
    assign_rbac_roles
    store_github_secrets
    print_summary
    
    log_success "Identity federation setup complete!"
}

main "$@"
