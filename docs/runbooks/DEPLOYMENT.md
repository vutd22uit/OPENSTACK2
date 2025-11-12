# Deployment Runbook

## Overview

This runbook provides step-by-step procedures for deploying the application to different environments.

## Pre-Deployment Checklist

- [ ] All tests passing in CI/CD
- [ ] Security scans completed with no critical/high vulnerabilities
- [ ] Code review approved
- [ ] Change request approved (for production)
- [ ] Deployment window scheduled (for production)
- [ ] Rollback plan documented
- [ ] Stakeholders notified

## Deployment Environments

### Development (dev)
- **Purpose**: Active development and testing
- **Approval**: Not required
- **Deployment**: Automatic on merge to develop branch
- **Data**: Synthetic test data

### Staging (staging)
- **Purpose**: Pre-production validation
- **Approval**: Team lead
- **Deployment**: Manual trigger
- **Data**: Anonymized production data

### Production (prod)
- **Purpose**: Live customer-facing environment
- **Approval**: Product owner + Security team
- **Deployment**: Manual trigger with approval
- **Data**: Production data

## Standard Deployment Procedure

### 1. Pre-Deployment Validation

\`\`\`bash
# Verify CI/CD pipeline passed
gh run list --workflow=ci-security.yml --limit 1

# Check for security vulnerabilities
gh api repos/:owner/:repo/code-scanning/alerts?state=open

# Verify image exists and is signed
cosign verify --key cosign.pub ghcr.io/org/app:${TAG}
\`\`\`

### 2. Infrastructure Preparation

\`\`\`bash
# Verify cluster health
kubectl get nodes
kubectl top nodes

# Check resource availability
kubectl describe nodes | grep -A 5 "Allocated resources"

# Verify namespace exists
kubectl get namespace devsecops-app
\`\`\`

### 3. Database Migration (if required)

\`\`\`bash
# Backup database
pg_dump -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} > backup_$(date +%Y%m%d_%H%M%S).sql

# Test migration on staging
kubectl apply -f migrations/

# Verify migration
kubectl logs -f job/db-migration -n devsecops-app
\`\`\`

### 4. Application Deployment

\`\`\`bash
# Set image tag
export IMAGE_TAG=$(git rev-parse --short HEAD)

# Update deployment manifest
cd infrastructure/kubernetes/overlays/${ENV}
kustomize edit set image ghcr.io/org/app:${IMAGE_TAG}

# Apply deployment
kubectl apply -k .

# Watch rollout
kubectl rollout status deployment/devsecops-app -n devsecops-app --timeout=5m
\`\`\`

### 5. Post-Deployment Verification

\`\`\`bash
# Check pod status
kubectl get pods -n devsecops-app

# Check pod logs for errors
kubectl logs -f deployment/devsecops-app -n devsecops-app --tail=50

# Run smoke tests
./scripts/deploy/smoke-tests.sh ${SERVICE_URL}

# Verify health endpoints
curl -f ${SERVICE_URL}/health
curl -f ${SERVICE_URL}/ready

# Check metrics
curl ${SERVICE_URL}/metrics
\`\`\`

### 6. Monitoring and Alerting

\`\`\`bash
# Verify Prometheus targets
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Check targets at http://localhost:9090/targets

# Check Grafana dashboards
kubectl port-forward -n monitoring svc/grafana 3000:3000
# View at http://localhost:3000

# Verify alerts are configured
kubectl get prometheusrules -n monitoring
\`\`\`

## Rollback Procedure

### Quick Rollback

\`\`\`bash
# Rollback to previous version
kubectl rollout undo deployment/devsecops-app -n devsecops-app

# Verify rollback
kubectl rollout status deployment/devsecops-app -n devsecops-app

# Check application health
curl -f ${SERVICE_URL}/health
\`\`\`

### Full Rollback

\`\`\`bash
# Rollback to specific revision
kubectl rollout history deployment/devsecops-app -n devsecops-app
kubectl rollout undo deployment/devsecops-app -n devsecops-app --to-revision=<revision>

# Rollback database migration (if required)
psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} < backup_YYYYMMDD_HHMMSS.sql

# Verify application
./scripts/deploy/smoke-tests.sh ${SERVICE_URL}
\`\`\`

## Blue-Green Deployment

### Procedure

\`\`\`bash
# Deploy to green environment
kubectl apply -f infrastructure/kubernetes/overlays/green/

# Verify green deployment
kubectl get pods -n devsecops-app-green

# Run smoke tests on green
./scripts/deploy/smoke-tests.sh ${GREEN_SERVICE_URL}

# Switch traffic to green
kubectl patch service devsecops-app -n devsecops-app -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for issues
kubectl logs -f deployment/devsecops-app -n devsecops-app-green --tail=100

# If successful, scale down blue
kubectl scale deployment devsecops-app -n devsecops-app-blue --replicas=0

# If issues, revert traffic to blue
kubectl patch service devsecops-app -n devsecops-app -p '{"spec":{"selector":{"version":"blue"}}}'
\`\`\`

## Canary Deployment

### Procedure

\`\`\`bash
# Deploy canary with 10% traffic
kubectl apply -f infrastructure/kubernetes/overlays/canary/

# Configure traffic split (using Istio)
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: devsecops-app
  namespace: devsecops-app
spec:
  hosts:
  - devsecops-app
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: devsecops-app
        subset: canary
      weight: 10
    - destination:
        host: devsecops-app
        subset: stable
      weight: 90
EOF

# Monitor canary metrics
kubectl logs -f deployment/devsecops-app-canary -n devsecops-app

# Gradually increase traffic
# 10% -> 25% -> 50% -> 75% -> 100%

# If successful, promote canary
kubectl apply -f infrastructure/kubernetes/overlays/prod/

# If issues, rollback canary
kubectl delete deployment devsecops-app-canary -n devsecops-app
\`\`\`

## Emergency Procedures

### Complete Service Outage

1. **Immediate Actions**
   - Check cluster health: `kubectl get nodes`
   - Check pod status: `kubectl get pods -A`
   - Check events: `kubectl get events -A --sort-by='.lastTimestamp'`

2. **Common Issues**
   - **ImagePullBackOff**: Check image exists and credentials
   - **CrashLoopBackOff**: Check logs for application errors
   - **Pending**: Check resource availability

3. **Escalation**
   - Page on-call engineer
   - Notify incident commander
   - Start incident channel

### Degraded Performance

1. **Check Metrics**
   \`\`\`bash
   # CPU/Memory usage
   kubectl top pods -n devsecops-app

   # Response time
   curl -w "@curl-format.txt" -o /dev/null -s ${SERVICE_URL}/health

   # Error rate
   kubectl logs deployment/devsecops-app -n devsecops-app | grep ERROR | wc -l
   \`\`\`

2. **Scale Resources**
   \`\`\`bash
   # Horizontal scaling
   kubectl scale deployment devsecops-app -n devsecops-app --replicas=10

   # Vertical scaling
   kubectl set resources deployment devsecops-app -n devsecops-app --limits=cpu=1000m,memory=1Gi
   \`\`\`

### Security Incident

1. **Contain**
   \`\`\`bash
   # Isolate affected pods
   kubectl label pod ${POD_NAME} -n devsecops-app quarantine=true

   # Update network policy to block traffic
   kubectl apply -f network-policy-lockdown.yaml
   \`\`\`

2. **Investigate**
   \`\`\`bash
   # Export logs
   kubectl logs ${POD_NAME} -n devsecops-app > incident_logs.txt

   # Get pod description
   kubectl describe pod ${POD_NAME} -n devsecops-app

   # Check audit logs
   kubectl get events -n devsecops-app
   \`\`\`

3. **Remediate**
   - Follow security incident response plan
   - Deploy patched version
   - Rotate credentials if compromised

## Maintenance Windows

### Scheduled Maintenance

**Timing**: Saturdays 02:00-04:00 UTC (lowest traffic period)

**Procedure**:
1. Send maintenance notification 72 hours in advance
2. Enable maintenance mode
3. Perform updates
4. Run full test suite
5. Disable maintenance mode
6. Send completion notification

### Enable Maintenance Mode

\`\`\`bash
# Deploy maintenance page
kubectl apply -f infrastructure/kubernetes/maintenance/

# Verify maintenance mode
curl ${SERVICE_URL}
\`\`\`

## Post-Deployment

### Documentation

- [ ] Update deployment log
- [ ] Document any issues encountered
- [ ] Update runbook if new procedures discovered
- [ ] Share deployment summary with team

### Monitoring Period

- Monitor application for 24 hours post-deployment
- Check error rates, response times, resource usage
- Review alerts and incidents
- Confirm no regressions

---

**Last Updated**: 2024-01-15
**Owner**: DevOps Team
**Review Frequency**: Quarterly
