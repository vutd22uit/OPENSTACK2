# Incident Response Runbook

## Incident Response Process

### 1. Detection and Reporting

**Automated Detection**
- Security scanner alerts
- Monitoring system alerts
- Audit log anomalies
- OPA Gatekeeper violations

**Manual Reporting**
- User reports
- Team member observations
- External security researchers

### 2. Triage (15 minutes)

**Assess Severity**
- P1: Critical - Active attack, data breach, complete outage
- P2: High - High-risk vulnerability, partial outage
- P3: Medium - Medium-risk issue, minor impact
- P4: Low - Low-risk, no immediate threat

**Initial Actions**
\`\`\`bash
# Check system status
kubectl get pods -A
kubectl get events -A --sort-by='.lastTimestamp' | head -20

# Check recent deployments
kubectl rollout history deployment/devsecops-app -n devsecops-app

# Export logs
kubectl logs deployment/devsecops-app -n devsecops-app --since=1h > incident_$(date +%Y%m%d_%H%M%S).log
\`\`\`

### 3. Containment (30 minutes)

**Network Isolation**
\`\`\`bash
# Apply restrictive network policy
kubectl apply -f security/network-policy-lockdown.yaml

# Isolate compromised pods
kubectl label pod ${POD_NAME} -n devsecops-app quarantine=true
\`\`\`

**Access Revocation**
\`\`\`bash
# Revoke service account tokens
kubectl delete secret ${SECRET_NAME} -n devsecops-app

# Rotate credentials
./scripts/security/rotate-credentials.sh
\`\`\`

### 4. Investigation

**Collect Evidence**
- Pod logs
- Audit logs
- Network traffic captures
- File system snapshots
- Memory dumps (if needed)

**Analysis**
- Timeline of events
- Attack vectors identified
- Scope of compromise
- Data accessed/exfiltrated

### 5. Remediation

**Deploy Fix**
\`\`\`bash
# Build patched version
make docker-build IMAGE_TAG=hotfix-$(date +%Y%m%d)

# Security scan
./scripts/security/scan-image.sh devsecops-app:hotfix-$(date +%Y%m%d)

# Deploy
kubectl set image deployment/devsecops-app app=ghcr.io/org/app:hotfix-$(date +%Y%m%d) -n devsecops-app
\`\`\`

**Verification**
- Verify fix resolves issue
- No new vulnerabilities introduced
- System functionality restored

### 6. Recovery

**Restore Normal Operations**
\`\`\`bash
# Remove network restrictions
kubectl delete -f security/network-policy-lockdown.yaml

# Scale back to normal
kubectl scale deployment devsecops-app -n devsecops-app --replicas=3
\`\`\`

### 7. Post-Incident Review

**Within 48 hours**
- Timeline documentation
- Root cause analysis
- Lessons learned
- Action items

**Document**
- What happened
- How it was detected
- Response actions taken
- What worked well
- What could be improved
- Preventive measures

## Contact Information

- **Incident Commander**: on-call-ic@example.com
- **Security Team**: security@example.com
- **DevOps On-Call**: oncall-devops@example.com
- **Emergency**: +1-555-0100

## Communication Templates

### Initial Alert
\`\`\`
Subject: [P1/P2/P3/P4] Security Incident - [Brief Description]

Incident ID: INC-YYYYMMDD-NNN
Severity: P[1-4]
Status: Investigating/Contained/Resolved
Affected Systems: [List]

Description: [Brief description of the incident]

Current Status: [What we know so far]

Actions Taken: [What has been done]

Next Steps: [What will be done next]

Impact: [User/business impact]

Updates: [How often updates will be provided]
\`\`\`

## Common Scenarios

### Scenario 1: Compromised Container

1. Isolate container
2. Export forensic data
3. Kill container
4. Deploy from known-good image
5. Investigate root cause

### Scenario 2: Credential Leak

1. Immediately revoke credentials
2. Audit access logs for misuse
3. Generate new credentials
4. Update systems with new credentials
5. Review credential management practices

### Scenario 3: Vulnerability Exploit

1. Verify exploitation occurred
2. Deploy patched version
3. Scan for indicators of compromise
4. Review similar systems

### Scenario 4: DDoS Attack

1. Enable rate limiting
2. Activate DDoS protection
3. Scale infrastructure
4. Contact ISP/CDN provider
5. Implement traffic filtering

## Tools and Resources

- kubectl cheat sheet
- Security playbooks
- Contact lists
- Forensics tools
- Backup/restore procedures
