#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - CLI PREREQUISITES VALIDATION
# =============================================================================
#
# Validates all required CLI tools are installed and authenticated
# for the Open Horizons Platform v7.2.6
#
# Usage: ./scripts/validate-cli-prerequisites.sh [--install]
#
# =============================================================================

set -euo pipefail

# --- requires bash 4+ (associative arrays); macOS ships bash 3.2 by default ---
if (( ${BASH_VERSINFO[0]:-0} < 4 )); then
    echo "ERROR: this script requires bash 4 or newer (found ${BASH_VERSION:-unknown})." >&2
    echo "       On macOS run: brew install bash, then invoke the script with that bash." >&2
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Flags
INSTALL_MODE="${1:-}"

# =============================================================================
# CLI TOOLS DEFINITIONS
# =============================================================================

declare -A CLI_TOOLS=(
    # Core Infrastructure
    ["terraform"]="Terraform IaC|terraform version|brew install terraform"
    ["az"]="Azure CLI|az version|curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    ["kubectl"]="Kubernetes CLI|kubectl version --client|az aks install-cli"
    ["helm"]="Helm Charts|helm version|brew install helm"
    
    # GitHub
    ["gh"]="GitHub CLI|gh --version|brew install gh"
    
    # Utilities
    ["jq"]="JSON Processor|jq --version|brew install jq"
    ["yq"]="YAML Processor|yq --version|brew install yq"
    ["curl"]="HTTP Client|curl --version|built-in"
    ["git"]="Git|git --version|brew install git"
    
    # Container
    ["docker"]="Docker|docker --version|brew install docker"
    
    # Optional but recommended
    ["kubelogin"]="Azure AKS Auth|kubelogin --version|brew install Azure/kubelogin/kubelogin"
    ["argocd"]="ArgoCD CLI|argocd version --client|brew install argocd"
)

declare -A AUTH_CHECKS=(
    ["az"]="az account show"
    ["gh"]="gh auth status"
    ["docker"]="docker info"
)

# =============================================================================
# FUNCTIONS
# =============================================================================

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error()   { echo -e "${RED}[FAIL]${NC} $1"; }

header() {
    echo ""
    echo -e "${PURPLE}============================================================${NC}"
    echo -e "${PURPLE} $1${NC}"
    echo -e "${PURPLE}============================================================${NC}"
}

check_tool() {
    local tool=$1
    local info="${CLI_TOOLS[$tool]}"
    local name=$(echo "$info" | cut -d'|' -f1)
    local check_cmd=$(echo "$info" | cut -d'|' -f2)
    local install_cmd=$(echo "$info" | cut -d'|' -f3)
    
    printf "  %-15s " "$tool"
    
    if command -v "$tool" &> /dev/null; then
        local version=$(eval "$check_cmd" 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "installed")
        echo -e "${GREEN}[OK]${NC} ${version}"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} not installed"
        if [ "$INSTALL_MODE" = "--install" ]; then
            log_info "Installing $tool..."
            eval "$install_cmd" 2>/dev/null || log_warning "Auto-install failed. Run manually: $install_cmd"
        fi
        return 1
    fi
}

check_auth() {
    local tool=$1
    local check_cmd="${AUTH_CHECKS[$tool]:-}"
    
    if [ -z "$check_cmd" ]; then
        return 0
    fi
    
    printf "  %-15s " "$tool"
    
    if eval "$check_cmd" &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} authenticated"
        return 0
    else
        echo -e "${YELLOW}!${NC} not authenticated"
        return 1
    fi
}

check_azure_extensions() {
    header "Azure CLI Extensions"
    
    local extensions=(
        "aks-preview"
        "azure-devops"
        "ssh"
    )
    
    for ext in "${extensions[@]}"; do
        printf "  %-20s " "$ext"
        if az extension show --name "$ext" &> /dev/null; then
            echo -e "${GREEN}[OK]${NC} installed"
        else
            echo -e "${YELLOW}!${NC} not installed"
            if [ "$INSTALL_MODE" = "--install" ]; then
                az extension add --name "$ext" 2>/dev/null || true
            fi
        fi
    done
}

check_gh_extensions() {
    header "GitHub CLI Extensions"
    
    printf "  %-20s " "gh-copilot"
    if gh extension list | grep -q "copilot"; then
        echo -e "${GREEN}[OK]${NC} installed"
    else
        echo -e "${YELLOW}!${NC} not installed"
        if [ "$INSTALL_MODE" = "--install" ]; then
            gh extension install github/gh-copilot 2>/dev/null || true
        fi
    fi
}

check_mcp_servers() {
    header "MCP Server Dependencies (Node.js)"
    
    printf "  %-15s " "node"
    if command -v node &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} $(node --version)"
    else
        echo -e "${RED}[FAIL]${NC} not installed (required for MCP servers)"
    fi
    
    printf "  %-15s " "npx"
    if command -v npx &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} available"
    else
        echo -e "${RED}[FAIL]${NC} not available"
    fi
}

generate_summary() {
    local required_missing=$1
    local optional_missing=$2
    local auth_missing=$3
    
    header "Summary"
    
    if [ "$required_missing" -eq 0 ] && [ "$auth_missing" -eq 0 ]; then
        log_success "All required tools installed and authenticated!"
        echo ""
        echo -e "${GREEN}Ready to run:${NC}"
        echo "  ./scripts/bootstrap.sh [express|standard|enterprise]"
    else
        if [ "$required_missing" -gt 0 ]; then
            log_error "$required_missing required tool(s) missing"
        fi
        if [ "$auth_missing" -gt 0 ]; then
            log_warning "$auth_missing tool(s) need authentication"
            echo ""
            echo "Run authentication commands:"
            echo "  az login"
            echo "  gh auth login"
        fi
        echo ""
        echo "Re-run with --install to auto-install missing tools:"
        echo "  ./scripts/validate-cli-prerequisites.sh --install"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  OPEN HORIZONS PLATFORM v7.2.6 - CLI VALIDATION        ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════╝${NC}"
    
    local required_missing=0
    local optional_missing=0
    local auth_missing=0
    
    # Required tools
    header "Required CLI Tools"
    
    local required_tools=("terraform" "az" "kubectl" "helm" "gh" "jq" "yq" "git" "curl")
    for tool in "${required_tools[@]}"; do
        check_tool "$tool" || required_missing=$((required_missing + 1))
    done
    
    # Optional tools
    header "Optional CLI Tools (Recommended)"
    
    local optional_tools=("oc" "docker" "kubelogin" "argocd")
    for tool in "${optional_tools[@]}"; do
        check_tool "$tool" || optional_missing=$((optional_missing + 1))
    done
    
    # Authentication status
    header "Authentication Status"
    
    for tool in "${!AUTH_CHECKS[@]}"; do
        if command -v "$tool" &> /dev/null; then
            check_auth "$tool" || auth_missing=$((auth_missing + 1))
        fi
    done
    
    # Azure extensions
    if command -v az &> /dev/null; then
        check_azure_extensions
    fi
    
    # GitHub extensions
    if command -v gh &> /dev/null; then
        check_gh_extensions
    fi
    
    # MCP dependencies
    check_mcp_servers
    
    # Summary
    generate_summary "$required_missing" "$optional_missing" "$auth_missing"
    
    # Exit code
    if [ "$required_missing" -gt 0 ]; then
        exit 1
    fi
}

main "$@"
