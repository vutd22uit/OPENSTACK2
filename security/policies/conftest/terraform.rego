# Conftest policies for Terraform
package main

import future.keywords.contains
import future.keywords.if
import future.keywords.in

# METADATA
# title: S3 Bucket must not be public
# description: Ensures S3 buckets are not publicly accessible
deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    resource.acl == "public-read"
    msg := sprintf("S3 bucket '%s' must not have public-read ACL", [name])
}

deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    resource.acl == "public-read-write"
    msg := sprintf("S3 bucket '%s' must not have public-read-write ACL", [name])
}

# METADATA
# title: S3 Bucket must have encryption enabled
# description: Ensures S3 buckets have encryption at rest
deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    not resource.server_side_encryption_configuration
    msg := sprintf("S3 bucket '%s' must have encryption enabled", [name])
}

# METADATA
# title: S3 Bucket must have versioning enabled
# description: Ensures S3 buckets have versioning for data protection
warn[msg] {
    resource := input.resource.aws_s3_bucket[name]
    not resource.versioning
    msg := sprintf("S3 bucket '%s' should have versioning enabled", [name])
}

# METADATA
# title: RDS must have encryption enabled
# description: Ensures RDS instances are encrypted at rest
deny[msg] {
    resource := input.resource.aws_db_instance[name]
    resource.storage_encrypted == false
    msg := sprintf("RDS instance '%s' must have storage encryption enabled", [name])
}

# METADATA
# title: RDS must have backup retention
# description: Ensures RDS instances have adequate backup retention
deny[msg] {
    resource := input.resource.aws_db_instance[name]
    resource.backup_retention_period < 7
    msg := sprintf("RDS instance '%s' must have backup retention >= 7 days", [name])
}

# METADATA
# title: RDS must not be publicly accessible
# description: Ensures RDS instances are not publicly accessible
deny[msg] {
    resource := input.resource.aws_db_instance[name]
    resource.publicly_accessible == true
    msg := sprintf("RDS instance '%s' must not be publicly accessible", [name])
}

# METADATA
# title: EKS cluster must have encryption
# description: Ensures EKS clusters have envelope encryption enabled
deny[msg] {
    resource := input.resource.aws_eks_cluster[name]
    not resource.encryption_config
    msg := sprintf("EKS cluster '%s' must have encryption_config defined", [name])
}

# METADATA
# title: EKS cluster must have logging enabled
# description: Ensures EKS clusters have control plane logging enabled
deny[msg] {
    resource := input.resource.aws_eks_cluster[name]
    not resource.enabled_cluster_log_types
    msg := sprintf("EKS cluster '%s' must have control plane logging enabled", [name])
}

# METADATA
# title: Security groups must not allow unrestricted ingress
# description: Prevents security groups from allowing 0.0.0.0/0 on sensitive ports
deny[msg] {
    resource := input.resource.aws_security_group[name]
    rule := resource.ingress[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    sensitive_port(rule.from_port)
    msg := sprintf("Security group '%s' allows unrestricted access on sensitive port %d", [name, rule.from_port])
}

sensitive_port(port) {
    port == 22  # SSH
}

sensitive_port(port) {
    port == 3389  # RDP
}

sensitive_port(port) {
    port == 3306  # MySQL
}

sensitive_port(port) {
    port == 5432  # PostgreSQL
}

# METADATA
# title: Resources must have required tags
# description: Ensures resources have required tagging for governance
warn[msg] {
    resource := input.resource[resource_type][name]
    startswith(resource_type, "aws_")
    not has_required_tags(resource)
    msg := sprintf("Resource '%s' of type '%s' should have required tags: Project, Environment, Owner", [name, resource_type])
}

has_required_tags(resource) {
    resource.tags.Project
    resource.tags.Environment
    resource.tags.Owner
}
