terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  # Backend configuration for state management
  backend "s3" {
    bucket         = "devsecops-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = var.owner
      CostCenter  = var.cost_center
    }
  }
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  availability_zones   = data.aws_availability_zones.available.names
  enable_nat_gateway   = var.enable_nat_gateway
  enable_vpn_gateway   = var.enable_vpn_gateway
  enable_flow_logs     = true
  flow_logs_retention  = 30
}

# EKS Module
module "eks" {
  source = "./modules/eks"

  project_name       = var.project_name
  environment        = var.environment
  cluster_version    = var.eks_cluster_version
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  node_groups = var.eks_node_groups

  enable_irsa                    = true
  enable_cluster_encryption      = true
  enable_log_types               = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = var.eks_public_access
}

# RDS Module
module "rds" {
  source = "./modules/rds"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  engine                = var.rds_engine
  engine_version        = var.rds_engine_version
  instance_class        = var.rds_instance_class
  allocated_storage     = var.rds_allocated_storage

  database_name         = var.rds_database_name
  master_username       = var.rds_master_username

  backup_retention_period = var.rds_backup_retention
  multi_az               = var.rds_multi_az
  storage_encrypted      = true
  deletion_protection    = var.environment == "prod" ? true : false

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  performance_insights_enabled    = true
}

# S3 Module for application storage
module "s3" {
  source = "./modules/s3"

  project_name = var.project_name
  environment  = var.environment

  buckets = {
    app_data = {
      versioning     = true
      encryption     = "AES256"
      lifecycle_rules = {
        expire_old_versions = {
          enabled = true
          days    = 90
        }
      }
    }
    logs = {
      versioning     = true
      encryption     = "AES256"
      lifecycle_rules = {
        transition_to_glacier = {
          enabled = true
          days    = 30
        }
        expire = {
          enabled = true
          days    = 365
        }
      }
    }
  }

  enable_public_access_block = true
  enable_server_access_logging = true
}
