#!/bin/bash
# Deployment script with security checks
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing_tools=()

    command -v kubectl >/dev/null 2>&1 || missing_tools+=("kubectl")
    command -v docker >/dev/null 2>&1 || missing_tools+=("docker")
    command -v cosign >/dev/null 2>&1 || missing_tools+=("cosign")

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    log_info "All prerequisites met"
}

verify_image_signature() {
    local image=$1
    log_info "Verifying image signature for: ${image}"

    if cosign verify --key cosign.pub "${image}"; then
        log_info "Image signature verified successfully"
        return 0
    else
        log_error "Image signature verification failed"
        return 1
    fi
}

apply_kubernetes_manifests() {
    local environment=$1
    log_info "Applying Kubernetes manifests for environment: ${environment}"

    kubectl apply -f "${PROJECT_ROOT}/infrastructure/kubernetes/base/"

    if [ -d "${PROJECT_ROOT}/infrastructure/kubernetes/overlays/${environment}" ]; then
        kubectl apply -f "${PROJECT_ROOT}/infrastructure/kubernetes/overlays/${environment}/"
    fi

    log_info "Kubernetes manifests applied successfully"
}

wait_for_rollout() {
    local deployment=$1
    local namespace=${2:-devsecops-app}

    log_info "Waiting for deployment rollout: ${deployment}"
    kubectl rollout status deployment/"${deployment}" -n "${namespace}" --timeout=5m

    log_info "Deployment rolled out successfully"
}

run_smoke_tests() {
    log_info "Running smoke tests..."

    local service_url=$1

    # Wait for service to be ready
    sleep 10

    # Health check
    if curl -f -s "${service_url}/health" > /dev/null; then
        log_info "Health check passed"
    else
        log_error "Health check failed"
        return 1
    fi

    # Readiness check
    if curl -f -s "${service_url}/ready" > /dev/null; then
        log_info "Readiness check passed"
    else
        log_error "Readiness check failed"
        return 1
    fi

    log_info "All smoke tests passed"
}

main() {
    local environment=${1:-dev}
    local image_tag=${2:-latest}

    log_info "Starting deployment for environment: ${environment}"

    check_prerequisites

    # Verify image signature (optional in dev)
    if [ "${environment}" != "dev" ]; then
        verify_image_signature "ghcr.io/organization/devsecops-app:${image_tag}" || exit 1
    fi

    apply_kubernetes_manifests "${environment}"

    wait_for_rollout "devsecops-app" "devsecops-app"

    # Get service URL
    local service_url="http://$(kubectl get svc devsecops-app -n devsecops-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"

    run_smoke_tests "${service_url}" || {
        log_error "Smoke tests failed, rolling back..."
        kubectl rollout undo deployment/devsecops-app -n devsecops-app
        exit 1
    }

    log_info "Deployment completed successfully!"
}

main "$@"
