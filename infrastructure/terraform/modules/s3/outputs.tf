output "bucket_names" {
  description = "S3 bucket names"
  value       = { for k, v in aws_s3_bucket.main : k => v.id }
}

output "bucket_arns" {
  description = "S3 bucket ARNs"
  value       = { for k, v in aws_s3_bucket.main : k => v.arn }
}
