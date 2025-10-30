
variable "location" {
  default     = "swedencentral"
}

variable "resource_group_name" {
  type        = string
  default     = "rg-hr-analytics"
}


variable "acr_name" {
  type        = string
}

variable "storage_account_name" {
  type        = string
}

variable "environment" {
  type        = string
  default     = "dev"
}

variable "tags" {
  type        = map(string)
  default = {
    Project     = "HR-Analytics"
    Environment = "Development"
    ManagedBy   = "Terraform"
  }
}
