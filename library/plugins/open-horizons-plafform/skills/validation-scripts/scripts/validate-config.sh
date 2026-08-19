#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - CONFIGURATION VALIDATOR
# =============================================================================
#
# Validates customer configuration before deployment.
# Checks Azure access, GitHub access, quotas, and configuration syntax.
#
# Usage: ./validate-config.sh [options]
#
# Options:
#   --config FILE    Path to customer.tfvars (default: customer-config/customer.tfvars)
#   --strict         Fail on warnings (default: warnings don't fail)
#   --skip-azure     Skip Azure validation
#   --skip-github    Skip GitHub validation
#   --skip-quotas    Skip quota checks
#   --json           Output results as JSON
#   --help           Show this help message
#
# Exit Codes:
#   0 - All validations passed
#   1 - Configuration errors found
#   2 - Azure access issues
#   3 - GitHub access issues
#   4 - Quota issues
#   5 - Missing prerequisites
#
# =============================================================================

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../customer-config/customer.tfvars"
STRICT_MODE=false
SKIP_AZURE=false
SKIP_GITHUB=false
SKIP_QUOTAS=false
JSON_OUTPUT=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
CHECKS_PASSED=0

# Results array for JSON output
declare -a RESULTS=()

# =============================================================================
# FUNCTIONS
# =============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  OPEN HORIZONS PLATFORM - Configuration Validator${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_section() {
    local section=$1
    echo ""
    echo -e "${BLUE}▶ ${section}${NC}"
    echo -e "${BLUE}─────────────────────────────────────────────────────────────────────────${NC}"
}

check_pass() {
    local message=$1
    echo -e "  ${GREEN}[OK]${NC} ${message}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    RESULTS+=("{\"status\":\"pass\",\"message\":\"${message}\"}")
}

check_fail() {
    local message=$1
    echo -e "  ${RED}[FAIL]${NC} ${message}"
    ERRORS=$((ERRORS + 1))
    RESULTS+=("{\"status\":\"fail\",\"message\":\"${message}\"}")
}

check_warn() {
    local message=$1
    echo -e "  ${YELLOW}[WARN]${NC} ${message}"
    WARNINGS=$((WARNINGS + 1))
    RESULTS+=("{\"status\":\"warn\",\"message\":\"${message}\"}")
}

check_info() {
    local message=$1
    echo -e "  ${BLUE}[INFO]${NC} ${message}"
}

parse_tfvars() {
    local key=$1
    grep -E "^${key}\s*=" "$CONFIG_FILE" 2>/dev/null | sed 's/.*=\s*"\?\([^"]*\)"\?.*/\1/' | tr -d '"' || echo ""
}

parse_tfvars_bool() {
    local key=$1
    local value=$(grep -E "^${key}\s*=" "$CONFIG_FILE" 2>/dev/null | sed 's/.*=\s*//' | tr -d ' ')
    [[ "$value" == "true" ]] && echo "true" || echo "false"
}

command_exists() {
    command -v "$1" &> /dev/null
}

# =============================================================================
# PREREQUISITE CHECKS
# =============================================================================

check_prerequisites() {
    print_section "Prerequisites"
    
    # Check required tools
    local tools=("terraform" "az" "kubectl" "helm" "gh" "jq" "yq")
    
    for tool in "${tools[@]}"; do
        if command_exists "$tool"; then
            local version=$($tool version 2>/dev/null | head -n1 || echo "installed")
            check_pass "$tool is installed (${version})"
        else
            check_fail "$tool is not installed"
        fi
    done
    
    # Check config file exists
    if [[ -f "$CONFIG_FILE" ]]; then
        check_pass "Configuration file exists: $CONFIG_FILE"
    else
        check_fail "Configuration file not found: $CONFIG_FILE"
        echo ""
        echo -e "  ${YELLOW}Please copy the example file:${NC}"
        echo "  cp customer-config/customer.tfvars.example customer-config/customer.tfvars"
        echo ""
        exit 5
    fi
}

# =============================================================================
# CONFIGURATION SYNTAX VALIDATION
# =============================================================================

validate_config_syntax() {
    print_section "Configuration Syntax"
    
    # Required fields
    local required_fields=(
        "customer_name"
        "environment"
        "azure_subscription_id"
        "azure_tenant_id"
        "azure_region"
    )
    
    for field in "${required_fields[@]}"; do
        local value=$(parse_tfvars "$field")
        if [[ -n "$value" && "$value" != "REPLACE_" ]]; then
            check_pass "$field is set: ${value:0:30}..."
        else
            check_fail "$field is not set or contains placeholder"
        fi
    done
    
    # Validate customer_name format
    local customer_name=$(parse_tfvars "customer_name")
    if [[ "$customer_name" =~ ^[a-z][a-z0-9-]{2,20}$ ]]; then
        check_pass "customer_name format is valid"
    else
        check_fail "customer_name must be lowercase, 3-21 chars, start with letter"
    fi
    
    # Validate environment
    local environment=$(parse_tfvars "environment")
    if [[ "$environment" =~ ^(dev|staging|prod)$ ]]; then
        check_pass "environment is valid: $environment"
    else
        check_fail "environment must be one of: dev, staging, prod"
    fi
    
    # Validate Azure subscription ID format
    local sub_id=$(parse_tfvars "azure_subscription_id")
    if [[ "$sub_id" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]]; then
        check_pass "azure_subscription_id format is valid"
    else
        check_fail "azure_subscription_id format is invalid (expected UUID)"
    fi
    
    # Validate Azure tenant ID format
    local tenant_id=$(parse_tfvars "azure_tenant_id")
    if [[ "$tenant_id" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]]; then
        check_pass "azure_tenant_id format is valid"
    else
        check_fail "azure_tenant_id format is invalid (expected UUID)"
    fi
    
    # Validate deployment mode
    local mode=$(parse_tfvars "deployment_mode")
    if [[ "$mode" =~ ^(express|standard|enterprise)$ ]]; then
        check_pass "deployment_mode is valid: $mode"
    else
        check_warn "deployment_mode not set, defaulting to 'standard'"
    fi
}

# =============================================================================
# AZURE VALIDATION
# =============================================================================

validate_azure() {
    if [[ "$SKIP_AZURE" == "true" ]]; then
        check_info "Skipping Azure validation (--skip-azure)"
        return
    fi
    
    print_section "Azure Access"
    
    local sub_id=$(parse_tfvars "azure_subscription_id")
    local tenant_id=$(parse_tfvars "azure_tenant_id")
    local region=$(parse_tfvars "azure_region")
    
    # Check Azure CLI login
    if az account show &>/dev/null; then
        local current_sub=$(az account show --query id -o tsv)
        check_pass "Azure CLI is logged in"
        
        # Check if we can access the target subscription
        if az account set --subscription "$sub_id" 2>/dev/null; then
            check_pass "Can access subscription: $sub_id"
            
            # Check subscription name
            local sub_name=$(az account show --query name -o tsv)
            check_info "Subscription name: $sub_name"
        else
            check_fail "Cannot access subscription: $sub_id"
            echo "  Run: az login --tenant $tenant_id"
        fi
    else
        check_fail "Azure CLI not logged in"
        echo "  Run: az login --tenant $tenant_id"
        return
    fi
    
    # Check region availability
    local region_valid=$(az account list-locations --query "[?name=='$region'].name" -o tsv)
    if [[ -n "$region_valid" ]]; then
        check_pass "Region is valid: $region"
    else
        check_fail "Region not found: $region"
    fi
    
    # Check resource providers
    print_section "Azure Resource Providers"
    
    local providers=(
        "Microsoft.Compute"
        "Microsoft.ContainerService"
        "Microsoft.Network"
        "Microsoft.Storage"
        "Microsoft.KeyVault"
        "Microsoft.ManagedIdentity"
        "Microsoft.ContainerRegistry"
        "Microsoft.OperationalInsights"
        "Microsoft.DBforPostgreSQL"
        "Microsoft.Cache"
        "Microsoft.CognitiveServices"
        "Microsoft.Search"
    )
    
    for provider in "${providers[@]}"; do
        local state=$(az provider show -n "$provider" --query "registrationState" -o tsv 2>/dev/null)
        if [[ "$state" == "Registered" ]]; then
            check_pass "$provider is registered"
        else
            check_warn "$provider is not registered (state: $state)"
            echo "  Run: az provider register -n $provider"
        fi
    done
}

# =============================================================================
# QUOTA VALIDATION
# =============================================================================

validate_quotas() {
    if [[ "$SKIP_QUOTAS" == "true" ]]; then
        check_info "Skipping quota validation (--skip-quotas)"
        return
    fi
    
    print_section "Azure Quotas"
    
    local region=$(parse_tfvars "azure_region")
    local deployment_mode=$(parse_tfvars "deployment_mode")
    
    # Determine required vCPUs based on deployment mode
    local required_vcpus=32
    case "$deployment_mode" in
        "express") required_vcpus=16 ;;
        "standard") required_vcpus=32 ;;
        "enterprise") required_vcpus=64 ;;
    esac
    
    # Check vCPU quota for Dv5 family
    local quota_info=$(az vm list-usage --location "$region" --query "[?contains(name.value, 'standardDSv5Family')]" -o json 2>/dev/null)
    
    if [[ -n "$quota_info" ]]; then
        local current=$(echo "$quota_info" | jq -r '.[0].currentValue // 0')
        local limit=$(echo "$quota_info" | jq -r '.[0].limit // 0')
        local available=$((limit - current))
        
        if [[ $available -ge $required_vcpus ]]; then
            check_pass "vCPU quota sufficient: $available available (need $required_vcpus)"
        else
            check_fail "Insufficient vCPU quota: $available available, need $required_vcpus"
            echo "  Request quota increase in Azure Portal"
        fi
    else
        check_warn "Could not check vCPU quota"
    fi
    
    # Check public IP quota
    local ip_quota=$(az network list-usages --location "$region" --query "[?name.value=='PublicIPAddresses']" -o json 2>/dev/null)
    
    if [[ -n "$ip_quota" ]]; then
        local ip_current=$(echo "$ip_quota" | jq -r '.[0].currentValue // 0')
        local ip_limit=$(echo "$ip_quota" | jq -r '.[0].limit // 0')
        local ip_available=$((ip_limit - ip_current))
        
        if [[ $ip_available -ge 5 ]]; then
            check_pass "Public IP quota sufficient: $ip_available available"
        else
            check_warn "Low public IP quota: $ip_available available"
        fi
    fi
}

# =============================================================================
# GITHUB VALIDATION
# =============================================================================

validate_github() {
    if [[ "$SKIP_GITHUB" == "true" ]]; then
        check_info "Skipping GitHub validation (--skip-github)"
        return
    fi
    
    print_section "GitHub Access"
    
    # Check GitHub CLI login
    if gh auth status &>/dev/null; then
        local gh_user=$(gh api user --jq '.login' 2>/dev/null)
        check_pass "GitHub CLI is logged in as: $gh_user"
    else
        check_fail "GitHub CLI not logged in"
        echo "  Run: gh auth login"
        return
    fi
    
    # Get GitHub org from config
    local github_org=$(grep -E "organization\s*=" "$CONFIG_FILE" | head -1 | sed 's/.*=\s*"\([^"]*\)".*/\1/')
    
    if [[ -z "$github_org" ]]; then
        check_warn "GitHub organization not found in config"
        return
    fi
    
    # Check org access
    local org_info=$(gh api "/orgs/$github_org" 2>/dev/null)
    
    if [[ -n "$org_info" ]]; then
        check_pass "Can access GitHub organization: $github_org"
        
        # Check if user is admin
        local membership=$(gh api "/orgs/$github_org/memberships/$gh_user" --jq '.role' 2>/dev/null)
        
        if [[ "$membership" == "admin" ]]; then
            check_pass "User has admin access to organization"
        else
            check_warn "User role is '$membership' (admin recommended for setup)"
        fi
        
        # Check if GitHub Enterprise
        local plan=$(echo "$org_info" | jq -r '.plan.name // "unknown"')
        check_info "GitHub plan: $plan"
        
        if [[ "$plan" != "enterprise" ]]; then
            check_warn "GitHub Enterprise Cloud recommended for full features"
        fi
    else
        check_fail "Cannot access GitHub organization: $github_org"
    fi
    
    # Check if Copilot is available
    local copilot_enabled=$(gh api "/orgs/$github_org/copilot/billing" --jq '.seat_breakdown.total // 0' 2>/dev/null || echo "0")
    
    if [[ "$copilot_enabled" != "0" && -n "$copilot_enabled" ]]; then
        check_pass "GitHub Copilot is enabled ($copilot_enabled seats)"
    else
        check_info "GitHub Copilot status unknown or not configured"
    fi
}

# =============================================================================
# DNS VALIDATION
# =============================================================================

validate_dns() {
    print_section "DNS Configuration"
    
    local dns_zone=$(parse_tfvars "dns_zone_name")
    local dns_rg=$(grep -E "dns_zone_resource_group\s*=" "$CONFIG_FILE" | sed 's/.*=\s*"\([^"]*\)".*/\1/')
    
    if [[ -z "$dns_zone" ]]; then
        check_warn "DNS zone not configured"
        return
    fi
    
    check_info "DNS zone: $dns_zone"
    
    # Check if DNS zone exists in Azure
    if [[ -n "$dns_rg" ]]; then
        local zone_exists=$(az network dns zone show -n "$dns_zone" -g "$dns_rg" --query name -o tsv 2>/dev/null)
        
        if [[ -n "$zone_exists" ]]; then
            check_pass "Azure DNS zone exists: $dns_zone"
            
            # Check name servers
            local ns=$(az network dns zone show -n "$dns_zone" -g "$dns_rg" --query "nameServers[0]" -o tsv 2>/dev/null)
            check_info "Primary name server: $ns"
        else
            check_warn "Azure DNS zone not found: $dns_zone in $dns_rg"
            echo "  Will be created during deployment if using Azure DNS"
        fi
    fi
    
    # Check if domain resolves
    if command_exists dig; then
        local ns_check=$(dig +short NS "$dns_zone" 2>/dev/null | head -1)
        if [[ -n "$ns_check" ]]; then
            check_pass "Domain has NS records: $ns_check"
        else
            check_info "Domain NS records not found (may not be delegated yet)"
        fi
    fi
}

# =============================================================================
# NETWORKING VALIDATION
# =============================================================================

validate_networking() {
    print_section "Network Configuration"
    
    # Check for existing VNet configuration
    local existing_vnet=$(grep -E "existing_vnet_id\s*=" "$CONFIG_FILE" | sed 's/.*=\s*"\([^"]*\)".*/\1/')
    
    if [[ -n "$existing_vnet" && "$existing_vnet" != "null" && "$existing_vnet" != '""' ]]; then
        check_info "Using existing VNet: ${existing_vnet:0:60}..."
        
        # Validate VNet exists
        local vnet_name=$(echo "$existing_vnet" | grep -oP 'virtualNetworks/\K[^/]+')
        local vnet_rg=$(echo "$existing_vnet" | grep -oP 'resourceGroups/\K[^/]+')
        
        if [[ -n "$vnet_name" && -n "$vnet_rg" ]]; then
            local vnet_check=$(az network vnet show -n "$vnet_name" -g "$vnet_rg" --query name -o tsv 2>/dev/null)
            
            if [[ -n "$vnet_check" ]]; then
                check_pass "Existing VNet found: $vnet_name"
                
                # Check address space
                local address_space=$(az network vnet show -n "$vnet_name" -g "$vnet_rg" --query "addressSpace.addressPrefixes[0]" -o tsv)
                check_info "Address space: $address_space"
            else
                check_fail "Existing VNet not found: $vnet_name"
            fi
        fi
    else
        check_info "Will create new VNet during deployment"
        
        # Validate CIDR if specified
        local vnet_cidr=$(grep -E "vnet_cidr\s*=" "$CONFIG_FILE" | sed 's/.*=\s*"\([^"]*\)".*/\1/')
        
        if [[ -n "$vnet_cidr" ]]; then
            if [[ "$vnet_cidr" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]+$ ]]; then
                check_pass "VNet CIDR format is valid: $vnet_cidr"
            else
                check_fail "VNet CIDR format is invalid: $vnet_cidr"
            fi
        fi
    fi
}

# =============================================================================
# TEAMS VALIDATION
# =============================================================================

validate_teams() {
    print_section "Teams Configuration"
    
    local teams_file="${SCRIPT_DIR}/../customer-config/teams.yaml"
    
    if [[ -f "$teams_file" ]]; then
        check_pass "teams.yaml file exists"
        
        # Validate YAML syntax
        if yq eval '.' "$teams_file" &>/dev/null; then
            check_pass "teams.yaml syntax is valid"
            
            # Count teams
            local team_count=$(yq eval '.teams | length' "$teams_file")
            check_info "Teams defined: $team_count"
            
            # Check each team has required fields
            local invalid_teams=$(yq eval '.teams[] | select(.name == null or .name == "")' "$teams_file")
            
            if [[ -z "$invalid_teams" ]]; then
                check_pass "All teams have names defined"
            else
                check_fail "Some teams missing name field"
            fi
        else
            check_fail "teams.yaml has invalid YAML syntax"
        fi
    else
        check_warn "teams.yaml not found (optional)"
        echo "  Teams can be added later via Backstage"
    fi
}

# =============================================================================
# SUMMARY
# =============================================================================

print_summary() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  VALIDATION SUMMARY${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo -e "  ${GREEN}[OK] Passed:${NC}   $CHECKS_PASSED"
    echo -e "  ${RED}[FAIL] Errors:${NC}   $ERRORS"
    echo -e "  ${YELLOW}[WARN] Warnings:${NC} $WARNINGS"
    echo ""
    
    if [[ $ERRORS -gt 0 ]]; then
        echo -e "${RED}  [FAIL] VALIDATION FAILED${NC}"
        echo ""
        echo "  Please fix the errors above before proceeding."
        echo ""
        
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            output_json
        fi
        
        exit 1
    elif [[ $WARNINGS -gt 0 && "$STRICT_MODE" == "true" ]]; then
        echo -e "${YELLOW}  [WARN] VALIDATION FAILED (strict mode)${NC}"
        echo ""
        echo "  Please fix the warnings above or run without --strict."
        echo ""
        
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            output_json
        fi
        
        exit 1
    else
        echo -e "${GREEN}  [OK] VALIDATION PASSED${NC}"
        echo ""
        
        if [[ $WARNINGS -gt 0 ]]; then
            echo "  Note: There are $WARNINGS warning(s) that may need attention."
            echo ""
        fi
        
        echo "  You can now proceed with deployment:"
        echo ""
        echo "    ./scripts/bootstrap.sh"
        echo ""
    fi
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        output_json
    fi
}

output_json() {
    echo ""
    echo "--- JSON OUTPUT ---"
    echo "{"
    echo "  \"passed\": $CHECKS_PASSED,"
    echo "  \"errors\": $ERRORS,"
    echo "  \"warnings\": $WARNINGS,"
    echo "  \"success\": $([[ $ERRORS -eq 0 ]] && echo "true" || echo "false"),"
    echo "  \"results\": ["
    
    local first=true
    for result in "${RESULTS[@]}"; do
        if [[ "$first" == "true" ]]; then
            first=false
        else
            echo ","
        fi
        echo -n "    $result"
    done
    
    echo ""
    echo "  ]"
    echo "}"
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --strict)
                STRICT_MODE=true
                shift
                ;;
            --skip-azure)
                SKIP_AZURE=true
                shift
                ;;
            --skip-github)
                SKIP_GITHUB=true
                shift
                ;;
            --skip-quotas)
                SKIP_QUOTAS=true
                shift
                ;;
            --json)
                JSON_OUTPUT=true
                shift
                ;;
            --help)
                head -30 "$0" | tail -25
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    print_header
    
    check_prerequisites
    validate_config_syntax
    validate_azure
    validate_quotas
    validate_github
    validate_dns
    validate_networking
    validate_teams
    
    print_summary
}

main "$@"
