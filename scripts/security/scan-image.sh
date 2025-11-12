#!/bin/bash
# Comprehensive container image security scanning script
set -euo pipefail

IMAGE="${1:-}"
SEVERITY="${2:-CRITICAL,HIGH}"

if [ -z "$IMAGE" ]; then
    echo "Usage: $0 <image> [severity]"
    echo "Example: $0 myapp:latest CRITICAL,HIGH,MEDIUM"
    exit 1
fi

echo "🔍 Scanning image: $IMAGE"
echo "📊 Severity levels: $SEVERITY"
echo ""

# Create reports directory
REPORTS_DIR="security-reports"
mkdir -p "$REPORTS_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. Trivy Scan
echo "=== Running Trivy Scan ==="
trivy image \
    --severity "$SEVERITY" \
    --format json \
    --output "$REPORTS_DIR/trivy-${TIMESTAMP}.json" \
    "$IMAGE"

trivy image \
    --severity "$SEVERITY" \
    --format table \
    "$IMAGE"

# 2. Generate SBOM with Syft
echo ""
echo "=== Generating SBOM with Syft ==="
syft "$IMAGE" -o spdx-json > "$REPORTS_DIR/sbom-spdx-${TIMESTAMP}.json"
syft "$IMAGE" -o cyclonedx-json > "$REPORTS_DIR/sbom-cyclonedx-${TIMESTAMP}.json"
echo "✅ SBOM generated: $REPORTS_DIR/sbom-*-${TIMESTAMP}.json"

# 3. Grype Scan on SBOM
echo ""
echo "=== Running Grype Scan on SBOM ==="
grype "sbom:$REPORTS_DIR/sbom-spdx-${TIMESTAMP}.json" \
    -o json > "$REPORTS_DIR/grype-${TIMESTAMP}.json" || true

grype "sbom:$REPORTS_DIR/sbom-spdx-${TIMESTAMP}.json" \
    -o table || true

# 4. Dockle for best practices
if command -v dockle &> /dev/null; then
    echo ""
    echo "=== Running Dockle Best Practices Check ==="
    dockle --format json --output "$REPORTS_DIR/dockle-${TIMESTAMP}.json" "$IMAGE" || true
    dockle "$IMAGE" || true
fi

# Summary
echo ""
echo "=========================================="
echo "📋 Security Scan Summary"
echo "=========================================="
echo "Image: $IMAGE"
echo "Timestamp: $TIMESTAMP"
echo "Reports directory: $REPORTS_DIR"
echo ""
echo "Generated files:"
ls -lh "$REPORTS_DIR"/*"${TIMESTAMP}"*
echo ""
echo "✅ Scan completed!"
