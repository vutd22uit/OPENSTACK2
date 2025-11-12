# 🔒 DevSecOps CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/organization/devsecops-pipeline/actions/workflows/ci-security.yml/badge.svg)](https://github.com/organization/devsecops-pipeline/actions)
[![Security Scan](https://img.shields.io/badge/security-scanned-brightgreen)](https://github.com/organization/devsecops-pipeline/security)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Enterprise-grade DevSecOps CI/CD pipeline with comprehensive security scanning, automated testing, and policy enforcement for production-ready deployments.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Security Scanning](#security-scanning)
- [Infrastructure](#infrastructure)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project demonstrates a complete DevSecOps CI/CD pipeline implementing security best practices throughout the software development lifecycle. It includes:

- **Sample Application**: Production-ready Flask REST API with security hardening
- **Infrastructure as Code**: Terraform modules for AWS (VPC, EKS, RDS, S3)
- **Kubernetes Manifests**: Secure deployments with security contexts and policies
- **Comprehensive Security Scanning**: SAST, DAST, IaC scanning, container scanning, SBOM generation
- **Automated CI/CD**: GitHub Actions workflows with security gates
- **Policy Enforcement**: OPA Gatekeeper policies for runtime security

## ✨ Features

### 🔐 Security Features

- **Secrets Detection**: Gitleaks pre-commit and CI scanning
- **SAST**: Semgrep, Bandit, ESLint with multiple rulesets
- **Dependency Scanning**: Safety, pip-audit, GitHub Dependabot
- **IaC Security**: Checkov, tfsec, Conftest/OPA policies
- **Container Security**: Trivy, Grype vulnerability scanning
- **SBOM Generation**: Syft (SPDX & CycloneDX formats)
- **Image Signing**: Cosign for supply chain security
- **DAST**: OWASP ZAP automated scanning
- **Runtime Security**: OPA Gatekeeper admission control

### 🚀 DevOps Features

- **Multi-stage Docker Builds**: Optimized images with security hardening
- **Kubernetes Security**: Pod Security Standards, Network Policies, RBAC
- **Infrastructure as Code**: Modular Terraform with multiple environments
- **GitOps Ready**: Structured manifests for ArgoCD/Flux
- **Observability**: Prometheus metrics, structured logging
- **High Availability**: HPA, PDB, multi-AZ deployments

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Developer Workstation                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Pre-commit   │  │   Gitleaks   │  │   Semgrep    │     │
│  │   Hooks      │  │   Scanning   │  │    SAST      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Repository                       │
│                   (Source Code + IaC)                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   CI/CD Pipeline (GitHub Actions)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  SAST    │  │Dependency│  │   IaC    │  │Container │   │
│  │Scanning  │  │ Scanning │  │Scanning  │  │Scanning  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  SBOM    │  │  Image   │  │   DAST   │                 │
│  │Generation│  │ Signing  │  │ Scanning │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Container Registry (GHCR/Harbor)                │
│          (Signed Images + SBOM + Vulnerability Data)         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            Kubernetes Cluster (EKS/GKE/AKS)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            OPA Gatekeeper Admission Control           │  │
│  │  (Verify Signatures, Enforce Security Policies)       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Pods   │  │ Network  │  │   RBAC   │  │ Security │  │
│  │(Hardened)│  │ Policies │  │          │  │ Contexts │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

See [Architecture Documentation](docs/architecture/README.md) for detailed diagrams.

## 📦 Prerequisites

### Local Development

- Python 3.11+
- Docker 20.10+
- Docker Compose 2.0+
- Make
- Git

### CI/CD

- GitHub account with Actions enabled
- Container registry (GHCR, Docker Hub, or Harbor)
- Kubernetes cluster (for deployment)

### Infrastructure

- AWS account (for Terraform deployment)
- Terraform 1.5+
- kubectl
- AWS CLI configured

## 🚀 Quick Start

### 1. Clone Repository

\`\`\`bash
git clone https://github.com/organization/devsecops-pipeline.git
cd devsecops-pipeline
\`\`\`

### 2. Set Up Local Environment

\`\`\`bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
make install

# Install pre-commit hooks
make install-hooks

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 3. Run Application Locally

\`\`\`bash
# Using Docker Compose
make docker-run

# Or run directly
python app.py
\`\`\`

Visit http://localhost:5000/health to verify the application is running.

### 4. Run Tests

\`\`\`bash
# Run all tests with coverage
make test

# Run linting
make lint

# Run security scans
make security-scan
\`\`\`

## 🔍 Security Scanning

### Pre-Commit Checks (Local)

Pre-commit hooks automatically run before each commit:

\`\`\`bash
# Manual run
pre-commit run --all-files
\`\`\`

Checks include:
- Secrets detection (Gitleaks)
- Code formatting (Black, isort)
- Linting (Flake8, Pylint)
- Security scanning (Bandit, Semgrep)
- IaC scanning (Checkov, tfsec)
- Dockerfile linting (Hadolint)

### CI Pipeline Scans

The GitHub Actions pipeline performs comprehensive scanning:

1. **Secret Detection**: Scans entire repository history
2. **SAST**: Multiple tools for code vulnerabilities
3. **Dependency Scanning**: Known CVEs in dependencies
4. **IaC Scanning**: Terraform misconfigurations
5. **Container Scanning**: Image vulnerabilities
6. **SBOM Generation**: Software Bill of Materials
7. **Image Signing**: Cryptographic signing with Cosign
8. **DAST**: Runtime vulnerability testing

### Manual Security Scans

\`\`\`bash
# Scan Docker image
./scripts/security/scan-image.sh myapp:latest

# Scan infrastructure
make iac-scan

# Full security suite
make security-scan
\`\`\`

## 🏗️ Infrastructure

### Terraform Modules

The infrastructure is organized into reusable modules:

- **VPC**: Multi-AZ VPC with public/private subnets, NAT gateways
- **EKS**: Managed Kubernetes cluster with encrypted secrets
- **RDS**: PostgreSQL with encryption and automated backups
- **S3**: Encrypted buckets with versioning and lifecycle policies

### Deploy Infrastructure

\`\`\`bash
cd infrastructure/terraform

# Initialize
terraform init

# Plan with environment-specific vars
terraform plan -var-file=environments/dev/terraform.tfvars

# Apply
terraform apply -var-file=environments/dev/terraform.tfvars
\`\`\`

See [Infrastructure Documentation](docs/infrastructure/README.md) for details.

## 🚢 Deployment

### Deploy to Kubernetes

\`\`\`bash
# Development
make deploy-dev

# Staging
make deploy-staging

# Production (requires approval)
make deploy-prod
\`\`\`

### Manual Deployment

\`\`\`bash
# Apply base manifests
kubectl apply -f infrastructure/kubernetes/base/

# Apply environment-specific overlays
kubectl apply -f infrastructure/kubernetes/overlays/prod/

# Verify deployment
kubectl get pods -n devsecops-app
kubectl logs -f deployment/devsecops-app -n devsecops-app
\`\`\`

## 📊 Monitoring

### Application Metrics

The application exposes Prometheus metrics at `/metrics`:

- Request rate, latency, errors
- Resource usage (CPU, memory)
- Business metrics

### Security Monitoring

- **Falco**: Runtime threat detection
- **OPA Gatekeeper**: Policy violations
- **Audit Logs**: Kubernetes API access

See [Monitoring Documentation](docs/monitoring/README.md) for setup.

## 📚 Documentation

- [Architecture Overview](docs/architecture/README.md)
- [Security Policies](docs/security/SECURITY_POLICIES.md)
- [Deployment Runbook](docs/runbooks/DEPLOYMENT.md)
- [Incident Response](docs/runbooks/INCIDENT_RESPONSE.md)
- [Compliance](docs/security/COMPLIANCE.md)

## 🧪 Testing

\`\`\`bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_api.py

# Run security tests
pytest -m security
\`\`\`

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `SECRET_KEY`: Application secret key (generate with `openssl rand -hex 32`)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ALLOWED_ORIGINS`: CORS allowed origins

### Security Configuration

- **TLS**: Certificates managed by cert-manager
- **Secrets**: Stored in Kubernetes Secrets or external vault
- **Network Policies**: Restrict pod-to-pod communication
- **RBAC**: Least-privilege service accounts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and security scans (`make ci`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Pre-commit hooks will automatically run security checks.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OWASP](https://owasp.org/) for security best practices
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/) for hardening guidelines
- [NIST](https://www.nist.gov/) for security frameworks
- All open-source security tools integrated in this project

## 📞 Support

- 📧 Email: security@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/organization/devsecops-pipeline/issues)
- 📖 Documentation: [Wiki](https://github.com/organization/devsecops-pipeline/wiki)

---

**Made with ❤️ for secure software development**
