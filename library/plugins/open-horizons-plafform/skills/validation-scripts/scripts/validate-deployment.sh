#!/bin/bash
# =============================================================================
# OPEN HORIZONS PLATFORM - DEPLOYMENT VALIDATION SCRIPT
# =============================================================================
#
# Validates that a Open Horizons platform deployment is healthy and functional.
#
# Usage:
#   ./validate-deployment.sh [options]
#
# Options:
#   --environment [dev|staging|prod]  Target environment (default: dev)
#   --horizon [h1|h2|h3|all]          Validate specific horizon (default: all)
#   --verbose                         Show detailed output
#   --quick                           Quick check (skip slow tests)
#   --help                            Show this help message
#
# Exit Codes:
#   0 - All validations passed
#   1 - One or more validations failed
#   2 - Prerequisites not met
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
NC='\033[0m' # No Color

# Default values
ENVIRONMENT="dev"
HORIZON="all"
VERBOSE=false
QUICK=false

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# =============================================================================
# FUNCTIONS
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $*"
    PASSED=$((PASSED + 1))
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $*"
    WARNINGS=$((WARNINGS + 1))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $*"
    FAILED=$((FAILED + 1))
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $*"
    fi
}

print_banner() {
    echo ""
    echo "============================================================"
    echo "  OPEN HORIZONS PLATFORM - DEPLOYMENT VALIDATION"
    echo "============================================================"
    echo ""
    echo "  Environment: $ENVIRONMENT"
    echo "  Horizon:     $HORIZON"
    echo "  Mode:        $([ "$QUICK" == "true" ] && echo "Quick" || echo "Full")"
    echo ""
    echo "============================================================"
    echo ""
}

show_help() {
    head -30 "$0" | tail -25
    exit 0
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            --horizon)
                HORIZON="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --quick)
                QUICK=true
                shift
                ;;
            --help)
                show_help
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                ;;
        esac
    done
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing=()

    command -v kubectl >/dev/null 2>&1 || missing+=("kubectl")
    command -v az >/dev/null 2>&1 || missing+=("az")
    command -v helm >/dev/null 2>&1 || missing+=("helm")
    command -v jq >/dev/null 2>&1 || missing+=("jq")

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing[*]}"
        exit 2
    fi

    # Check kubectl context
    if ! kubectl config current-context >/dev/null 2>&1; then
        log_error "No kubectl context configured"
        exit 2
    fi

    log_success "Prerequisites check passed"
}

# =============================================================================
# H1 FOUNDATION VALIDATIONS
# =============================================================================

validate_h1_nodes() {
    log_info "Validating AKS cluster nodes..."

    local ready_nodes
    ready_nodes=$(kubectl get nodes --no-headers 2>/dev/null | grep -c " Ready " || echo "0")
    local total_nodes
    total_nodes=$(kubectl get nodes --no-headers 2>/dev/null | wc -l | tr -d ' ')

    if [[ "$ready_nodes" -eq "$total_nodes" ]] && [[ "$total_nodes" -gt 0 ]]; then
        log_success "All $total_nodes nodes are Ready"
    else
        log_error "Only $ready_nodes/$total_nodes nodes are Ready"
    fi

    # Check for node conditions
    local node_issues
    node_issues=$(kubectl get nodes -o json 2>/dev/null | jq -r '.items[].status.conditions[] | select(.type != "Ready" and .status == "True") | .type' | wc -l | tr -d ' ')

    if [[ "$node_issues" -gt 0 ]]; then
        log_warning "Found $node_issues node condition issues"
        log_verbose "Run: kubectl describe nodes | grep -A5 Conditions"
    fi
}

validate_h1_system_pods() {
    log_info "Validating system pods..."

    local namespaces=("kube-system" "default")

    for ns in "${namespaces[@]}"; do
        local running
        running=$(kubectl get pods -n "$ns" --no-headers 2>/dev/null | grep -c "Running" || echo "0")
        local total
        total=$(kubectl get pods -n "$ns" --no-headers 2>/dev/null | wc -l | tr -d ' ')

        if [[ "$total" -eq 0 ]]; then
            log_verbose "No pods in namespace $ns"
            continue
        fi

        if [[ "$running" -eq "$total" ]]; then
            log_success "All $total pods in $ns are Running"
        else
            log_error "Only $running/$total pods in $ns are Running"
            log_verbose "Run: kubectl get pods -n $ns | grep -v Running"
        fi
    done
}

validate_h1_networking() {
    log_info "Validating networking..."

    # Check CoreDNS
    local coredns_ready
    coredns_ready=$(kubectl get pods -n kube-system -l k8s-app=kube-dns --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$coredns_ready" -gt 0 ]]; then
        log_success "CoreDNS is running ($coredns_ready replicas)"
    else
        log_error "CoreDNS is not running"
    fi

    # Quick DNS test
    if [[ "$QUICK" != "true" ]]; then
        if kubectl run dns-test --image=busybox:1.36 --restart=Never --rm -it --command -- nslookup kubernetes.default >/dev/null 2>&1; then
            log_success "DNS resolution is working"
        else
            log_warning "DNS resolution test inconclusive"
        fi
    fi
}

validate_h1_storage() {
    log_info "Validating storage classes..."

    local sc_count
    sc_count=$(kubectl get storageclass --no-headers 2>/dev/null | wc -l | tr -d ' ')

    if [[ "$sc_count" -gt 0 ]]; then
        log_success "Found $sc_count storage classes"

        # Check for default storage class
        local default_sc
        default_sc=$(kubectl get storageclass -o json 2>/dev/null | jq -r '.items[] | select(.metadata.annotations["storageclass.kubernetes.io/is-default-class"] == "true") | .metadata.name' | head -1)

        if [[ -n "$default_sc" ]]; then
            log_success "Default storage class: $default_sc"
        else
            log_warning "No default storage class configured"
        fi
    else
        log_error "No storage classes found"
    fi
}

# =============================================================================
# H2 ENHANCEMENT VALIDATIONS
# =============================================================================

validate_h2_argocd() {
    log_info "Validating ArgoCD..."

    if ! kubectl get namespace argocd >/dev/null 2>&1; then
        log_warning "ArgoCD namespace not found (H2 may not be deployed)"
        return
    fi

    # Check ArgoCD server
    local argocd_ready
    argocd_ready=$(kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$argocd_ready" -gt 0 ]]; then
        log_success "ArgoCD server is running"
    else
        log_error "ArgoCD server is not running"
    fi

    # Check ArgoCD applications health
    local healthy_apps
    healthy_apps=$(kubectl get applications -n argocd -o json 2>/dev/null | jq '[.items[] | select(.status.health.status == "Healthy")] | length' || echo "0")
    local total_apps
    total_apps=$(kubectl get applications -n argocd --no-headers 2>/dev/null | wc -l | tr -d ' ')

    if [[ "$total_apps" -gt 0 ]]; then
        if [[ "$healthy_apps" -eq "$total_apps" ]]; then
            log_success "All $total_apps ArgoCD applications are Healthy"
        else
            log_warning "$healthy_apps/$total_apps ArgoCD applications are Healthy"
        fi
    fi
}

validate_h2_observability() {
    log_info "Validating observability stack..."

    local namespaces=("observability" "monitoring")
    local found_ns=""

    for ns in "${namespaces[@]}"; do
        if kubectl get namespace "$ns" >/dev/null 2>&1; then
            found_ns="$ns"
            break
        fi
    done

    if [[ -z "$found_ns" ]]; then
        log_warning "Observability namespace not found (H2 may not be deployed)"
        return
    fi

    # Check Prometheus
    local prometheus_ready
    prometheus_ready=$(kubectl get pods -n "$found_ns" -l app.kubernetes.io/name=prometheus --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$prometheus_ready" -gt 0 ]]; then
        log_success "Prometheus is running"
    else
        log_warning "Prometheus not detected in $found_ns"
    fi

    # Check Grafana
    local grafana_ready
    grafana_ready=$(kubectl get pods -n "$found_ns" -l app.kubernetes.io/name=grafana --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$grafana_ready" -gt 0 ]]; then
        log_success "Grafana is running"
    else
        log_warning "Grafana not detected in $found_ns"
    fi
}

validate_h2_external_secrets() {
    log_info "Validating External Secrets Operator..."

    if ! kubectl get namespace external-secrets >/dev/null 2>&1; then
        log_warning "External Secrets namespace not found"
        return
    fi

    local eso_ready
    eso_ready=$(kubectl get pods -n external-secrets -l app.kubernetes.io/name=external-secrets --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$eso_ready" -gt 0 ]]; then
        log_success "External Secrets Operator is running"
    else
        log_error "External Secrets Operator is not running"
    fi

    # Check ClusterSecretStore
    local css_ready
    css_ready=$(kubectl get clustersecretstore --no-headers 2>/dev/null | grep -c "Valid" || echo "0")

    if [[ "$css_ready" -gt 0 ]]; then
        log_success "Found $css_ready valid ClusterSecretStore(s)"
    else
        log_warning "No valid ClusterSecretStore found"
    fi
}

validate_h2_gatekeeper() {
    log_info "Validating Gatekeeper..."

    if ! kubectl get namespace gatekeeper-system >/dev/null 2>&1; then
        log_warning "Gatekeeper namespace not found"
        return
    fi

    local gk_ready
    gk_ready=$(kubectl get pods -n gatekeeper-system --no-headers 2>/dev/null | grep -c "Running" || echo "0")

    if [[ "$gk_ready" -gt 0 ]]; then
        log_success "Gatekeeper is running ($gk_ready pods)"
    else
        log_error "Gatekeeper is not running"
    fi

    # Check constraint templates
    local templates
    templates=$(kubectl get constrainttemplates --no-headers 2>/dev/null | wc -l | tr -d ' ')

    if [[ "$templates" -gt 0 ]]; then
        log_success "Found $templates constraint templates"
    fi
}

# =============================================================================
# H3 INNOVATION VALIDATIONS
# =============================================================================

validate_h3_ai_services() {
    log_info "Validating AI services connectivity..."

    # Check if AI-related secrets exist
    local ai_secrets
    ai_secrets=$(kubectl get secrets --all-namespaces -o json 2>/dev/null | jq '[.items[] | select(.metadata.name | contains("openai") or contains("ai-"))] | length' || echo "0")

    if [[ "$ai_secrets" -gt 0 ]]; then
        log_success "Found $ai_secrets AI-related secrets"
    else
        log_warning "No AI-related secrets found (H3 may not be deployed)"
    fi
}

# =============================================================================
# SUMMARY
# =============================================================================

print_summary() {
    echo ""
    echo "============================================================"
    echo "  VALIDATION SUMMARY"
    echo "============================================================"
    echo ""
    echo -e "  ${GREEN}Passed:${NC}   $PASSED"
    echo -e "  ${RED}Failed:${NC}   $FAILED"
    echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
    echo ""

    if [[ "$FAILED" -eq 0 ]]; then
        echo -e "  ${GREEN}Overall Status: HEALTHY${NC}"
        echo ""
        echo "============================================================"
        return 0
    else
        echo -e "  ${RED}Overall Status: UNHEALTHY${NC}"
        echo ""
        echo "  Run with --verbose for more details"
        echo ""
        echo "============================================================"
        return 1
    fi
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    parse_args "$@"
    print_banner
    check_prerequisites

    echo ""
    log_info "Starting validation for horizon: $HORIZON"
    echo ""

    # H1 Foundation validations
    if [[ "$HORIZON" == "all" ]] || [[ "$HORIZON" == "h1" ]]; then
        echo "--- H1: FOUNDATION ---"
        validate_h1_nodes
        validate_h1_system_pods
        validate_h1_networking
        validate_h1_storage
        echo ""
    fi

    # H2 Enhancement validations
    if [[ "$HORIZON" == "all" ]] || [[ "$HORIZON" == "h2" ]]; then
        echo "--- H2: ENHANCEMENT ---"
        validate_h2_argocd
        validate_h2_observability
        validate_h2_external_secrets
        validate_h2_gatekeeper
        echo ""
    fi

    # H3 Innovation validations
    if [[ "$HORIZON" == "all" ]] || [[ "$HORIZON" == "h3" ]]; then
        echo "--- H3: INNOVATION ---"
        validate_h3_ai_services
        echo ""
    fi

    print_summary
}

main "$@"
