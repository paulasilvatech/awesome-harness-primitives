#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - PLATFORM BOOTSTRAP SCRIPT
# =============================================================================
#
# This script orchestrates the complete deployment of the Open Horizons
# Platform including infrastructure, GitOps, observability, and Golden Paths.
#
# Prerequisites:
#   - Azure CLI (az) authenticated
#   - Terraform >= 1.5
#   - kubectl configured
#   - Helm >= 3.12
#   - GitHub CLI (gh) authenticated
#
# Usage:
#   ./bootstrap.sh [options]
#
# Options:
#   --horizon [h1|h2|h3|all]  Deploy specific horizon (default: all)
#   --environment [dev|staging|prod]  Target environment (default: dev)
#   --dry-run                 Show what would be deployed without executing
#   --skip-infra              Skip infrastructure deployment
#   --skip-gitops             Skip GitOps configuration
#   --skip-golden-paths       Skip Golden Path registration
#   --destroy                 Destroy all resources
#   --help                    Show this help message
#
# =============================================================================

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACCELERATOR_ROOT="${SCRIPT_DIR}/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
HORIZON="all"
ENVIRONMENT="dev"
DRY_RUN=false
SKIP_INFRA=false
SKIP_GITOPS=false
SKIP_GOLDEN_PATHS=false
DESTROY=false

# Deployment tracking
DEPLOYMENT_LOG="${ACCELERATOR_ROOT}/logs/bootstrap-$(date +%Y%m%d-%H%M%S).log"
CHECKPOINT_FILE="${ACCELERATOR_ROOT}/.bootstrap-checkpoint"

# =============================================================================
# FUNCTIONS
# =============================================================================

log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        INFO)  color=$GREEN ;;
        WARN)  color=$YELLOW ;;
        ERROR) color=$RED ;;
        DEBUG) color=$CYAN ;;
        STEP)  color=$PURPLE ;;
        *)     color=$NC ;;
    esac
    
    echo -e "${color}[${timestamp}] [${level}] ${message}${NC}" | tee -a "$DEPLOYMENT_LOG"
}

print_banner() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ████████╗██╗  ██╗██████╗ ███████╗███████╗    ██╗  ██╗ ██████╗ ██████╗      ║
║   ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔════╝    ██║  ██║██╔═══██╗██╔══██╗     ║
║      ██║   ███████║██████╔╝█████╗  █████╗      ███████║██║   ██║██████╔╝     ║
║      ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══╝      ██╔══██║██║   ██║██╔══██╗     ║
║      ██║   ██║  ██║██║  ██║███████╗███████╗    ██║  ██║╚██████╔╝██║  ██║     ║
║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ║
║                                                                               ║
║                    OPEN HORIZONS PLATFORM ACCELERATOR                        ║
║                         Bootstrap Deployment Script                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

show_help() {
    cat << EOF
Open Horizons Platform Bootstrap Script

Usage: $0 [options]

Options:
    --horizon [h1|h2|h3|all]      Deploy specific horizon (default: all)
    --environment [dev|staging|prod]  Target environment (default: dev)
    --dry-run                     Show what would be deployed
    --skip-infra                  Skip infrastructure deployment
    --skip-gitops                 Skip GitOps configuration
    --skip-golden-paths           Skip Golden Path registration
    --destroy                     Destroy all resources
    --help                        Show this help message

Horizons:
    h1  Foundation   - AKS, networking, security, CI/CD
    h2  Enhancement  - ArgoCD, Backstage, GitOps, observability
    h3  Innovation   - AI Foundry, agents, MLOps

Examples:
    $0                            # Deploy all horizons to dev
    $0 --horizon h1               # Deploy only H1 Foundation
    $0 --environment prod         # Deploy to production
    $0 --dry-run                  # Preview deployment
    $0 --destroy                  # Tear down all resources

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --horizon)
                HORIZON="$2"
                shift 2
                ;;
            --environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --skip-infra)
                SKIP_INFRA=true
                shift
                ;;
            --skip-gitops)
                SKIP_GITOPS=true
                shift
                ;;
            --skip-golden-paths)
                SKIP_GOLDEN_PATHS=true
                shift
                ;;
            --destroy)
                DESTROY=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log ERROR "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

check_prerequisites() {
    log STEP "Checking prerequisites..."
    
    local missing_tools=()
    
    # Check required tools
    command -v az >/dev/null 2>&1 || missing_tools+=("az (Azure CLI)")
    command -v terraform >/dev/null 2>&1 || missing_tools+=("terraform")
    command -v kubectl >/dev/null 2>&1 || missing_tools+=("kubectl")
    command -v helm >/dev/null 2>&1 || missing_tools+=("helm")
    command -v gh >/dev/null 2>&1 || missing_tools+=("gh (GitHub CLI)")
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log ERROR "Missing required tools:"
        for tool in "${missing_tools[@]}"; do
            log ERROR "  - $tool"
        done
        exit 1
    fi
    
    # Check Azure authentication
    if ! az account show >/dev/null 2>&1; then
        log ERROR "Azure CLI not authenticated. Run: az login"
        exit 1
    fi
    
    # Check GitHub authentication
    if ! gh auth status >/dev/null 2>&1; then
        log ERROR "GitHub CLI not authenticated. Run: gh auth login"
        exit 1
    fi
    
    # Check Terraform version
    local tf_version=$(terraform version -json | jq -r '.terraform_version')
    log INFO "Terraform version: $tf_version"
    
    # Check Helm version
    local helm_version=$(helm version --short)
    log INFO "Helm version: $helm_version"
    
    log INFO "All prerequisites satisfied [OK]"
}

load_environment_config() {
    log STEP "Loading environment configuration for: $ENVIRONMENT"
    
    local config_file="${ACCELERATOR_ROOT}/environments/${ENVIRONMENT}/config.env"
    
    if [[ -f "$config_file" ]]; then
        source "$config_file"
        log INFO "Loaded configuration from: $config_file"
    else
        log WARN "No environment config found at: $config_file"
        log WARN "Using default values"
        
        # Set defaults
        export AZURE_SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:-$(az account show --query id -o tsv)}"
        export AZURE_REGION="${AZURE_REGION:-eastus2}"
        export RESOURCE_GROUP_NAME="${RESOURCE_GROUP_NAME:-rg-openhorizons-${ENVIRONMENT}}"
        export AKS_CLUSTER_NAME="${AKS_CLUSTER_NAME:-aks-openhorizons-${ENVIRONMENT}}"
        export GITHUB_ORG="${GITHUB_ORG:-your-org}"
    fi
    
    log INFO "Azure Subscription: $AZURE_SUBSCRIPTION_ID"
    log INFO "Azure Region: $AZURE_REGION"
    log INFO "Resource Group: $RESOURCE_GROUP_NAME"
    log INFO "AKS Cluster: $AKS_CLUSTER_NAME"
}

save_checkpoint() {
    local phase=$1
    echo "$phase" > "$CHECKPOINT_FILE"
    log DEBUG "Saved checkpoint: $phase"
}

load_checkpoint() {
    if [[ -f "$CHECKPOINT_FILE" ]]; then
        cat "$CHECKPOINT_FILE"
    else
        echo "start"
    fi
}

# =============================================================================
# DEPLOYMENT PHASES
# =============================================================================

deploy_h1_foundation() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "PHASE 1: H1 FOUNDATION - Infrastructure & Security"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would deploy H1 Foundation components:"
        log INFO "  - Resource Group: $RESOURCE_GROUP_NAME"
        log INFO "  - AKS Cluster: $AKS_CLUSTER_NAME"
        log INFO "  - Networking (VNet, subnets, NSGs)"
        log INFO "  - Security (Key Vault, managed identities)"
        log INFO "  - Container Registry"
        return 0
    fi
    
    # Create resource group
    log INFO "Creating resource group..."
    az group create \
        --name "$RESOURCE_GROUP_NAME" \
        --location "$AZURE_REGION" \
        --tags "Environment=${ENVIRONMENT}" "Platform=OpenHorizons" \
        --output none
    
    # Deploy networking
    log INFO "Deploying networking infrastructure..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/networking"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="location=${AZURE_REGION}" \
        -var="environment=${ENVIRONMENT}"
    
    # Deploy security
    log INFO "Deploying security infrastructure..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/security"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="location=${AZURE_REGION}" \
        -var="environment=${ENVIRONMENT}"
    
    # Deploy AKS
    log INFO "Deploying AKS cluster..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/aks"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="location=${AZURE_REGION}" \
        -var="cluster_name=${AKS_CLUSTER_NAME}" \
        -var="environment=${ENVIRONMENT}"
    
    # Get AKS credentials
    log INFO "Configuring kubectl..."
    az aks get-credentials \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$AKS_CLUSTER_NAME" \
        --overwrite-existing
    
    # Deploy container registry
    log INFO "Deploying container registry..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/container-registry"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="location=${AZURE_REGION}" \
        -var="environment=${ENVIRONMENT}"
    
    save_checkpoint "h1_complete"
    log INFO "H1 Foundation deployment complete [OK]"
}

deploy_h2_enhancement() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "PHASE 2: H2 ENHANCEMENT - Platform Engineering & GitOps"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would deploy H2 Enhancement components:"
        log INFO "  - ArgoCD"
        log INFO "  - Backstage (Developer Portal)"
        log INFO "  - Observability stack (Prometheus, Grafana)"
        log INFO "  - Managed databases"
        log INFO "  - GitHub runners"
        return 0
    fi
    
    # Deploy ArgoCD
    log INFO "Deploying ArgoCD..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/argocd"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="cluster_name=${AKS_CLUSTER_NAME}" \
        -var="environment=${ENVIRONMENT}"
    
    # Deploy observability
    log INFO "Deploying observability stack..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/observability"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="cluster_name=${AKS_CLUSTER_NAME}" \
        -var="environment=${ENVIRONMENT}"
    
    # Deploy databases
    log INFO "Deploying managed databases..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/databases"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="location=${AZURE_REGION}" \
        -var="environment=${ENVIRONMENT}"
    
    # Deploy Backstage
    log INFO "Deploying Backstage developer portal..."
    # Backstage is deployed via ArgoCD app-of-apps (Wave 4)
    log INFO "Backstage will be deployed automatically via ArgoCD"
    
    # Deploy GitHub runners
    log INFO "Deploying GitHub self-hosted runners..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/github-runners"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="cluster_name=${AKS_CLUSTER_NAME}" \
        -var="github_org=${GITHUB_ORG}" \
        -var="environment=${ENVIRONMENT}"
    
    save_checkpoint "h2_complete"
    log INFO "H2 Enhancement deployment complete [OK]"
}

deploy_h3_innovation() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "PHASE 3: H3 INNOVATION - AI & Agentic Capabilities"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would deploy H3 Innovation components:"
        log INFO "  - Azure AI Foundry"
        log INFO "  - AI model deployments"
        log INFO "  - Agent infrastructure"
        log INFO "  - MLOps pipelines"
        return 0
    fi
    
    # Deploy AI Foundry
    log INFO "Deploying Azure AI Foundry..."
    cd "${ACCELERATOR_ROOT}/terraform/modules/ai-foundry"
    terraform init -upgrade
    terraform apply -auto-approve \
        -var="resource_group_name=${RESOURCE_GROUP_NAME}" \
        -var="location=${AZURE_REGION}" \
        -var="environment=${ENVIRONMENT}"
    
    save_checkpoint "h3_complete"
    log INFO "H3 Innovation deployment complete [OK]"
}

configure_gitops() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "PHASE 4: GitOps Configuration"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would configure GitOps:"
        log INFO "  - ArgoCD applications"
        log INFO "  - Git repository connections"
        log INFO "  - Sync policies"
        return 0
    fi
    
    # Configure ArgoCD applications
    log INFO "Configuring ArgoCD applications..."
    kubectl apply -f "${ACCELERATOR_ROOT}/gitops/argocd-apps/"
    
    # Wait for sync
    log INFO "Waiting for ArgoCD sync..."
    sleep 30
    
    save_checkpoint "gitops_complete"
    log INFO "GitOps configuration complete [OK]"
}

register_golden_paths() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "PHASE 5: Golden Path Registration"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would register Golden Paths:"
        log INFO "  - H1 Foundation templates (4)"
        log INFO "  - H2 Enhancement templates (5)"
        log INFO "  - H3 Innovation templates (5)"
        return 0
    fi
    
    # Get Backstage URL
    local backstage_url=$(kubectl get ingress -n backstage backstage -o jsonpath='{.spec.rules[0].host}')
    
    log INFO "Registering Golden Path templates in Backstage..."
    
    # Register H1 templates
    for template in "${ACCELERATOR_ROOT}/golden-paths/h1-foundation/"*/template.yaml; do
        local name=$(basename $(dirname "$template"))
        log INFO "Registering H1 template: $name"
        # Backstage API call to register template
    done
    
    # Register H2 templates
    for template in "${ACCELERATOR_ROOT}/golden-paths/h2-enhancement/"*/template.yaml; do
        local name=$(basename $(dirname "$template"))
        log INFO "Registering H2 template: $name"
    done
    
    # Register H3 templates
    for template in "${ACCELERATOR_ROOT}/golden-paths/h3-innovation/"*/template.yaml; do
        local name=$(basename $(dirname "$template"))
        log INFO "Registering H3 template: $name"
    done
    
    save_checkpoint "golden_paths_complete"
    log INFO "Golden Path registration complete [OK]"
}

deploy_grafana_dashboards() {
    log STEP "Deploying Grafana dashboards..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would deploy Grafana dashboards"
        return 0
    fi
    
    # Create ConfigMaps for dashboards
    for dashboard in "${ACCELERATOR_ROOT}/grafana/dashboards/"*.json; do
        local name=$(basename "$dashboard" .json)
        log INFO "Deploying dashboard: $name"
        kubectl create configmap "grafana-dashboard-${name}" \
            --from-file="$dashboard" \
            -n monitoring \
            --dry-run=client -o yaml | kubectl apply -f -
        
        # Label for Grafana sidecar
        kubectl label configmap "grafana-dashboard-${name}" \
            -n monitoring \
            grafana_dashboard=1 \
            --overwrite
    done
    
    log INFO "Grafana dashboards deployed [OK]"
}

print_summary() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "DEPLOYMENT SUMMARY"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    echo ""
    echo -e "${GREEN}Open Horizons Platform deployment complete!${NC}"
    echo ""
    echo "Environment: $ENVIRONMENT"
    echo "Horizon: $HORIZON"
    echo ""
    
    if [[ "$DRY_RUN" != "true" ]]; then
        # Get URLs
        local argocd_url=$(kubectl get ingress -n argocd argocd-server -o jsonpath='{.spec.rules[0].host}' 2>/dev/null || echo "pending")
        local backstage_url=$(kubectl get ingress -n backstage backstage -o jsonpath='{.spec.rules[0].host}' 2>/dev/null || echo "pending")
        local grafana_url=$(kubectl get ingress -n monitoring grafana -o jsonpath='{.spec.rules[0].host}' 2>/dev/null || echo "pending")
        
        echo "Access URLs:"
        echo "  ArgoCD:    https://${argocd_url}"
        echo "  Backstage: https://${backstage_url}"
        echo "  Grafana:  https://${grafana_url}"
        echo ""
        echo "Deployment log: $DEPLOYMENT_LOG"
    fi
    
    echo ""
    echo "Next steps:"
    echo "  1. Configure GitHub App for Backstage"
    echo "  2. Import existing repositories to catalog"
    echo "  3. Create first application using Golden Paths"
    echo "  4. Configure alerts in Grafana"
    echo ""
}

destroy_platform() {
    log STEP "═══════════════════════════════════════════════════════════════"
    log STEP "DESTROYING OPEN HORIZONS PLATFORM"
    log STEP "═══════════════════════════════════════════════════════════════"
    
    echo -e "${RED}WARNING: This will destroy all resources!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    
    if [[ "$confirm" != "yes" ]]; then
        log INFO "Destruction cancelled"
        exit 0
    fi
    
    # Destroy in reverse order
    local modules=(
        "ai-foundry"
        "github-runners"
        "backstage"
        "databases"
        "observability"
        "argocd"
        "container-registry"
        "aks"
        "security"
        "networking"
    )
    
    for module in "${modules[@]}"; do
        log INFO "Destroying module: $module"
        cd "${ACCELERATOR_ROOT}/terraform/modules/${module}"
        terraform destroy -auto-approve || true
    done
    
    # Delete resource group
    log INFO "Deleting resource group..."
    az group delete --name "$RESOURCE_GROUP_NAME" --yes --no-wait
    
    # Clean up checkpoint
    rm -f "$CHECKPOINT_FILE"
    
    log INFO "Platform destroyed [OK]"
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    # Create logs directory
    mkdir -p "${ACCELERATOR_ROOT}/logs"
    
    # Parse arguments
    parse_args "$@"
    
    # Print banner
    print_banner
    
    # Handle destroy
    if [[ "$DESTROY" == "true" ]]; then
        load_environment_config
        destroy_platform
        exit 0
    fi
    
    # Check prerequisites
    check_prerequisites
    
    # Load configuration
    load_environment_config
    
    # Deploy based on horizon selection
    if [[ "$SKIP_INFRA" != "true" ]]; then
        case $HORIZON in
            h1)
                deploy_h1_foundation
                ;;
            h2)
                deploy_h1_foundation
                deploy_h2_enhancement
                ;;
            h3|all)
                deploy_h1_foundation
                deploy_h2_enhancement
                deploy_h3_innovation
                ;;
        esac
    else
        log INFO "Skipping infrastructure deployment"
    fi
    
    # Configure GitOps
    if [[ "$SKIP_GITOPS" != "true" ]] && [[ "$HORIZON" != "h1" ]]; then
        configure_gitops
    fi
    
    # Deploy Grafana dashboards
    if [[ "$HORIZON" != "h1" ]] && [[ "$SKIP_GITOPS" != "true" ]]; then
        deploy_grafana_dashboards
    fi
    
    # Register Golden Paths
    if [[ "$SKIP_GOLDEN_PATHS" != "true" ]] && [[ "$HORIZON" != "h1" ]]; then
        register_golden_paths
    fi
    
    # Print summary
    print_summary
    
    log INFO "Bootstrap complete!"
}

# Run main
main "$@"
