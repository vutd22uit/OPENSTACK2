.PHONY: help install test lint security-scan build docker-build docker-scan clean

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
IMAGE_NAME := devsecops-app
IMAGE_TAG := latest
REGISTRY := ghcr.io/organization

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

install-hooks: ## Install pre-commit hooks
	$(PIP) install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg

test: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term-missing

lint: ## Run code quality checks
	black --check app/
	isort --check-only app/
	flake8 app/
	pylint app/

format: ## Format code
	black app/
	isort app/

security-scan: ## Run security scans
	@echo "Running Bandit..."
	bandit -r app/ -f txt
	@echo "Running Safety..."
	safety check
	@echo "Running Semgrep..."
	semgrep --config=auto app/

iac-scan: ## Scan infrastructure as code
	@echo "Running Checkov..."
	checkov -d infrastructure/terraform/
	@echo "Running tfsec..."
	tfsec infrastructure/terraform/
	@echo "Running Conftest..."
	conftest test --policy security/policies/conftest infrastructure/terraform/

docker-build: ## Build Docker image
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-scan: docker-build ## Scan Docker image
	./scripts/security/scan-image.sh $(IMAGE_NAME):$(IMAGE_TAG)

docker-run: ## Run Docker container
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

deploy-dev: ## Deploy to development
	./scripts/deploy/deploy.sh dev

deploy-staging: ## Deploy to staging
	./scripts/deploy/deploy.sh staging

deploy-prod: ## Deploy to production
	./scripts/deploy/deploy.sh prod

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist htmlcov .coverage .pytest_cache
	rm -rf security-reports/

all: install install-hooks lint test security-scan ## Run all checks

ci: lint test security-scan iac-scan ## Run CI pipeline locally
