locals {
  bucket_names = { for k, v in var.buckets : k => "${var.project_name}-${var.environment}-${k}" }
}

resource "aws_s3_bucket" "main" {
  for_each = var.buckets

  bucket = local.bucket_names[each.key]

  tags = {
    Name = local.bucket_names[each.key]
  }
}

resource "aws_s3_bucket_versioning" "main" {
  for_each = { for k, v in var.buckets : k => v if v.versioning }

  bucket = aws_s3_bucket.main[each.key].id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  for_each = var.buckets

  bucket = aws_s3_bucket.main[each.key].id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = each.value.encryption
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "main" {
  for_each = var.enable_public_access_block ? var.buckets : {}

  bucket = aws_s3_bucket.main[each.key].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "main" {
  for_each = { for k, v in var.buckets : k => v if length(v.lifecycle_rules) > 0 }

  bucket = aws_s3_bucket.main[each.key].id

  dynamic "rule" {
    for_each = each.value.lifecycle_rules

    content {
      id     = rule.key
      status = rule.value.enabled ? "Enabled" : "Disabled"

      dynamic "transition" {
        for_each = try(rule.value.days, null) != null && contains(keys(rule.value), "transition_to_glacier") ? [1] : []

        content {
          days          = rule.value.days
          storage_class = "GLACIER"
        }
      }

      dynamic "expiration" {
        for_each = try(rule.value.days, null) != null && contains(keys(rule.value), "expire") ? [1] : []

        content {
          days = rule.value.days
        }
      }

      dynamic "noncurrent_version_expiration" {
        for_each = try(rule.value.days, null) != null && contains(keys(rule.value), "expire_old_versions") ? [1] : []

        content {
          noncurrent_days = rule.value.days
        }
      }
    }
  }
}

# Logging bucket
resource "aws_s3_bucket" "logs" {
  count = var.enable_server_access_logging ? 1 : 0

  bucket = "${var.project_name}-${var.environment}-access-logs"

  tags = {
    Name = "${var.project_name}-${var.environment}-access-logs"
  }
}

resource "aws_s3_bucket_acl" "logs" {
  count = var.enable_server_access_logging ? 1 : 0

  bucket = aws_s3_bucket.logs[0].id
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_logging" "main" {
  for_each = var.enable_server_access_logging ? var.buckets : {}

  bucket = aws_s3_bucket.main[each.key].id

  target_bucket = aws_s3_bucket.logs[0].id
  target_prefix = "${each.key}/"
}
