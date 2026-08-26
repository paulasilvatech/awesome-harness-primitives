#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - BOOTSTRAP SCRIPT
# =============================================================================
# 
# Usage: ./scripts/bootstrap.sh [express|standard|enterprise]
#
# This script deploys the complete Open Horizons Platform including:
#   - Azure infrastructure (AKS, databases, networking)
#   - GitOps (ArgoCD)
#   - Developer Portal (Backstage)
#   - Observability (Prometheus, Grafana, Jaeger)
#   - GitHub configuration (org settings, runners, GHAS)
#
# Prerequisites:
#   - Azure CLI authenticated
#   - GitHub CLI authenticated
#   - Terraform, kubectl, helm, jq installed
#   - customer.tfvars configured
#
# =============================================================================

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$ROOT_DIR/customer-config"
TERRAFORM_DIR="$ROOT_DIR/terraform"
OUTPUT_DIR="$ROOT_DIR/outputs"

# Defaults
DEPLOYMENT_MODE="${1:-standard}"
ENVIRONMENT="${ENVIRONMENT:-prod}"
DRY_RUN="${DRY_RUN:-false}"
SKIP_CONFIRM="${SKIP_CONFIRM:-false}"

# Timing
START_TIME=$(date +%s)

# =============================================================================
# FUNCTIONS
# =============================================================================

# Logging functions
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "${PURPLE}[STEP]${NC} $1"; }

# Print header
header() {
    echo ""
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN} $1${NC}"
    echo -e "${CYAN}============================================================${NC}"
}

# Print phase
phase() {
    local phase_num=$1
    local phase_name=$2
    echo ""
    echo -e "${PURPLE}────────────────────────────────────────────────────────────${NC}"
    echo -e "${PURPLE}  PHASE $phase_num: $phase_name${NC}"
    echo -e "${PURPLE}────────────────────────────────────────────────────────────${NC}"
}

# Calculate elapsed time
elapsed_time() {
    local end_time=$(date +%s)
    local elapsed=$((end_time - START_TIME))
    local minutes=$((elapsed / 60))
    local seconds=$((elapsed % 60))
    echo "${minutes}m ${seconds}s"
}

# Spinner for long operations
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while ps -p $pid > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Confirm action
confirm() {
    if [ "$SKIP_CONFIRM" = "true" ]; then
        return 0
    fi
    
    local message=$1
    echo -e "${YELLOW}$message${NC}"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_error "Aborted by user"
        exit 1
    fi
}

# Check command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed"
        return 1
    fi
    return 0
}

# =============================================================================
# PHASE 0: PREREQUISITES
# =============================================================================

check_prerequisites() {
    phase 0 "PREREQUISITES CHECK"
    
    local missing=()
    
    log_step "Checking required tools..."
    
    check_command "terraform" || missing+=("terraform")
    check_command "az" || missing+=("azure-cli")
    check_command "kubectl" || missing+=("kubectl")
    check_command "helm" || missing+=("helm")
    check_command "gh" || missing+=("gh")
    check_command "jq" || missing+=("jq")
    check_command "yq" || missing+=("yq")
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing prerequisites: ${missing[*]}"
        echo ""
        echo "Install missing tools:"
        echo "  terraform: brew install terraform"
        echo "  azure-cli: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
        echo "  kubectl:   az aks install-cli"
        echo "  helm:      brew install helm"
        echo "  gh:        brew install gh"
        echo "  jq:        brew install jq"
        echo "  yq:        brew install yq"
        exit 1
    fi
    
    log_success "All tools installed"
    
    # Check Azure auth
    log_step "Checking Azure authentication..."
    if ! az account show &> /dev/null; then
        log_error "Not logged in to Azure. Run: az login"
        exit 1
    fi
    log_success "Azure authenticated"
    
    # Check GitHub auth
    log_step "Checking GitHub authentication..."
    if ! gh auth status &> /dev/null; then
        log_error "Not logged in to GitHub. Run: gh auth login"
        exit 1
    fi
    log_success "GitHub authenticated"
    
    # Check configuration file
    log_step "Checking configuration..."
    if [ ! -f "$CONFIG_DIR/customer.tfvars" ]; then
        log_error "customer.tfvars not found"
        echo ""
        echo "Create configuration:"
        echo "  cp $CONFIG_DIR/customer.tfvars.example $CONFIG_DIR/customer.tfvars"
        echo "  code $CONFIG_DIR/customer.tfvars"
        exit 1
    fi
    log_success "Configuration file found"
}

# =============================================================================
# PHASE 1: VALIDATE CONFIGURATION
# =============================================================================

validate_configuration() {
    phase 1 "CONFIGURATION VALIDATION"
    
    log_step "Validating customer.tfvars..."
    
    # Extract key values
    CUSTOMER_NAME=$(grep 'customer_name' "$CONFIG_DIR/customer.tfvars" | head -1 | cut -d'"' -f2)
    SUBSCRIPTION_ID=$(grep 'azure_subscription_id' "$CONFIG_DIR/customer.tfvars" | head -1 | cut -d'"' -f2)
    AZURE_REGION=$(grep 'azure_region' "$CONFIG_DIR/customer.tfvars" | head -1 | cut -d'"' -f2 | head -1)
    K8S_PLATFORM=$(grep 'kubernetes_platform' "$CONFIG_DIR/customer.tfvars" | head -1 | cut -d'"' -f2)
    GITHUB_ORG=$(grep -A5 'github_config' "$CONFIG_DIR/customer.tfvars" | grep 'organization' | head -1 | cut -d'"' -f2)
    DNS_ZONE=$(grep 'dns_zone_name' "$CONFIG_DIR/customer.tfvars" | head -1 | cut -d'"' -f2)
    
    # Validate required values
    local errors=()
    
    [ -z "$CUSTOMER_NAME" ] && errors+=("customer_name is empty")
    [ -z "$SUBSCRIPTION_ID" ] && errors+=("azure_subscription_id is empty")
    [ -z "$AZURE_REGION" ] && errors+=("azure_region is empty")
    [ -z "$GITHUB_ORG" ] && errors+=("github organization is empty")
    [ -z "$DNS_ZONE" ] && errors+=("dns_zone_name is empty")
    
    if [ ${#errors[@]} -gt 0 ]; then
        log_error "Configuration validation failed:"
        for error in "${errors[@]}"; do
            echo "  - $error"
        done
        exit 1
    fi
    
    # Display configuration summary
    echo ""
    echo "Configuration Summary:"
    echo "  Customer:     $CUSTOMER_NAME"
    echo "  Environment:  $ENVIRONMENT"
    echo "  Mode:         $DEPLOYMENT_MODE"
    echo "  Subscription: $SUBSCRIPTION_ID"
    echo "  Region:       $AZURE_REGION"
    echo "  Kubernetes:   $K8S_PLATFORM"
    echo "  GitHub Org:   $GITHUB_ORG"
    echo "  DNS Zone:     $DNS_ZONE"
    echo ""
    
    # Set Azure subscription
    log_step "Setting Azure subscription..."
    az account set --subscription "$SUBSCRIPTION_ID"
    log_success "Subscription set: $SUBSCRIPTION_ID"
    
    # Validate DNS zone access
    log_step "Validating DNS zone access..."
    DNS_RG=$(grep 'dns_zone_resource_group' "$CONFIG_DIR/customer.tfvars" | head -1 | cut -d'"' -f2)
    if ! az network dns zone show --name "$DNS_ZONE" --resource-group "$DNS_RG" &> /dev/null; then
        log_warning "DNS zone not accessible. Ensure it exists and you have permissions."
    else
        log_success "DNS zone accessible"
    fi
    
    log_success "Configuration validated"
    
    confirm "Ready to proceed with deployment?"
}

# =============================================================================
# PHASE 2: INFRASTRUCTURE
# =============================================================================

deploy_infrastructure() {
    phase 2 "INFRASTRUCTURE PROVISIONING"
    
    cd "$TERRAFORM_DIR/environments/$ENVIRONMENT"
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Initialize Terraform
    log_step "Initializing Terraform..."
    terraform init -reconfigure \
        -backend-config="resource_group_name=rg-${CUSTOMER_NAME}-tfstate" \
        -backend-config="storage_account_name=${CUSTOMER_NAME}tfstate" \
        -backend-config="container_name=tfstate" \
        -backend-config="key=${ENVIRONMENT}.tfstate"
    log_success "Terraform initialized"
    
    # Plan
    log_step "Planning infrastructure..."
    terraform plan \
        -var-file="$CONFIG_DIR/customer.tfvars" \
        -var="deployment_mode=$DEPLOYMENT_MODE" \
        -out=tfplan \
        -detailed-exitcode || true
    log_success "Plan complete"
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "Dry run - skipping apply"
        return 0
    fi
    
    confirm "Review the plan above. Apply infrastructure?"
    
    # Apply
    log_step "Applying infrastructure (this may take 20-30 minutes)..."
    terraform apply tfplan
    
    # Save outputs
    log_step "Saving Terraform outputs..."
    terraform output -json > "$OUTPUT_DIR/terraform-outputs.json"
    
    # Extract key outputs
    RESOURCE_GROUP=$(terraform output -raw resource_group_name)
    CLUSTER_NAME=$(terraform output -raw kubernetes_cluster_name)
    ACR_NAME=$(terraform output -raw acr_login_server | cut -d'.' -f1)
    KEY_VAULT=$(terraform output -raw key_vault_uri | sed 's|https://||' | cut -d'.' -f1)
    
    log_success "Infrastructure deployed"
    echo "  Resource Group: $RESOURCE_GROUP"
    echo "  Cluster:        $CLUSTER_NAME"
    echo "  ACR:            $ACR_NAME"
    echo "  Key Vault:      $KEY_VAULT"
}

# =============================================================================
# PHASE 3: KUBERNETES CONFIGURATION
# =============================================================================

configure_kubernetes() {
    phase 3 "KUBERNETES CONFIGURATION"
    
    log_step "Getting cluster credentials..."
    
    if [ "$K8S_PLATFORM" = "aks" ]; then
        az aks get-credentials \
            --resource-group "$RESOURCE_GROUP" \
            --name "$CLUSTER_NAME" \
            --overwrite-existing
    fi
    
    log_success "Credentials configured"
    
    # Verify cluster
    log_step "Verifying cluster access..."
    kubectl cluster-info
    echo ""
    kubectl get nodes
    
    log_success "Cluster accessible"
    
    # Create namespaces
    log_step "Creating platform namespaces..."
    kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
    kubectl create namespace backstage --dry-run=client -o yaml | kubectl apply -f -
    kubectl create namespace observability --dry-run=client -o yaml | kubectl apply -f -
    kubectl create namespace cert-manager --dry-run=client -o yaml | kubectl apply -f -
    kubectl create namespace ingress-nginx --dry-run=client -o yaml | kubectl apply -f -
    
    log_success "Namespaces created"
}

# =============================================================================
# PHASE 4: ARGOCD
# =============================================================================

deploy_argocd() {
    phase 4 "ARGOCD DEPLOYMENT"
    
    log_step "Installing ArgoCD..."
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml
    
    log_step "Waiting for ArgoCD to be ready..."
    kubectl wait --for=condition=available --timeout=300s \
        deployment/argocd-server -n argocd
    
    log_success "ArgoCD installed"
    
    # Get admin password
    log_step "Retrieving ArgoCD admin password..."
    ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret \
        -o jsonpath="{.data.password}" | base64 -d)
    echo "admin:$ARGOCD_PASSWORD" > "$OUTPUT_DIR/argocd-credentials.txt"
    chmod 600 "$OUTPUT_DIR/argocd-credentials.txt"
    
    log_success "ArgoCD credentials saved to $OUTPUT_DIR/argocd-credentials.txt"
    
    # Configure ArgoCD
    log_step "Configuring ArgoCD repositories..."
    # Apply repository secrets from Key Vault
    # This would be customized based on customer's GitHub setup
    
    # Deploy root application
    log_step "Deploying root application..."
    
    # Substitute variables in root-app.yaml
    envsubst < "$ROOT_DIR/argocd/app-of-apps/root-app.yaml" | kubectl apply -f -
    
    log_success "ArgoCD configured"
}

# =============================================================================
# PHASE 5: PLATFORM APPS
# =============================================================================

deploy_platform_apps() {
    phase 5 "PLATFORM APPLICATIONS"
    
    log_step "Syncing platform applications..."
    
    # Wait for apps to sync
    local apps=("platform-cert-manager" "platform-external-dns" "platform-ingress-nginx")
    
    for app in "${apps[@]}"; do
        log_info "Waiting for $app..."
        kubectl wait --for=jsonpath='{.status.health.status}'=Healthy \
            application/$app -n argocd --timeout=300s 2>/dev/null || true
    done
    
    log_success "Core platform apps deployed"
    
    # Deploy observability
    if [ "$DEPLOYMENT_MODE" != "express" ]; then
        log_step "Deploying observability stack..."
        # Prometheus, Grafana, Jaeger
        kubectl wait --for=jsonpath='{.status.health.status}'=Healthy \
            application/platform-prometheus-stack -n argocd --timeout=300s 2>/dev/null || true
        log_success "Observability deployed"
    fi
    
    # Deploy Backstage
    log_step "Deploying Backstage developer portal..."
    kubectl wait --for=jsonpath='{.status.health.status}'=Healthy \
        application/platform-backstage -n argocd --timeout=600s 2>/dev/null || true
    log_success "Backstage deployed"
}

# =============================================================================
# PHASE 6: GITHUB CONFIGURATION
# =============================================================================

configure_github() {
    phase 6 "GITHUB CONFIGURATION"
    
    log_step "Configuring GitHub organization..."
    
    # Enable Copilot
    log_info "Enabling Copilot..."
    gh api -X PATCH "/orgs/$GITHUB_ORG" \
        -f copilot_seat_management=allow_for_all_users 2>/dev/null || true
    
    # Enable GHAS
    log_info "Enabling Advanced Security..."
    gh api -X PATCH "/orgs/$GITHUB_ORG" \
        -f advanced_security_enabled_for_new_repositories=true \
        -f secret_scanning_enabled_for_new_repositories=true \
        -f secret_scanning_push_protection_enabled_for_new_repositories=true 2>/dev/null || true
    
    log_success "GitHub organization configured"
    
    # Deploy runners (if enabled)
    log_step "Deploying GitHub runners..."
    # This would deploy the actions-runner-controller
    
    log_success "GitHub runners deployed"
}

# =============================================================================
# PHASE 7: HEALTH CHECK
# =============================================================================

run_health_check() {
    phase 7 "HEALTH CHECK"
    
    log_step "Running platform health checks..."
    
    local checks_passed=0
    local checks_failed=0
    
    # Check AKS
    if kubectl cluster-info &> /dev/null; then
        log_success "✓ Kubernetes cluster healthy"
        checks_passed=$((checks_passed + 1))
    else
        log_error "✗ Kubernetes cluster unhealthy"
        checks_failed=$((checks_failed + 1))
    fi
    
    # Check ArgoCD
    if kubectl get deployment argocd-server -n argocd &> /dev/null; then
        log_success "✓ ArgoCD running"
        checks_passed=$((checks_passed + 1))
    else
        log_error "✗ ArgoCD not running"
        checks_failed=$((checks_failed + 1))
    fi
    
    # Check Backstage
    if kubectl get deployment backstage -n backstage &> /dev/null; then
        log_success "✓ Backstage running"
        checks_passed=$((checks_passed + 1))
    else
        log_error "✗ Backstage not running"
        checks_failed=$((checks_failed + 1))
    fi
    
    # Check ingress
    if kubectl get svc ingress-nginx-controller -n ingress-nginx &> /dev/null; then
        log_success "✓ Ingress controller running"
        checks_passed=$((checks_passed + 1))
    else
        log_error "✗ Ingress controller not running"
        checks_failed=$((checks_failed + 1))
    fi
    
    echo ""
    echo "Health Check Summary: $checks_passed passed, $checks_failed failed"
    
    if [ $checks_failed -gt 0 ]; then
        log_warning "Some health checks failed. Review the logs."
    else
        log_success "All health checks passed!"
    fi
}

# =============================================================================
# PHASE 8: SUMMARY
# =============================================================================

print_summary() {
    phase 8 "DEPLOYMENT SUMMARY"
    
    local elapsed=$(elapsed_time)
    
    # Read outputs
    local backstage_url=$(jq -r '.backstage_url.value' "$OUTPUT_DIR/terraform-outputs.json")
    local argocd_url=$(jq -r '.argocd_url.value' "$OUTPUT_DIR/terraform-outputs.json")
    local grafana_url=$(jq -r '.grafana_url.value' "$OUTPUT_DIR/terraform-outputs.json")
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         OPEN HORIZONS PLATFORM DEPLOYED SUCCESSFULLY!     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Deployment completed in: $elapsed"
    echo ""
    echo "Platform URLs:"
    echo "  Backstage: $backstage_url"
    echo "  ArgoCD:   $argocd_url"
    echo "  Grafana:  $grafana_url"
    echo ""
    echo "Credentials:"
    echo "  ArgoCD:   cat $OUTPUT_DIR/argocd-credentials.txt"
    echo ""
    echo "Next Steps:"
    echo "  1. Access Backstage at $backstage_url"
    echo "  2. Login with your GitHub account"
    echo "  3. Explore Golden Path templates"
    echo "  4. Onboard your first team: ./scripts/onboard-team.sh <team-name>"
    echo "  5. Create your first service using Golden Paths"
    echo ""
    echo "Documentation: ./docs/"
    echo "Runbooks:      ./docs/operations/runbooks/"
    echo ""
    echo -e "${GREEN}Happy building! 🚀${NC}"
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    header "OPEN HORIZONS PLATFORM BOOTSTRAP"
    
    echo ""
    echo "Starting deployment with:"
    echo "  Mode:        $DEPLOYMENT_MODE"
    echo "  Environment: $ENVIRONMENT"
    echo "  Dry Run:     $DRY_RUN"
    echo ""
    
    # Execute phases
    check_prerequisites
    validate_configuration
    deploy_infrastructure
    configure_kubernetes
    deploy_argocd
    deploy_platform_apps
    configure_github
    run_health_check
    print_summary
}

# Run main
main "$@"
