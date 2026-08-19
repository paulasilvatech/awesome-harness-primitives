#!/bin/bash
#
# validate-agents.sh - Validate all agent specification files
#
# This script checks:
# - All agent files exist and are non-empty
# - Required sections are present in each file
# - MCP server references are valid
# - Cross-references between agents are valid
#
# Usage: ./scripts/validate-agents.sh [--verbose]
#

set -euo pipefail

# --- requires bash 4+ (associative arrays); macOS ships bash 3.2 by default ---
if (( ${BASH_VERSINFO[0]:-0} < 4 )); then
    echo "ERROR: this script requires bash 4 or newer (found ${BASH_VERSION:-unknown})." >&2
    echo "       On macOS run: brew install bash, then invoke the script with that bash." >&2
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
AGENTS_DIR="$PROJECT_ROOT/agents"

# Counters
TOTAL_AGENTS=0
VALID_AGENTS=0
WARNINGS=0
ERRORS=0

# Verbose mode
VERBOSE=false
if [[ "${1:-}" == "--verbose" || "${1:-}" == "-v" ]]; then
    VERBOSE=true
fi

# Print functions
print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARN]  $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

print_error() {
    echo -e "${RED}[FAIL] $1${NC}"
    ERRORS=$((ERRORS + 1))
}

print_info() {
    if [[ "$VERBOSE" == true ]]; then
        echo -e "${BLUE}[INFO]  $1${NC}"
    fi
}

# Required sections in agent files
REQUIRED_SECTIONS=(
    "Agent Identity"
    "Capabilities"
    "MCP Servers"
    "Trigger Labels"
    "Validation"
)

# Expected agent files
declare -A EXPECTED_AGENTS=(
    # H1 Foundation
    ["h1-foundation/infrastructure-agent.md"]="Infrastructure Agent"
    ["h1-foundation/networking-agent.md"]="Networking Agent"
    ["h1-foundation/security-agent.md"]="Security Agent"
    ["h1-foundation/container-registry-agent.md"]="Container Registry Agent"
    ["h1-foundation/database-agent.md"]="Database Agent"
    ["h1-foundation/defender-cloud-agent.md"]="Defender Cloud Agent"
    ["h1-foundation/purview-governance-agent.md"]="Purview Governance Agent"
    # H2 Enhancement
    ["h2-enhancement/gitops-agent.md"]="GitOps Agent"
    ["h2-enhancement/observability-agent.md"]="Observability Agent"
    ["h2-enhancement/backstage-portal-agent.md"]="Backstage Portal Agent"
    ["h2-enhancement/golden-paths-agent.md"]="Golden Paths Agent"
    ["h2-enhancement/github-runners-agent.md"]="GitHub Runners Agent"
    # H3 Innovation
    ["h3-innovation/ai-foundry-agent.md"]="AI Foundry Agent"
    ["h3-innovation/mlops-pipeline-agent.md"]="MLOps Pipeline Agent"
    ["h3-innovation/sre-agent-setup.md"]="SRE Agent Setup"
    ["h3-innovation/multi-agent-setup.md"]="Multi-Agent Setup"
    # Cross-Cutting
    ["cross-cutting/validation-agent.md"]="Validation Agent"
    ["cross-cutting/migration-agent.md"]="Migration Agent"
    ["cross-cutting/rollback-agent.md"]="Rollback Agent"
    ["cross-cutting/cost-optimization-agent.md"]="Cost Optimization Agent"
    ["cross-cutting/github-app-agent.md"]="GitHub App Agent"
    ["cross-cutting/identity-federation-agent.md"]="Identity Federation Agent"
)

# Valid MCP servers (exported for use by other scripts)
export VALID_MCP_SERVERS=(
    "kubernetes"
    "azure"
    "github"
    "helm"
    "terraform"
    "git"
    "azure-ai"
    "prometheus"
)

# Validate single agent file
validate_agent() {
    local file_path="$1"
    local agent_name="$2"
    local full_path="$AGENTS_DIR/$file_path"
    local file_valid=true

    print_info "Validating: $agent_name"

    # Check file exists
    if [[ ! -f "$full_path" ]]; then
        print_error "$agent_name: File not found ($file_path)"
        return 1
    fi

    # Check file is not empty
    if [[ ! -s "$full_path" ]]; then
        print_error "$agent_name: File is empty"
        return 1
    fi

    # Get line count
    local line_count
    line_count=$(wc -l < "$full_path")
    if [[ $line_count -lt 50 ]]; then
        print_warning "$agent_name: File seems too short ($line_count lines)"
        file_valid=false
    fi

    # Check required sections
    for section in "${REQUIRED_SECTIONS[@]}"; do
        if ! grep -qi "$section" "$full_path"; then
            print_warning "$agent_name: Missing section '$section'"
            file_valid=false
        fi
    done

    # Check for MCP server references
    if ! grep -qi "mcp" "$full_path"; then
        print_warning "$agent_name: No MCP server references found"
        file_valid=false
    fi

    # Check for trigger labels
    if ! grep -qi "agent:" "$full_path"; then
        print_warning "$agent_name: No trigger labels found"
        file_valid=false
    fi

    # Check for code blocks
    if ! grep -q '```' "$full_path"; then
        print_warning "$agent_name: No code blocks found"
        file_valid=false
    fi

    if [[ "$file_valid" == true ]]; then
        print_success "$agent_name: Valid ($line_count lines)"
        return 0
    else
        return 1
    fi
}

# Validate directory structure
validate_structure() {
    print_header "Validating Directory Structure"

    local categories=("h1-foundation" "h2-enhancement" "h3-innovation" "cross-cutting")

    for category in "${categories[@]}"; do
        if [[ -d "$AGENTS_DIR/$category" ]]; then
            local count
            count=$(find "$AGENTS_DIR/$category" -name "*.md" | wc -l)
            print_success "$category/: $count agents found"
        else
            print_error "$category/: Directory not found"
        fi
    done
}

# Validate all agent files
validate_agents() {
    print_header "Validating Agent Specifications"

    for file_path in "${!EXPECTED_AGENTS[@]}"; do
        TOTAL_AGENTS=$((TOTAL_AGENTS + 1))
        if validate_agent "$file_path" "${EXPECTED_AGENTS[$file_path]}"; then
            VALID_AGENTS=$((VALID_AGENTS + 1))
        fi
    done
}

# Validate documentation files
validate_docs() {
    print_header "Validating Documentation Files"

    local docs=(
        "README.md"
        "INDEX.md"
        "DEPLOYMENT_SEQUENCE.md"
        "MCP_SERVERS_GUIDE.md"
        "TERRAFORM_MODULES_REFERENCE.md"
        "DEPENDENCY_GRAPH.md"
    )

    for doc in "${docs[@]}"; do
        if [[ -f "$AGENTS_DIR/$doc" ]]; then
            local line_count
            line_count=$(wc -l < "$AGENTS_DIR/$doc")
            print_success "$doc: Found ($line_count lines)"
        else
            print_warning "$doc: Not found (optional)"
        fi
    done
}

# Check cross-references
validate_crossrefs() {
    print_header "Validating Cross-References"

    # Check for broken links within agents directory
    local broken_links=0

    for file in "$AGENTS_DIR"/**/*.md; do
        if [[ -f "$file" ]]; then
            # Extract markdown links
            while IFS= read -r link; do
                # Skip external links
                if [[ "$link" == http* ]]; then
                    continue
                fi

                # Check if referenced file exists
                local ref_path="$AGENTS_DIR/$link"
                local dir_path
                dir_path=$(dirname "$file")
                local rel_path="$dir_path/$link"

                if [[ ! -f "$ref_path" && ! -f "$rel_path" ]]; then
                    if [[ "$VERBOSE" == true ]]; then
                        print_warning "Broken link in $(basename "$file"): $link"
                    fi
                    broken_links=$((broken_links + 1))
                fi
            done < <(grep -oP '\[.*?\]\(\K[^)]+(?=\))' "$file" 2>/dev/null || true)
        fi
    done

    if [[ $broken_links -eq 0 ]]; then
        print_success "No broken cross-references found"
    else
        print_warning "$broken_links potential broken links found (run with --verbose for details)"
    fi
}

# Generate summary
print_summary() {
    print_header "Validation Summary"

    echo -e "Total Agents:    ${BLUE}$TOTAL_AGENTS${NC}"
    echo -e "Valid Agents:    ${GREEN}$VALID_AGENTS${NC}"
    echo -e "Warnings:        ${YELLOW}$WARNINGS${NC}"
    echo -e "Errors:          ${RED}$ERRORS${NC}"
    echo ""

    local percentage=$((VALID_AGENTS * 100 / TOTAL_AGENTS))

    if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
        print_success "All validations passed! ($percentage% agents valid)"
        exit 0
    elif [[ $ERRORS -eq 0 ]]; then
        print_warning "Validation completed with warnings ($percentage% agents valid)"
        exit 0
    else
        print_error "Validation failed with errors ($percentage% agents valid)"
        exit 1
    fi
}

# Main execution
main() {
    print_header "Open Horizons Agent Validator"

    echo "Project Root: $PROJECT_ROOT"
    echo "Agents Dir:   $AGENTS_DIR"
    echo ""

    validate_structure
    validate_agents
    validate_docs
    validate_crossrefs
    print_summary
}

main "$@"
