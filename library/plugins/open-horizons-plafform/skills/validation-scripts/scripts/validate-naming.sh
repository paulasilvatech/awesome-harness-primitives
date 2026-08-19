#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - AZURE NAMING VALIDATION
# =============================================================================
#
# Validates Azure resource names against naming rules
#
# Usage: ./scripts/validate-naming.sh <resource_type> <name>
#        ./scripts/validate-naming.sh --all <project> <env> <region>
#
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Validation functions
validate_storage_account() {
    local name="$1"
    local errors=()
    
    # Length: 3-24
    if [[ ${#name} -lt 3 || ${#name} -gt 24 ]]; then
        errors+=("Length must be 3-24 characters (got ${#name})")
    fi
    
    # Only lowercase and numbers
    if [[ ! "$name" =~ ^[a-z0-9]+$ ]]; then
        errors+=("Only lowercase letters and numbers allowed")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} Storage Account: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} Storage Account: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

validate_container_registry() {
    local name="$1"
    local errors=()
    
    # Length: 5-50
    if [[ ${#name} -lt 5 || ${#name} -gt 50 ]]; then
        errors+=("Length must be 5-50 characters (got ${#name})")
    fi
    
    # Only alphanumeric (no hyphens!)
    if [[ ! "$name" =~ ^[a-zA-Z0-9]+$ ]]; then
        errors+=("Only alphanumeric characters allowed (no hyphens)")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} Container Registry: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} Container Registry: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

validate_key_vault() {
    local name="$1"
    local errors=()
    
    # Length: 3-24
    if [[ ${#name} -lt 3 || ${#name} -gt 24 ]]; then
        errors+=("Length must be 3-24 characters (got ${#name})")
    fi
    
    # Alphanumeric and hyphens
    if [[ ! "$name" =~ ^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$ && ${#name} -gt 2 ]]; then
        errors+=("Must start with letter, contain only alphanumeric and hyphens, end with alphanumeric")
    fi
    
    # Cannot have consecutive hyphens
    if [[ "$name" =~ -- ]]; then
        errors+=("Cannot have consecutive hyphens")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} Key Vault: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} Key Vault: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

validate_aks_cluster() {
    local name="$1"
    local errors=()
    
    # Length: 1-63
    if [[ ${#name} -lt 1 || ${#name} -gt 63 ]]; then
        errors+=("Length must be 1-63 characters (got ${#name})")
    fi
    
    # Alphanumeric, underscore, hyphen
    if [[ ! "$name" =~ ^[a-zA-Z][a-zA-Z0-9_-]*[a-zA-Z0-9]$ && ${#name} -gt 1 ]]; then
        errors+=("Must start with letter, end with alphanumeric")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} AKS Cluster: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} AKS Cluster: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

validate_aks_node_pool() {
    local name="$1"
    local errors=()
    
    # Length: 1-12 (Linux)
    if [[ ${#name} -lt 1 || ${#name} -gt 12 ]]; then
        errors+=("Length must be 1-12 characters (got ${#name})")
    fi
    
    # Lowercase alphanumeric only
    if [[ ! "$name" =~ ^[a-z][a-z0-9]*$ ]]; then
        errors+=("Lowercase alphanumeric only, must start with letter")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} AKS Node Pool: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} AKS Node Pool: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

validate_postgresql() {
    local name="$1"
    local errors=()
    
    # Length: 3-63
    if [[ ${#name} -lt 3 || ${#name} -gt 63 ]]; then
        errors+=("Length must be 3-63 characters (got ${#name})")
    fi
    
    # Lowercase, numbers, hyphens
    if [[ ! "$name" =~ ^[a-z][a-z0-9-]*[a-z0-9]$ && ${#name} -gt 2 ]]; then
        errors+=("Lowercase, numbers, hyphens only; must start with letter")
    fi
    
    # Cannot start/end with hyphen
    if [[ "$name" =~ ^- || "$name" =~ -$ ]]; then
        errors+=("Cannot start or end with hyphen")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} PostgreSQL Server: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} PostgreSQL Server: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

validate_resource_group() {
    local name="$1"
    local errors=()
    
    # Length: 1-90
    if [[ ${#name} -lt 1 || ${#name} -gt 90 ]]; then
        errors+=("Length must be 1-90 characters (got ${#name})")
    fi
    
    # Cannot end with period
    if [[ "$name" =~ \.$ ]]; then
        errors+=("Cannot end with period")
    fi
    
    if [[ ${#errors[@]} -eq 0 ]]; then
        echo -e "${GREEN}[OK]${NC} Resource Group: $name"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} Resource Group: $name"
        for err in "${errors[@]}"; do
            echo "   - $err"
        done
        return 1
    fi
}

# Region code mapping
get_region_code() {
    local region="$1"
    case "$region" in
        brazilsouth) echo "brs" ;;
        brazilsoutheast) echo "brse" ;;
        eastus) echo "eus" ;;
        eastus2) echo "eus2" ;;
        westus2) echo "wus2" ;;
        westeurope) echo "weu" ;;
        southcentralus) echo "scus" ;;
        *) echo "${region:0:4}" ;;
    esac
}

# Generate and validate all names
validate_all() {
    local project="$1"
    local env="$2"
    local region="$3"
    local region_code=$(get_region_code "$region")
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║        AZURE NAMING VALIDATION                                      ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Project: $project | Environment: $env | Region: $region ($region_code)"
    echo ""
    
    local prefix="${project}-${env}-${region_code}"
    local prefix_no_dash="${project}${env}${region_code}"
    
    local exit_code=0
    
    # Validate each resource type
    validate_resource_group "rg-${prefix}" || exit_code=1
    validate_aks_cluster "aks-${prefix}" || exit_code=1
    validate_aks_node_pool "system" || exit_code=1
    validate_aks_node_pool "user001" || exit_code=1
    validate_container_registry "cr${prefix_no_dash}" || exit_code=1
    validate_storage_account "st${prefix_no_dash}001" || exit_code=1
    validate_key_vault "kv-${prefix}" || exit_code=1
    validate_postgresql "psql-${prefix}" || exit_code=1
    
    echo ""
    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}All naming validations passed!${NC}"
    else
        echo -e "${RED}Some naming validations failed!${NC}"
    fi
    
    return $exit_code
}

# Main
main() {
    case "${1:-}" in
        --all)
            if [[ $# -lt 4 ]]; then
                echo "Usage: $0 --all <project> <environment> <region>"
                echo "Example: $0 --all openhorizons prd brazilsouth"
                exit 1
            fi
            validate_all "$2" "$3" "$4"
            ;;
        storage)
            validate_storage_account "${2:-}"
            ;;
        acr|container-registry)
            validate_container_registry "${2:-}"
            ;;
        keyvault|kv)
            validate_key_vault "${2:-}"
            ;;
        aks)
            validate_aks_cluster "${2:-}"
            ;;
        nodepool)
            validate_aks_node_pool "${2:-}"
            ;;
        postgresql|psql)
            validate_postgresql "${2:-}"
            ;;
        rg|resource-group)
            validate_resource_group "${2:-}"
            ;;
        *)
            echo "Azure Naming Validator"
            echo ""
            echo "Usage:"
            echo "  $0 --all <project> <environment> <region>"
            echo "  $0 <resource_type> <name>"
            echo ""
            echo "Resource Types:"
            echo "  storage           Storage Account"
            echo "  acr               Container Registry"
            echo "  keyvault          Key Vault"
            echo "  aks               AKS Cluster"
            echo "  nodepool          AKS Node Pool"
            echo "  postgresql        PostgreSQL Server"
            echo "  rg                Resource Group"
            echo ""
            echo "Examples:"
            echo "  $0 --all openhorizons prd brazilsouth"
            echo "  $0 storage stopenhorizonsprd001"
            echo "  $0 acr cropenhorizonsprd"
            ;;
    esac
}

main "$@"
