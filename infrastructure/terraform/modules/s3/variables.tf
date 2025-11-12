variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "buckets" {
  description = "Map of S3 bucket configurations"
  type = map(object({
    versioning = bool
    encryption = string
    lifecycle_rules = map(object({
      enabled = bool
      days    = number
    }))
  }))
}

variable "enable_public_access_block" {
  description = "Enable public access block"
  type        = bool
  default     = true
}

variable "enable_server_access_logging" {
  description = "Enable server access logging"
  type        = bool
  default     = true
}
